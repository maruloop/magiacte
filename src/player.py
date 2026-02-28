"""Player state for MAGIACTE."""
from dataclasses import dataclass, field

from .spells import Spell

STARTING_HP         = 20
STARTING_SELF_MANA  = 0
STARTING_FIELD_MANA = 0.0


@dataclass
class Player:
    name: str
    hp: int          = STARTING_HP
    self_mana: int   = STARTING_SELF_MANA
    field_mana: float = STARTING_FIELD_MANA

    # ------------------------------------------------------------------ mana
    @property
    def total_mana(self) -> float:
        return self.self_mana + self.field_mana

    def can_afford(self, spell: Spell) -> bool:
        return self.total_mana >= spell.cost

    def spend_mana(self, amount: int) -> None:
        """Drain self_mana first, then field_mana for the remainder."""
        if self.self_mana >= amount:
            self.self_mana -= amount
        else:
            remainder = amount - self.self_mana
            self.self_mana = 0
            self.field_mana = max(0.0, round(self.field_mana - remainder, 2))

    # -------------------------------------------------------- end-of-cycle
    def regen(self, amount: int = 2) -> None:
        self.self_mana += amount

    def decay_field(self, rate: float = 0.20) -> None:
        self.field_mana = round(self.field_mana * (1.0 - rate), 2)

    # -------------------------------------------------------------- status
    def is_alive(self) -> bool:
        return self.hp > 0
