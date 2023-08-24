import random
import threading
import time
from dataclasses import dataclass, field
from enum import Enum

WAIT = 0.5
PHILOSOPHERS = 5
TIMEOUT = 5


@dataclass
class Fork:
    lock: threading.Lock = field(default_factory=threading.Lock)

    def acquire(self) -> bool:
        return self.lock.acquire(blocking=False)

    def release(self) -> None:
        if self.lock.locked():
            self.lock.release()


class Side(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'


@dataclass
class Philosopher:
    forks: dict[Side, Fork]
    name: str
    ate_count: int = 0

    def run(self) -> None:
        begin = time.monotonic()
        while time.monotonic() - begin < TIMEOUT:
            self._eat()
            self._think()

    def _eat(self) -> None:
        while True:
            if not self._acquire_fork(Side.LEFT):
                continue
            if not self._acquire_fork(Side.RIGHT):
                self._release_fork(Side.LEFT)
                continue
            print(f'{self.name} is eating')
            time.sleep(random.random())
            self.ate_count += 1

            self._release_fork(Side.LEFT)
            self._release_fork(Side.RIGHT)
            return

    def _acquire_fork(self, side: Side) -> bool:
        print(f'{self.name} is trying to acquire {side} fork')
        fork = self.forks[side]
        time.sleep(WAIT)
        return fork.acquire()

    def _release_fork(self, side: Side) -> None:
        fork = self.forks[side]
        fork.release()

    def _think(self) -> None:
        print(f'{self.name} is thinking')
        time.sleep(random.random())


# def main() -> None:
def main() -> None:
    forks = [Fork() for _ in range(PHILOSOPHERS)]
    philosophers = [
        Philosopher(
            name=f'Philosopher {i}',
            forks={
                Side.LEFT: forks[i],
                Side.RIGHT: forks[(i + 1) % 5],
            },
        ) for i in range(5)
    ]

    threads = [threading.Thread(target=philosopher.run) for philosopher in philosophers]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('Philosophers ate:')
    for philosopher in philosophers:
        print(f'{philosopher.name}: {philosopher.ate_count}')


if __name__ == '__main__':
    main()
