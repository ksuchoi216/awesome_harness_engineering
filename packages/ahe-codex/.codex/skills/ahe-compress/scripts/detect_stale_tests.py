import sys
import os

def main():
    test_dir = "tests"
    if not os.path.isdir(test_dir):
        sys.exit(0)

    overlap_map = {
        "test_new_workflow.py": ["test_ahe_new.py"],
        "test_spec_workflow.py": ["test_clarification_prompt.py", "test_ahe_new.py"],
        "test_specialized_workflows.py": ["test_ahe_new.py", "test_clarification_prompt.py", "test_command_set.py"]
    }

    stale_found = False
    for legacy_file, keeper_files in overlap_map.items():
        legacy_path = os.path.join(test_dir, legacy_file)
        if os.path.exists(legacy_path):
            stale_found = True
            keepers_str = ",".join(f"tests/{f}" for f in keeper_files)
            print(f"REVIEW_TEST\ttests/{legacy_file}\tcovered_by={keepers_str}")

    if stale_found:
        print("TEST_COMPRESSION_REQUIRED")
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
