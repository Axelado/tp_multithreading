import threading

from Minion import Minion

nb_minions = 2


# Fonction exécutée par chaque thread
def worker():
    minion = Minion()
    while True:
        minion.do_job()


# Créer et démarrer 10 threads
threads = []
for _ in range(nb_minions):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)
