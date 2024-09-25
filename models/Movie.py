from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.base import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_title = Column(String(255), nullable=False)
    movie_gener = Column(String(32), nullable=False)
    movie_year = Column(Integer, nullable=False)

    rentals = relationship(
        "Rental",
        lazy="joined",
        back_populates="movie",
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (f"<Movie(id={self.id}, title={self.movie_title}, "
                f"gener={self.movie_gener}, year={self.movie_year})>")