from fastapi import APIRouter

import backend_server.schemas.item as item_schema
import backend_server.schemas.scent as scent_schema
import backend_server.schemas.user_scent as user_scent_schema

router = APIRouter(tags=["user_scent"])


@router.post(
    "/user_scent",
    response_model=user_scent_schema.UserScentApiRead,
    # ! Not implemented
    summary="Not implemented",
)
def create_user_scent(
    scent_api_data: scent_schema.ScentApiCreate,
):
    return user_scent_schema.UserScentApiRead(
        id=1,
        label="新しい香り",
        scent_id=1,
    )


@router.get(
    "/user_scents",
    response_model=list[user_scent_schema.UserScentApiRead],
    # ! Not implemented
    summary="Not implemented",
)
def get_multiple_user_scent(
    offset: int = 0,
    limit: int = 10,
    desc: bool = True,
):
    return [
        user_scent_schema.UserScentApiRead(
            id=1,
            label="新しい香り",
            scent_id=1,
        )
    ] * limit


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
    response_model=list[item_schema.ItemApiRead],
    tags=["item"],
    # ! Not implemented
    summary="Not implemented",
)
def find_similar_scent_items(user_scent_id: int):
    return [
        item_schema.ItemApiRead(
            id=1,
            item_name="item_name",
            product_label="product_label",
            scent_id=1,
            img_url="img_url",
            item_tags=[
                item_schema.ItemTagApiRead(id=1, item_tag_name="tag1"),
                item_schema.ItemTagApiRead(id=2, item_tag_name="tag2"),
            ],
        )
    ] * 10
