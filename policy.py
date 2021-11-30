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


class TakeOnePolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        if self.cars[car_id].passengers.count(None) != 4:
            return np.array([0 if personIdx == self.cars[car_id].passengers[0].id else np.inf for personIdx in range(len(self.people))])

        closest_distance = np.inf
        closest_person_idx = -1

        for personIdx in range(len(self.people)):
            if self.people[personIdx].where_to() is None:
                continue
            if self.distances[(self.cars[car_id].at, self.people[personIdx].where_to())] < closest_distance:
                closest_distance = self.distances[(self.cars[car_id].at, self.people[personIdx].where_to())]
                closest_person_idx = personIdx
        return np.array([0 if personIdx == closest_person_idx else np.inf for personIdx in range(len(self.people))])


class TakeUpTo4Policy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        if self.cars[car_id].passengers.count(None) != 4:
            return np.array([self.distances[(self.cars[car_id].at, self.people[personIdx].where_to())] if self.people[personIdx] in self.cars[car_id].passengers else np.inf for personIdx in range(len(self.people))])

        closest_distances = [np.inf] * (4 if len(self.people) > 4 else len(self.people))
        closest_person_indexes = [-1] * (4 if len(self.people) > 4 else len(self.people))

        for personIdx in range(len(self.people)):
            if self.people[personIdx].where_to() is None:
                continue
            if self.distances[(self.cars[car_id].at, self.people[personIdx].where_to())] < max(closest_distances):
                index = closest_distances.index(max(closest_distances))
                closest_distances[index] = self.distances[(self.cars[car_id].at, self.people[personIdx].where_to())]
                closest_person_indexes[index] = personIdx
        return np.array([closest_distances[closest_person_indexes.index(personIdx)] if personIdx in closest_person_indexes else np.inf for personIdx in range(len(self.people))])

