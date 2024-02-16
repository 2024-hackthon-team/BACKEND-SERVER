from sqlalchemy import Column, DateTime, Double, Integer, JSON

from backend_server.database import Base


class Scent(Base):
    __tablename__ = "scents"

    id = Column(Integer, primary_key=True, index=True)
    sensored_at = Column(DateTime, nullable=False)
    temperature = Column(Double, nullable=False)
    humidity = Column(Double, nullable=False)
    pressure = Column(Double, nullable=False)
    gas_feature = Column(JSON, nullable=False)
