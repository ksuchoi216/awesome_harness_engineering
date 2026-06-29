#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
#
# How to run:
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly:
#      uv run write_fix_plan.py --root "$PWD" --plan-name "Fix Plan Title" < /tmp/ahe-fix-plan.md
# 3. Or with Python when dependencies are already available:
#      python3 write_fix_plan.py --root "$PWD" --plan-name "Fix Plan Title" < /tmp/ahe-fix-plan.md

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WriteFixPlanArgs:
    root: Path
    plan_name: str
    overwrite: bool


class ArgumentError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class PlanAlreadyExistsError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Plan file already exists: {path}")


def sanitize_plan_name(plan_name: str) -> str:
    normalized_name = re.sub(r"[^a-z0-9]+", "-", plan_name.strip().lower()).strip("-")
    if normalized_name:
        return normalized_name
    raise ArgumentError("plan name must contain at least one letter or digit")


def parse_args(argv: list[str]) -> WriteFixPlanArgs:
    root: Path | None = None
    plan_name: str | None = None
    overwrite = False
    index = 0

    while index < len(argv):
        argument = argv[index]
        match argument:
            case "--root":
                index += 1
                if index >= len(argv):
                    raise ArgumentError("--root requires a value")
                root = Path(argv[index])
            case "--plan-name":
                index += 1
                if index >= len(argv):
                    raise ArgumentError("--plan-name requires a value")
                plan_name = argv[index]
            case "--overwrite":
                overwrite = True
            case _:
                raise ArgumentError(f"unknown argument: {argument}")
        index += 1

    if root is None:
        raise ArgumentError("--root is required")
    if plan_name is None:
        raise ArgumentError("--plan-name is required")

    return WriteFixPlanArgs(root=root, plan_name=plan_name, overwrite=overwrite)


def write_fix_plan(args: WriteFixPlanArgs, markdown: str) -> Path:
    filename = f"{sanitize_plan_name(args.plan_name)}.md"
    plans_dir = args.root / ".plans"
    plan_path = plans_dir / filename

    if plan_path.exists() and not args.overwrite:
        raise PlanAlreadyExistsError(plan_path)

    plans_dir.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(markdown, encoding="utf-8")
    return plan_path


def main() -> int:
    try:
        args = parse_args(sys.argv[1:])
        plan_path = write_fix_plan(args, sys.stdin.read())
    except (ArgumentError, PlanAlreadyExistsError) as error:
        print(error, file=sys.stderr)
        return 1

    print(plan_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
