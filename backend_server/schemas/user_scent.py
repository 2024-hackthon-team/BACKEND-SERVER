from pydantic import BaseModel, ConfigDict


class UserScentDBCreate(BaseModel):
    label: str = "新しい香り"
    scent_id: int


class UserScentApiRead(UserScentDBCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserScentApiUpdate(BaseModel):
    label: str


class WebSocketMessage(BaseModel):
    message: str
