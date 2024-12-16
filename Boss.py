from QueueManager import QueueClient
from task import Task

class Boss (QueueClient):
    def create_job(self, identifier=0):
        task = Task(identifier)
        self.task_queue.put(task)
    
    def print_result(self):
        result = self.result_queue.get()
        print(result)
    
if __name__ == '__main__':
    boss = Boss()
    
    for i in range(100):
        boss.create_job(i)
        print(f"job {i} create")
    
    for i in range(100):
        boss.print_result()
                
    
        
        
        