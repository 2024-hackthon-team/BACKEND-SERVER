from backend_server.api.item import router as item_router
from backend_server.api.scent import router as scent_router
from backend_server.api.server_info import router as server_info_router
from backend_server.api.user_scent import router as user_scent_router

__all__ = [
    "server_info_router",
    "scent_router",
    "item_router",
    "user_scent_router",
]
