# MAGIACTE — Terminology Reference

---

## Core Mechanics

**Attack Value (A)**
Offensive parameter of a spell. Compared against the opponent's Counter Value to determine Effective Damage. Range: 0–5 in the prototype.

**Counter Value (C)**
Defensive parameter of a spell. Compared against the opponent's Attack Value to determine Effective Damage. Range: 0–5 in the prototype.

**Cost**
Mana required to cast a spell. Paid from Self Mana first, then Field Mana as overflow.

**Cycle**
The fundamental unit of game time (tentatively 10 seconds). Each cycle: mana regenerates → spells are selected → mana is spent → interference resolves → field mana decays → win condition is checked.

**Effective Damage (ED)**
`ED = A_attacker − C_defender`. Positive → HIT. Negative → COUNTER. Zero → PERFECT CANCEL.

**HIT**
Outcome when ED > 0. Deals ED as HP damage to the defender and scatters ED to the defender's Field Mana.

**COUNTER**
Outcome when ED < 0. Siphons |ED| × 70% to the defender's Field Mana (anti-turtling penalty).

**PERFECT CANCEL**
Outcome when ED = 0. Grants +2 Field Mana to the defender. Requires Attack Value of one spell to equal Counter Value of the opposing spell.

---

## Mana

**Self Mana**
Private mana owned by each player. Regenerates +2 per cycle. Spent first when casting.

**Field Mana**
Shared positional resource, split into Left (P1 side) and Right (P2 side). Accumulates from scatter/siphon. Decays −20% per cycle. Spent as overflow when Self Mana is insufficient.

**Mana Scatter**
Field Mana transferred to the opponent's side as a result of a HIT.

**Siphon**
Field Mana transferred to the defender's own side as a result of a COUNTER (at 70% efficiency).

---

## Casting Systems

> ⚠️ **Inconsistency note:** The four input systems are named differently across documents.
> SPEC.md §7 and PROTOTYPE.md list: **Grimoire, Vox, Sigil, Arca**.
> CIVILIZATION.md lists: **Card, Grimoire, Vox (Chant), Rod** — omitting Sigil and using "Card" instead of "Arca".
> Rod is absent from SPEC.md's list. These need to be reconciled.

**Card** *(also called Arca in SPEC.md and PROTOTYPE.md)*
Instant activation casting system. Compact format. Small cost ceiling.

**Grimoire**
Book-based casting system. Structured and stable. Medium cost ceiling.

**Vox** *(also called Chant in CIVILIZATION.md)*
Voice-based casting system. Skill-based compression. Medium–High cost ceiling.

**Sigil**
Drawing-based creation system. Spell parameters are derived via shape feature extraction. Listed in SPEC.md and PROTOTYPE.md; absent from CIVILIZATION.md.

**Rod**
Creation and research casting system. No inherent cost ceiling. Used to invent new spells (TheOrigin). Not listed in SPEC.md's input systems section.

---

## Spell Lifecycle

**TheOrigin**
Stage 1 of a spell's lifecycle. Created via Rod. Usable only by the creator.

**Replica**
Stage 2. The spell is tradable via the marketplace. Usable by buyers.

**Common (World Imprinted)**
Stage 3. The spell becomes part of the world system. Usable by all casting systems within their respective cost ceilings. Performance is identical to earlier stages; differences are cosmetic.

---

## Civilization Systems

**Marketplace**
The trading layer where Rod-created spells (as Replicas) are bought and sold.

**World Imprint**
Process by which a widely-used spell is absorbed into the world system, enabling cross-system usage and structural standardization.

**Parts**
Abstract structural components extracted from an imprinted spell (e.g., Core structure, Modifier, Trigger, Propagation pattern). Parts become combinable by other designers.

**Era**
A global environmental state declared by the Game Master. Limited duration, announced in advance. Modifies casting efficiency, spell cost, or interference behavior across the entire meta.

**Erosion**
The forgetting system. Spells degrade across Eras:
`Active → Fading (Cost +1) → Forgotten (further restrictions)`
After roughly three Eras a spell may become unusable outside Rod reconstruction.

---

## Spell Classification

**Attack Spell**
A spell where A > C. Optimized for dealing HP damage.

**Defence Spell**
A spell where C > A. Optimized for countering and siphoning Field Mana.

**Pass**
A no-op action. The passing player's Attack direction uses A = 0 and C = 0, leaving them fully exposed to the opponent's attack.
