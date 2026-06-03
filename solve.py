#!/usr/bin/env python3
import re

# ─── Step 1: Caesar cipher decode (shift 20) ──────────────────────────────────

with open("score.txt") as f:
    raw = f.read()

decoded = ""
for c in raw:
    if c.isalpha():
        base = ord("A") if c.isupper() else ord("a")
        decoded += chr((ord(c) - base - 20) % 26 + base)
    else:
        decoded += c

# ─── Step 2: SPL interpreter ──────────────────────────────────────────────────

# In Shakespeare Programming Language:
#   positive noun = 1,  negative noun = -1
#   each adjective multiplies the value by 2
POSITIVE_NOUNS = {
    "Lord", "King", "Heaven", "angel", "flower", "joy", "plum", "hero",
    "rose", "kingdom", "happiness", "peace",
}
NEGATIVE_NOUNS = {
    "Hell", "devil", "bastard", "villain", "coward", "death", "plague",
    "war", "hatred", "curse", "blot", "toad", "pig", "worm", "lie",
}


def eval_noun_phrase(phrase: str) -> int:
    words = phrase.strip().split()
    noun, adjs = words[-1], words[:-1]
    val = 1 if noun in POSITIVE_NOUNS else (-1 if noun in NEGATIVE_NOUNS else 1)
    for _ in adjs:
        val *= 2
    return val


def split_and(s: str) -> list[str]:
    """Split 'X and Y' at the outermost ' and ', respecting nested 'the sum of'."""
    depth = i = 0
    while i < len(s):
        if s[i:].startswith("the sum of "):
            depth += 1
            i += 11
        elif s[i:].startswith(" and ") and depth == 0:
            return [s[:i], s[i + 5:]]
        elif s[i:].startswith(" and ") and depth > 0:
            depth -= 1
            i += 5
        else:
            i += 1
    return [s]


def eval_expr(expr: str, cur: int) -> int:
    expr = expr.strip()
    if expr.startswith("the sum of "):
        parts = split_and(expr[11:])
        if len(parts) == 2:
            return eval_expr(parts[0], cur) + eval_expr(parts[1], cur)
        return eval_expr(parts[0], cur)
    if expr == "thyself":
        return cur
    if expr.startswith(("a ", "an ")):
        return eval_noun_phrase(expr[expr.index(" ") + 1:])
    return eval_noun_phrase(expr)


def roman(s: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = prev = 0
    for ch in reversed(s):
        v = vals.get(ch, 0)
        result += v if v >= prev else -v
        prev = v
    return result


# Parse all scenes
scene_dict: dict[int, str] = {}
for s in re.split(r"\n {20}Scene ", decoded)[1:]:
    m = re.match(r"([\w]+):\s", s)
    if m:
        scene_dict[roman(m.group(1))] = s[m.end():]


def run_scene(num: int, romeo: int, output: list[int]) -> tuple[int, int]:
    """Execute one scene; return (new_romeo_value, next_scene_number)."""
    content = scene_dict.get(num, "")
    next_scene = num + 1
    for line in content.split("\n"):
        line = line.strip()
        if line == "Thou art nothing!":
            romeo = 0
        elif line.startswith("Thou art the sum of thyself and "):
            romeo += eval_expr(line[32:].rstrip("!"), romeo)
        elif line.startswith("Thou art the sum of ") and "thyself" not in line:
            romeo = eval_expr(line[9:].rstrip("!"), romeo)
        elif line.startswith(("Thou art a ", "Thou art an ")):
            romeo = eval_expr(line[9:].rstrip("!"), romeo)
        elif line in ("Open your mind!", "Speak thy mind!"):
            output.append(romeo)
        elif "proceed to scene" in line and line.startswith("If so"):
            m2 = re.search(r"scene (\w+)", line)
            if m2:
                next_scene = roman(m2.group(1))
            break
        elif line.startswith("Let us proceed to scene"):
            m2 = re.search(r"scene (\w+)", line)
            if m2:
                next_scene = roman(m2.group(1))
            break
    return romeo, next_scene


# Execute the play
romeo, output, current, steps = 0, [], 1, 0
while current in scene_dict and steps < 500:
    romeo, current = run_scene(current, romeo, output)
    steps += 1

plaintext = "".join(chr(v) if v > 0 else " " for v in output)

# ─── Step 3: Leetspeak + underscore spaces ────────────────────────────────────

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "t": "7", "s": "5", "g": "9", "b": "8"}
leet = "".join(LEET.get(c, c) for c in plaintext).replace(" ", "_")

print(f"Decoded play message : {plaintext}")
print(f"Flag                 : THEM?!CTF{{{leet}}}")
