from sqlalchemy import Date, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.base import Base

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rental_date = Column(Date, nullable=False)
    return_date = Column(Date)

    movie = relationship("Movie", back_populates="rentals")
    subscription = relationship("Subscription", back_populates="rentals")

    def __repr__(self):
        return (f"<Rental(id={self.id}, subscription id={self.subscription_id}, "
                f"movie id={self.movie_id}, rental date={self.rental_date}, "
                f"return date={self.return_date})>")