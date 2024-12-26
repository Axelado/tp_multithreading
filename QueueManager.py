from multiprocessing.managers import BaseManager
from multiprocessing import Queue

PORT = 50000
PASSWORD = b"axelTheGoat007"


class QueueManager(BaseManager):
    pass


class QueueClient:
    def __init__(self):
        self.port = PORT
        self.password = PASSWORD
        QueueManager.register("get_task_queue")
        QueueManager.register("get_result_queue")

        self.manager = QueueManager(address=("localhost", PORT), authkey=PASSWORD)
        self.manager.connect()

        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()


if __name__ == "__main__":
    task_queue = Queue(100)
    result_queue = Queue(100)
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)

    manager = QueueManager(address=("localhost", PORT), authkey=PASSWORD)
    server = manager.get_server()
    server.serve_forever()
