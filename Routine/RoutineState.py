import enum


class RoutineState(enum.Enum):
    Running = 0
    Failed = 1
    Timeout = 2
    Finished = 3


class Result(enum.Enum):
    Run = 0
    Done = 1
    Fail = 2
    Timeout = 3
