

from abc import ABC
from Motor import Motor
from ServoValve import ThreeWayValve
from Routine.IRoutine import IRoutine
from enum import IntEnum
from Routine.SequenceRoutine import SequenceRoutine
from Routine.SequenceRoutine import RoutineFailedException
from Routine.SequenceRoutine import RoutineBreakException
from Routine.RoutineState import Result
import Interface.PSEsPicoLib


class ElectroRoutine(SequenceRoutine, IRoutine, ABC):
    def __init__(self):
        super().__init__()
        self.pump1 = Motor(1, 3000)
        self.pump2 = Motor(2, 3000)
        self.valve_green = ThreeWayValve(25, 1750)
        self.valve_red = ThreeWayValve(8, 2000)

    class Detection(IntEnum):
        # saliva
        TurnValveG_1 = 0
        TurnValveR_1 = 1
        PumpRun_1 = 2
        PumpStop_1 = 3
        # incubation
        Delay_1 = 4
        
        PumpRun_2 = 5
        PumpStop_2 = 6

    def abort(self):
        pass

    def start(self) -> Result:
        """
        Setting up the routine's variables
        :param direction: The direction of the pump(s), false - suck from input, true - blow from input
        :param duty_cycle: Duty cycle of the motor
        :param running_time_ms: Running time of the motor
        :param pump_config: 1: Pump1 only; 2: Pump2 only; 3: Both pump
        :return: Return the Result
        """
        self.Reset()
        return Result.Run

    def monitor(self) -> Result:
        try:
            self.turn_valve(self.Detection.TurnValveG_1, 1, 1)
            self.turn_valve(self.Detection.TurnValveR_1, 2, 2)
            self.start_pump(self.Detection.PumpRun_1, 1, False, 3, 2000)
            self.stop_pump(self.Detection.PumpStop_1, 1)
            
            
            # incubation
            # self.wait(self.Detection.Delay_1, 30000)
        except RoutineBreakException:
            return Result.Run
        except RoutineFailedException:
            return Result.Fail
        else:
            print("Done")
            return Result.Done
        
    def wait(self, step_id: int, delay_time: int) -> None:
        ret = self.delay(step_id, delay_time)
        if ret[0]:
            if ret[1] == Result.Fail:
                raise RoutineFailedException
            elif ret[1] == Result.Run:
                raise RoutineBreakException
            else:
                raise RoutineFailedException
    

    def start_pump(self, step_id: int, pump_no: int, direction: bool, duty_cycle: int, pump_running_time: int) -> None:
        """
        Start the pump
        :param step_id: Step id
        :param direction: Pump's direction
        :param duty_cycle: Pump's duty cycle
        :param running_time: The running time of the pump (ms)
        """
        def StartPump() -> bool:
            return_bool = False
            print("pump ",pump_no, " start, ", direction, " direction, at ", duty_cycle, " duty cycle, will run for ", pump_running_time, " ms")
            if pump_no == 1:
                b1 = self.pump1.Start(direction, duty_cycle)
                return_bool |= b1
            if pump_no == 2:
                b2 = self.pump2.Start(direction, duty_cycle)
                return_bool |= b2
            return return_bool
        ret = self.ExecuteAndWait(step_id, StartPump, lambda : True, pump_running_time)
        if ret[0]:
            if ret[1] == Result.Fail:
                raise RoutineFailedException
            elif ret[1] == Result.Run:
                raise RoutineBreakException
            else:
                raise RoutineFailedException

    def stop_pump(self, step_id: int, pump_no: int) -> None:
        """
        Stop the pump
        :param step_id:
        :return: None
        """

        def StopPump() -> bool:
            print("pump ", pump_no, " stopped")
            return_bool = False
            if pump_no == 1:
                b1 = self.pump1.Stop()
                return_bool |= b1
            if pump_no == 2:
                b2 = self.pump2.Stop()
                return_bool |= b2
            return return_bool

        ret = self.Execute(step_id, StopPump)
        if ret[0]:
            if ret[1] == Result.Fail:
                raise RoutineFailedException

    def turn_valve(self, step_id: int, valve_no: int, valve_open: int) -> None:
        """
        Valve operation
        :param step_id:
        :param valve_no: 1 -> green 2-> red
        :return: None
        """
        def operation() -> bool:
            print("Valve No.", valve_no, " open ", valve_open, " valve.")
            if valve_no == 1 and valve_open == 1:
                self.valve_green.open_one()
            elif valve_no == 1 and valve_open == 2:
                self.valve_green.open_two()
            elif valve_no == 1 and valve_open == 3:
                self.valve_green.open_three()
            elif valve_no == 2 and valve_open == 1:
                self.valve_red.open_one()
            elif valve_no == 2 and valve_open == 2:
                self.valve_red.open_two()
            elif valve_no == 2 and valve_open == 3:
                self.valve_red.open_three()
                
            return True
        ret = self.Execute(step_id, operation)
        if ret[0]:
            if ret[1] == Result.Fail:
                raise RoutineFailedException
