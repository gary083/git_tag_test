import git  # 3.1.30
import subprocess


def get_tags(repo):
    try:
        return repo.git.tag(l='1.*').split('\n')
    except (git.NoSuchPathError, git.InvalidGitRepositoryError):
        return []


def get_head_tag(repo):
    head_tag = None
    for tag_ref in repo.tags:
        if tag_ref.commit == repo.head.commit and tag_ref.tag is not None:
            head_tag = tag_ref.tag.tag
    return head_tag


def check_head(repo):
    return any([tag.commit == repo.head.commit for tag in repo.tags])


def get_latest_tag(repo):
    return max(get_tags(repo))


def parse_tag(tag):
    return map(int, tag.split('.'))


repo = git.Repo(subprocess.getoutput('git rev-parse --show-toplevel'))
print(check_head(repo))
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
    return repo.create_tag(tag, message=f'Automatic tag "{tag}"')


def push_tag(repo, tag):
    repo.remote('origin').push(tag)


new_tag = add_tag(repo, next_tag)
push_tag(repo, new_tag)
