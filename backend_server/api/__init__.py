from backend_server.api.item import router as item_router
from backend_server.api.scent import router as scent_router
from backend_server.api.server_info import router as server_info_router

__all__ = [
    "server_info_router",
    "scent_router",
    "item_router",
]
