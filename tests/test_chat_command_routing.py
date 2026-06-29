from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATHS = (
    REPO_ROOT / ".codex/skills/ahe-new/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-fix/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-solver/SKILL.md",
)


def test_each_skill_md_has_yaml_frontmatter() -> None:
    for skill_path in SKILL_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"{skill_path} must start with YAML frontmatter"

        parts = content.split("---\n")
        assert len(parts) >= 3, f"{skill_path} must have closing frontmatter dashes"
        frontmatter_text = parts[1]

        lines = frontmatter_text.strip().split("\n")
        metadata = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        assert metadata.get("name"), f"Missing skill name in {skill_path}"
        assert "description" in metadata, f"Missing description in {skill_path}"


def test_skill_files_match_expected_command_names() -> None:
    init_content = (REPO_ROOT / ".codex/skills/ahe-new/SKILL.md").read_text(encoding="utf-8")
    assert "$ahe-new" in init_content

    for skill_name in (
        "ahe-thinker",
        "ahe-reviewer",
        "ahe-conversator",
        "ahe-harness",
        "ahe-solver",
        "ahe-compression",
    ):
        content = (REPO_ROOT / f".codex/skills/{skill_name}/SKILL.md").read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()


if __name__ == "__main__":
    test_each_skill_md_has_yaml_frontmatter()
    test_skill_files_match_expected_command_names()
    print("test_chat_command_routing.py passed!")
