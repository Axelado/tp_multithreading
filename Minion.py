from QueueManager import QueueClient


class Minion(QueueClient):
    def __init__(self):
        super().__init__()

    def do_job(self):
        task = self.task_queue.get()
        id = task.get_identifier()
        task.work()
        time = task.get_time()
        print(f"job {id}, exécuté par un minion. Temps d'exécution : {time}")
        self.result_queue.put(task)


if __name__ == "__main__":
    minion = Minion()
    while True:
        minion.do_job()
