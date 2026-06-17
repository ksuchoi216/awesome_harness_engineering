#!/usr/bin/env sh
set -eu

limit_agent_md=180
limit_product_md=180
limit_instructions_md=180
limit_feature_list_json=180
limit_progress_md=180
limit_session_handoff_md=180
limit_todo_md=180
limit_total=750

config_file=".codex/ahe-shared/config.yaml"
if [ -f "${config_file}" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    case "$line" in
      "" | \#*) continue ;;
    esac
    
    key="${line%%:*}"
    val="${line#*:}"
    key="${key%"${key##*[![:space:]]}"}"
    val="${val#"${val%%[![:space:]]*}"}"
    
    case "$val" in
      ''|*[!0-9]*) continue ;;
    esac

    case "$key" in
      agent_md) limit_agent_md="$val" ;;
      product_md) limit_product_md="$val" ;;
      instructions_md) limit_instructions_md="$val" ;;
      feature_list_json) limit_feature_list_json="$val" ;;
      progress_md) limit_progress_md="$val" ;;
      session_handoff_md) limit_session_handoff_md="$val" ;;
      todo_md) limit_todo_md="$val" ;;
      total) limit_total="$val" ;;
    esac
  done < "${config_file}"
fi

limit_agent_md="${AHE_AGENT_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_agent_md}}"
limit_product_md="${AHE_PRODUCT_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_product_md}}"
limit_instructions_md="${AHE_INSTRUCTIONS_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_instructions_md}}"
limit_feature_list_json="${AHE_FEATURE_LIST_JSON_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_feature_list_json}}"
limit_progress_md="${AHE_PROGRESS_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_progress_md}}"
limit_session_handoff_md="${AHE_SESSION_HANDOFF_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_session_handoff_md}}"
limit_todo_md="${AHE_TODO_MD_LIMIT:-${AHE_FILE_LINE_LIMIT:-$limit_todo_md}}"
total_limit="${AHE_TOTAL_LINE_LIMIT:-$limit_total}"

total_lines=0
compression_required=0

if [ "$#" -eq 0 ]; then
  set -- \
    "AGENTS.md" \
    "docs/PRODUCT.md" \
    "docs/INSTRUCTIONS.md" \
    "feature-list.json" \
    "PROGRESS.md" \
    "SESSION-HANDOFF.md" \
    "docs/todo.md"
fi

for file_path in "$@"; do
  if [ ! -f "${file_path}" ]; then
    continue
  fi

  line_count="$(wc -l < "${file_path}")"
  line_count="${line_count#"${line_count%%[![:space:]]*}"}"
  line_count="${line_count%"${line_count##*[![:space:]]}"}"
  total_lines=$((total_lines + line_count))

  current_limit=180
  case "${file_path}" in
    "AGENTS.md") current_limit="${limit_agent_md}" ;;
    "docs/PRODUCT.md") current_limit="${limit_product_md}" ;;
    "docs/INSTRUCTIONS.md") current_limit="${limit_instructions_md}" ;;
    "feature-list.json") current_limit="${limit_feature_list_json}" ;;
    "PROGRESS.md") current_limit="${limit_progress_md}" ;;
    "SESSION-HANDOFF.md") current_limit="${limit_session_handoff_md}" ;;
    "docs/todo.md") current_limit="${limit_todo_md}" ;;
    *) current_limit="${AHE_FILE_LINE_LIMIT:-180}" ;;
  esac

  if [ "${line_count}" -ge "${current_limit}" ]; then
    compression_required=1
    printf 'COMPRESS\t%s\t%s\tlimit=%s\n' "${file_path}" "${line_count}" "${current_limit}"
  else
    printf 'OK\t%s\t%s\tlimit=%s\n' "${file_path}" "${line_count}" "${current_limit}"
  fi
done

if [ "${total_lines}" -ge "${total_limit}" ]; then
  compression_required=1
  printf 'COMPRESS_TOTAL\t%s\tlimit=%s\n' "${total_lines}" "${total_limit}"
else
  printf 'OK_TOTAL\t%s\tlimit=%s\n' "${total_lines}" "${total_limit}"
fi

if [ "${compression_required}" -eq 1 ]; then
  printf 'COMPRESSION_REQUIRED\n'
  exit 2
fi

printf 'COMPRESSION_NOT_REQUIRED\n'
