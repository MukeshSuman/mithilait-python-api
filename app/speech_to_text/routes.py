from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile, WebSocket, WebSocketDisconnect
# from sqlalchemy.orm import Session

# from app.auth.schemas import UserWithToken
# from app.core.database import get_db
from app.core.schemas import BaseResponse
from app.speech_to_text.schemas import PronunciationAssessmentResult
# from app.core.security import get_current_user
# from app.role.service import add_role, update_role, get_all_role, get_role, delete_role

from app.core.config import settings

from fastapi.responses import JSONResponse
from app.speech_to_text.service import AzureSpeechService
import io


router = APIRouter()

speech_service = AzureSpeechService(
    settings.AZ_SPEECH_KEY, settings.AZ_SERVICE_REGION)


@router.post("/upload-audio/", response_model=BaseResponse[PronunciationAssessmentResult])
async def upload_audio(file: UploadFile = File(...)):
    try:
        audio_file_path = f"temp_{file.filename}"
        with open(audio_file_path, "wb") as buffer:
            buffer.write(await file.read())
        result = speech_service.recognize_speech_from_file(audio_file_path)
        if type(result) == dict or type(result) == PronunciationAssessmentResult:
            return BaseResponse[PronunciationAssessmentResult](data=result, message="success")
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.websocket("/ws/stream-audio/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        audio_stream = io.BytesIO()
        while True:
            data = await websocket.receive_bytes()
            audio_stream.write(data)
    except WebSocketDisconnect:
        audio_stream.seek(0)
        text = speech_service.recognize_speech_from_stream(audio_stream)
        await websocket.send_json({"text": text})

# @router.post("/", response_model=BaseResponse[RoleOut])
# async def create_role(role: RoleCreate, current_user: UserWithToken = Depends(get_current_user), db: Session = Depends(get_db)):
#     try:
#         result = await add_role(role, db, current_user)
#         if type(result) == dict or type(result) == RoleOut:
#             return BaseResponse[RoleOut](data=result, message="Role created successfully")
#         elif type(result) == str:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=result
#             )
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code, detail=str(e.detail))
#     except Exception as e:
#         print('e Exception', e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=e
#         )


# @router.get("/", response_model=BasePaginatedResponse[RoleOut], summary="Get all roles")
# async def get_all_role_route(
#     current_user: UserWithToken = Depends(get_current_user),
#     paginatedParams: PaginatedParams = Depends(),
#     db: Session = Depends(get_db)
# ):
#     try:
#         print("paginatedParams.orderBy", paginatedParams.orderBy)
#         result = await get_all_role(paginatedParams, db)
#         print(type(result))
#         print(result)
#         if type(result) == dict and hasattr(result, 'items'):
#             return BasePaginatedResponse[RoleOut](data=result, message="Roles fetched successfully")
#         elif type(result) == str:
#             print("errr", result)
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=result
#             )
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code, detail=str(e.detail))
#     except Exception as e:
#         # print(e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=e
#         )


# @router.get("/{id}", response_model=BaseResponse[RoleOut], summary="Get role")
# async def get_role_route(
#         id: int,
#         current_user: UserWithToken = Depends(get_current_user),
#         db: Session = Depends(get_db)):
#     try:
#         result = await get_role(id, db)
#         if type(result) == dict or type(result) == RoleOut:
#             return BaseResponse[RoleOut](data=result, message="Role fetched successfully")
#         elif type(result) == str:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=result
#             )
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code, detail=str(e.detail))
#     except Exception as e:
#         print('e Exception', e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=e
#         )


# @router.put("/{id}", response_model=BaseResponse[RoleOut], summary="Update role")
# async def put_role(id: int, role: RoleCreate, current_user: UserWithToken = Depends(get_current_user), db: Session = Depends(get_db)):
#     try:
#         result = await update_role(id, role, db, current_user)
#         if type(result) == dict or type(result) == RoleOut:
#             return BaseResponse[RoleOut](data=result, message="Role updated successfully")
#         elif type(result) == str:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=result
#             )
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code, detail=str(e.detail))
#     except Exception as e:
#         print('e Exception', e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=e
#         )


# @router.delete("/{id}", response_model=BaseResponse[Any], summary="Delete role")
# async def delete_role_route(
#     id: int,
#     current_user: UserWithToken = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     print(id, current_user)
#     try:
#         result = await delete_role(id, db, current_user)
#         if type(result) == dict or type(result) == RoleOut:
#             return BaseResponse[Any](data="", message="Role deleted successfully")
#         elif type(result) == str:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=result
#             )
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code, detail=str(e.detail))
#     except Exception as e:
#         print('e Exception', e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=e
#         )
