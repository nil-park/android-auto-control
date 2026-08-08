# CLAUDE.md

## Repository

- Remote: https://github.com/nil-park/android-auto-control
- Scope: the PC-side Python package only. ESP32 firmware lives in a separate repository.

## Required Reading

- [README.md](README.md) — big picture only; don't assume a feature is missing just because it isn't listed there
- [docs/architecture/pipeline.md](docs/architecture/pipeline.md) — component boundaries, coordinate systems, and the PC↔ESP32 serial protocol
- [docs/development/preconditions.md](docs/development/preconditions.md) — what the code is allowed to assume; don't add defensive code for cases ruled out there
- [docs/development/branch-naming.md](docs/development/branch-naming.md)

## Design Constraint

Touch input goes through a BLE HID device, never through adb. Don't propose `adb shell input tap`
or any other adb-based input injection as a substitute.

## Language

- CLAUDE.md, commit messages, and PR titles/descriptions: English.
- Issues and everything under `docs/`: Korean.

## Git Convention

- Branch naming: [docs/development/branch-naming.md](docs/development/branch-naming.md)
- If a PR is linked to an issue, prefix the PR title with the issue number, e.g. `[#40] Add template matching`.

## Formatting

- Python is formatted and linted with ruff, type-checked with pyright (strict), tested with pytest.
  Run `make format` after editing Python.
- Markdown, JSON, and YAML are formatted with Prettier, which `make format` also runs.
- Run `make format` as the last step of a PR so formatting never lands in a separate follow-up.
- Prettier markdown gotcha: a wrapped prose line that begins with `+`, `-`, or `*` is reparsed as a
  list marker. Don't start a continuation line with those, or the formatter will turn it into a
  nested bullet and change the meaning.
