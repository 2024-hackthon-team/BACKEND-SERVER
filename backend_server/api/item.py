from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import backend_server.models.item as item_model
import backend_server.schemas.item as item_schema
from backend_server.database import get_db

router = APIRouter(tags=["item"])


@router.post(
    "/item",
    response_model=item_schema.ItemApiRead,
)
async def create_item(
    item: item_schema.ItemApiCreate,
    db: Session = Depends(get_db),
):

    obj_in = {
        **item.model_dump(),
        "item_tags": [],
    }

    for tag in item.item_tags:
        item_tag = (
            db.query(item_model.ItemTag)
            .where(item_model.ItemTag.item_tag_name == tag)
            .first()
        )
        if item_tag is None:
            item_tag = item_model.ItemTag(item_tag_name=tag)

        obj_in["item_tags"].append(item_tag)

    item = item_model.Item(**obj_in)

    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        # errの種類を指定してエラーを返す
    except IntegrityError as e:
        if "foreign key constraint" in str(e) and "scent_id" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scent not found",
            )
        raise e

    return item


@router.get(
    "/item/{item_id}",
    response_model=item_schema.ItemApiRead,
)
async def read_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = db.query(item_model.Item).get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.patch(
    "/item/{item_id}/scent",
    response_model=item_schema.ItemApiRead,
)
def register_scent_to_item(
    item_id: int,
    scent_id: int,
    db: Session = Depends(get_db),
):
    item: item_model.Item = db.query(item_model.Item).get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    item.scent_id = scent_id

    try:
        db.add(item)
        db.commit()
        db.refresh(item)
    except IntegrityError as e:
        if "foreign key constraint" in str(e) and "scent_id" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scent not found",
            )
        raise e

    return item
