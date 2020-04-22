#!/bin/bash -eux

function die() {
	echo "$(basename "$0"): $*" >&2
	exit 1
}

#HEAD=$(git symbolic-ref --short HEAD) || die "HEAD is not a symbolic ref"
#[[ -n "$HEAD" ]] || die "unable to determine symbolic ref for HEAD"

[[ -z "${GITHUB_REF}" ]] && die "GITHUB_REF is empty"

#
# We only want to operate on branches, so we verify the passed in ref is
# a branch (e.g. rather than a tag) here.
#
git show-ref --heads "${GITHUB_REF}" &>/dev/null ||
	die "GITHUB_REF (${GITHUB_REF}) is not a branch"

git fetch --prune --unshallow

git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git merge origin/master
git push

echo hi
echo ho
