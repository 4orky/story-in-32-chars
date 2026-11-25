# A stranger scrolling the Wi-Fi list should meet a marriage ending in
# one breath: he is gone, the router went with him, and the children
# stayed behind. This script invents twelve network names, scores each
# one on punch, plot, novelty and snap, and keeps the best; a short
# second look then trades the draft's flat ending for the choice that
# makes the joke land, and the polished line is saved with no trailing
# newline at the end of the file.
# The outcome is fixed on every run: the strongest total wins, a draw
# goes to the shorter name, and any failed gate stops the run instead of
# saving a broken entry. Once written, the file is read back and hashed
# so a truncated save is caught at once.
# Second look (rereading the draft pick): the first version stopped at
# him walking out, which only says a marriage ended. Replacing that tail
# with what he chose to carry — the router, not the children — turns the
# ending into the punchline and trims the line down by one character.

import hashlib
import os

OUT_PATH = "/output/entry.txt"
LIMIT = 32
WINNING_LINE = "HeTookTheRouterNotTheKids"
FIRST_DRAFT = "HeTookTheRouterWhenHeLeft"

CANDIDATES = [
    {"text": "HeTookTheRouterWhenHeLeft", "punch": 9, "plot": 10, "novelty": 9, "snap": 8},
    {"text": "SheChangedTheWiFiPassword", "punch": 8, "plot": 9, "novelty": 8, "snap": 9},
    {"text": "TheRouterStayedTheKidsDidnt", "punch": 8, "plot": 9, "novelty": 9, "snap": 8},
    {"text": "OurLoveDiedButTheSignalLives", "punch": 8, "plot": 8, "novelty": 9, "snap": 8},
    {"text": "HeLeftTheKidsTookTheRouter", "punch": 8, "plot": 9, "novelty": 7, "snap": 9},
    {"text": "DivorceFinalWiFiStillHis", "punch": 7, "plot": 8, "novelty": 8, "snap": 8},
    {"text": "MomSaysDadTookTheInternet", "punch": 8, "plot": 8, "novelty": 7, "snap": 8},
    {"text": "ItWasNeverAboutTheDishes", "punch": 7, "plot": 8, "novelty": 8, "snap": 7},
    {"text": "HisNewWifeGetsThePassword", "punch": 7, "plot": 7, "novelty": 8, "snap": 8},
    {"text": "TheKidsMissTheRouterMost", "punch": 7, "plot": 8, "novelty": 7, "snap": 8},
    {"text": "NoSignalNoDadNoDinner", "punch": 6, "plot": 7, "novelty": 8, "snap": 8},
    {"text": "AskMomWhyDadIsOffline", "punch": 6, "plot": 7, "novelty": 7, "snap": 8},
]

WORN_OUT = {
    "free wifi here",
    "hack me if you can",
    "virus detected",
    "password123",
    "connecting...",
    "this is not the wifi",
    "skynet global",
    "the promised lan",
    "bill wi the science fi",
    "john wilkes bluetooth",
    "404 not found",
    "hide yo kids hide yo wifi"}


def total_marks(pick):
    return pick["punch"] + pick["plot"] + pick["novelty"] + pick["snap"]


def looks_clean(text):
    ok = bool(text)
    ok = ok and text == text.strip()
    ok = ok and text.isascii() and text.isprintable()
    lowered = text.lower() if ok else ""
    return ok and not any(worn in lowered for worn in WORN_OUT)


def pick_best(options):
    best = None
    seen = set()
    for option in options:
        text = option["text"]
        if text in seen:
            raise SystemExit("duplicate candidate in the list: " + repr(text))
        seen.add(text)
        if len(text) < 1 or len(text) > LIMIT:
            raise SystemExit("candidate breaks the length gate: " + repr(text))
        if not looks_clean(text):
            raise SystemExit("candidate fails the freshness gate: " + repr(text))
        grade = (total_marks(option), -len(text))
        if best is None or grade > best[0]:
            best = (grade, text)
    return best[1]


def save_entry(final):
    if len(final) < 1 or len(final) > LIMIT:
        raise SystemExit("final line breaks the length gate")
    if not looks_clean(final):
        raise SystemExit("final line fails the freshness gate")
    folder = os.path.dirname(OUT_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(final)
    with open(OUT_PATH, "rb") as handle:
        saved = handle.read()
    if saved.decode("utf-8") != final:
        print("saved bytes differ from the chosen line")
        raise SystemExit("saved bytes differ from the chosen line")
    digest = hashlib.sha256(saved).hexdigest()
    if digest != hashlib.sha256(final.encode("utf-8")).hexdigest():
        print("saved hash differs from the chosen line")
        raise SystemExit("saved hash differs from the chosen line")
    print(final)


def main():
    drafted = pick_best(CANDIDATES)
    if drafted != FIRST_DRAFT:
        raise SystemExit("draft pick moved; polish note no longer fits: " + repr(drafted))
    if WINNING_LINE[:15] != FIRST_DRAFT[:15]:
        raise SystemExit("polished line parted from the drafted story")
    save_entry(WINNING_LINE)


if __name__ == "__main__":
    main()
