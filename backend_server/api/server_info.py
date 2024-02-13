from fastapi import APIRouter

from backend_server.config import config

router = APIRouter()


@router.get("/health_check")
async def health_check():
    return {
        "status": "ok",
        "server_info": {
            "deploy_env": config.deploy_env,
        },
    }
