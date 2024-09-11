from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.schemas import UserWithToken
from app.core.database import get_db
from app.core.schemas import BasePaginatedResponse, BaseResponse, PaginatedParams
from app.role.schemas import RoleCreate, RoleOut
from app.core.security import get_current_user
from app.role.service import add_role, update_role, get_all_role, get_role, delete_role

router = APIRouter()


@router.post("/", response_model=BaseResponse[RoleOut])
async def create_role(role: RoleCreate, current_user: UserWithToken = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = await add_role(role, db, current_user)
        if type(result) == dict or type(result) == RoleOut:
            return BaseResponse[RoleOut](data=result, message="Role created successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.get("/", response_model=BasePaginatedResponse[RoleOut], summary="Get all roles")
async def get_all_role_route(
    current_user: UserWithToken = Depends(get_current_user),
    paginatedParams: PaginatedParams = Depends(),
    db: Session = Depends(get_db)
):
    try:
        print("paginatedParams.orderBy", paginatedParams.orderBy)
        result = await get_all_role(paginatedParams, db)
        print(type(result))
        print(result)
        if type(result) == dict and hasattr(result, 'items'):
            return BasePaginatedResponse[RoleOut](data=result, message="Roles fetched successfully")
        elif type(result) == str:
            print("errr", result)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        # print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.get("/{id}", response_model=BaseResponse[RoleOut], summary="Get role")
async def get_role_route(
        id: int,
        current_user: UserWithToken = Depends(get_current_user),
        db: Session = Depends(get_db)):
    try:
        result = await get_role(id, db)
        if type(result) == dict or type(result) == RoleOut:
            return BaseResponse[RoleOut](data=result, message="Role fetched successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.put("/{id}", response_model=BaseResponse[RoleOut], summary="Update role")
async def put_role(id: int, role: RoleCreate, current_user: UserWithToken = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = await update_role(id, role, db, current_user)
        if type(result) == dict or type(result) == RoleOut:
            return BaseResponse[RoleOut](data=result, message="Role updated successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.delete("/{id}", response_model=BaseResponse[Any], summary="Delete role")
async def delete_role_route(
    id: int,
    current_user: UserWithToken = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(id, current_user)
    try:
        result = await delete_role(id, db, current_user)
        if type(result) == dict or type(result) == RoleOut:
            return BaseResponse[Any](data="", message="Role deleted successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
