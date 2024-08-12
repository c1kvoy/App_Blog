from src.back.database.db import Base

from sqlalchemy.orm import mapped_column, Mapped


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
