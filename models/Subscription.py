from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from config.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    rental_id = Column(Integer, ForeignKey("rentals.id"), nullable=False)
    total_payment = Column(Float, nullable=False, default=0.0)

    user = relationship("User", back_populates="subscriptions")
    store = relationship("Store", back_populates="subscriptions")
    rentals = relationship("Rental",
        lazy="joined",
        back_populates="subscription"
    )


    def __repr__(self):
        return (f"<Subscription(id={self.id}, user id={self.user_id}, "
                f"store id={self.store_id}, total payment={self.total_payment})>")