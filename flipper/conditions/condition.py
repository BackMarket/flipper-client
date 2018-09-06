from collections import defaultdict
from typing import Any, Dict, List

from .check import Check


class Condition:
    def __init__(self, **checks):
        self._checks = self._parse_checks(checks)

    def _parse_checks(self, checks: Dict[str, Any]) -> Dict[str, List[Check]]:
        parsed_checks = defaultdict(list)  # type: Dict[str, List[Check]]
        for check_key, check_value in checks.items():
            check = Check.factory(check_key, check_value)
            parsed_checks[check.variable].append(check)
        return parsed_checks

    def check(self, **checks) -> bool:
        for check_name, check_value in checks.items():
            checkers = self._checks[check_name]

            for checker in checkers:
                if checker.check(check_value) is False:
                    return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            variable: [check.to_dict() for check in checkers]
            for variable, checkers in self._checks.items()
        }

    @classmethod
    def from_dict(cls, conditions: Dict[str, Any]) -> "Condition":
        constructor_kwargs = {}

        for _, checks in conditions.items():
            for check in checks:
                check_key = cls._make_key_for_check(check)
                constructor_kwargs[check_key] = check["value"]

        return cls(**constructor_kwargs)

    @classmethod
    def _make_key_for_check(cls, check: Dict[str, Any]) -> str:
        return Check.make_check_key(check["variable"], check["operator"])
