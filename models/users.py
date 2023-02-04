from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    user_hash: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"lastname={self.lastname!r}, user_hash={self.user_hash!r})"
        )
