from QueueManager import QueueClient
from task import Task

class Minion (QueueClient):
    def __init__(self):
        super().__init__()
        
    def do_job(self):
        task = self.task_queue.get()
        id = task.get_identifier()
        work = task.work()
        print(f"job {id}, take by a minion. result {work}")
        result = (id, work)
        self.result_queue.put(result)

if __name__ == '__main__':
    minion = Minion()
    while True:
        minion.do_job()
        