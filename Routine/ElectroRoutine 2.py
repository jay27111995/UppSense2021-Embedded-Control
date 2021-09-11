

from abc import ABC
from Motor import Motor
from .IRoutine import IRoutine
from enum import IntEnum
from .SequenceRoutine import SequenceRoutine
from .SequenceRoutine import RoutineFailedException
from .SequenceRoutine import RoutineBreakException
from .RoutineState import Result
import Interface.PSEsPicoLib


class ElectroRoutine(SequenceRoutine, IRoutine, ABC):
    def __init__(self):
        super().__init__()
        self.pump1 = Motor(1, 20000)
        self.pump2 = Motor(2, 20000)
        self.pump_direction = False
        self.pump_config = 0
        self.motor_duty_cycle = 0
        self.pump_running_time = 0

    class Detection(IntEnum):
        PumpRun = 0
        PumpStop = 1

    def Start(self, direction: bool, duty_cycle: int, running_time_ms: int, pump_config: int) -> Result:
        """
        Setting up the routine's variables
        :param direction: The direction of the pump(s), false - suck from input, true - blow from input
        :param duty_cycle: Duty cycle of the motor
        :param running_time_ms: Running time of the motor
        :param pump_config: 1: Pump1 only; 2: Pump2 only; 3: Both pump
        :return: Return the Result
        """
        self.Reset()
        self.pump_direction = direction
        self.motor_duty_cycle = duty_cycle
        self.pump_running_time = running_time_ms
        self.pump_config = pump_config
        return Result.Run

    def Monitor(self) -> Result:
        try:
            self.start_pump(self.Detection.PumpRun)
            self.stop_pump(self.Detection.PumpStop)
        except SequenceRoutine.RoutineBreakException:
            return Result.Run
        except SequenceRoutine.RoutineFailedException:
            return Result.Fail
        else:
            return Result.Done

    def start_pump(self, step_id: int) -> None:
        """
        Start the pump
        :param step_id: Step id
        :param direction: Pump's direction
        :param duty_cycle: Pump's duty cycle
        :param running_time: The running time of the pump (ms)
        """

        def StartPump() -> bool:
            return_bool = False
            if self.pump_config == 1 or self.pump_config == 3:
                b1 = self.pump1.Start(self.pump_direction, self.motor_duty_cycle)
                return_bool |= b1
            if self.pump_config == 2 or self.pump_config == 3:
                b2 = self.pump2.Start(self.pump_direction, self.motor_duty_cycle)
                return_bool |= b2
            return return_bool

        ret = self.ExecuteAndWait(step_id, lambda: StartPump(), lambda x: True, self.pump_running_time)
        if ret[0]:
            if ret[1] == Result.Fail:
                raise SequenceRoutine.RoutineFailedException
            elif ret[1] == Result.Run:
                raise SequenceRoutine.RoutineBreakException
            else:
                raise SequenceRoutine.RoutineFailedException

    def stop_pump(self, step_id: int) -> None:
        """
        Stop the pump
        :param step_id:
        :return: None
        """

        def StopPump() -> bool:
            return_bool = False
            if self.pump_config == 1 or self.pump_config == 3:
                b1 = self.pump1.Stop()
                return_bool |= b1
            if self.pump_config == 2 or self.pump_config == 3:
                b2 = self.pump2.Stop()
                return_bool |= b2
            return return_bool

        ret = self.Execute(step_id, StopPump())
        if ret[0]:
            if ret[1] == Result.Fail:
                raise SequenceRoutine.RoutineFailedException

    def turn_valve(self, step_id: int, valve_no: int, valve_open: int) -> None:
        pass
