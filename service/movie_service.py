from models import Movie
from typing import List
from returns.result import Result, Success, Failure
import statistics

def most_common_genre(movies: List[Movie]) -> Result[str, str]:
   try:
       genres = [movie['genre'] for movie in movies]
       return Success(statistics.mode(genres))
   except statistics.StatisticsError:
       return Failure("No unique mode found")
