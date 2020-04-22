#!/bin/bash -eux

function die() {
	echo "$(basename "$0"): $*" >&2
	exit 1
}

HEAD=$(git symbolic-ref --short HEAD) || die "HEAD is not a symbolic ref"
[[ -z "$HEAD" ]] || die "unable to determine symbolic ref for HEAD"

echo "$HEAD"

[[ -z "${GITHUB_REF}" ]] && die "GITHUB_REF is empty"

#
# We only want to operate on branches, so we verify the passed in ref is
# a branch (e.g. rather than a tag) here.
#
git show-ref --heads "${GITHUB_REF}" &>/dev/null ||
	die "GITHUB_REF (${GITHUB_REF}) is not a branch"

[[ "${GITHUB_REF}"

git branch -v -a

sudo apt-get install -y tree

tree -a .
