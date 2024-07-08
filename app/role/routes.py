from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.role.models import Role
from app.role.schemas import RoleCreate, RoleOut

router = APIRouter()


@router.post("/", response_model=RoleOut)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.get("/", response_model=list[RoleOut])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Role).all()
    return categories


@router.get("/{id}", response_model=RoleOut)
async def get_role(id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{id}", response_model=RoleOut)
async def update_role(id: int, role: RoleCreate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.id == id).first()
    if existing_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    existing_role.name = role.name
    db.commit()
    db.refresh(existing_role)
    return existing_role


@router.delete("/{id}")
async def delete_role(id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}
