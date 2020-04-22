#!/bin/bash -eux

function die() {
	echo "$(basename "$0"): $*" >&2
	exit 1
}

[[ -z "${GITHUB_REF}" ]] && die "GITHUB_REF is empty"

#
# We only want to operate on branches, so we verify the passed in ref is
# a branch (e.g. rather than a tag) here.
#
git show-ref --heads "${GITHUB_REF}" &>/dev/null ||
	die "GITHUB_REF (${GITHUB_REF}) is not a branch"

#
# In order to perform the merge below, we need to have the following git
# configuration to be set.
#
git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"

#
# Additionally, in order to perform the merge below, we need the full
# history for the repository, so the merge can operate on that history.
#
git fetch --unshallow

#
# Now we can actually attempt the merge with the master branch.
#
git merge origin/master

BRANCH=$(git symbolic-ref --short HEAD) || die "HEAD is not a symbolic ref"
[[ -n "${BRANCH}" ]] || die "unable to determine symbolic ref for HEAD"
git push origin "HEAD:sync-with-master/${BRANCH}"
