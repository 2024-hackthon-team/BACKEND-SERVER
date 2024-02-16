import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_server.api import scent_router, server_info_router
from backend_server.config import config

if config.deploy_env != "production":
    logging.basicConfig(level=logging.DEBUG)


app = FastAPI()
app.include_router(server_info_router)
app.include_router(scent_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
