import enum


class Gender(enum.Enum):
    Male = 0
    Female = 1
    Unknown = 2


class Weekday(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


class TrainingType(enum.Enum):
    FBW = "FBW"
    Push = "Push"
    Pull = "Pull"
    Upper = "Upper"
    Lower = "Lower"
    Custom = "Custom"
