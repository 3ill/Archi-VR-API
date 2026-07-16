import uuid
from datetime import UTC, datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String

from app.db.db import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, ForeignKey("waitlist.email"), nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
