from pydantic import BaseModel, ConfigDict, field_serializer


class ItemBase(BaseModel):
    item_name: str
    product_label: str
    scent_id: int | None = None


class ItemApiCreate(ItemBase):
    item_tags: list[str] = []


class ItemTagApiRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_tag_name: str


class ItemApiRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_tags: list[ItemTagApiRead] = []

    @field_serializer("item_tags")
    def serialize_item_tags(item_tags: list[ItemTagApiRead]) -> list[str]:
        return [item_tag.item_tag_name for item_tag in item_tags]
