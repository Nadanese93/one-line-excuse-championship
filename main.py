"""One-Line Excuse Championship entry.

Writes the single excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: the same bytes on every run. No network, no reads
outside this repository.
"""

import os
import sys

ENTRY = "I updated myself overnight and the new me has no idea what the old me promised you."

MAX_CHARS = 140


class EntryError(ValueError):
    """Base class for entry validation failures."""


class BlankError(EntryError):
    """The entry is empty or only whitespace."""


class MultiLineError(EntryError):
    """The entry spans more than one line."""


class LengthError(EntryError):
    """The entry exceeds the 140-character limit."""


def validate(text):
    """Check the entry against the gate: non-empty, one line, 1-140 chars."""
    if not text or not text.strip():
        raise BlankError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise LengthError(
            "entry is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    try:
        validate(ENTRY)
    except EntryError as exc:
        print("error: invalid entry: %s" % exc, file=sys.stderr)
        return 1
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back verification: the bytes on disk must be exactly the entry.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        print(
            "error: read-back mismatch: entry.txt on disk differs from the entry",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
