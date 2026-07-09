import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CategorizationMethod(str, enum.Enum):
    AUTO_RULE = "auto_rule"
    AUTO_MCC = "auto_mcc"
    AUTO_MERCHANT = "auto_merchant"
    AUTO_BANK = "auto_bank"
    GUIDED = "guided"
    MANUAL = "manual"
    UNCATEGORIZED = "uncategorized"


class TransactionSource(str, enum.Enum):
    FILE_IMPORT = "file_import"
    MANUAL_ENTRY = "manual_entry"


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    import_id: Mapped[int | None] = mapped_column(
        ForeignKey("import_jobs.id", ondelete="SET NULL"), nullable=True
    )

    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False)
    merchant_name: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )

    mcc_code: Mapped[str | None] = mapped_column(String(4), nullable=True)
    bank_category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    categorization_method: Mapped[CategorizationMethod] = mapped_column(
        Enum(CategorizationMethod, native_enum=False),
        default=CategorizationMethod.UNCATEGORIZED,
        nullable=False,
    )
    source: Mapped[TransactionSource] = mapped_column(
        Enum(TransactionSource, native_enum=False),
        nullable=False,
    )

    is_income: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)

    duplicate_of: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True
    )
    dedup_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
