import os
import subprocess
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path
from click.exceptions import ClickException
from git import Repo
from git.exc import InvalidGitRepositoryError


@dataclass
class RepoContext:
    """Represents files/folders in the RFC repo."""

    template_file: Path
    rfc_number_file: Path
    drafts: Path
    accepted: Path
    final: Path
    rejected: Path
    superseded: Path
    withdrawn: Path


def determine_project_root():
    cwd = Path(os.getcwd())

    try:
        repo = Repo(cwd)
        urls = set(repo.remote().urls)
        valid = {
            "git@github.com:multinet-app/multinet-rfcs.git",
            "https://github.com/multinet-app/multinet-rfcs.git",
        }
        if not valid & urls:
            raise InvalidGitRepositoryError()

    except InvalidGitRepositoryError:
        raise ClickException("Must be run in a checked-out Multinet-RFC repository.")

    return cwd


@lru_cache(maxsize=1)
def get_context() -> RepoContext:
    project_root = determine_project_root()
    return RepoContext(
        template_file=project_root / "template.md",
        rfc_number_file=project_root / "next_rfc_number.txt",
        drafts=project_root / "draft",
        accepted=project_root / "accepted",
        final=project_root / "final",
        rejected=project_root / "rejected",
        superseded=project_root / "superseded",
        withdrawn=project_root / "withdrawn",
    )


def get_github_username():
    try:
        res = subprocess.check_output(["git", "config", "user.name"])
        return res.decode().strip()
    except subprocess.CalledProcessError:
        return None


def burn_version():
    context = get_context()
    with open(context.rfc_number_file) as infile:
        next_version = int(infile.read().strip())

    with open(context.rfc_number_file, "w") as outfile:
        outfile.write(str(next_version + 1).zfill(4))

    return str(next_version).zfill(4)
