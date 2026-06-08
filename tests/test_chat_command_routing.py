from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"

def test_skill_md_has_yaml_frontmatter() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert content.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    
    parts = content.split("---\n")
    assert len(parts) >= 3, "SKILL.md must have closing frontmatter dashes"
    frontmatter_text = parts[1]
    
    lines = frontmatter_text.strip().split("\n")
    metadata = {}
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    
    assert metadata.get("name") == "ahe", f"Expected name 'ahe', got '{metadata.get('name')}'"
    assert "description" in metadata, "Missing 'description' in frontmatter"

def test_skill_md_contains_command_routing_instructions() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Router Rule" in content, "Missing '## Command Router Rule' section"
    assert "$ahe-init" in content
    assert "$ahe-agent" in content
    assert "$ahe-product" in content
    assert "$ahe-constraints" in content
    assert "$ahe-architecture" in content
    assert "$ahe-update" in content
    assert "$ahe-clear" in content

if __name__ == "__main__":
    test_skill_md_has_yaml_frontmatter()
    test_skill_md_contains_command_routing_instructions()
    print("test_chat_command_routing.py passed!")
