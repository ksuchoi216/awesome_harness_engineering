#!/bin/bash
stdout_path="stdout.txt"
stderr_path="stderr.txt"
printf 'AHE_PLAN_COMPLETE\n' > "$stdout_path"
touch "$stderr_path"
combined_output="$(cat "${stdout_path}")"$'\n'"$(cat "${stderr_path}")"
case "${combined_output}" in
  *AHE_PLAN_COMPLETE*)
    echo "Matched!"
    ;;
  *)
    echo "Failed to match!"
    ;;
esac
