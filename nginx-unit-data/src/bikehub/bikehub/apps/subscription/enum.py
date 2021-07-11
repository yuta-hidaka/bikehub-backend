from enum import Enum


class StatusEnum(Enum):
    payment_waiting = 100
    payment_failed = 101
    canceled = 200
    subscribing = 300
