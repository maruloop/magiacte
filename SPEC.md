# MAGIACTE — Current Specification

## 1. Game Concept

* Genre: Magical interference battle game
* Core Themes:

  * Creation
  * Interference
  * Cancellation (Counter)
  * Mana circulation
* Title: **MAGIACTE**
* Tone: Chuunibyou / Arcane / Competitive-ready

---

## 2. Core Loop (Cycle-Based Resolution)

Each cycle (tentatively 10 seconds):

1. Players select or activate a spell
2. Compare Attack (A) and Counter (C)
3. Apply differential resolution
4. Apply damage / siphon / mana scatter
5. Field mana decay
6. Self mana regeneration

---

## 3. Resource System

### Self Mana (Private Mana)

* Owned individually by each player
* Used to pay spell costs
* Regenerates each cycle (tentative: +3)

### Field Mana

* Split into Left (P1 side) and Right (P2 side)
* When attack succeeds → scatter mana to opponent's field side
* When counter succeeds → siphon mana to own field side
* Decays each cycle (tentative: -20%)

---

## 4. Spell Parameters

Each spell has:

* Cost
* Attack Value (A)
* Counter Value (C)

---

## 5. Resolution Algorithm (Tentative)

For Player 1 attacking Player 2:

Effective Damage = A1 - C2

If Effective Damage > 0:

* Deal that amount as HP damage
* Scatter same amount to opponent's field mana

If Effective Damage < 0:

* Siphon |value| mana to defender's field side

If Effective Damage = 0:

* Perfect cancellation bonus (e.g., +1 siphon)

Both sides are calculated simultaneously.

---

## 6. Anti-Turtling Measures (Prevent "Wait is OP")

* Counter siphon is not 100% efficient (e.g., 70%)
* Field mana decays each cycle
* Successful attack grants small self-mana bonus

---

## 7. Future Input Systems (Not in CUI Prototype)

* Grimoire (Book)
* Vox (Voice casting)
* Sigil (Drawing-based creation)
* Arca (Card instant spells)

---

# TODO LIST

## Phase 1: CUI Prototype

* [ ] Define player structure
* [ ] Define 6 prototype spells
* [ ] Implement cycle processing
* [ ] Implement interference (A/C differential logic)
* [ ] Implement field mana scatter
* [ ] Implement counter siphon
* [ ] Implement field mana decay
* [ ] Implement self mana regeneration
* [ ] Implement battle log output
* [ ] Implement win condition (HP <= 0)

---

## Phase 2: Balance Validation

* [ ] Decide A/C range (1–5 recommended)
* [ ] Tune cost vs A/C ratio
* [ ] Tune siphon multiplier
* [ ] Tune decay rate
* [ ] Tune regen amount
* [ ] Test anti-turtle effectiveness

---

## Phase 3: UI Prototype

* [ ] Mana bar UI
* [ ] Field left/right display
* [ ] Cycle countdown display
* [ ] Counter effect animation
* [ ] Damage animation

---

## Phase 4: Input System Expansion

* [ ] Card slot implementation
* [ ] Fast input system (temporary Spell placeholder)
* [ ] Drawing system (Sigil)
* [ ] Shape feature extraction logic
* [ ] Deterministic parameter conversion

---

## Phase 5: Online (Later)

* [ ] Sync logic
* [ ] Cycle latency compensation
* [ ] Matchmaking
* [ ] Replay system

---

# Current Decisions

* Title fixed: MAGIACTE
* Cycle-based resolution system
* Dual-axis Attack/Counter interference model
* Attack → future advantage (opponent field mana)
* Counter → present advantage (self field mana)
* Start with CUI prototype
