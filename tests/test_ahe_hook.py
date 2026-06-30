from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_PATH = REPO_ROOT / "packages/ahe-codex/.codex/hooks/ahe-hook.js"


def run_hook(payload: str) -> str:
    completed_process = subprocess.run(
        ("node", str(HOOK_PATH)),
        input=payload,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    return completed_process.stdout


def hook_output_for_prompt(prompt: str) -> dict[str, object] | None:
    payload = json.dumps(
        {
            "hook_event_name": "UserPromptSubmit",
            "prompt": prompt,
        }
    )
    output = run_hook(payload)

    if not output:
        return None

    return json.loads(output)


def additional_context_for_prompt(prompt: str) -> str:
    output = hook_output_for_prompt(prompt)

    assert output is not None

    hook_output = output["hookSpecificOutput"]
    assert isinstance(hook_output, dict)
    assert hook_output["hookEventName"] == "UserPromptSubmit"

    additional_context = hook_output["additionalContext"]
    assert isinstance(additional_context, str)

    return additional_context


def test_exact_ahe_prompt_emits_auto_operation_context() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "AHE automatic operation activated." in additional_context
    assert "AGENTS.md" in additional_context
    assert "docs/product.md" in additional_context
    assert "product/specification source of truth" in additional_context
    assert "feature-list.json" in additional_context
    assert "derived tracker" in additional_context
    assert "CodeGraph" in additional_context
    assert ".codegraph/" in additional_context
    assert "unfinished feature" in additional_context
    assert "ask the user" in additional_context
    assert "ahe-new" in additional_context
    assert "ahe-think" in additional_context


def test_auto_operation_requires_first_response_status_table() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "first response" in additional_context.lower()
    assert "| Item | Content |" in additional_context
    assert "|---|---|" in additional_context
    assert "AGENTS.md" in additional_context
    assert "product.md" in additional_context
    assert "INSTRUCTIONS.md" in additional_context
    assert "feature-list.json" in additional_context
    assert "progress.md" in additional_context
    assert "| Next step |" not in additional_context
    assert "docs/constraints.md" not in additional_context
    assert "docs/achitecture.md" not in additional_context
    assert "docs/todo.md" not in additional_context
    assert "session-handoff.md" not in additional_context
    assert "status.json" not in additional_context
    assert "| CodeGraph |" not in additional_context
    assert additional_context.index("status report table") < additional_context.index(
        "Decide the next AHE workflow"
    )


def test_auto_operation_routes_through_thinker_network() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "After the table, classify the harness into exactly one state." in additional_context
    assert "If `docs/product.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough`" in additional_context
    assert "`harness engineering not enough`" in additional_context
    assert "`in the middle of building features`" in additional_context
    assert "`completed all`" in additional_context
    assert "Do not include the next step inside the table." in additional_context
    assert "Continue automatically after classification." in additional_context
    assert "ahe-think" in additional_context
    assert "ahe-review" in additional_context
    assert "ahe-converse" in additional_context
    assert "ahe-harness" in additional_context
    assert "ahe-solve" in additional_context
    assert "confirm the next step directly" not in additional_context
    assert "`start a new task`" not in additional_context
    assert "`resume existing harness work`" not in additional_context


def test_auto_operation_describes_staged_product_docs() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "docs/product1.md" in additional_context
    assert "docs/product2.md" in additional_context
    assert "numeric suffix order" in additional_context
    assert "derive features from only the active product stage" in additional_context
    assert "docs/product-alpha.md" in additional_context
    assert additional_context.index("docs/product1.md") < additional_context.index(
        "docs/product2.md"
    )


def test_auto_operation_requires_codegraph_preflight_before_status_checks() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "CodeGraph preflight" in additional_context
    assert "command -v codegraph" in additional_context
    assert "NOT INSTALLATION of codegraph" in additional_context
    assert "skip `codegraph init` and `codegraph sync`" in additional_context
    assert "If `.codegraph/` does not exist, run `codegraph init`" in additional_context
    assert "If `.codegraph/` exists, run `codegraph sync`" in additional_context
    assert additional_context.index("CodeGraph preflight") < additional_context.index(
        "Inspect current harness state"
    )


def test_uppercase_ahe_prompt_emits_auto_operation_context() -> None:
    additional_context = additional_context_for_prompt("AHE")

    assert "AHE automatic operation activated." in additional_context


def test_exact_ahe_new_prompt_emits_new_start_context() -> None:
    for prompt in ("ahe-new", "ahe-new"):
        additional_context = additional_context_for_prompt(prompt)

        assert "AHE automatic operation activated." in additional_context
        assert "ahe-new" in additional_context
        assert "ahe-think" in additional_context
        assert "If no AHE-managed harness files exist, start initialization normally." in additional_context
        assert "If any AHE-managed harness file exists, read the existing files" in additional_context
        assert "ask what restart scope the user wants" in additional_context
        assert "Do not remove, overwrite, or refresh existing harness files before the user answers" in additional_context
        assert "instead of creating backup copies" in additional_context
        assert "Product/instructions specification details belong in `docs/product.md` and `docs/INSTRUCTIONS.md`, not `AGENTS.md`." in additional_context
        assert "ahe-harness" in additional_context
        assert ".ahe/backups/" not in additional_context


def test_exact_ahe_ship_emit_independent_ship_context() -> None:
    for prompt in ("ahe-ship", "ahe-ship"):
        additional_context = additional_context_for_prompt(prompt)

        assert "AHE plan export activated." in additional_context
        assert "ahe-think" in additional_context
        assert "ahe-ship" in additional_context
        assert "Detect if the current conversation is still in Plan Mode." in additional_context
        assert "If Plan Mode is active, exit Plan Mode first before continuing." in additional_context
        assert "most recent `<proposed_plan>`" in additional_context
        assert ".plans/{plan_name}.md" in additional_context
        assert "write the final markdown and stop" in additional_context
        assert "status report table" not in additional_context
        assert "explicit AHE query" not in additional_context


def test_exact_ahe_fix_emit_fix_plan_context() -> None:
    for prompt in ("ahe-fix", "ahe-fix"):
        additional_context = additional_context_for_prompt(prompt)

        assert "AHE fix planning activated." in additional_context
        assert "ahe-think" in additional_context
        assert "ahe-fix" in additional_context
        assert ".plans/{plan_name}.md" in additional_context
        assert "fixing errors or following the user's intention" in additional_context
        assert "ahe-converse" in additional_context
        assert "status report table" not in additional_context
        assert "explicit AHE query" not in additional_context


def test_exact_ahe_overview_emit_overview_context() -> None:
    additional_context = additional_context_for_prompt("ahe-overview")

    assert "AHE overview activated." in additional_context
    assert "ahe-overview" in additional_context
    assert ".codex/skills/ahe-overview/SKILL.md" in additional_context
    assert "explain the AHE concept" in additional_context
    assert "status report table" not in additional_context
    assert "Do not run the normal AHE harness workflow." in additional_context


def test_middle_ahe_mention_does_not_trigger() -> None:
    assert hook_output_for_prompt("please explain ahe commands today") is None


def test_malformed_json_emits_nothing() -> None:
    assert run_hook("not json") == ""


def test_non_user_prompt_submit_event_emits_nothing() -> None:
    payload = json.dumps(
        {
            "hook_event_name": "OtherEvent",
            "prompt": "ahe",
        }
    )

    assert run_hook(payload) == ""


def test_nonprefixed_natural_language_prompts_do_not_trigger() -> None:
    prompts = [
        "I want to add features",
        "update the product spec",
        "track this as work",
        "Can we add an instruction about writing clean code?",
    ]
    for prompt in prompts:
        assert hook_output_for_prompt(prompt) is None
