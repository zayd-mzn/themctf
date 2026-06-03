# Some Play's Libretto — MISC

**Flag:** `THEM?!CTF{5h4k35p34r3_fr0m_73mu8r0_m19h7_4c7u4lly_83_5h4k35p34r3}`

---

## Challenge Description

> Convert to leetspeak before submitting flag  
> Example: `THEM?!CTF{50m3_pl41n73x7_6035_h3r3}`  
> File: `score.txt`

We're given a single file called `score.txt` and told the flag needs to be converted to leetspeak. Opening the file reveals a wall of garbled text that looks like a play script — but nothing is readable.

---

## Step 1 — Caesar Cipher

The first few characters of `score.txt`:

```
Nby Ulcnbgyncw Nluayxs iz nby Vulx'm Mywlyn.

Ligyi, u guh iz fynnylm uhx bcxxyh nlonbm.
Dofcyn, u eyyjyl iz hogylcwuf gsmnylcym.
```

The structure looks like a play (character names, stage directions) but every word is garbled. This is a classic Caesar cipher. Trying all 26 shifts, shift **20** produces readable English:

```
The Arithmetic Tragedy of the Bard's Secret.

Romeo, a man of letters and hidden truths.
Juliet, a keeper of numerical mysteries.
```

The title is the first hint: *"The Arithmetic Tragedy"* — this isn't just a play, it's a **program**.

```python
decoded = ""
for c in raw:
    if c.isalpha():
        base = ord("A") if c.isupper() else ord("a")
        decoded += chr((ord(c) - base - 20) % 26 + base)
    else:
        decoded += c
```

---

## Step 2 — Shakespeare Programming Language (SPL)

Once decoded, the play has two characters — **Romeo** and **Juliet** — going through 24 scenes with lines like:

```
Juliet:
Thou art nothing!
Thou art the sum of a happy sweet warm proud brave honest rose and the sum of a
mighty loving bold good gentle flower and a noble lovely rich sunny kingdom!
Thou art the sum of thyself and the sum of a golden Lord and a plum!

Romeo:
Open your mind!
```

This is [Shakespeare Programming Language (SPL)](http://shakespearelang.sourceforge.net/), an esoteric programming language where programs are written as Shakespearean plays. The key rules are:

| Construct | Meaning |
|---|---|
| `Thou art nothing!` | Set the listener's value to **0** |
| `Thou art the sum of X and Y` | Set listener = X + Y |
| `Thou art the sum of thyself and X` | listener += X |
| `Open your mind!` / `Speak thy mind!` | Print `chr(listener)` |
| `If so, let us proceed to scene N` | Conditional jump |
| `Let us proceed to scene N` | Unconditional jump |
| Positive noun (rose, kingdom, Lord…) | **+1** |
| Negative noun (devil, plague, war…) | **-1** |
| Each adjective (happy, golden, brave…) | **×2** the noun's value |

So a phrase like `a happy sweet warm proud brave honest rose` evaluates as:

```
rose = 1
honest rose     → 1 × 2 = 2
brave ...       → 2 × 2 = 4
proud ...       → 4 × 2 = 8
warm  ...       → 8 × 2 = 16
sweet ...       → 16 × 2 = 32
happy ...       → 32 × 2 = 64
```

The play's structure is:

- **Scenes I–XXI**: Juliet assigns a value to Romeo, Romeo outputs it with `Open your mind!`, then Juliet checks `Am I as good as thee?` — if the output was a valid character the play continues, otherwise it jumps to Scene XXII (dead end → Scene XXIV, exit).
- **Scene XXII**: The "unworthy" branch — unconditionally jumps to Scene XXIV (end).
- **Scene XXIII**: The "revelation" — a long sequence of `Thou art nothing! ... Speak thy mind!` blocks outputting the rest of the message.
- **Scene XXIV**: Exeunt.

Each scene in the first act outputs one ASCII character. Running the full interpreter gives:

| Scenes | Output |
|---|---|
| I – XI | `shakespeare` |
| XII | ` ` (space, value 32) |
| XIII – XVI | `from` |
| XVII | ` ` |
| XVIII – XXI | `temu` |
| XXIII | `bro might actually be shakespeare` |

Full decoded message:

```
shakespeare from temubro might actually be shakespeare
```

---

## Step 3 — Leetspeak Conversion

The challenge tells us to convert the flag to leetspeak before wrapping it. Standard leet substitutions:

| Letter | Leet |
|---|---|
| a | 4 |
| e | 3 |
| i | 1 |
| o | 0 |
| t | 7 |
| s | 5 |
| g | 9 |
| b | 8 |

Spaces become underscores per the example format.

```
shakespeare from temubro might actually be shakespeare
        ↓
5h4k35p34r3_fr0m_73mu8r0_m19h7_4c7u4lly_83_5h4k35p34r3
```

---

## Flag

```
THEM?!CTF{5h4k35p34r3_fr0m_73mu8r0_m19h7_4c7u4lly_83_5h4k35p34r3}
```
