# POLI 172 labs

Student lab materials are in the numbered `labNN/` folders. Keep each question
QMD with its accompanying data files and render completed work in RStudio.

## Publishing safeguards

This repository contains question sources and public data/assets. PDFs and
filenames or directories containing `-solutions` stay outside the repository.
Matching is case-insensitive.

After cloning, enable the local commit hook once:

```sh
python3 scripts/install-hooks.py
```

The installer preserves existing active hooks and changes only this repository's
Git configuration. Run it again safely to check that installation is current.
If an existing pre-commit hook requires combining, the installer stops without
replacing it.

`.gitignore` prevents ordinary staging of PDFs and solution paths. The
pre-commit hook checks the full Git index and rejects prohibited paths even
after `git add -f`; staging a deletion of a prohibited file is allowed.
It checks filenames, not whether prose or code contains an answer, so review
the question files before publishing.

Hooks are local: new clones need the installation command above. They do not
run for GitHub web uploads, and `git commit --no-verify` bypasses them.
