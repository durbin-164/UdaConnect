from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class Person:
    id: int
    first_name: str
    last_name: str
    company_name: str


@dataclass()
class Location:
    id: int
    person_id: int
    creation_time: str
    longitude: float
    latitude: float


@dataclass
class Connection:
    location: Location
    person: Person
