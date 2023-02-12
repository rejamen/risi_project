from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from .base import Base
from typing import List

# m2m relationships
# user_parent_rel = Table(
#     "user_parent_rel",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
#     Column("parent_id", Integer, ForeignKey("users.id"), primary_key=True),
# )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    user_hash: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(300))
    # responsible: Mapped[int] = Column(Integer, ForeignKey("users.id"))  # o2m relationship
    # m2m
    # parent_ids: Mapped[List[int]] = relationship(
    #     "User",
    #     secondary=user_parent_rel,
    #     primaryjoin=id==user_parent_rel.c.parent_id,
    #     secondaryjoin=id==user_parent_rel.c.user_id,
    #     back_populates="child_ids"
    # )
    # child_ids: Mapped[List[int]] = relationship(
    #     "User",
    #     secondary=user_parent_rel,
    #     primaryjoin=id==user_parent_rel.c.user_id,
    #     secondaryjoin=id==user_parent_rel.c.parent_id,
    #     back_populates="parent_ids"
    # )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"lastname={self.lastname!r}, user_hash={self.user_hash!r})"
            f"description={self.description!r}"
        )
