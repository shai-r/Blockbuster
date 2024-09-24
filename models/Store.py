from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.base import Base


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String(255), nullable=False)
    store_state = Column(String(7), nullable=False)
    store_city = Column(String(31), nullable=False)
    store_address = Column(String(63), nullable=False)
    rental_fee = Column(Float, default=0.0)
    late_fee = Column(Float, default=0.0)

    subscriptions = relationship(
        "Subscription",
        lazy="joined",
        back_populates="store"
    )

    def __repr__(self):
        return (f"<Store(id={self.id}, name={self.store_name}, "
                f"state={self.store_state}, city={self.store_city}, "
                f"address={self.store_address}, rental fee={self.rental_fee}, "
                f"late fee={self.late_fee})>")