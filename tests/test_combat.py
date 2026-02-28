"""Phase 2: Balance validation tests for MAGIACTE.

Covers:
  - Differential resolution (hit / counter / perfect cancel)
  - Siphon efficiency (70%)
  - Perfect cancel bonus (+2)
  - Pass mechanics
  - Win condition
  - Resource system (regen, decay, spend)
  - Spell sheet constraints (A/C range, attack > C, defence C > A)
"""
import pytest

from src.combat import (
    PERFECT_CANCEL_BONUS,
    SIPHON_EFF,
    resolve,
)
from src.player import Player
from src.spells import (
    DODGE,
    FIREBALL,
    IRON_WALL,
    MIRROR_FIELD,
    PASS,
    SPELLS,
    SWIFT_STRIKE,
    THUNDER_BOLT,
)


def fresh() -> tuple[Player, Player]:
    return Player("P1"), Player("P2")


# ======================================================================
# Differential resolution
# ======================================================================

class TestResolutionHit:
    def test_simple_hit_deals_damage(self):
        """Fireball (A:4) vs Dodge (C:2) — ED=+2, P2 takes 2 HP."""
        p1, p2 = fresh()
        resolve(p1, FIREBALL, p2, DODGE)
        # P1→P2: 4-2=2 hit
        assert p2.hp == 18
        # Scatter: P2 field += 2
        assert p2.field_mana == pytest.approx(2.0)

    def test_hit_does_not_damage_attacker(self):
        p1, p2 = fresh()
        resolve(p1, FIREBALL, p2, DODGE)
        # P2→P1: 1-1=0, perfect cancel
        assert p1.hp == 20

    def test_mutual_hit(self):
        """Both attack spells → both take damage."""
        p1, p2 = fresh()
        # Swift Strike (A:2,C:1) vs Swift Strike (A:2,C:1)
        resolve(p1, SWIFT_STRIKE, p2, SWIFT_STRIKE)
        # P1→P2: 2-1=1; P2→P1: 2-1=1
        assert p1.hp == 19
        assert p2.hp == 19


class TestResolutionCounter:
    def test_counter_siphon_efficiency(self):
        """Counter siphon is 70% — Iron Wall (C:4) vs Fireball (A:4) = 0 cancel,
        but use Mirror Field (C:5) vs Fireball (A:4): ED = 4-5 = -1."""
        p1, p2 = fresh()
        # P1 casts Fireball (A:4, C:1), P2 casts Mirror Field (A:2, C:5)
        # P1→P2: 4-5=-1 counter → P2 siphons 1*0.7=0.7
        # P2→P1: 2-1=+1 hit     → P1 takes 1 HP, P1 field +=1
        resolve(p1, FIREBALL, p2, MIRROR_FIELD)
        assert p2.field_mana == pytest.approx(0.7)
        assert p1.hp == 19
        assert p1.field_mana == pytest.approx(1.0)

    def test_large_counter(self):
        """Thunder Bolt (A:5) vs Iron Wall (C:4): ED = 5-4 = +1 (hit, not counter).
        Test a clear counter: Swift Strike (A:2) vs Iron Wall (C:4): ED = 2-4 = -2."""
        p1, p2 = fresh()
        # P1→P2: 2-4=-2 counter → P2 siphons 2*0.7=1.4
        # P2→P1: 1-1=0 perfect cancel → P1 field +=2
        resolve(p1, SWIFT_STRIKE, p2, IRON_WALL)
        assert p2.field_mana == pytest.approx(1.4)
        assert p1.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))
        assert p1.hp == 20
        assert p2.hp == 20


class TestPerfectCancel:
    def test_swift_vs_dodge_both_cancel(self):
        """Swift Strike (A:2) vs Dodge (C:2) → ED=0 each direction."""
        p1, p2 = fresh()
        resolve(p1, SWIFT_STRIKE, p2, DODGE)
        # P1→P2: 2-2=0 → P2 gets +2 field
        # P2→P1: 1-1=0 → P1 gets +2 field
        assert p1.hp == 20 and p2.hp == 20
        assert p1.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))
        assert p2.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))

    def test_fireball_vs_iron_wall_both_cancel(self):
        p1, p2 = fresh()
        resolve(p1, FIREBALL, p2, IRON_WALL)
        assert p1.hp == 20 and p2.hp == 20
        assert p1.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))
        assert p2.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))

    def test_thunder_vs_mirror_both_cancel(self):
        p1, p2 = fresh()
        resolve(p1, THUNDER_BOLT, p2, MIRROR_FIELD)
        assert p1.hp == 20 and p2.hp == 20
        assert p1.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))
        assert p2.field_mana == pytest.approx(float(PERFECT_CANCEL_BONUS))

    def test_perfect_cancel_bonus_value(self):
        assert PERFECT_CANCEL_BONUS == 2


class TestPassMechanics:
    def test_pass_skips_attack(self):
        """P1 passes: no P1→P2 interaction; P2 attacks freely."""
        p1, p2 = fresh()
        resolve(p1, PASS, p2, SWIFT_STRIKE)
        # P1 passed → skip P1→P2
        # P2→P1: A:2 - C:0 = +2 hit → P1 -2 HP, P1 field +2
        assert p1.hp == 18
        assert p1.field_mana == pytest.approx(2.0)
        assert p2.hp == 20
        assert p2.field_mana == pytest.approx(0.0)

    def test_both_pass(self):
        """Both pass: no combat interaction at all."""
        p1, p2 = fresh()
        resolve(p1, PASS, p2, PASS)
        assert p1.hp == 20 and p2.hp == 20
        assert p1.field_mana == 0.0 and p2.field_mana == 0.0


# ======================================================================
# Win condition
# ======================================================================

class TestWinCondition:
    def test_hp_reaches_zero(self):
        p1, p2 = fresh()
        p2.hp = 3
        # Thunder Bolt (A:5) vs Dodge (A:1, C:2)
        # P1→P2: 5-2=3 → P2.hp = 3-3 = 0 → dead
        resolve(p1, THUNDER_BOLT, p2, DODGE)
        assert not p2.is_alive()

    def test_hp_goes_negative(self):
        p1, p2 = fresh()
        p2.hp = 1
        resolve(p1, THUNDER_BOLT, p2, DODGE)
        assert p2.hp < 0
        assert not p2.is_alive()

    def test_survivor_stays_alive(self):
        p1, p2 = fresh()
        p2.hp = 1
        resolve(p1, THUNDER_BOLT, p2, DODGE)
        assert p1.is_alive()

    def test_simultaneous_kill(self):
        """Both die in the same cycle."""
        p1, p2 = fresh()
        p1.hp = 1
        p2.hp = 1
        resolve(p1, SWIFT_STRIKE, p2, SWIFT_STRIKE)
        # P1→P2: 2-1=1; P2→P1: 2-1=1 → both hp=0
        assert not p1.is_alive()
        assert not p2.is_alive()


# ======================================================================
# Resource system
# ======================================================================

class TestResourceSystem:
    def test_regen_increases_self_mana(self):
        p = Player("P")
        p.regen(2)
        assert p.self_mana == 2

    def test_spend_self_mana_first(self):
        p = Player("P")
        p.self_mana = 5
        p.field_mana = 10.0
        p.spend_mana(3)
        assert p.self_mana == 2
        assert p.field_mana == pytest.approx(10.0)

    def test_spend_overflow_to_field_mana(self):
        p = Player("P")
        p.self_mana = 1
        p.field_mana = 5.0
        p.spend_mana(3)   # 1 from self, 2 from field
        assert p.self_mana == 0
        assert p.field_mana == pytest.approx(3.0)

    def test_field_mana_decay_20pct(self):
        p = Player("P")
        p.field_mana = 10.0
        p.decay_field(0.20)
        assert p.field_mana == pytest.approx(8.0)

    def test_field_mana_decay_rounds(self):
        p = Player("P")
        p.field_mana = 1.4
        p.decay_field(0.20)
        assert p.field_mana == pytest.approx(1.12)

    def test_can_afford_uses_combined_mana(self):
        p = Player("P")
        p.self_mana = 1
        p.field_mana = 3.0
        assert p.can_afford(THUNDER_BOLT)   # cost 4, total 4.0

    def test_cannot_afford_insufficient_mana(self):
        p = Player("P")
        p.self_mana = 0
        p.field_mana = 0.0
        assert not p.can_afford(SWIFT_STRIKE)   # cost 1


# ======================================================================
# Phase 2: Spell sheet constraints
# ======================================================================

class TestSpellSheetConstraints:
    def test_exactly_six_spells(self):
        assert len(SPELLS) == 6

    def test_attack_spells_a_greater_than_c(self):
        attack = [s for s in SPELLS if s.kind == "attack"]
        assert len(attack) == 3
        for spell in attack:
            assert spell.attack > spell.counter, \
                f"{spell.name}: attack spell must have A > C"

    def test_defence_spells_c_greater_than_a(self):
        defence = [s for s in SPELLS if s.kind == "defence"]
        assert len(defence) == 3
        for spell in defence:
            assert spell.counter > spell.attack, \
                f"{spell.name}: defence spell must have C > A"

    def test_all_values_in_range_1_to_5(self):
        for spell in SPELLS:
            assert 1 <= spell.attack  <= 5, f"{spell.name}: A out of range"
            assert 1 <= spell.counter <= 5, f"{spell.name}: C out of range"
            assert 1 <= spell.cost    <= 5, f"{spell.name}: Cost out of range"

    def test_perfect_cancel_pairs_exist(self):
        """Each attack spell should have at least one defence spell whose C equals its A."""
        attack_spells  = [s for s in SPELLS if s.kind == "attack"]
        defence_spells = [s for s in SPELLS if s.kind == "defence"]
        defence_c_vals = {s.counter for s in defence_spells}
        for spell in attack_spells:
            assert spell.attack in defence_c_vals, \
                f"{spell.name} has no perfect-cancel defence partner"

    def test_siphon_efficiency_below_1(self):
        """Anti-turtling: siphon must be less than 100%."""
        assert 0.0 < SIPHON_EFF < 1.0
