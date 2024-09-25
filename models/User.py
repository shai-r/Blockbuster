from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(127), nullable=False)
    user_email = Column(String(63), unique=True, nullable=False)
    user_phone = Column(Integer, nullable=False)

    subscribers = relationship(
        "Subscriber",
        lazy="joined",
        back_populates="user",
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (f"<User(id={self.id}, name={self.user_name}, "
                f"email={self.user_email}, phone={self.user_phone})>")