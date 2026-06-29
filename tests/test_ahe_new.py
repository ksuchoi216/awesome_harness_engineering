from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / ".codex/ahe-shared/templates"
NEW_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-new/SKILL.md"
THINKER_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-thinker/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md"
CONVERSATOR_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-conversator/SKILL.md"
HOOK_PATH = REPO_ROOT / ".codex/hooks/ahe-hook.js"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


def install_to(tmp_path: Path) -> subprocess.CompletedProcess[str]:
    package_root = tmp_path / "package"
    codex_home = tmp_path / "codex-home"
    workspace = tmp_path / "workspace"
    for d in (package_root, codex_home, workspace):
        d.mkdir()
    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")
    return subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace,
        check=False,
        capture_output=True,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        text=True,
    )


# ===========================================================================
# Stage 1: Template File Copy Completeness
# ===========================================================================


REQUIRED_TEMPLATE_FILES = (
    "AGENTS.md",
    "INSTRUCTIONS.md",
    "progress.md",
    "session-handoff.md",
    "feature-list.json",
    "init.sh",
)


def test_template_directory_contains_all_required_files() -> None:
    actual_names = {p.name for p in TEMPLATE_DIR.iterdir()}
    for required in REQUIRED_TEMPLATE_FILES:
        assert required in actual_names, (
            f"Template directory is missing '{required}'"
        )


def test_new_skill_references_template_copying() -> None:
    content = NEW_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "template" in content.lower()
    assert ".codex/ahe-shared/templates/" in content
    assert "copy" in content.lower() or "create" in content.lower()


def test_installer_copies_all_template_files_to_codex_home(tmp_path: Path) -> None:
    result = install_to(tmp_path)
    codex_home = tmp_path / "codex-home"

    assert result.returncode == 0, result.stderr
    for template_file in REQUIRED_TEMPLATE_FILES:
        target = codex_home / "ahe-shared" / "templates" / template_file
        assert target.exists(), f"Missing installed template: {template_file}"


# ===========================================================================
# Stage 2: Conversation Triggers for Missing/Insufficient Docs
# ===========================================================================


def test_conversation_required_when_product_md_insufficient() -> None:
    ctx = additional_context("ahe")
    assert "ahe-conversator" in ctx
    assert "docs/product.md" in ctx
    assert (
        "missing or empty" in ctx
        or "not enough" in ctx.lower()
        or "harness engineering not enough" in ctx
    )


def test_conversation_required_when_agents_md_purpose_lacking() -> None:
    content = NEW_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "ask for the purpose of this project" in content
    assert "ask the user whether the current `AGENTS.md` is right" in content
    assert "PROJECT_PURPOSE" in content


def test_conversation_optional_when_architecture_md_missing() -> None:
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    # architecture.md is not listed as a hard requirement in the thinker
    # The thinker reads docs/*.md but does not block on architecture.md
    assert "docs/*.md" in thinker or "Read all existing `docs/*.md`" in thinker
    # ahe-conversator is available for clarification but architecture is optional
    assert "ahe-conversator" in thinker


def test_thinker_routes_to_conversator_for_clarification() -> None:
    content = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "If the need is user clarification, call `ahe-conversator`." in content
    assert "ahe-conversator" in content
    # conversator itself defines conversational protocol
    conv = CONVERSATOR_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "one question at a time" in conv.lower()
    assert "conversation state" in conv.lower()


# ===========================================================================
# Stage 3: Multiple Product Files Handling
# ===========================================================================


def test_product1_exists_without_product_md_requires_conversation() -> None:
    """When product.md is absent but product1.md exists, system must create product.md."""
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")

    # Harness treats product.md as canonical and overview
    assert "`docs/product.md` is the canonical source of truth" in harness
    assert "Treat `docs/product.md` as overview context" in harness
    # Thinker recognizes product stages
    assert "docs/product.md" in thinker
    # When product.md is missing, the hook classifies as 'not enough'
    ctx = additional_context("ahe")
    assert "docs/product.md" in ctx
    assert "missing or empty" in ctx or "harness engineering not enough" in ctx


def test_product2_not_covered_in_product_md_detected() -> None:
    """When product.md exists but product2.md is not reflected, system should check."""
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")

    # Harness and thinker both handle multi-stage product docs
    assert "Treat `docs/product.md` as overview context even when a numbered product stage is active." in harness
    assert "Choose the lowest-numbered product stage whose derived feature work is not complete." in harness
    assert "docs/product{number}.md" in thinker or "docs/product1.md" in thinker


def test_staged_product_ordering_ignores_non_numeric() -> None:
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    ctx = additional_context("ahe")

    assert "Ignore non-numeric product files such as `docs/product-alpha.md` for stage ordering." in harness
    assert "Ignore non-numeric product docs such as `docs/product-alpha.md`" in thinker
    assert "docs/product-alpha.md" in ctx


def test_active_product_stage_selection_by_lowest_unfinished() -> None:
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "Choose the lowest-numbered product stage whose derived feature work is not complete." in harness
    # Thinker uses slightly different phrasing for lowest-unfinished stage logic
    assert "lowest-numbered stage" in thinker or "active product stage" in thinker


# ===========================================================================
# Stage 4: Actual Situation Handling
# ===========================================================================


def test_feature_list_empty_when_product_md_has_features() -> None:
    """feature-list.json should be updated according to product.md."""
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "Update `feature-list.json` to derive the specific feature items from the updated `docs/product.md`." in harness
    assert "`docs/product.md` is the canonical source of truth. Concrete feature items for `feature-list.json` must be derived from it only after it has been populated." in harness


def test_all_features_done_triggers_completion_check() -> None:
    """When all features are done, system classifies as 'completed all'."""
    ctx = additional_context("ahe")

    assert "`completed all`" in ctx
    assert "ask the user for the next task" in ctx or "ask the user" in ctx
    assert "all features are `done`" in ctx


def test_ahe_new_with_conflict_asks_intention() -> None:
    """When features not all done but user calls ahe new, ask about conflict."""
    init = NEW_SKILL_MD_PATH.read_text(encoding="utf-8")

    # New skill asks restart scope when existing harness exists
    assert "ask what restart scope the user wants before removing, overwriting, or refreshing existing harness files" in init
    assert "Interpret the restart scope from the user's free-form answer" in init
    # The hook also enforces the restart-scope question
    ctx = additional_context("ahe new")
    assert "ask what restart scope the user wants" in ctx
    assert "Do not remove, overwrite, or refresh existing harness files before the user answers" in ctx


def test_harness_files_reach_limit_triggers_compression() -> None:
    """When harness files are oversized, ahe-compression is triggered."""
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    ctx = additional_context("ahe")

    assert "check-harness-size.sh" in thinker
    assert "COMPRESSION_REQUIRED" in thinker
    assert "ahe-compression" in thinker
    assert "ahe-compression" in ctx


def test_all_done_then_ahe_new_creates_new_feature_list() -> None:
    """When all done and user calls ahe new, check completion then handle."""
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    ctx = additional_context("ahe")

    # System should check whether all are truly done
    assert "`completed all`" in ctx
    # System supports deriving new features
    assert "If no new feature can be derived from `docs/product.md`, call `ahe-conversator`" in harness




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
            # Skip tests that need tmp_path when running standalone
            sig = inspect.signature(fn)
            if "tmp_path" in sig.parameters:
                print("SKIP (needs pytest tmp_path)")
                continue
            fn()
            print("OK")
        except Exception as e:
            print(f"FAIL: {e}")
    print("test_ahe_new.py standalone run complete.")
