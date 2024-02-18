from fastapi import APIRouter

import backend_server.schemas.scent as scent_schema
import backend_server.schemas.user_scent as user_scent_schema
import backend_server.schemas.item as item_schema

router = APIRouter(tags=["user_scent"])


@router.post(
    "/user_scent",
    response_model=user_scent_schema.UserScentApiRead,
)
def create_user_scent(
    scent_api_data: scent_schema.ScentApiCreate,
):
    return "not implemented yet!"


@router.get(
    "/user_scents",
    response_model=list[user_scent_schema.UserScentApiRead],
)
def get_multiple_user_scent(
    offset: int = 0,
    limit: int = 10,
    desc: bool = True,
):
    return "not implemented yet!"


@router.patch(
    "/user_scent/{user_scent_id}",
    response_model=user_scent_schema.UserScentApiRead,
)
def update_user_scent(
    user_scent_id: int,
    updated_user_scent: user_scent_schema.UserScentApiUpdate,
):
    return "not implemented yet!"


@router.get(
    "/user_scent/{user_scent_id}/similar_scent_items",
    response_model=list[item_schema.ItemApiRead],
    tags=["item"],
)
def find_similar_scent_items(user_scent_id: int):
    return "not implemented yet!"
