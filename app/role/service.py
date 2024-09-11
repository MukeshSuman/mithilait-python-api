from fastapi import Depends, status
from sqlalchemy import or_, asc, desc
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.schemas import BasePaginatedResponse, PaginatedParams
from app.role.models import Role

from typing import Any

from app.role.schemas import RoleCreate, RoleOut


async def get_role(id: int, db: Session = Depends(get_db), current_user: Any = None):
    try:
        existing_role = db.query(Role).filter(
            Role.id == id, Role.isDeleted == False).first()
        if existing_role is None:
            return "Role not found"
        temp_role = existing_role.toDict()
        data = {
            **temp_role
        }
        finalData = RoleOut(**data)
        return finalData
    except Exception as e:
        print(e)
        return str(e)


async def get_all_role(paginatedParams: PaginatedParams, db: Session = Depends(get_db)):
    try:
        roles_query = db.query(Role)
        if paginatedParams.search:
            roles_query = roles_query.filter(
                or_(Role.name.contains(paginatedParams.search))
            )
        roles_query = roles_query.filter(Role.isDeleted == False)
        if paginatedParams.sortBy and hasattr(Role, paginatedParams.sortBy):
            order = asc if paginatedParams.orderBy == "asc" else desc
            roles_query = roles_query.order_by(
                order(getattr(Role, paginatedParams.sortBy)))
        else:
            return "sortBy field is invalid"
        roles = roles_query.offset(paginatedParams.offset).limit(
            paginatedParams.limit).all()
        totalItems = roles_query.count()
        totalPages = paginatedParams.getTotalPages(totalItems)
        # # totalPages = (totalItems + paginatedParams.pageSize -
        # #               1) // paginatedParams.pageSize
        # totalPages = 0
        temp_list = [RoleOut.model_validate(
            role).model_dump() for role in roles]
        data = {
            "pageNumber": paginatedParams.pageNumber,
            "pageSize": paginatedParams.pageSize,
            "totalItems": totalItems,
            "totalPage": totalPages,
            "items": temp_list
        }
        return data
    except Exception as e:
        print(e)
        return str(e)


async def add_role(role: RoleCreate, db: Session = Depends(get_db), current_user: Any = None):
    try:
        db_role = db.query(Role).filter(
            Role.name == role.name, Role.isDeleted == False).first()
        if db_role:
            return "Role name already exists"
        new_role = Role(name=role.name)
        db.add(new_role)
        if current_user:
            new_role.set_created_by(current_user)
        db.commit()
        db.refresh(new_role)
        temp_role = new_role.toDict()
        data = {
            **temp_role
        }
        finalData = RoleOut(**data)
        return finalData
    except Exception as e:
        db.rollback()
        print(e)
        return str(e)


async def update_role(id: int, role: RoleCreate, db: Session = Depends(get_db), current_user: Any = None):
    try:
        existing_role = db.query(Role).filter(Role.id == id).first()
        if existing_role is None:
            return "Role not found"
        existing_role.name = role.name
        if current_user:
            existing_role.set_updated_by(current_user)
        db.commit()
        db.refresh(existing_role)
        temp_role = existing_role.toDict()
        data = {
            **temp_role
        }
        finalData = RoleOut(**data)
        return finalData
    except Exception as e:
        db.rollback()
        print(e)
        return str(e)


async def delete_role(id: int, db: Session = Depends(get_db), current_user: Any = None):
    try:
        existing_role = db.query(Role).filter(
            Role.id == id, Role.isDeleted == False).first()
        if existing_role is None:
            return "Role not found"
        if current_user:
            existing_role.soft_delete(current_user)
            db.commit()
            db.refresh(existing_role)
        temp_role = existing_role.toDict()
        data = {
            **temp_role
        }
        finalData = RoleOut(**data)
        return finalData
    except Exception as e:
        print(e)
        return str(e)
