from datetime import datetime
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Enum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.types import TargetTypeEnum
from app.database.base import Base
from app.models.feature_flag import FeatureFlag


class FeatureFlagOverride(Base):
    __tablename__ = "feature_flag_overrides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    feature_flag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("feature_flags.id", ondelete="CASCADE"),
        nullable=False,
    )
    feature_flag: Mapped[FeatureFlag] = relationship(
        "FeatureFlag", back_populates="overrides"
    )

    target_type: Mapped[TargetTypeEnum] = mapped_column(
        Enum(TargetTypeEnum), nullable=False
    )
    target_id: Mapped[str] = mapped_column(String(100), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"<FeatureFlagOverride(id={self.id}, feature_flag_id={self.feature_flag_id}, "
            f"target_type={self.target_type}, target_id={self.target_id}, is_enabled={self.is_enabled})>"
        )


# Make sure to add the reverse relationship in FeatureFlag model:
# FeatureFlag.overrides = relationship("FeatureFlagOverride", back_populates="feature_flag", cascade="all, delete-orphan")
