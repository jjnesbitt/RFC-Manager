#!/usr/bin/env python3
import re
import click
import shutil
from datetime import datetime
from pathlib import Path

from multinet_rfc.utils import get_context, get_github_username, burn_version


context = get_context()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name", type=click.STRING, nargs=1)
def create(name):
    if re.search(r"\s+", name):
        click.echo("Error: Draft names cannot contain spaces")

    new_folder = context.drafts / ("XXXX-" + name)
    readme = new_folder / "README.md"
    new_folder.mkdir(parents=True)
    shutil.copy(context.template_file, readme)

    with open(readme) as infile:
        lines = [line.strip() for line in infile.readlines()]

    user = get_github_username()

    datestring = datetime.now().strftime("%Y-%m-%d")
    created_line = "Created: " + datestring
    last_modified_line = "Last-Modified: " + datestring

    if user:
        lines[2] = "Author: " + user

    lines[4] = created_line
    lines[5] = last_modified_line

    # Delete superseded, since this is new
    del lines[6:8]

    with open(readme, "w") as outfile:
        outfile.write("\n".join(lines))


@cli.command()
@click.argument("folder", type=click.STRING, nargs=1)
def accept(folder):
    draft_to_accept = Path(folder)

    if not draft_to_accept.exists():
        click.echo("Error: Folder does not exist")
        return

    name_match = re.search(r"XXXX-(\S+)", draft_to_accept.name)
    if name_match is None:
        click.echo("Error: Folder name is malformed")
        return

    draft_name = name_match.group(1)
    version = burn_version()

    new_folder_name = str(version) + "-" + draft_name
    accepted_draft = context.accepted / new_folder_name

    shutil.move(folder, accepted_draft)

    readme = accepted_draft / "README.md"
    with open(readme) as infile:
        lines = [line.strip() for line in infile.readlines()]

    lines[1] = "RFC: " + version
    lines[3] = "Status: accepted"

    for i, line in enumerate(lines):
        search = re.search(r"# RFC XXXX: (.+)", line)
        if search:
            lines[i] = "# RFC " + version + ": " + search.group(1)

    with open(readme, "w") as outfile:
        outfile.write("\n".join(lines))


@cli.command()
def reject():
    pass


@cli.command()
def finalize():
    pass


@cli.command()
def withdraw():
    pass


@cli.command()
def revive():
    pass


@cli.command()
def supersede():
    pass


# #####################
def main():
    cli()


if __name__ == "__main__":
    main()
