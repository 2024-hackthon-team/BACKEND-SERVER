from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend_server.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    product_label = Column(String(255), nullable=False)
    img_url = Column(String(1024))

    scent_id = Column(Integer, ForeignKey("scents.id"))
    scent = relationship("Scent", back_populates="item")

    item_tags = relationship(
        "ItemTag",
        secondary="tag_relations",
        back_populates="items",
    )


class ItemTag(Base):
    __tablename__ = "item_tags"

    id = Column(Integer, primary_key=True)
    item_tag_name = Column(
        String(64),
        nullable=False,
        unique=True,
    )

    items = relationship(
        "Item",
        secondary="tag_relations",
        back_populates="item_tags",
    )


class TagRelation(Base):
    __tablename__ = "tag_relations"

    item_id = Column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True
    )
    item_tag_id = Column(
        Integer,
        ForeignKey("item_tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
