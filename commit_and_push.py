#!/usr/bin/env python3
import subprocess
import sys
import os

def is_git_repo():
    """Check if current directory is inside a Git repository."""
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.returncode == 0 and result.stdout.strip() == "true"

def commit_and_push(message: str):
    """Stage all changes, commit with the given message, and push to the current branch."""
    # Stage all changes
    print("🔄 Staging changes...")
    subprocess.run(["git", "add", "."], check=True)

    # Commit
    print(f"✏️  Committing with message: '{message}'")
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        stderr = result.stderr.lower()
        if "nothing to commit" in stderr:
            print("ℹ️  Nothing to commit.")
        else:
            print(f"❌ Commit failed:\n{result.stderr.strip()}")
            sys.exit(1)
    else:
        print(result.stdout.strip())

    # Push
    print("🚀 Pushing to remote...")
    subprocess.run(["git", "push"], check=True)
    print("✅ Push complete.")

def main():
    if not is_git_repo():
        print("❌ Error: This directory is not a Git repository.")
        sys.exit(1)

    # Determine commit message
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "Student work update"

    try:
        commit_and_push(message)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ An error occurred during Git operations:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
