# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base
from schemas import StudentCreate, Student, GroupCreate, Group
from crud import (
    create_student, get_student, get_all_students, delete_student,
    create_group, get_group, get_all_groups, delete_group,
    add_student_to_group, remove_student_from_group,
    get_students_in_group, transfer_student_between_groups
)

# Создаем таблицы при запуске (в продакшене лучше использовать Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API для управления студентами и группами",
    description="Реализация задания по созданию API для студентов и групп"
)

# === Эндпоинты для студентов ===

@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    """Создать нового студента"""
    return create_student(db, student)

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Получить информацию о студенте по ID"""
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@app.get("/students/", response_model=List[Student])
def read_all_students(db: Session = Depends(get_db)):
    """Получить список всех студентов"""
    return get_all_students(db)

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента по ID"""
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Студент не найден")

# === Эндпоинты для групп ===

@app.post("/groups/", response_model=Group, status_code=status.HTTP_201_CREATED)
def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    """Создать новую группу"""
    return create_group(db, group)

@app.get("/groups/{group_id}", response_model=Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """Получить информацию о группе по ID"""
    db_group = get_group(db, group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@app.get("/groups/", response_model=List[Group])
def read_all_groups(db: Session = Depends(get_db)):
    """Получить список всех групп"""
    return get_all_groups(db)

@app.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """Удалить группу по ID"""
    success = delete_group(db, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Группа не найдена")

# === Эндпоинты для взаимодействия студентов и групп ===

@app.post("/groups/{group_id}/students/{student_id}", response_model=Student)
def add_student_to_group_endpoint(group_id: int, student_id: int, db: Session = Depends(get_db)):
    """Добавить студента в группу"""
    student = add_student_to_group(db, student_id, group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент или группа не найдены")
    return student

@app.delete("/groups/{group_id}/students/{student_id}", response_model=Student)
def remove_student_from_group_endpoint(group_id: int, student_id: int, db: Session = Depends(get_db)):
    """Удалить студента из группы"""
    # group_id здесь для совместимости с URL, но логически не обязателен
    student = remove_student_from_group(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student

@app.get("/groups/{group_id}/students/", response_model=List[Student])
def get_students_in_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """Получить всех студентов в группе"""
    students = get_students_in_group(db, group_id)
    return students

@app.post("/transfer/", response_model=Student)
def transfer_student(
    student_id: int,
    from_group_id: int,  # Можно не использовать, но для ясности
    to_group_id: int,
    db: Session = Depends(get_db)
):
    """Перевести студента из одной группы в другую"""
    student = transfer_student_between_groups(db, student_id, to_group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент или целевая группа не найдены")
    return student