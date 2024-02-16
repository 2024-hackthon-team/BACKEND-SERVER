from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import backend_server.schemas.scent as scent_schema
import backend_server.service.scent as scent_service
from backend_server.database import get_db

router = APIRouter()


@router.post("/item-scent")
def create_item_scent(
    scent_data: scent_schema.ScentApiCreate,
    db: Session = Depends(get_db),
):

    db_obj_in = scent_service.convert_api_data_to_db_data(scent_data)
    scent_service.create_scent(db, db_obj_in)

    return {"message": "post scent data completed."}
