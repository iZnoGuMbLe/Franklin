import enum
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AchievementType(str, enum.Enum):
    FIRST_ENTRY = "first_entry"
    STREAK_7 = "streak_7"
    STREAK_30 = "streak_30"
    STREAK_100 = "streak_100"
    BUDGET_MASTER = "budget_master"
    ECONOMIST = "economist"
    DETECTIVE = "detective"
    SNIPER = "sniper"


class AchievementModel(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[AchievementType] = mapped_column(
        Enum(AchievementType, native_enum=False), nullable=False, unique=True
    )
    unlocked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_seen: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
