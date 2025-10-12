# Changelog
All notable changes to this project are documented here.

### Added
- Initial release.
- Project skeleton, `/ping`, guild/global command sync.
- Rich logging, pre-commit, Ruff, pytest, Makefile.

## v1.0.0 (2025-10-12)

### BREAKING CHANGE

- imports have changed
- adds new dependencies
- commands moved under the /tools namespace (e.g. /wiki
-> /tools wiki)

### Feat

- **tools**: introduce /tools group and port Harbinger utilites and subcommands

### Fix

- **imports**: fix import statements in the wrong places causing precommit fail
- **dice**: change magic value -> MIN_SIDES
- **fun.py**: correctly-import discord.Interaction

## v0.2.1 (2025-10-05)

### Feat

- **about**: improve overall aesthetics of the embed
- **about**: include system platform information in about
- **about**: create command  to see bot version info

### Fix

- **about**: fix broken function call due to missing import (sys)

## v0.2.0 (2025-10-05)

### Feat

- **dice**: add /roll slash command with NdM parser and modifiers

## v0.1.1 (2025-10-05)

### Feat

- **branding**: add official Portent icon & banner; add assets docs

## v0.1.0 (2025-10-05)

### Feat

- clean initial import of Portent (CLI + /ping + tooling)
