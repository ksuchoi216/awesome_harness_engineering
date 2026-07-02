#!/bin/bash
set -euo pipefail
my_func() {
  exit 1
}
test_local() {
  local val
  val="$(my_func)"
  echo "val is $val"
}
test_local_inline() {
  local val="$(my_func)"
  echo "inline val is $val"
}
test_local_inline
