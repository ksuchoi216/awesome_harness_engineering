from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_PATH = REPO_ROOT / ".codex/hooks/ahe-hook.js"


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
    assert "docs/PRODUCT.md" in additional_context
    assert "product/specification source of truth" in additional_context
    assert "feature-list.json" in additional_context
    assert "derived tracker" in additional_context
    assert "CodeGraph" in additional_context
    assert ".codegraph/" in additional_context
    assert "unfinished feature" in additional_context
    assert "ask the user" in additional_context
    assert "$ahe-init" in additional_context
    assert "ahe-thinker" in additional_context


def test_auto_operation_requires_first_response_status_table() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "first response" in additional_context.lower()
    assert "| Item | Content |" in additional_context
    assert "|---|---|" in additional_context
    assert "AGENTS.md" in additional_context
    assert "PRODUCT.md" in additional_context
    assert "INSTRUCTIONS.md" in additional_context
    assert "feature-list.json" in additional_context
    assert "PROGRESS.md" in additional_context
    assert "| Next step |" not in additional_context
    assert "docs/constraints.md" not in additional_context
    assert "docs/achitecture.md" not in additional_context
    assert "docs/todo.md" not in additional_context
    assert "SESSION-HANDOFF.md" not in additional_context
    assert ".ahe/process_status.json" not in additional_context
    assert "| CodeGraph |" not in additional_context
    assert additional_context.index("status report table") < additional_context.index(
        "Decide the next AHE workflow"
    )


def test_auto_operation_routes_through_thinker_network() -> None:
    additional_context = additional_context_for_prompt("ahe")

    assert "After the table, classify the harness into exactly one state." in additional_context
    assert "If `docs/PRODUCT.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough`" in additional_context
    assert "`harness engineering not enough`" in additional_context
    assert "`in the middle of building features`" in additional_context
    assert "`completed all`" in additional_context
    assert "Do not include the next step inside the table." in additional_context
    assert "Continue automatically after classification." in additional_context
    assert "ahe-thinker" in additional_context
    assert "ahe-reviewer" in additional_context
    assert "ahe-conversator" in additional_context
    assert "ahe-harness" in additional_context
    assert "ahe-solver" in additional_context
    assert "confirm the next step directly" not in additional_context
    assert "`start a new task`" not in additional_context
    assert "`resume existing harness work`" not in additional_context


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


def test_exact_ahe_init_prompt_emits_new_start_context() -> None:
    additional_context = additional_context_for_prompt("ahe init")

    assert "AHE automatic operation activated." in additional_context
    assert "$ahe-init" in additional_context
    assert "new start" in additional_context.lower() or "initialize" in additional_context.lower()
    assert "If no AHE-managed harness files exist, start initialization normally." in additional_context
    assert "If any AHE-managed harness file exists, read the existing files" in additional_context
    assert "ask what restart scope the user wants" in additional_context
    assert "Do not remove, overwrite, or refresh existing harness files before the user answers" in additional_context
    assert "instead of creating backup copies" in additional_context
    assert "Product/instructions specification details belong in `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`, not `AGENTS.md`." in additional_context
    assert "ahe-harness" in additional_context
    assert ".ahe/backups/" not in additional_context


def test_exact_ahe_init_aliases_emit_new_start_context() -> None:
    for prompt in ("ahe-init", "$ahe-init"):
        additional_context = additional_context_for_prompt(prompt)

        assert "AHE automatic operation activated." in additional_context
        assert "$ahe-init" in additional_context
        assert "new start" in additional_context.lower()


def test_ahe_mention_inside_normal_prompt_does_not_trigger() -> None:
    assert hook_output_for_prompt("please explain ahe") is None


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


def test_explicit_ahe_query_routes_to_thinker() -> None:
    prompts = [
        "ahe compress feature-list",
        "ahe update product spec",
        "ahe add a new dashboard feature",
    ]
    for prompt in prompts:
        context = additional_context_for_prompt(prompt)
        assert context is not None
        assert "AHE automatic operation activated." in context
        assert f'Original prompt: "{prompt}"' in context
        assert "ahe-thinker" in context
        assert "explicit AHE query" in context


def test_nonprefixed_natural_language_prompts_do_not_trigger() -> None:
    prompts = [
        "I want to add features",
        "update the product spec",
        "track this as work",
        "Can we add an instruction about writing clean code?",
    ]
    for prompt in prompts:
        assert hook_output_for_prompt(prompt) is None


def test_query_directive_contract() -> None:
    context = additional_context_for_prompt("ahe compress feature-list")
    assert context is not None
    assert "Inspect current harness state before choosing a workflow" in context
    assert "| AGENTS.md |" in context
    assert "Use `ahe-thinker` as the internal decision layer" in context
    assert "ahe-harness" in context
    assert "replace old completed feature entries with one summarized done feature" in context
    assert "If no new feature can be derived from `docs/PRODUCT.md`, call `ahe-conversator`" in context
