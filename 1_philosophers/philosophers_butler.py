import threading
import time
from dataclasses import dataclass, field
from enum import Enum

WAIT = 0.5
PHILOSOPHERS = 5


@dataclass
class Fork:
    lock: threading.Lock = field(default_factory=threading.Lock)

    def acquire(self) -> bool:
        return self.lock.acquire()

    def release(self) -> None:
        if self.lock.locked():
            self.lock.release()


class Side(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'


@dataclass
class Philosopher:
    butler: threading.Semaphore
    forks: dict[Side, Fork]
    name: str
    ate_count: int = 0

    def run(self) -> None:
        begin = time.monotonic()
        while time.monotonic() - begin < 5:
            self._eat()
            self._think()

    def _eat(self) -> None:
        acquired = self.butler.acquire(blocking=False)
        if not acquired:
            return

        self._acquire_fork(Side.LEFT)
        self._acquire_fork(Side.RIGHT)
        print(f'{self.name} is eating')
        self.ate_count += 1

        self._release_fork(Side.LEFT)
        self._release_fork(Side.RIGHT)
        self.butler.release()

    def _acquire_fork(self, side: Side) -> None:
        print(f'{self.name} is trying to acquire {side} fork')
        fork = self.forks[side]
        fork.acquire()
        time.sleep(WAIT)

    def _release_fork(self, side: Side) -> None:
        fork = self.forks[side]
        fork.release()

    def _think(self) -> None:
        print(f'{self.name} is thinking')
        time.sleep(WAIT)


def main() -> None:
    butler = threading.Semaphore(PHILOSOPHERS - 1)
    forks = [Fork() for _ in range(PHILOSOPHERS)]

    philosophers = [
        Philosopher(
            butler=butler,
            forks={
                Side.LEFT: forks[i - 1],
                Side.RIGHT: forks[i],
            },
            name=f'Philosopher {i}',
        )
        for i in range(PHILOSOPHERS)
    ]

    threads = [
        threading.Thread(target=philosopher.run)
        for philosopher in philosophers
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for philosopher in philosophers:
        print(f'{philosopher.name} ate {philosopher.ate_count} times')


if __name__ == '__main__':
    main()