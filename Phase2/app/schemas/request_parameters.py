from enum import Enum
from pydantic import BaseModel

# Enum to enforce only the (performance/security/style/architecture focus points)
class FocusOptions(str, Enum):
    performance = "performance"
    security = "security"
    style = "style"
    architecture = "architecture"

class languageOptions(str, Enum):
    c = "C"
    cpp = "C++"
    python = "Python"


class CodeReviewRequest(BaseModel):
    code: str
    language: languageOptions
    focus: FocusOptions