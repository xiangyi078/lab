from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas, auth, database
from .database import engine
from .redis_client import redis_client
from typing import List, Optional
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth-сервис", description="Сервис аутентификации и авторизации с JWT")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session):
    if auth.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отозван")
    payload = auth.decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется access-токен")
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные в токене")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return user

@app.post("/register", status_code=status.HTTP_201_CREATED, summary="Регистрация пользователя")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь успешно зарегистрирован"}

@app.post("/login", response_model=schemas.TokenResponse, summary="Авторизация пользователя")
def login(user: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    # Запись в историю входов
    user_agent = request.headers.get("user-agent", "unknown")
    history = models.LoginHistory(user_id=db_user.id, user_agent=user_agent)
    db.add(history)
    db.commit()

    access_token = auth.create_access_token(data={"sub": db_user.email})
    refresh_token = auth.create_refresh_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.post("/refresh", response_model=schemas.TokenResponse, summary="Обновление access-токена")
def refresh(refresh: schemas.RefreshRequest, db: Session = Depends(get_db)):
    if auth.is_token_blacklisted(refresh.refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh-токен отозван")
    payload = auth.decode_token(refresh.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Передан не refresh-токен")
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    new_access = auth.create_access_token(data={"sub": email})
    new_refresh = auth.create_refresh_token(data={"sub": email})
    # Отзываем старый refresh-токен
    redis_client.setex(f"blacklist:{refresh.refresh_token}", 7*24*3600, "revoked")
    return {"access_token": new_access, "refresh_token": new_refresh}

@app.put("/user/update", summary="Изменение данных пользователя")
def update_user(
    update: schemas.UserUpdate,
    request: Request,
    token: str = Depends(lambda x: x.headers.get("Authorization", "").replace("Bearer ", "")),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    if update.email:
        if db.query(models.User).filter(models.User.email == update.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже используется")
        user.email = update.email
    if update.password:
        user.hashed_password = auth.get_password_hash(update.password)
    db.commit()
    return {"message": "Данные обновлены"}

@app.get("/user/history", response_model=List[schemas.LoginRecord], summary="История входов")
def get_history(
    token: str = Depends(lambda x: x.headers.get("Authorization", "").replace("Bearer ", "")),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    records = db.query(models.LoginHistory).filter(models.LoginHistory.user_id == user.id).order_by(models.LoginHistory.login_date.desc()).all()
    return [
        schemas.LoginRecord(
            user_agent=r.user_agent,
            login_date=r.login_date.isoformat()
        ) for r in records
    ]

@app.post("/logout", summary="Выход из системы")
def logout(token: str = Depends(lambda x: x.headers.get("Authorization", "").replace("Bearer ", ""))):
    payload = auth.decode_token(token)
    # Добавляем оба токена в чёрный список
    redis_client.setex(f"blacklist:{token}", 15*60, "revoked")  # access живёт 15 мин
    # Если это refresh — тоже можно добавить, но обычно logout вызывается с access
    return {"message": "Выход выполнен успешно"}