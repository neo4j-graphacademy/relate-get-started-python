#!/usr/bin/env bash
# Runs once, after the Codespace is created and the repository is cloned.
# It prepares the lab folder and confirms the tools work. It is safe to rerun:
# it never deletes anything a student made.
set -euo pipefail

echo "post-create: preparing the lab folder"
lab-reset --init

echo "post-create: checking the environment"
lab-check

echo "post-create: done"
