import sys

from Routine.RoutineState import RoutineState
from Routine.RoutineState import Result
from Routine.DeviceTimer import DeviceTimer
from collections import deque
from typing import Callable
import enum


class State(enum.Enum):
    IDLE = 0
    WAIT = 1


def CheckResult(value: (bool, bool)) -> (bool, Result):
    if value[0]:
        if value[1] is None:
            return_tuple = (True, Result.Fail)
            return return_tuple
        return_tuple = (True, Result.Run)
        return return_tuple
    return_tuple = (False, Result.Run)
    return return_tuple


class RoutineFailedException(Exception):
    """Raised when the routine failed"""
    pass


class RoutineBreakException(Exception):
    """Raised when the routine is still running"""
    pass


class SequenceRoutine(object):
    def __init__(self):
        self.counter = DeviceTimer()
        self.delay_timer = DeviceTimer()
        self.id = 0
        self.step = deque()
        self.state = State.IDLE
        self.routine_token = RoutineState.Running
        # loop control
        self.loop = 0

    def Reset(self):
        self.id = 0
        self.step.clear()
        self.loop = 0
        self.state = State.IDLE
        # 1 hour default timer
        # self.counter.Start(60 * 60 * 100)
        self.routine_token = RoutineState.Running

    def Active(self, step_id: int) -> bool:
        if (step_id in self.step) :
            return False
        self.id = step_id
        return True 
    

    def Next(self):
        self.step.append(self.id)
        self.state = State.IDLE

    def CheckFunction(self, step_id: int, func) -> (bool, bool):
        is_active = self.Active(step_id)
        is_executed = False
        if is_active:
            is_executed = func()
            self.Next()
        return_tuple = (is_active, is_executed)
        return return_tuple

    # wrapped check function
    def Check(self, step_id: int, func) -> (bool, Result):
        return CheckResult(self.CheckFunction(step_id, func))

    def ExecuteFunction(self, step_id: int, func) -> (bool, bool):
        is_active = self.Active(step_id)
        is_executed = False
        if is_active:
            is_executed = func()
            if is_executed:
                self.Next()
        return_tuple = (is_active, is_executed)
        return return_tuple

    # wrapped execute function
    def Execute(self, step_id: int, func) -> (bool, Result):
        """
        Execute the function in the argument
        :param step_id:  Step ID of an routine
        :param func: The function to be executed
        :return: Tuple of a bool and an Result
        """
        return CheckResult(self.ExecuteFunction(step_id, func))

    # When use, call this
    def ExecuteAndWait(self, step_id: int,
                       execute_function: Callable[[], bool],
                       check_function: Callable[[], bool],
                       timeout: int = sys.maxsize):
        """
        Execute and wait for some time
        :param step_id: Step ID of an routine
        :param execute_function: The function to be executed
        :param check_function: The guarding function
        :param timeout: Time interval
        :return: Tuple of a bool and an Result
        """
        is_active = self.Active(step_id)
        is_execute = None
        if is_active:
            if self.state == State.IDLE:
                if not execute_function():
                    return_tuple = (is_active, Result.Fail)
                    return return_tuple
                self.delay_timer.Start(timeout)
                self.state = State.WAIT

            is_execute = check_function()
            # if empty return Fail
            if is_execute is None:
                return_tuple = (is_active, Result.Fail)
                return return_tuple
            else:
                # is_execute is not empty
                if is_execute and not self.delay_timer.IsTimeout():
                    return_tuple = (True, Result.Run)
                    return return_tuple

            # time out
            if self.delay_timer.IsTimeout():
                self.Next()
                return_tuple = (True, Result.Timeout)
                return return_tuple

            # not time out, means still running
            return_tuple = (True, Result.Run)
            return return_tuple

        # not active (already done this step)
        return_tuple = (False, Result.Run)
        return return_tuple
    
    def delay(self, step_id: int, timeout: int = sys.maxsize):
        is_active = self.Active(step_id)
        is_execute = None
        if is_active:
            if self.state == State.IDLE:
                print("Start delay")
                self.delay_timer.Start(timeout)
                self.state = State.WAIT

            # time out
            if self.delay_timer.IsTimeout():
                self.Next()
                return_tuple = (True, Result.Timeout)
                return return_tuple

            # not time out, means still running
            return_tuple = (True, Result.Run)
            return return_tuple

        # not active (already done this step)
        return_tuple = (False, Result.Run)
        return return_tuple
