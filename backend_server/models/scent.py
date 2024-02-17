from sqlalchemy import JSON, Column, DateTime, Double, Integer
from sqlalchemy.orm import relationship

from backend_server.database import Base


class Scent(Base):
    __tablename__ = "scents"

    id = Column(Integer, primary_key=True, index=True)
    sensored_at = Column(DateTime, nullable=False)
    temperature = Column(Double, nullable=False)
    humidity = Column(Double, nullable=False)
    pressure = Column(Double, nullable=False)
    gas_feature = Column(JSON, nullable=False)

    item = relationship("Item", back_populates="scent")
    # user_scent_meta = relationship("UserScentMeta", back_populates="scent")
