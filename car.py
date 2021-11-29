import numpy as np
from enum import Enum
from person import Person


class CarState(Enum):
    idle = 0
    to_start = 1
    to_end = 2


class Car:

    def __init__(self, id_: int, start_node: int, time_init: int, limit: int):
        self.id = id_
        self.at = start_node
        self.state = CarState.idle
        self.limit = limit
        self.busy_until = time_init - 1
        self.passengers = [None] * limit
        self.current_person = None

    def ride_to_start(self, person: Person, time: int, distance: float):
        self.current_person = person
        self.state = CarState.to_start
        person.assign(time)
        self.at = person.s
        self.busy_until = time + int(distance)

    def ride_to_end(self, person: Person, time: int, distance: float):
        self.current_person = person
        self.state = CarState.to_end
        self.at = person.t
        self.busy_until = time + int(distance)

    def pick_up(self, time: int):
        self.passengers[self.passengers.index(None)] = self.current_person
        self.current_person.start_ride(time)
        self.current_person = None

    def drop_off(self, time: int):
        self.passengers[self.passengers.index(self.current_person)] = None
        self.current_person.finish_ride(time)
        self.current_person = None

    def is_full(self) -> bool:
        return all(p is not None for p in self.passengers)

    def free_check(self, time: int) -> bool:
        if time >= self.busy_until:
            if self.state == CarState.to_start:
                self.pick_up(time)
            elif self.state == CarState.to_end:
                self.drop_off(time)
            self.state = CarState.idle
        return self.state == CarState.idle

    def __repr__(self):
        return f'Car {self.id}'


class CarFactory:

    def __init__(self):
        self.max_id = -1

    def generate_car(self, nodes, time):
        self.max_id += 1
        return Car(
            self.max_id,
            np.random.choice(nodes),
            time,
            4
        )
