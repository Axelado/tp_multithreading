from QueueManager import QueueClient
from task import Task
import time


class Boss(QueueClient):
    def create_job(self, identifier=0, size=None):
        task = Task(identifier=identifier, size=size)
        self.task_queue.put(task)

    def get_result(self):
        task = self.result_queue.get()
        exec_time = task.get_time()
        id = task.get_identifier()
        return id, exec_time


if __name__ == "__main__":
    boss = Boss()
    nb_job = 100
    problem_size = 1500
    total_exec_time = 0  # somme des temps d'exécution des différents jobs

    for i in range(nb_job):
        boss.create_job(i, problem_size)
        print(f"job {i} créé")

    start = 0
    for i in range(nb_job):
        id, exec_time = boss.get_result()
        if i == 0:
            start = (
                time.perf_counter()
            )  # commence à compter le temps quand la premiere tache est réalisé
        total_exec_time += exec_time
        print(f"Tâche {id}")
        print(f"\tTemps d'exécution : {exec_time}")

    total_time = (
        time.perf_counter() - start
    )  # Temps total mis pour l'exécution des taches
    print(f"Temps total d'éxécution : {total_exec_time}")
    print(f"Temps total : {total_time}")
