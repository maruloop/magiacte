# MAGIACTE — Prototype Spec (Phase 1 & 2)

## Overview

A two-player, turn-based CUI battle game built to validate the core
interference mechanics before moving to a graphical UI.

---

## How to Run

```bash
python main.py
```

Requires Python 3.11+. No external runtime dependencies.

To run balance tests:

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Starting HP | 20 | Win when opponent reaches ≤ 0 |
| Starting self mana | 0 | |
| Starting field mana | 0 | |
| Self mana regen | +2 / cycle | Applied at **start** of each cycle |
| Field mana decay | −20% / cycle | Applied at **end** of each cycle |
| Counter siphon efficiency | 70% | Anti-turtling measure |
| Perfect cancel bonus | +2 field mana | Goes to the **defender** |
| Mana spending order | Self → Field | Field mana supplements when self is short |

---

## Spell Sheet

| # | Name | A | C | Cost | Kind |
|---|------|---|---|------|------|
| 1 | Swift Strike | 2 | 1 | 1 | attack |
| 2 | Fireball | 4 | 1 | 3 | attack |
| 3 | Thunder Bolt | 5 | 2 | 4 | attack |
| 4 | Dodge | 1 | 2 | 1 | defence |
| 5 | Iron Wall | 1 | 4 | 2 | defence |
| 6 | Mirror Field | 2 | 5 | 3 | defence |
| 0 | Pass | 0 | 0 | 0 | — |

**Rules:**
- Attack spells: A > C
- Defence spells: C > A
- A and C are in the range 1–5

**Perfect-cancel pairs** (A of attack == C of matching defence):

| Attack | Defence | Shared A/C |
|--------|---------|------------|
| Swift Strike | Dodge | 2 |
| Fireball | Iron Wall | 4 |
| Thunder Bolt | Mirror Field | 5 |

---

## Resolution Algorithm

Both sides are resolved **simultaneously** — EDs are computed before any
state is mutated.

```
ED = A_attacker − C_defender

ED > 0  → HIT
           defender.hp       -= ED
           defender.field    += ED          (scatter)

ED < 0  → COUNTER
           defender.field    += |ED| × 0.70  (siphon, 70% efficient)

ED = 0  → PERFECT CANCEL
           defender.field    += 2            (bonus to defender)
```

**Pass** skips the caster's attack direction. The opponent still resolves
their attack against C = 0 (full exposure).

---

## Cycle Order

```
1. Self mana regeneration  (+2 to each player)
2. Spell selection         (P1 picks, then P2 picks — sequential CUI)
3. Mana spent              (self mana first, field mana as overflow)
4. Interference resolved   (both directions simultaneously)
5. Field mana decay        (×0.80 for each player)
6. Win condition check     (HP ≤ 0)
```

---

## Sample Battle Log

```
========================================================
  MAGIACTE   —   Cycle 3
========================================================
  Magi              HP: 16  Self:  4  Field:  1.28
  Arcas             HP: 18  Self:  4  Field:  2.56
========================================================

  [Magi]   available mana: 5.28
  #   Name            A   C  Cost  Kind
  --------------------------------------------
  1   Swift Strike    2   1     1  attack
  2   Fireball        4   1     3  attack
  3   Thunder Bolt    5   2     4  attack
  4   Dodge           1   2     1  defence
  5   Iron Wall       1   4     2  defence
  6   Mirror Field    2   5     3  defence
  0   Pass            0   0     0  pass

  Magi › 2

  [Arcas]  available mana: 6.56
  Arcas › 5

--------------------------------------------------------
  COMBAT RESOLUTION
--------------------------------------------------------
  Magi             Fireball        A:4  C:1
  Arcas            Iron Wall       A:1  C:4

  [Magi→Arcas] ED= 0   PERFECT CANCEL! +2 field → Arcas
  [Arcas→Magi] ED= 0   PERFECT CANCEL! +2 field → Magi
--------------------------------------------------------
  [Decay -20%]  Magi field:  2.00 → 1.60  |  Arcas field:  4.56 → 3.65
```

---

## Known Prototype Limitations

- Input is sequential (P1 visible to P2). Blind simultaneous input is a
  Phase 3+ concern (requires a UI layer).
- No AI opponent — strictly 2-player local.
- Fractional field mana is displayed but spell costs are integers; a
  player with 0.9 field mana and 0 self mana cannot afford a cost-1 spell
  (total_mana check uses float comparison ≥ cost).
- No draw-by-stalemate detection (infinite pass loops are theoretically
  possible but self-correcting due to field decay + no regen benefit).

---

## Out of Scope for Prototype

- Grimoire / Chant / Sigil / Arcana input systems (Phase 4)
- Graphical UI, animations (Phase 3)
- Online sync, matchmaking (Phase 5)
- Self mana bonus on successful attack (deferred — set to 0 for now)
