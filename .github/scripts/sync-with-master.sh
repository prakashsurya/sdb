#!/bin/bash -eux

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
BRANCH=$(git symbolic-ref --short HEAD)
[[ -n "${BRANCH}" ]] || exit 1

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

#
# In order to open a pull request, we need to push to a remote branch.
# To avoid conflicting with existing remote branches, we use branches
# within the "sync-with-master" namespace on the remote repository.
#
git push -f origin "sync-with-master/${BRANCH}"

#
# Opening a pull request may fail if there already exists a pull request
# for the branch; e.g. if a previous pull request was previously made,
# but not yet merged by the time we run this "sync" script again. Thus,
# rather than causing the automation to report a failure in this case,
# we swallow the error and report success.
#
# Additionally, as along as the git branch was properly updated (via the
# "git push" above), the existing PR will have been updated as well, so
# the "hub" command is unnecessary (hence ignoring the error).
#
git log -1 --format=%B | hub pull-request -F - -b "${BRANCH}" || true
