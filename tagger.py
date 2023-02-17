import os
import logging
import subprocess
from typing import List, Union

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

def get_latest_tag(repo):
    return max(get_tags(repo))

print (get_latest_tag(repo))

# hotfix = False
# def get_next_tag(repo, major, hotfix):

