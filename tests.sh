#!/bin/sh
echo "Running Unit Tests"
echo "=================="
nose2 -v --pretty-assert -t . -s tests/unit "$@"

echo "Running Integration Tests"
echo "========================="
nose2 -v --pretty-assert -t . -s tests/integration "$@"
