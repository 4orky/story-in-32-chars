# Tell a Whole Story in 32 Characters — make.fun bounty
# u-xvader-tell-a-whole-story-in-32-characters-f86dd978
#
# The program writes one Wi-Fi network name (1-32 characters) to
# /output/entry.txt: the funniest name that hints at a whole story, as a
# stranger would read it in a phone's network list.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a Wi-Fi network name of at most 32 characters that reads as a joke
#      and hints at a story (a plain label or a slogan loses)
#   2. the joke lands on the first read, with a clear twist or punchline
#      a stranger gets without explanation
#   3. it tells a whole story: the name implies a situation, a character
#      and something that happened, so a reader can fill in the rest
#   4. it is fresh: it avoids the stock Wi-Fi jokes everyone has seen
#      ("Pretty Fly for a Wi-Fi", "FBI Surveillance Van", "It Burns When
#      IP", "Abraham Linksys", "The LAN Before Time", "No Free WiFi",
#      "Tell My WiFi Love Her", "Drop It Like It's Hotspot") or turns a
#      familiar one into something new
#   5. it is tight: every character earns its place, and the wording is
#      clean, readable and easy to say out loud
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# REVISION (second pass, on the winning line):
#   First draft winner: "HeTookTheRouterInTheDivorce" (27 chars).
#   Weakness found on re-read: it only *states* the event (a divorce
#   happened, the router was taken). The punchline is the divorce itself,
#   and the reader has to supply the joke.
#   Revised line: "HeTookTheRouterNotTheKids" (25 chars).
#   The ending now *shows the choice*: he walked out with the router and
#   left the kids — the same divorce story, but the twist lands on the
#   first read, it is two characters shorter, and the absurd priority
#   (router over children) is the joke rather than the divorce. The
#   revision keeps the winner's situation, character and event, and
#   sharpens only its punchline.

CANDIDATES = [
    # score: joke 9, story 10, fresh 9, tight 8 = 36
    # Divorce, one man, one router taken. The whole split is in the
    # choice of what he carried out the door.
    ("HeTookTheRouterInTheDivorce",
     36),
    # score: joke 8, story 10, fresh 8, tight 9 = 35
    # Breakup inventory: the router and the dog both went with the ex.
    ("MyExTookTheRouterAndTheDog",
     35),
    # score: joke 8, story 9, fresh 9, tight 9 = 35
    # Cheating story retold as a signal-strength upgrade: left for the
    # neighbour's 5G.
    ("HeLeftMeForThe5GNextDoor",
     35),
    # score: joke 9, story 7, fresh 8, tight 9 = 33
    # The classic breakup line, with the relationship replaced by the
    # connection. Punchy, but the story behind it is thin.
    ("ItsNotYouItsTheConnection",
     33),
    # score: joke 8, story 9, fresh 8, tight 8 = 33
    # Still paying for the ex's Netflix: the breakup ended, the billing
    # did not.
    ("IStillPayForHisNetflixToo",
     33),
    # score: joke 8, story 8, fresh 8, tight 9 = 33
    # A baby, a cable, a dead network: one small bite, one big outage.
    ("TheBabyAteTheRouterCable",
     33),
    # score: joke 8, story 9, fresh 8, tight 7 = 32
    # Exes under one roof: the Wi-Fi is shared, the feelings are not.
    # Long for its punchline.
    ("WeShareWiFiNotFeelingsAnymore",
     32),
    # score: joke 8, story 9, fresh 8, tight 7 = 32
    # It worked until the in-laws arrived. Blame, precisely assigned.
    ("ItWorkedBeforeTheInLawsCame",
     32),
    # score: joke 7, story 9, fresh 8, tight 8 = 32
    # The password is still your birthday: tender, awkward, and a whole
    # unfinished breakup in six words.
    ("PasswordIsStillYourBirthday",
     32),
    # score: joke 7, story 8, fresh 7, tight 9 = 31
    # Grandma unplugged it again: warm, but the joke is gentle and the
    # "again" does most of the work.
    ("GrandmaUnpluggedItAgain",
     31),
    # score: joke 7, story 7, fresh 7, tight 9 = 30
    # The cat sits on the router again: relatable, but every cat owner
    # has already told this story.
    ("MyCatSitsOnTheRouterAgain",
     30),
    # score: joke 6, story 7, fresh 7, tight 8 = 28
    # Dave knows the password: a household IT guy, but no event, no
    # twist — a setup waiting for a punchline.
    ("AskDaveHeKnowsThePassword",
     28),
]

# The winner's second-pass revision, applied deterministically: same
# divorce story, sharper ending (see the REVISION note above).
REVISED_WINNER = "HeTookTheRouterNotTheKids"

# Stock Wi-Fi jokes and worn lines the brief rules out; no candidate
# may contain one.
BANNED_CLICHES = ("pretty fly", "fbi", "it burns when ip",
                   "abraham linksys", "martin router king", "wu-tang lan",
                   "lan before time", "no free wifi", "tell my wifi",
                   "drop it like it", "virus", "connect and die",
                   "password is password", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 32, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert text == text.strip(), "candidate has edge whitespace"
        assert all(32 <= ord(ch) < 127 for ch in text), \
            f"candidate is not printable ASCII: {text!r}"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    winner = pick(CANDIDATES)
    # The revision only ever applies to the drafted winner; if a future
    # edit changed the winner, fail loudly instead of silently revising
    # a different line.
    assert winner == "HeTookTheRouterInTheDivorce", \
        f"unexpected winner, revision does not apply: {winner!r}"
    message = REVISED_WINNER
    assert 1 <= len(message) <= 32, \
        f"revised entry over gate: {len(message)} chars"
    assert message == message.strip() and "\n" not in message
    assert all(32 <= ord(ch) < 127 for ch in message)
    assert not any(c in message.lower() for c in BANNED_CLICHES)
    import os
    import sys
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(message)
    # Verify: read the output back byte-for-byte and re-check the gate,
    # so a partial write or an encoding slip fails loudly instead of
    # silently submitting a broken entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != message:
        print("error: /output/entry.txt does not match the selected message",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(message) <= 32) or "\n" in message or not message.strip():
        print("error: selected message fails the gate (1-32 chars, one line)",
              file=sys.stderr)
        sys.exit(1)
    print(message)


if __name__ == "__main__":
    main()
