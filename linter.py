import git  # 3.1.30
import subprocess


def get_changed_files(repo):
    return repo.git.diff(
        "--name-only", "--pretty=format:", "--cached", "--no-color"
    ).split("\n")


def check_cc_linter(changed_files):
    result = ''
    for file in changed_files:
        if file.lower().endswith((".h", ".cc")):
            result += subprocess.getoutput(
                f"clang-format --dry-run --style=Google {file} "
            )

    return result


def check_py_linter(changed_files):
    result = ''
    for file in changed_files:
        if file.lower().endswith((".py")):
            result += subprocess.getoutput(
                f"flake8 {file}")
    return result


print(subprocess.getoutput("git rev-parse --show-toplevel"))
repo = git.Repo(subprocess.getoutput("git rev-parse --show-toplevel"))

files = get_changed_files(repo)
cc_results = check_cc_linter(changed_files=files)
print(cc_results)

py_results = check_py_linter(changed_files=files)
print(py_results)
