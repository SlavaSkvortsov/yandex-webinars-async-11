from dataclasses import dataclass, field
from time import sleep
from typing import Any, Callable, Optional


@dataclass
class Scheduler:
    running_jobs: list['Job'] = field(default_factory=list)

    def add_job(self, job: 'Job') -> None:
        self.running_jobs.append(job)

    def run(self):
        while True:
            try:
                for job in self.running_jobs:
                    job.evaluate()

            except StopIteration:
                print('Job finished')
                break


@dataclass
class Job:
    name: str
    task: Callable
    _task: Optional[Any] = None

    def evaluate(self):
        if self._task is None:
            self._task = self.task(self.name)

        try:
            next(self._task)
        except Exception:
            self._task = self.task(self.name)


def task(name: str) -> None:
    for i in range(10):
        sleep(1)
        print(name, i)
        yield


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.add_job(Job('Job 1', task))
    scheduler.add_job(Job('Job 2', task))
    scheduler.run()
