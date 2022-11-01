from corutine import Job

def go_error():
    for i in range(10):
        print(15)
        raise ValueError


class TestJob:
    def setup(self) -> None:
        self.job = Job(go_error)
        self.corutine = self.job.run()
        self.tries = 4

    def test_run_tries(self):
        assert self.corutine.send((self.job.task, self.tries)) == None





