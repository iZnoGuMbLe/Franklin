import enum
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BankType(str, enum.Enum):
    TINKOFF = "tinkoff"
    SBER = "sber"
    ALFA = "alfa"
    VTB = "vtb"
    RAIFFEISEN = "raiffeisen"
    UNIVERSAL = "universal"


class ImportStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    CATEGORIZING = "categorizing"
    QUESTIONS_READY = "questions_ready"
    DONE = "done"
    FAILED = "failed"


class ImportJobModel(Base):
    __tablename__ = "import_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_type: Mapped[BankType] = mapped_column(
        Enum(BankType, native_enum=False), nullable=False
    )
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus, native_enum=False),
        default=ImportStatus.UPLOADED,
        nullable=False,
    )
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_transactions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    auto_categorized: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
