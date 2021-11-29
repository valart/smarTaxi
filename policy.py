from abc import ABC, abstractmethod
from person import *
from car import *


class Policy(ABC):

    def __init__(self, cars: list, people: list, distances: dict):
        self.cars = cars
        self.people = people
        self.distances = distances

    def score(self, car_id: int, time: int) -> np.array:
        non_target = [p.state != PersonState.waiting and p not in self.cars[car_id].passengers for p in self.people]
        scores = self._score(car_id, time)
        scores[non_target] = np.inf
        return scores

    @abstractmethod
    def _score(self, car_id: int, time: int) -> np.array:
        pass


class DummyPolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.ndarray:
        return np.random.rand(len(self.people))


class ClosestPolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        v1 = self.cars[car_id].at
        return np.array([self.distances[(v1, p.where_to())] if p.where_to() is not None else np.inf for p in self.people])


class QueuePolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        return np.array(range(len(self.people)), dtype=np.float)
