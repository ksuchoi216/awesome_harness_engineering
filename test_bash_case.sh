#!/bin/bash
str="hello
AHE_PLAN_COMPLETE
world"

case "$str" in
  *AHE_PLAN_COMPLETE*)
    echo "Matched"
    ;;
  *)
    echo "Not matched"
    ;;
esac
