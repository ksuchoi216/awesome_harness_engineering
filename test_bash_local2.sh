#!/bin/bash
set -euo pipefail
my_func() {
  exit 1
}
test_split() {
  local val
  val="$(my_func)"
  echo "This should not be printed"
}
test_split
