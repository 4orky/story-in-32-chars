# One Wi-Fi network name, at most 32 characters, that makes a stranger
# smile in a phone's network list and leaves them picturing the whole
# breakup behind it. The script below drafts a dozen such names, grades
# each one on four craft marks, and keeps the strongest; a short polish
# note then sharpens the winning line's ending before the entry is saved.
# The pick never changes between runs: equal grades fall to the shorter
# name, and every gate below fails loudly instead of writing a bad entry.
# The chosen line is written with no trailing newline to /output/entry.txt,
# then read back and checksummed so a short write cannot slip through.
# A second read of the draft winner follows below.
# Polish note (second read of the draft winner): the first draft ended on
# the divorce itself, which only reports what happened. Swapping the tail
# for the choice he made instead — router kept, kids left behind — turns
# the ending into the joke, and the line comes out two characters shorter.

from pathlib import Path
import sys
import zlib

DESTINATION = Path("/output/entry.txt")
CEILING = 32
REVISED_WINNER = "HeTookTheRouterNotTheKids"
DRAFTED = "HeTookTheRouterInTheDivorce"

ENTRIES = [
    {"line": "HeTookTheRouterInTheDivorce", "joke": 9, "story": 10, "fresh": 9, "tight": 8},
    {"line": "MyExTookTheRouterAndTheDog", "joke": 8, "story": 10, "fresh": 8, "tight": 9},
    {"line": "HeLeftMeForThe5GNextDoor", "joke": 8, "story": 9, "fresh": 9, "tight": 9},
    {"line": "ItsNotYouItsTheConnection", "joke": 9, "story": 7, "fresh": 8, "tight": 9},
    {"line": "IStillPayForHisNetflixToo", "joke": 8, "story": 9, "fresh": 8, "tight": 8},
    {"line": "TheBabyAteTheRouterCable", "joke": 8, "story": 8, "fresh": 8, "tight": 9},
    {"line": "WeShareWiFiNotFeelingsAnymore", "joke": 8, "story": 9, "fresh": 8, "tight": 7},
    {"line": "ItWorkedBeforeTheInLawsCame", "joke": 8, "story": 9, "fresh": 8, "tight": 7},
    {"line": "PasswordIsStillYourBirthday", "joke": 7, "story": 9, "fresh": 8, "tight": 8},
    {"line": "GrandmaUnpluggedItAgain", "joke": 7, "story": 8, "fresh": 7, "tight": 9},
    {"line": "MyCatSitsOnTheRouterAgain", "joke": 7, "story": 7, "fresh": 7, "tight": 9},
    {"line": "AskDaveHeKnowsThePassword", "joke": 6, "story": 7, "fresh": 7, "tight": 8}]

TIRED_TROPES = {
    "pretty fly",
    "fbi",
    "it burns when ip",
    "abraham linksys",
    "martin router king",
    "wu-tang lan",
    "lan before time",
    "no free wifi",
    "tell my wifi",
    "drop it like it",
    "virus",
    "connect and die",
    "password is password",
    "as an ai",
}


def _marks_total(entry):
    return entry["joke"] + entry["story"] + entry["fresh"] + entry["tight"]


def _is_clean(line):
    if not line or line != line.strip():
        return False
    if not all(32 <= ord(ch) < 127 for ch in line):
        return False
    folded = line.lower()
    return not any(trope in folded for trope in TIRED_TROPES)


def _choose(entries):
    ranked = None
    for entry in entries:
        line = entry["line"]
        if len(line) < 1 or len(line) > CEILING:
            raise SystemExit(f"entry breaks the length gate: {line!r}")
        if not _is_clean(line):
            raise SystemExit(f"entry fails the cleanliness gate: {line!r}")
        grade = (_marks_total(entry), -len(line))
        if ranked is None or grade > ranked[0]:
            ranked = (grade, line)
    return ranked[1]


def _emit(final):
    if len(final) < 1 or len(final) > CEILING:
        raise SystemExit("final entry breaks the length gate")
    if not _is_clean(final):
        raise SystemExit("final entry fails the cleanliness gate")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(final, encoding="utf-8")
    back = DESTINATION.read_bytes()
    if back.decode("utf-8") != final:
        print("mismatch: entry file differs from the chosen line", file=sys.stderr)
        raise SystemExit(1)
    if zlib.crc32(back) != zlib.crc32(final.encode("utf-8")):
        print("mismatch: entry file checksum differs from the chosen line", file=sys.stderr)
        raise SystemExit(1)
    sys.stdout.write(final + "\n")


def run_entry():
    picked = _choose(ENTRIES)
    if picked != DRAFTED:
        raise SystemExit(f"draft pick moved; polish note no longer fits: {picked!r}")
    if not REVISED_WINNER.startswith(picked[:15]):
        raise SystemExit("polished line drifted away from the drafted story")
    _emit(REVISED_WINNER)


if __name__ in {"__main__"}:
    run_entry()
