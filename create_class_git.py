#!/usr/bin/env python3
import subprocess
import os

# Inherit your normal env, but turn off SSL verification for Git
GIT_ENV = os.environ.copy()
GIT_ENV["GIT_SSL_NO_VERIFY"] = "true"


def local_branch_exists(name: str) -> bool:
    """Return True if a local branch called `name` already exists."""
    result = subprocess.run(
        ["git", "branch", "--list", name],
        stdout=subprocess.PIPE,
        text=True,
        # local operation, env override isn’t needed here
    )
    return bool(result.stdout.strip())


def remote_branch_exists(name: str) -> bool:
    """Return True if origin already has a branch called `name`."""
    result = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", name],
        stdout=subprocess.PIPE,
        text=True,
        env=GIT_ENV,                   # ← disable SSL verify here
    )
    return bool(result.stdout.strip())


def make_branch(name: str):
    # 1. Create local branch if missing
    if not local_branch_exists(name):
        print(f"✔ Creating local branch '{name}'")
        subprocess.run(
            ["git", "branch", name],
            check=True,
            # local op, env override not required
        )
    else:
        print(f"→ Local branch '{name}' already exists, skipping creation")

    # 2. Push to remote only if it’s not already there
    if remote_branch_exists(name):
        print(f"→ Remote branch '{name}' already exists, skipping push")
    else:
        print(f"🔄 Pushing '{name}' to origin…")
        try:
            subprocess.run(
                ["git", "push", "-u", "origin", name],
                check=True,
                capture_output=True,
                text=True,
                env=GIT_ENV,               # ← and here
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to push '{name}':\n{e.stderr.strip()}\n")


def main():
    # Read one student name per line
    with open("students.txt") as f:
        students = [line.strip() for line in f if line.strip()]

    for student in students:
        make_branch(student)


if __name__ == "__main__":
    main()
