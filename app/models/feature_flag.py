from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    Text,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rollout_percentage: Mapped[int] = mapped_column(
        Integer, CheckConstraint("rollout_percentage BETWEEN 0 AND 100"), default=100
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    overrides = relationship("FeatureFlagOverride", back_populates="feature_flag")

    def __repr__(self) -> str:
        return f"<FeatureFlag(id={self.id}, key={self.key!r}, enabled={self.is_enabled})>"
