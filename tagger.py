import os
import logging
import subprocess
from typing import List, Union

# 3.1.30
import git

repo = git.Repo(subprocess.getoutput('git rev-parse --show-toplevel'))


def get_tags(repo) -> List[str]:
    """Get list of all tags for package"""
    try:
        return repo.git.tag(l=f'1.*').split('\n')
    except (git.NoSuchPathError, git.InvalidGitRepositoryError):
        # In case a git repo is not found
        return []


def get_head_tag(repo):
    HeadTag = None
    for tagRef in repo.tags:
        if tagRef.commit == repo.head.commit and tagRef.tag != None:
            HeadTag = tagRef.tag.tag
    return HeadTag


def check_head(repo):
    return any([tag.commit == repo.head.commit for tag in repo.tags])


print(check_head(repo))


def get_latest_tag(repo):
    return max(get_tags(repo))


def parse_tag(tag):
    return map(int, tag.split('.'))


print(get_head_tag(repo))
print(get_latest_tag(repo))


def get_next_tag(repo, new_major=None, hotfix=False):
    latest_tag = get_latest_tag(repo)
    major, minor, patch = parse_tag(latest_tag)
    if new_major:
        # Need to incremental new_major > major
        return f"{new_major}.{0}.{0}"
    if hotfix:
        return f"{major}.{minor}.{patch+1}"
    return f"{major}.{minor+1}.0"


print(get_next_tag(repo, new_major=2))
print(get_next_tag(repo, hotfix=True))
print(get_next_tag(repo))

next_tag = get_next_tag(repo)


def add_tag(repo, tag):
    new_tag = repo.create_tag(tag, message='Automatic tag "{0}"'.format(tag))
    return new_tag


def push_tag(repo, tag):
    repo.remote('origin').push(tag)

new_tag = add_tag(repo, next_tag)
push_tag(repo, new_tag)
