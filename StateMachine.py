from transitions import Machine
from ElectroRoutine import ElectroRoutine
from Routine.RoutineState import Result
#from Routine.TestRoutine import TestRoutine
from Singleton import Singleton
import threading
import queue

q = queue.Queue()


def worker():
    while True:
        item = q.get()
        item()
        q.task_done()


# need to do -> pip install transitions

class StateMachine(object, metaclass=Singleton):
    """ My dynamically extended Model
    Attributes:
        detect(callable): dynamically added method
    """
    states = ['Idle', 'Detecting', 'Detected', 'Analyzing', 'Analyzed', 'Transferring']

    def __init__(self, name):
        # Definition of the state machine
        self.name = name
        self.ElectroRoutine = ElectroRoutine()
        self.machine = Machine(model=self, states=StateMachine.states, initial='Idle', send_event=False)

        self.machine.add_transition(trigger='detect', source='Idle', dest='Detecting', after='RunRoutine')
        self.machine.add_transition(trigger='Abort', source='Detecting', dest='Idle', before='Clear')
        self.machine.add_transition(trigger='RoutineDone', source='Detecting', dest='Idle')

        self.machine.add_transition(trigger='Analyze', source='Idle', dest='Analyzing', after='RunAnalyze')
        self.machine.add_transition(trigger='Abort', source='Analyzing', dest='Idle', before='Clear')
        self.machine.add_transition(trigger='AnalyzingDone', source='Analyzing', dest='Analyzed')

        self.machine.add_transition(trigger='Transfer', source='Analyzed', dest='Transferring')
        self.machine.add_transition(trigger='Abort', source='Transferring', dest='Idle', before='Clear')
        self.machine.add_transition(trigger='TransferringDone', source='Transferring', dest='Idle')

        threading.Thread(target=worker, daemon=True).start()

    def Clear(self):
        pass

    def RunRoutine(self):
        print("Routine started")
        self.ElectroRoutine.start()

        def run():
            result = self.ElectroRoutine.monitor()
            while result != Result.Done:
                result = self.ElectroRoutine.monitor()

        q.put(run)
        q.put(self.RoutineDone)
