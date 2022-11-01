import logging
import os
import threading
from collections import deque
from datetime import datetime
from typing import Callable

from file_task import write_text
from system_task import file_system_job
from web_task import get_request_job


logging.basicConfig(level='WARNING', filename='mylog.log')
logger = logging.getLogger()

cond = threading.Condition()
event = threading.Event()


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Job:
    def __init__(
            self, task: Callable, start_at: datetime = datetime.now(), max_working_time: int = -1, tries: int = 0,
            depedencies: list = []
    ) -> None:
        self.task = task
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.depedencies = depedencies

    @staticmethod
    @coroutine
    def run() -> None:
        while True:
            try:
                func, tries = (yield)
                try:
                    func()
                except Exception:
                    logger.warning('Error - task')
                    while tries > 0:
                        logger.warning('Another attempt')
                        try:
                            func()
                        except Exception:
                            logger.warning('Error - task')
                        tries -= 1
            except (GeneratorExit, StopIteration):
                raise


class Scheduler:
    def __init__(self, pool_size: int = 10) -> None:
        self.queue = deque(maxlen=pool_size)
        self.corutine = Job.run()

    def schedule(self, *args: Job) -> None:
        logger.warning('Get tasks')
        for arg in args:
            self.queue.append(arg)

    def run(self) -> None:
        try:
            done_dop = []
            while self.queue:
                job = self.queue.popleft()
                now = datetime.now()
                sec = (job.start_at - now).total_seconds()
                if job.depedencies:
                    logger.warning('Task with dependencies')
                    with open('depedencies.txt', 'w') as f:
                        for task in job.depedencies:
                            if task in self.queue:
                                f.write(f'{task.task.__name__}' + '\n')
                    with cond:
                        cond.wait()
                        logger.warning('Dependencies - done, task starts')
                        self.corutine.send((job.task, job.tries))
                else:
                    if sec > 0:
                        logger.warning('Task starts timer')
                        timer = threading.Timer(interval=sec, function=self.corutine.send, args=(job.task, job.tries, ))
                        timer.run()
                    else:
                        logger.warning('Get task')
                        self.corutine.send((job.task, job.tries,))
                        if 'depedencies.txt' in os.listdir():
                            with open('depedencies.txt', 'r') as files:
                                for lines in files:
                                    if job.task.__name__ in lines:
                                        done_dop.append(job.task.__name__)
                if 'depedencies.txt' in os.listdir():
                    logger.warning('Check are depedencies done')
                    with open('depedencies.txt', 'r+') as file:
                        lines = len(file.readlines())
                    if lines == len(done_dop) and len(done_dop) > 0:
                        with cond:
                            logger.warning('Send task')
                            cond.notify()
        except KeyboardInterrupt:
            raise


if __name__ == '__main__':
    scheduler = Scheduler()
    j1 = Job(get_request_job, start_at=datetime(2022, 10, 28, 3, 00, 30))
    j2 = Job(file_system_job, start_at=datetime(2022, 10, 27, 23, 52, 50))
    j3 = Job(write_text, start_at=datetime(2022, 10, 29, 13, 4, 40), depedencies=[j1, j2])
    scheduler.schedule(j3, j1, j2)
    thread1 = threading.Thread(target=scheduler.run)
    thread2 = threading.Thread(target=scheduler.run)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
