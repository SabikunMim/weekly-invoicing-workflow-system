from dataclasses import dataclass


@dataclass
class ReviewFinding:
    severity: str
    file: str
    line: int | None
    title: str
    message: str
    recommendation: str
