"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""
from typing import Any

from structures.m_util import Hashable


class Entry(Hashable):
    """
    Implements a simple type that holds keys and values. Extends the Hashable
    type to ensure get_hash() is available/used for arbitrary key types.
    """
    def __init__(self, key: Any, value: Any) -> None:
        """
        An entry has a key (used for comparing to other entries or for hashing)
        and a corresponding value which represents some arbitrary data associated
        with the key. 
        """
        self._key = key
        self._value = value

    def get_key(self) -> Any:
        return self._key

    def get_value(self) -> Any:
        return self._value

    def update_key(self, nk: Any) -> None:
        self._key = nk

    def update_value(self, nv: Any) -> None:
        self._value = nv

    def __eq__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if keys are
        equal, false otherwise. Relies on keys having __eq__ implemented.
        """
        return self.get_key() == other.get_key()

    def __lt__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if self is less
        than other. Relies on keys having __lt__ implemented.
        """
        return self.get_key() < other.get_key()

    def get_hash(self) -> int:
        """
        Returns a hash of self._key - this hash function MUST be implemented if
        you need to hash Entry types. In other words, do not use Python's magic
        __hash__() function, but rather, you need to make your own. You are
        welcome to use existing functions, but you need to implement it here
        (and cite it in your report/statement file).
        """
        hash_value = 0
        key_str = str(self._key)
        for char in key_str:
            hash_value += ord(char)
        return hash_value
    # You may add helpers/additional functionality below if you wish


class Destination(Entry):
    """
    A special type of entry that tracks the monetary and stopover costs of
    a trip from some origin to a destination. You can use _value however
    you like, or ignore it completely.
    """
    def __init__(self, key: Any, value: Any, cost_money: int, cost_stopover: int) -> None:
        super().__init__(key, value)
        self._cost_m = cost_money
        self._cost_s = cost_stopover

    def get_cost_money(self) -> int:
        return self._cost_m

    def get_cost_stopover(self) -> int:
        return self._cost_s

    def update_cost_money(self, ncm) -> None:
        self._cost_m = ncm

    def update_cost_stopover(self, ncs) -> None:
        self._cost_s = ncs

    # override method
    def __lt__(self, other: "Destination") -> bool:
        if self._cost_m < other._cost_m:
            return True
        elif self._cost_m == other._cost_m:
            if self._cost_s < other._cost_s:
                return True
            elif self._cost_s == other._cost_s:
                return self._key < other._key
        return False

    def __str__(self) -> str:
        return f"Destination(ID: {self._key}, Cost: {self._cost_m}, Stopovers: {self._cost_s})"
    # You may add helpers/additional functionality below if you wish, and
    # you may override inherited methods here if you wish
