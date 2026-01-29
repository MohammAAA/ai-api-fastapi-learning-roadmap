from enum import Enum
from pydantic import BaseModel

# Enum to enforce only the (add/subtract/multiply operations)
class operations(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"


class CalculateRequest(BaseModel):
    operation: operations
    operand_a: float
    operand_b: float