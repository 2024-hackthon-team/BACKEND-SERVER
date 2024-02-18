from pydantic import BaseModel, ConfigDict


class UserScentApiRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str = "新しい香り"
    scent_id: int


class UserScentApiUpdate(BaseModel):
    label: str
