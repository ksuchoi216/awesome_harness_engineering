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
    assert "feature-list.json" in additional_context
    assert ".ahe/process_status.json" in additional_context
    assert "CodeGraph" in additional_context
    assert ".codegraph/" in additional_context
    assert "unfinished feature" in additional_context
    assert "ask the user" in additional_context
    assert "$ahe-init" in additional_context


def test_uppercase_ahe_prompt_emits_auto_operation_context() -> None:
    additional_context = additional_context_for_prompt("AHE")

    assert "AHE automatic operation activated." in additional_context


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
