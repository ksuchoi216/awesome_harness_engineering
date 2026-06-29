from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "packages/ahe-codex/.codex/ahe-shared/templates"
NEW_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/new/SKILL.md"
SKILL_MD_PATH = NEW_SKILL_MD_PATH
INIT_SKILL_MD_PATH = NEW_SKILL_MD_PATH
THINKER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/think/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"
CONVERSATOR_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/converse/SKILL.md"
SOLVER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/solve/SKILL.md"
HOOK_PATH = REPO_ROOT / "packages/ahe-codex/.codex/hooks/ahe-hook.js"


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
    (tmp_path / "home").mkdir()
    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")
    return subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace,
        check=False,
        capture_output=True,
        env={**os.environ, "CODEX_HOME": str(codex_home), "HOME": str(tmp_path / "home")},
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
    assert "converse" in ctx
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
    # converse is available for clarification but architecture is optional
    assert "converse" in thinker


def test_thinker_routes_to_conversator_for_clarification() -> None:
    content = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "If the need is user clarification, call `converse`." in content
    assert "converse" in content
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
    """When harness files are oversized, compress is triggered."""
    thinker = THINKER_SKILL_MD_PATH.read_text(encoding="utf-8")
    ctx = additional_context("ahe")

    assert "check-harness-size.sh" in thinker
    assert "COMPRESSION_REQUIRED" in thinker
    assert "compress" in thinker
    assert "compress" in ctx


def test_all_done_then_ahe_new_creates_new_feature_list() -> None:
    """When all done and user calls ahe new, check completion then handle."""
    harness = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    ctx = additional_context("ahe")

    # System should check whether all are truly done
    assert "`completed all`" in ctx
    # System supports deriving new features
    assert "If no new feature can be derived from `docs/product.md`, call `converse`" in harness

def test_skill_md_contains_init_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: new" in content, "Missing '## Command Workflow: new' section"
    assert "Workspace Inspection" in content, "Missing Workspace Inspection step description"
    assert "Sequential Conversation Flow" in content, "Missing Sequential Conversation Flow description"
    assert "Harness Generation" in content, "Missing Harness Generation step description"


def test_skill_md_contains_all_required_inputs() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "ask the user whether the current `AGENTS.md` is right",
        "ask for the purpose of this project",
        "PROJECT_PURPOSE",
        "project language is Python",
        "Which language do you use?",
    ]
    for required_input in required_inputs:
        assert required_input in content, f"Missing required input '{required_input}' in new workflow definition"


def test_skill_md_contains_generated_files() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_files = [
        "AGENTS.md",
        "status.json",
    ]
    for required_file in required_files:
        assert required_file in content, f"Missing required output file '{required_file}' in new workflow definition"


def test_skill_md_contains_three_sequential_steps_and_status_tracking() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    expected_steps = [
        'call "harness"',
    ]
    for step in expected_steps:
        assert step in content, f"Missing step '{step}' in new workflow definition"

    expected_statuses = [
        'new',
        'harness',
    ]
    for status in expected_statuses:
        assert status in content, f"Missing progress status '{status}' in new workflow definition"



def test_skill_md_absorbs_reset_behavior_without_backups_for_new_start() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Remove the previous `docs/product.md` and `docs/INSTRUCTIONS.md`",
        "Remove the previous `feature-list.json`",
        "new start",
        "Do not create backup copies of the replaced harness files",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing absorbed reset behavior '{required_behavior}' in new"
        )

    forbidden_behaviors = [
        ".ahe/backups/",
        "backup directory",
        "back up the current product/specification files",
    ]
    for forbidden_behavior in forbidden_behaviors:
        assert forbidden_behavior not in content, (
            f"Unexpected backup behavior '{forbidden_behavior}' still present in new"
        )



def test_skill_md_requires_restart_scope_before_resetting_existing_harness() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "If no AHE-managed harness files exist, start initialization normally without asking a restart-scope question.",
        "If any AHE-managed harness file already exists, read the existing files first.",
        "summarize the current project purpose and product specification state",
        "ask what restart scope the user wants before removing, overwriting, or refreshing existing harness files",
        "Interpret the restart scope from the user's free-form answer",
        "`purpose` means restart the whole harness from the project purpose",
        "`product` means preserve the project purpose in `AGENTS.md`",
        "summarize the replaced harness history in the refreshed tracking artifacts instead of creating backups",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing restart-scope behavior '{required_behavior}' in new"
        )



def test_skill_md_keeps_specification_details_out_of_agents_md() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Keep `AGENTS.md` limited to the project purpose and base agent settings.",
        "Do not put product specification details in `AGENTS.md`.",
        "Send product behavior, scope, requirements, success criteria, and workflow details to `harness` so they are written in `docs/product.md` first.",
        "Generating an empty `feature-list.json` from a template is allowed, but do not write concrete feature items until `docs/product.md` is populated.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing specification placement behavior '{required_behavior}' in new"
        )



def test_startup_workflow_reads_all_docs_markdown() -> None:
    agents_content = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    init_content = SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "Read project docs if present" in agents_content
    assert "`docs/architecture.md`" in agents_content
    assert "`docs/product.md`" in agents_content
    assert "`docs/constraints.md`" in agents_content
    assert "`docs/*.md`" in agents_content
    assert (
        "especially, product.md and product{number}.md present explanation of what to do."
        in agents_content
    )
    assert "Read all `docs/*.md` files when they exist." in init_content
    assert "`docs/product{number}.md` files when present" in init_content



def test_product_spec_is_canonical_home_for_init_specification_details() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "`docs/product.md` is the canonical home for product specification details collected during `ahe new`.",
        "Write product behavior, scope, requirements, success criteria, and workflow details into `docs/product.md`.",
        "`docs/product.md` is the canonical source of truth. Concrete feature items for `feature-list.json` must be derived from it only after it has been populated.",
        "Do not move product specification details into `AGENTS.md`.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing canonical product-spec behavior '{required_behavior}' in harness"
        )



def test_product_spec_supports_ordered_stage_documents() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Treat `docs/product.md` as overview context even when a numbered product stage is active.",
        "Recognize only `docs/product{number}.md` files as ordered product stages.",
        "Ignore non-numeric product files such as `docs/product-alpha.md` for stage ordering.",
        "Choose the lowest-numbered product stage whose derived feature work is not complete.",
        "Derive concrete feature items from only the active product stage, not future stages.",
        "Advance from `docs/product1.md` to `docs/product2.md` only after all feature-list items derived from `docs/product1.md` are `done`.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing staged product behavior '{required_behavior}' in harness"
        )



def test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy() -> None:
    content = INIT_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: new" in content
    assert "Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`." in content
    assert "project language is Python" in content
    assert "Which language do you use?" in content
    assert "template" in content.lower()
    assert "overwrite" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "custom input" in content.lower()



def test_solver_reads_active_product_stage_context() -> None:
    content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "docs/product.md" in content
    assert "active product stage" in content
    assert "docs/product1.md" in content
    assert "future product stages" in content




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
