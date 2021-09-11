import enum
import time


class DeviceTimerState(enum.Enum):
    DT_IDLE = 0
    DT_BUSY = 1
    DT_TIMEOUT = 3


class DeviceTimer(object):
    # All the time variables are in nano secs (apart from duration)
    def __init__(self):
        self.state = DeviceTimerState.DT_IDLE
        self.start_time = time.time_ns()
        self.time_out = self.start_time
        self.duration = 0

    def GetElapseTimeSeconds(self) -> float:
        return (time.time_ns() - self.start_time) / (10 ** 9)

    def GetElapseTimeNanoSeconds(self) -> float:
        return time.time_ns() - self.start_time

    def Start(self, delay_ms: int):
        self.start_time = time.time_ns()
        self.time_out = 1000000 * delay_ms + self.start_time
        self.state = DeviceTimerState.DT_BUSY
        self.duration = delay_ms

    def IsTimeout(self) -> bool:
        if self.state == DeviceTimerState.DT_BUSY and time.time_ns() >= self.time_out:
            self.state = DeviceTimerState.DT_TIMEOUT
            return True
        elif self.state == DeviceTimerState.DT_TIMEOUT:
            return True
        return False

    def IsIdle(self) -> bool:
        return self.state == DeviceTimerState.DT_IDLE
