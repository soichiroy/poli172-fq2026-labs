#!/usr/bin/env python3
"""Enable this repository's hook without replacing existing user hooks."""

from pathlib import Path
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def git(*args, check=True):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
    )


def main():
    git_dir = Path(git("rev-parse", "--absolute-git-dir").stdout.strip())
    hook_dir = git_dir / "hooks"
    source = ROOT / ".githooks" / "pre-commit"
    configured = git("config", "--path", "--get", "core.hooksPath", check=False)
    if configured.returncode not in (0, 1):
        raise RuntimeError("Unable to read the existing hooks configuration.")
    previous = Path(configured.stdout.strip()) if configured.returncode == 0 else hook_dir
    if not previous.is_absolute():
        previous = ROOT / previous
    previous = previous.resolve()

    links = {hook_dir / "pre-commit": source}
    if previous != hook_dir.resolve() and previous.is_dir():
        for hook in previous.iterdir():
            if hook.name.endswith(".sample") or not hook.is_file() or not os.access(hook, os.X_OK):
                continue
            if hook.name == "pre-commit" and hook.resolve() != source.resolve():
                raise RuntimeError(
                    "An existing pre-commit hook needs to be combined with this one; "
                    "no hooks or settings were changed."
                )
            links[hook_dir / hook.name] = hook

    # Check every destination before changing files or configuration.
    for destination, target in links.items():
        if destination.exists() or destination.is_symlink():
            if destination.resolve() != target.resolve():
                raise RuntimeError(f"Preserving existing hook {destination}; no changes made.")

    hook_dir.mkdir(parents=True, exist_ok=True)
    source.chmod(source.stat().st_mode | 0o111)
    for destination, target in links.items():
        if not destination.exists() and not destination.is_symlink():
            destination.symlink_to(target.resolve())
    git("config", "--local", "core.hooksPath", str(hook_dir))
    print("Enabled PDF/solution commit protection for this checkout.")
    print("Existing active hooks were preserved. Run this installer in each new clone.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, OSError) as error:
        print(f"Hook installation stopped: {error}", file=sys.stderr)
        sys.exit(1)
