import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RuleMatchType(str, enum.Enum):
    EXACT = "exact"
    CONTAINS = "contains"
    REGEX = "regex"
    MCC = "mcc"


class RuleModel(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_type: Mapped[RuleMatchType] = mapped_column(
        Enum(RuleMatchType, native_enum=False), nullable=False
    )
    match_value: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    hit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
