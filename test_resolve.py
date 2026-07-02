import subprocess
import tempfile
from pathlib import Path
import os

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir).resolve()
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")
    
    script = """
    resolve_plan_path() {
      local plan_path="$1"
      local plan_dir
      plan_dir="$(CDPATH= cd -- "$(dirname -- "${plan_path}")" && pwd)"
      printf '%s/%s\\n' "${plan_dir}" "$(basename -- "${plan_path}")"
    }
    resolve_plan_path "$1"
    """
    
    res = subprocess.run(["bash", "-c", script, "--", str(plan_path)], capture_output=True, text=True)
    print("Python path:", str(plan_path))
    print("Bash path:  ", res.stdout.strip())
