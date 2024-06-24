from itertools import pairwise
from typing import TypeVar
from collections.abc import Iterable, Generator


T = TypeVar('T')


def cyclic_pairwise(iterable: Iterable[T]) -> Generator[tuple[T, T]]:
    # naively implemented for now
    iterable = list(iterable)
    yield from pairwise(iterable)
    yield iterable[-1], iterable[0]