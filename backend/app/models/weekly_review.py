import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Satisfaction(str, enum.Enum):
    HAPPY = "happy"
    NEUTRAL = "neutral"
    UNHAPPY = "unhappy"


class WeeklyReviewModel(Base):
    __tablename__ = "weekly_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    week_start: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    week_end: Mapped[date] = mapped_column(Date, nullable=False)
    total_spent: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    vs_prev_week_pct: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    top_categories: Mapped[list | None] = mapped_column(JSON, nullable=True)
    satisfaction: Mapped[Satisfaction | None] = mapped_column(
        Enum(Satisfaction, native_enum=False), nullable=True
    )
    insights: Mapped[list | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
