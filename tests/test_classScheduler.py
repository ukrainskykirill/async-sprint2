from datetime import datetime

from corutine import Scheduler, Job

def go():
    for i in range(10):
        print(15)

def kotik():
    print('котик')

def jo_two():
    for i in range(10):
        print(12)

class TestScheduler:
    def setup(self) -> None:
        self.job = Job(go, start_at=datetime(2022, 10, 29, 13, 4, 40))
        self.job2 = Job(kotik, start_at=datetime(2022, 10, 29, 13, 4, 40))
        self.job3 = Job(jo_two, start_at=datetime(2022, 10, 29, 13, 4, 40))
        self.sch = Scheduler()
        self.corutine = self.job.run()

    def test_schedule(self) -> None:
        self.sch.schedule(self.job)
        assert len(self.sch.queue) == 1

    def test_sch_run(self) -> None:
        self.sch.schedule(self.job3, self.job, self.job2)
        self.sch.run()
        assert len(self.sch.queue) == 0