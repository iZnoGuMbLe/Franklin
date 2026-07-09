from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=True
    )
    icon: Mapped[str] = mapped_column(String(50), default="folder", nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#888888", nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    parent: Mapped["CategoryModel | None"] = relationship(
        "CategoryModel", remote_side="CategoryModel.id", back_populates="children"
    )
    children: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel", back_populates="parent", cascade="all, delete-orphan"
    )
