import argparse
import logging
from enum import StrEnum, auto
from pathlib import Path
from typing import Optional

import log_setup
from transaction import Category

log = log_setup.getLogger('arguments')


class Arguments:
    class ProgramAction(StrEnum):
        LUKSUS_FAELDEN = "lf"
        PRETTY_PRINT_CATEGORIES = "ppc"
        DISPOSABLE_INCOME = "disp"
        MATCHINGS = "matches"

    _args = None

    def __init__(self):
        parser = argparse.ArgumentParser()

        # Positional arguments
        parser.add_argument(
            "dir",
            type=Path,
            help="Absolute directory containing .csv files"
        )
        parser.add_argument(
            "actions",
            type=Arguments.ProgramAction,
            nargs="+",
            help="Program actions",
            choices=Arguments.ProgramAction,
        )

        # Optional arguments
        parser.add_argument("--log-level", type=str, default="debug")
        parser.add_argument("--filter-name", type=str, nargs="+")
        parser.add_argument("--filter-category", type=Category, nargs="+")
        parser.add_argument("--filter-description", type=str, nargs="+")
        parser.add_argument("--exclude-name", type=str, nargs="+")
        parser.add_argument("--exclude-category", type=Category, nargs="+")
        parser.add_argument("--exclude-description", type=str, nargs="+")

        # Parse
        args = parser.parse_args()

        self.dir: Path = args.dir
        self.actions: list[Arguments.ProgramAction] = [Arguments.ProgramAction(pa) for pa in args.actions]
        self.log_level: str = args.log_level
        log_setup.logger.setLevel(self.log_level.upper())
        self.filter_name: str | None = args.filter_name
        self.filter_category: list[Category] | None = args.filter_category
        self.filter_description: str | None = args.filter_description
        self.exclude_name: str | None = args.exclude_name
        self.exclude_category: list[Category] | None = args.exclude_category
        self.exclude_description: str | None = args.exclude_description

        log.debug(f"{self.dir=}")
        log.debug(f"{self.actions=}")
        log.debug(f"{self.log_level=}")
        log.debug(f"{self.filter_name=}")
        log.debug(f"{self.filter_category=}")
        log.debug(f"{self.filter_description=}")
        log.debug(f"{self.exclude_name=}")
        log.debug(f"{self.exclude_category=}")
        log.debug(f"{self.exclude_description=}")

    @property
    def luksus_faelden(self) -> bool:
        return Arguments.ProgramAction.LUKSUS_FAELDEN in self.actions

    @property
    def pretty_print_categories(self) -> bool:
        return Arguments.ProgramAction.PRETTY_PRINT_CATEGORIES in self.actions

    @property
    def disposable_income(self) -> bool:
        return Arguments.ProgramAction.DISPOSABLE_INCOME in self.actions

    @property
    def matches(self) -> bool:
        return Arguments.ProgramAction.MATCHINGS in self.actions


