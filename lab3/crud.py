# crud.py
from sqlalchemy.orm import Session
from models import Student, Group
from schemas import StudentCreate, GroupCreate

# === Студенты ===

def create_student(db: Session, student: StudentCreate):
    db_student = Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_all_students(db: Session):
    return db.query(Student).all()

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

# === Группы ===

def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

def get_all_groups(db: Session):
    return db.query(Group).all()

def delete_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group:
        # Проверяем, есть ли студенты в группе — можно удалить и так (CASCADE не настроен)
        # Но по ТЗ просто удаляем группу, студенты останутся без группы
        db.delete(group)
        db.commit()
        return True
    return False

# === Операции с группами и студентами ===

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()
    if not student or not group:
        return None
    student.group_id = group_id
    db.commit()
    db.refresh(student)
    return student

def remove_student_from_group(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        student.group_id = None
        db.commit()
        db.refresh(student)
        return student
    return None

def get_students_in_group(db: Session, group_id: int):
    return db.query(Student).filter(Student.group_id == group_id).all()

def transfer_student_between_groups(db: Session, student_id: int, new_group_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    new_group = db.query(Group).filter(Group.id == new_group_id).first()
    if not student or not new_group:
        return None
    student.group_id = new_group_id
    db.commit()
    db.refresh(student)
    return student