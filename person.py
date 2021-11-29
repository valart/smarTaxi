from enum import Enum
import pandas as pd
import numpy as np


class PersonState(Enum):
    waiting = 0
    assigned = 1
    riding = 2
    arrived = 3


class Person:

    def __init__(self, id_, s, t, time_init):
        self.id = id_
        self.s = s
        self.t = t
        self.state = PersonState.waiting
        self.time_init = time_init

    def assign(self, time_assign: int):
        self.state = PersonState.assigned
        self.time_assign = time_assign

    def start_ride(self, time_start: int):
        self.state = PersonState.riding
        self.time_start = time_start

    def finish_ride(self, time_finish: int):
        self.state = PersonState.arrived
        self.time_finish = time_finish

    def where_to(self):
        if self.state == PersonState.waiting:
            return self.s
        elif self.state == PersonState.riding:
            return self.t
        return None

    def stats(self):
        if self.state == PersonState.arrived:
            return pd.DataFrame({
                'assigning': [self.time_assign - self.time_init],
                'waiting': [self.time_start - self.time_assign],
                'riding': [self.time_finish - self.time_start]
            }, index=[self.id])

    def __repr__(self):
        return f'Person {self.id}'


class PersonFactory:

    def __init__(self):
        self.max_id = -1

    def generate_person(self, nodes, time):
        self.max_id += 1
        return Person(self.max_id, *np.random.choice(nodes, 2, replace=False), time)
