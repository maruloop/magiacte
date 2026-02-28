"""Interference resolution for MAGIACTE.

Algorithm (both directions computed simultaneously):

  ED = A_attacker - C_defender

  ED > 0  (attack hits)   : defender.hp -= ED
                             defender.field_mana += ED   (scatter)
  ED < 0  (counter)       : defender.field_mana += |ED| * SIPHON_EFF
  ED == 0 (perfect cancel): defender.field_mana += PERFECT_CANCEL_BONUS

When a player Passes (kind == "pass"), their attack direction is skipped
so the opponent resolves freely against C=0.
"""
from dataclasses import dataclass, field
from typing import List

from .player import Player
from .spells import Spell

SIPHON_EFF           = 0.70   # counter siphon efficiency (anti-turtling)
PERFECT_CANCEL_BONUS = 2      # field mana bonus for perfect cancel


@dataclass
class CombatResult:
    log: List[str] = field(default_factory=list)


def resolve(p1: Player, spell1: Spell, p2: Player, spell2: Spell) -> CombatResult:
    """Resolve one cycle of combat between p1 and p2."""
    result = CombatResult()
    log = result.log

    log.append(f"  {p1.name:<16} {spell1.name:<14} A:{spell1.attack}  C:{spell1.counter}")
    log.append(f"  {p2.name:<16} {spell2.name:<14} A:{spell2.attack}  C:{spell2.counter}")
    log.append("")

    # Pre-compute both EDs before mutating state (simultaneous resolution)
    ed_12 = spell1.attack - spell2.counter  # P1 → P2
    ed_21 = spell2.attack - spell1.counter  # P2 → P1

    if spell1.kind != "pass":
        _apply(ed_12, p1, p2, log)
    if spell2.kind != "pass":
        _apply(ed_21, p2, p1, log)

    return result


def _apply(ed: int, attacker: Player, defender: Player, log: List[str]) -> None:
    tag = f"[{attacker.name}→{defender.name}]"
    if ed > 0:
        defender.hp -= ed
        defender.field_mana = round(defender.field_mana + ed, 2)
        log.append(
            f"  {tag} ED={ed:+d}  HIT!           "
            f"-{ed} HP  +{ed} field → {defender.name}"
        )
    elif ed < 0:
        siphon = round(abs(ed) * SIPHON_EFF, 2)
        defender.field_mana = round(defender.field_mana + siphon, 2)
        log.append(
            f"  {tag} ED={ed:+d}  COUNTER!       "
            f"+{siphon:.1f} field → {defender.name}"
        )
    else:
        defender.field_mana = round(defender.field_mana + PERFECT_CANCEL_BONUS, 2)
        log.append(
            f"  {tag} ED= 0   PERFECT CANCEL! "
            f"+{PERFECT_CANCEL_BONUS} field → {defender.name}"
        )
