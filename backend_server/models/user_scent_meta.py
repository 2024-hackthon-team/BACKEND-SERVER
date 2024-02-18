from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend_server.database import Base


class UserScentMeta(Base):
    __tablename__ = "user_scent_meta"

    id = Column(Integer, primary_key=True)
    label = Column(String(128), nullable=False, default="新しい香り")
    scent_id = Column(Integer, ForeignKey("scents.id"), nullable=False)
    scent = relationship("Scent", back_populates="user_scent_meta")
