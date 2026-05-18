#!/usr/bin/env sh
set -eu

git config core.hooksPath .githooks
echo "Installed LLM Wiki git hooks from .githooks"
