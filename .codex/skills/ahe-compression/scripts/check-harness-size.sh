#!/usr/bin/env sh
set -eu

file_limit="${AHE_FILE_LINE_LIMIT:-180}"
total_limit="${AHE_TOTAL_LINE_LIMIT:-750}"
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

  if [ "${line_count}" -ge "${file_limit}" ]; then
    compression_required=1
    printf 'COMPRESS\t%s\t%s\tlimit=%s\n' "${file_path}" "${line_count}" "${file_limit}"
  else
    printf 'OK\t%s\t%s\tlimit=%s\n' "${file_path}" "${line_count}" "${file_limit}"
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
