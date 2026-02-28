"""Prototype spell definitions for MAGIACTE.

Rules:
  Attack spells : A > C
  Defence spells: A < C
  A/C range     : 1-5
  Cost range    : 1-4

Perfect-cancel pairs (A of attack == C of matching defence):
  Swift Strike (A:2) <-> Dodge       (C:2)
  Fireball     (A:4) <-> Iron Wall   (C:4)
  Thunder Bolt (A:5) <-> Mirror Field(C:5)
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Spell:
    name: str
    attack: int   # A — offensive power
    counter: int  # C — defensive power
    cost: int
    kind: str     # "attack" | "defence" | "pass"


# 3 attack spells (A > C)
SWIFT_STRIKE  = Spell("Swift Strike",  attack=2, counter=1, cost=1, kind="attack")
FIREBALL      = Spell("Fireball",      attack=4, counter=1, cost=3, kind="attack")
THUNDER_BOLT  = Spell("Thunder Bolt",  attack=5, counter=2, cost=4, kind="attack")

# 3 defence spells (A < C)
DODGE         = Spell("Dodge",         attack=1, counter=2, cost=1, kind="defence")
IRON_WALL     = Spell("Iron Wall",     attack=1, counter=4, cost=2, kind="defence")
MIRROR_FIELD  = Spell("Mirror Field",  attack=2, counter=5, cost=3, kind="defence")

# Special: cost-free no-op
PASS          = Spell("Pass",          attack=0, counter=0, cost=0, kind="pass")

SPELLS: List[Spell] = [
    SWIFT_STRIKE,
    FIREBALL,
    THUNDER_BOLT,
    DODGE,
    IRON_WALL,
    MIRROR_FIELD,
]
