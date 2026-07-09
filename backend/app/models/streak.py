from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class StreakModel(Base):
    __tablename__ = "streaks"

    id: Mapped[int] = mapped_column(primary_key=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    freeze_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    freeze_used_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_active_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
