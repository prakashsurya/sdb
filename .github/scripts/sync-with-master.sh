#!/bin/bash -eux

[[ -z "${GITHUB_REF}" ]] && exit 1

#
# We only want to operate on branches, so we verify the passed in ref is
# a branch (e.g. rather than a tag) here.
#
git show-ref --heads "${GITHUB_REF}" &>/dev/null || exit 0
