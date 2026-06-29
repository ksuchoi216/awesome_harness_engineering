import re
from pathlib import Path

def get_functions(file_path):
    content = Path(file_path).read_text()
    funcs = re.findall(r'(def test_[a-zA-Z0-9_]+\(.*?\)\s*->\s*None:.*?)(?=\ndef test_|\nif __name__ ==)', content, re.DOTALL)
    return funcs

def append_funcs(target_file, funcs):
    content = Path(target_file).read_text()
    if "__main__" in content:
        parts = content.split('if __name__ == "__main__":')
        new_content = parts[0].rstrip() + "\n\n" + "\n\n".join(funcs) + "\n\n\nif __name__ == \"__main__\":\n" + parts[1].lstrip()
    else:
        new_content = content.rstrip() + "\n\n" + "\n\n".join(funcs) + "\n"
    Path(target_file).write_text(new_content)

# legacy files
new_wf = "tests/test_new_workflow.py"
spec_wf = "tests/test_spec_workflow.py"
special_wf = "tests/test_specialized_workflows.py"

new_funcs = get_functions(new_wf)
spec_funcs = get_functions(spec_wf)
special_funcs = get_functions(special_wf)

# Mappings based on manual inspection
ahe_new_funcs = new_funcs + [
    f for f in spec_funcs if "ordered_stage_documents" in f or "canonical_home" in f
] + [
    f for f in special_funcs if "init_workflow_details_absorbed" in f or "solver_reads_active_product_stage_context" in f
]

clarif_funcs = [
    f for f in spec_funcs if "ordered_stage_documents" not in f and "canonical_home" not in f
] + [
    f for f in special_funcs if "harness_workflow" in f or "harness_tracking_workflow" in f
]

cmd_funcs = [
    f for f in special_funcs if "user_facing_commands" in f or "divide_and_plan_behavior" in f
]

append_funcs("tests/test_ahe_new.py", ahe_new_funcs)
append_funcs("tests/test_clarification_prompt.py", clarif_funcs)
append_funcs("tests/test_command_set.py", cmd_funcs)

Path(new_wf).unlink()
Path(spec_wf).unlink()
Path(special_wf).unlink()

print("Consolidation complete.")
