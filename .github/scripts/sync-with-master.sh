#!/bin/bash -eux

echo foo

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
# We need these config parameters set in order to do the git-merge.
#
git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"

#
# We obtain the original name for the branch we'll be syncing with
# master. We gather this information here, since we'll change the name
# of the local branch later, and we'd like to use the original branch
# name when opening the pull request.
#
BRANCH=$(git symbolic-ref --short HEAD) || die "HEAD is not a symbolic ref"
[[ -n "${BRANCH}" ]] || die "unable to determine symbolic ref for HEAD"

#
# We need the full git repository history in order to do the git-merge.
#
git fetch --unshallow
git merge origin/master

#
# We modify the local branch name and upstream tracking branch such that
# the correct operations occur when pushing and opening the pull request.
#
git branch -M "sync-with-master/${BRANCH}"
git branch --set-upstream-to "origin/${BRANCH}"

git push -f origin "sync-with-master/${BRANCH}"
git log -1 --format=%B | hub pull-request -F - -b "${BRANCH}"
