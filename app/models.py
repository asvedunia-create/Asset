from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(255), unique=True, nullable=False, index=True)
    address = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    os_name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    last_scanned_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    services = relationship("Service", back_populates="asset", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=False)

    asset = relationship("Asset", back_populates="services")
