from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_PATH = REPO_ROOT / "packages/ahe-codex/.codex/hooks/ahe-hook.js"
THINKER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/think/SKILL.md"


def run_hook(prompt: str) -> dict[str, object] | None:
    payload = json.dumps(
        {"hook_event_name": "UserPromptSubmit", "prompt": prompt}
    )
    completed = subprocess.run(
        ("node", str(HOOK_PATH)),
        input=payload,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    if not completed.stdout:
        return None
    return json.loads(completed.stdout)


def additional_context(prompt: str) -> str:
    output = run_hook(prompt)
    assert output is not None, f"Hook produced no output for prompt: {prompt}"
    ctx = output["hookSpecificOutput"]["additionalContext"]
    assert isinstance(ctx, str)
    return ctx


# ===========================================================================
# Orchestration Core
# ===========================================================================

def test_exact_ahe_uses_thinker_as_primary_orchestrator() -> None:
    ctx = additional_context("ahe")
    assert "Use `think` as the internal decision layer before choosing the next action" in ctx
    assert "Decide the next AHE workflow with `think`" in ctx


# ===========================================================================
# Situation 1: Completely Empty Workspace
# ===========================================================================

def test_exact_ahe_routes_to_init_when_no_harness_files_exist() -> None:
    ctx = additional_context("ahe")
    assert "If no harness files exist, route to `$new`." in ctx
    assert "$new" in ctx


# ===========================================================================
# Situation 2: Incomplete Harness (Missing/Empty Docs)
# ===========================================================================

def test_exact_ahe_detects_harness_engineering_not_enough() -> None:
    ctx = additional_context("ahe")
    assert "If `docs/product.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough`." in ctx
    assert "`harness engineering not enough`" in ctx


# ===========================================================================
# Situation 3: Mid-Implementation (Features Pending)
# ===========================================================================

def test_exact_ahe_detects_in_the_middle_of_building_features() -> None:
    ctx = additional_context("ahe")
    assert "If any feature in `feature-list.json` has a status other than `done`, classify the state as `in the middle of building features`" in ctx
    assert "continue the first unfinished feature whose dependencies are satisfied" in ctx
    assert "`in the middle of building features`" in ctx


# ===========================================================================
# Situation 4: All Work Completed
# ===========================================================================

def test_exact_ahe_detects_completed_all_when_features_done() -> None:
    ctx = additional_context("ahe")
    assert "If all features are `done` and no obvious harness gap remains, classify the state as `completed all`" in ctx
    assert "ask the user for the next task" in ctx
    assert "`completed all`" in ctx


# ===========================================================================
# Situation 5: Missing Feature List Tracker
# ===========================================================================

def test_exact_ahe_handles_missing_or_invalid_feature_list() -> None:
    ctx = additional_context("ahe")
    assert "If `feature-list.json` is missing or invalid, generating an empty one from template is allowed" in ctx
    assert "do not write specific features until `docs/product.md` and `docs/INSTRUCTIONS.md` are created and organized" in ctx


# ===========================================================================
# Situation 6: Skill Routing Delegations
# ===========================================================================

def test_exact_ahe_routes_to_specialized_skills_based_on_need() -> None:
    # Check the hook's routing directives for exact ahe
    ctx = additional_context("ahe")
    assert "Call `review` when repo or code understanding is needed" in ctx
    assert "Call `converse` when the next safe step is blocked on user input" in ctx
    assert "Call `harness` when product docs, instructions, tracking, todo sync, or compression-aware harness maintenance must change" in ctx
    assert "Call `solve` when the next job is solving or planning a feature" in ctx

    # Check the thinker's exact same routing rules
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "review" in thinker
    assert "converse" in thinker
    assert "harness" in thinker
    assert "solve" in thinker


if __name__ == "__main__":
    import sys
    import inspect

    test_functions = [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isfunction(obj) and name.startswith("test_")
    ]
    for fn in test_functions:
        fn.__module__ = __name__
        print(f"  {fn.__name__}...", end=" ")
        try:
            fn()
            print("OK")
        except Exception as e:
            print(f"FAIL: {e}")
    print("test_ahe_exact.py standalone run complete.")
