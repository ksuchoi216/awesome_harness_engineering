import subprocess

script = """
stdout_path="stdout.txt"
stderr_path="stderr.txt"
cat << 'INNEREOF' > "$stdout_path"
Reconcile this saved AHE plan against the current repository state.
Overwrite the original .plans/ file with the refreshed plan, then execute the refreshed plan exactly.

# Saved Plan
# Example Plan

When every requirement is fully complete and verified, print the exact line AHE_PLAN_COMPLETE.
AHE_PLAN_COMPLETE
INNEREOF

touch "$stderr_path"
combined_output="$(cat "${stdout_path}")"$'\n'"$(cat "${stderr_path}")"
case "${combined_output}" in
  *AHE_PLAN_COMPLETE*)
    echo "MATCHED"
    ;;
  *)
    echo "NOT_MATCHED"
    ;;
esac
"""

res = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
print(res.stdout)
