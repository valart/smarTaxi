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


class QueuePolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        return np.array(range(len(self.people)), dtype=np.float)


class NearestPolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        v1 = self.cars[car_id].at
        return np.array([self.distances[(v1, p.where_to())] if p.where_to() is not None else np.inf for p in self.people])


class NearestWithDistPolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        score = []
        car_location = self.cars[car_id].at
        for person in self.people:
            if person.where_to() is not None:
                if person.state == PersonState.waiting or person.state == PersonState.assigned:
                    score.append(self.distances[(car_location, person.s)] + self.distances[(person.s, person.t)])
                else:
                    score.append(self.distances[(car_location, person.where_to())])
            else:
                score.append(np.inf)
        return np.array(score)


class DiscountedNearestPolicy(Policy):
    
    def _score(self, car_id: int, time: int) -> np.array:
        v1 = self.cars[car_id].at
        return np.array([self.distances[(v1, p.where_to())] / (time - p.time_init + 1) if p.where_to() is not None else np.inf for p in self.people])

    
class DiscountedNearestWithDistPolicy(Policy):

    def _score(self, car_id: int, time: int) -> np.array:
        score = []
        car_location = self.cars[car_id].at
        for person in self.people:
            if person.where_to() is not None:
                wait_time = (time - person.time_init) if (time - person.time_init) > 0 else 1
                if person.state == PersonState.waiting or person.state == PersonState.assigned:
                    score.append((self.distances[(car_location, person.s)] + self.distances[(person.s, person.t)]) / (wait_time))
                else:
                    score.append((self.distances[(car_location, person.where_to())]) / (wait_time))
            else:
                score.append(np.inf)
        return np.array(score)


class WeightedNearestWithDistPolicy(Policy):
    
    def _score(self, car_id: int, time: int) -> np.array:
        score = []
        car_loc = self.cars[car_id].at
        for person in self.people:
            if person.where_to() is not None:
                score.append((self.distances[(car_loc,person.s)]+self.distances[(person.s,person.t)])*np.exp(-1/self.distances[(person.s,person.t)]))
            else:
                score.append(np.inf)
        return np.array(score)
