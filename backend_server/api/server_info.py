from fastapi import APIRouter
from fastapi.logger import logger

from backend_server.config import config

router = APIRouter()


@router.get("/health_check")
async def health_check():
    logger.debug(f"    - SERVER CONFIG - \n{config.model_dump_json(indent=4)}")
    return {
        "status": "ok",
        "server_info": {
            "deploy_env": config.deploy_env,
        },
    }
