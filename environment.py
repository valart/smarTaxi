from person import *
from policy import Policy
import pandas as pd
import numpy as np


class Environment:

    def __init__(self, cars: list, people: list, policy: Policy, distances: pd.DataFrame):
        self.cars = cars
        self.people = people
        self.policy = policy
        self.distances = distances

    def step(self, time: int, distances: dict):
        for car in self.cars:
            if car.free_check(time):
                scores = np.array(self.policy.score(car.id, time))
                if scores.min() == np.inf:
                    return
                if car.is_full():
                    p = np.argmin(scores[[p.id for p in car.passengers]])
                    person_id = car.passengers[p].id
                else:
                    person_id = np.argmin(scores)
                person = self.people[person_id]
                if person.state == PersonState.waiting:
                    car.ride_to_start(person, time, distances[car.at, person.s])
                elif person.state == PersonState.riding:
                    car.ride_to_end(person, time, distances[car.at, person.t])

    def stats(self):
        s = pd.concat([p.stats() for p in self.people if p.stats() is not None])
        t = np.array([p.state == PersonState.arrived for p in self.people]).mean()
        return s, t
