from QueueManager import QueueClient
from task import Task


class Boss(QueueClient):
    def create_job(self, identifier=0, size=None):
        task = Task(identifier=identifier, size=size)
        self.task_queue.put(task)

    def print_result(self):
        task = self.result_queue.get()
        time = task.get_time()
        id = task.get_identifier()
        print(f"Tâche {id}")
        print(f"\tTemps d'exécution : {time}")


if __name__ == "__main__":
    boss = Boss()
    nb_job = 10
    for i in range(nb_job):
        boss.create_job(i)
        print(f"job {i} create")

    for i in range(nb_job):
        boss.print_result()
