import enum


class Gender(enum.Enum):
    Male = 0
    Female = 1
    Unknown = 2


class TrainingType(enum.Enum):
    FBW = "FBW"
    Push = "Push"
    Pull = "Pull"
    Upper = "Upper"
    Lower = "Lower"
    Custom = "Custom"
