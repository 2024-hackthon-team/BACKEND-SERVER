from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend_server.models.user_scent_meta as user_scent_meta_model
import backend_server.schemas.item as item_schema
import backend_server.schemas.scent as scent_schema
import backend_server.schemas.user_scent as user_scent_schema
import backend_server.service.scent as scent_service
from backend_server.database import get_db

router = APIRouter(tags=["user_scent"])


@router.post(
    "/user_scent",
    response_model=user_scent_schema.UserScentApiRead,
)
def create_user_scent(
    scent_api_data: scent_schema.ScentApiCreate,
    db: Session = Depends(get_db),
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
    # TODO: User ws to notify web client

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
    # ! Not implemented
    summary="Not implemented",
)
def update_user_scent(
    user_scent_id: int,
    updated_user_scent: user_scent_schema.UserScentApiUpdate,
):
    return user_scent_schema.UserScentApiRead(
        id=user_scent_id,
        scent_id=1,
        **updated_user_scent.model_dump(),
    )


@router.get(
    "/user_scent/{user_scent_id}/similar_scent_items",
    response_model=list[item_schema.ItemApiResultRead],
    tags=["item"],
    # ! Not implemented
    summary="Not implemented",
)
def find_similar_scent_items(user_scent_id: int):
    return [
        item_schema.ItemApiResultRead(
            id=1,
            item_name="item_name",
            product_label="product_label",
            scent_id=1,
            img_url="img_url",
            similarity=0.5,
            item_tags=[
                item_schema.ItemTagApiRead(id=1, item_tag_name="tag1"),
                item_schema.ItemTagApiRead(id=2, item_tag_name="tag2"),
            ],
        )
    ] * 10
