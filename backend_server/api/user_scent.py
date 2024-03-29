from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import backend_server.models.user_scent_meta as user_scent_meta_model
import backend_server.models.item as item_model
import backend_server.schemas.item as item_schema
import backend_server.schemas.scent as scent_schema
import backend_server.schemas.user_scent as user_scent_schema
import backend_server.service.scent as scent_service
from backend_server.database import get_db
from backend_server.service.websocket import ConnectionManager, get_ws_manager

router = APIRouter(tags=["user_scent"])


@router.websocket("/ws/user_scent")
async def websocket_endpoint(
    websocket: WebSocket,
    ws_manager: ConnectionManager = Depends(get_ws_manager),
):
    await ws_manager.connect(websocket)
    await ws_manager.send_personal_message(
        user_scent_schema.WebSocketMessage(message="Connected, Welcome!"),
        websocket,
    )
    try:
        while True:
            await websocket.receive_text()
            await ws_manager.send_personal_message(
                user_scent_schema.WebSocketMessage(
                    message="Warning: You should not send any message"
                ),
                websocket,
            )
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@router.post(
    "/user_scent",
    response_model=user_scent_schema.UserScentApiRead,
)
async def create_user_scent(
    scent_api_data: scent_schema.ScentApiCreate,
    db: Session = Depends(get_db),
    ws_manager: ConnectionManager = Depends(get_ws_manager),
):
    # Create scent
    db_obj_in = scent_service.convert_api_data_to_db_data(scent_api_data)
    if db_obj_in is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid scent data",
        )
    scent_in_db = scent_service.create_scent(db, db_obj_in)

    # Create user_scent_meta
    obj_in = user_scent_schema.UserScentDBCreate(scent_id=scent_in_db.id)
    user_scent_meta = user_scent_meta_model.UserScentMeta(
        **obj_in.model_dump()
    )

    db.add(user_scent_meta)
    db.commit()
    db.refresh(user_scent_meta)

    # Notify web client
    await ws_manager.broadcast(
        user_scent_schema.WebSocketMessage(message="New user scent created")
    )

    return user_scent_meta


@router.get(
    "/user_scents",
    response_model=list[user_scent_schema.UserScentApiRead],
)
def get_multiple_user_scent(
    offset: int = 0,
    limit: int = 10,
    desc: bool = True,
    db: Session = Depends(get_db),
):
    return (
        db.query(user_scent_meta_model.UserScentMeta)
        .order_by(
            user_scent_meta_model.UserScentMeta.id.desc()
            if desc
            else user_scent_meta_model.UserScentMeta.id
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.patch(
    "/user_scent/{user_scent_id}",
    response_model=user_scent_schema.UserScentApiRead,
)
def update_user_scent(
    user_scent_id: int,
    updated_user_scent: user_scent_schema.UserScentApiUpdate,
    db: Session = Depends(get_db),
):
    user_scent_meta_in_db: user_scent_meta_model.UserScentMeta = db.query(
        user_scent_meta_model.UserScentMeta
    ).get(user_scent_id)

    if user_scent_meta_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User scent not found",
        )

    db_obj_data = jsonable_encoder(user_scent_meta_in_db)
    update_data = updated_user_scent.model_dump(exclude_unset=True)
    for field in db_obj_data:
        if field in update_data:
            setattr(user_scent_meta_in_db, field, update_data[field])

    db.add(user_scent_meta_in_db)
    db.commit()
    db.refresh(user_scent_meta_in_db)

    return user_scent_meta_in_db


@router.get(
    "/user_scent/{user_scent_id}/similar_scent_items",
    response_model=list[item_schema.ItemApiResultRead],
    tags=["item"],
)
def find_similar_scent_items(
    user_scent_id: int,
    db: Session = Depends(get_db),
):
    user_scent = db.query(user_scent_meta_model.UserScentMeta).get(
        user_scent_id
    )
    if user_scent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User scent not found",
        )

    item_li = db.query(item_model.Item).all()
    if not item_li:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No item found",
        )

    item_similarities = scent_service.find_similar_scent_items(
        user_scent,
        item_li,
    )

    for item, similarity in item_similarities:
        item.similarity = similarity

    sorted_response = sorted(
        [item for item, _ in item_similarities],
        key=lambda x: x.similarity,
        reverse=True,
    )

    return sorted_response
