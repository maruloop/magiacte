"""CUI game loop for MAGIACTE (Phase 1 prototype)."""
import os

from .combat import resolve, SIPHON_EFF, PERFECT_CANCEL_BONUS
from .player import Player
from .spells import Spell, SPELLS, PASS

FIELD_DECAY_RATE = 0.20
SELF_MANA_REGEN  = 2
SEP = "=" * 56


# ------------------------------------------------------------------ display

def _hr(char: str = "-", width: int = 56) -> str:
    return char * width


def _print_state(p1: Player, p2: Player, cycle: int) -> None:
    print(f"\n{SEP}")
    print(f"  MAGIACTE   —   Cycle {cycle}")
    print(SEP)
    print(
        f"  {p1.name:<18}  HP:{p1.hp:>3}  "
        f"Self:{p1.self_mana:>3}  Field:{p1.field_mana:>6.2f}"
    )
    print(
        f"  {p2.name:<18}  HP:{p2.hp:>3}  "
        f"Self:{p2.self_mana:>3}  Field:{p2.field_mana:>6.2f}"
    )
    print(SEP)


def _print_spell_menu(player: Player) -> None:
    print(f"\n  [{player.name}]  available mana: {player.total_mana:.2f}")
    print(f"  {'#':<3} {'Name':<15} {'A':>2}  {'C':>2}  {'Cost':>4}  {'Kind':<8}")
    print(f"  {_hr('-', 44)}")
    for i, spell in enumerate(SPELLS, start=1):
        note = "" if player.can_afford(spell) else "  (no mana)"
        print(
            f"  {i:<3} {spell.name:<15} {spell.attack:>2}  {spell.counter:>2}"
            f"  {spell.cost:>4}  {spell.kind:<8}{note}"
        )
    print(f"  {'0':<3} {'Pass':<15} {'0':>2}  {'0':>2}  {'0':>4}  {'pass':<8}")


# ------------------------------------------------------------------ input

def _choose_spell(player: Player) -> Spell:
    _print_spell_menu(player)
    while True:
        raw = input(f"\n  {player.name} › ").strip()
        if raw == "0":
            return PASS
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(SPELLS):
                chosen = SPELLS[idx]
                if player.can_afford(chosen):
                    return chosen
                print(
                    f"  ! Not enough mana "
                    f"(need {chosen.cost}, have {player.total_mana:.2f})"
                )
                continue
        print("  ! Invalid — enter a number from the list.")


# ------------------------------------------------------------------ main loop

def run_game() -> None:
    print(f"\n{SEP}")
    print("  MAGIACTE — CUI Prototype")
    print(f"{SEP}")
    p1_name = input("  Player 1 name [Magi]:  ").strip() or "Magi"
    p2_name = input("  Player 2 name [Arcas]: ").strip() or "Arcas"

    p1 = Player(p1_name)
    p2 = Player(p2_name)
    cycle = 1

    while p1.is_alive() and p2.is_alive():
        # ① Self mana regeneration (start of cycle, so cycle 1 isn't mana-starved)
        p1.regen(SELF_MANA_REGEN)
        p2.regen(SELF_MANA_REGEN)

        # ② Show state
        _print_state(p1, p2, cycle)

        # ③ Spell selection (sequential — simple CUI mode)
        spell1 = _choose_spell(p1)
        spell2 = _choose_spell(p2)

        # ④ Spend mana
        p1.spend_mana(spell1.cost)
        p2.spend_mana(spell2.cost)

        # ⑤ Resolve combat
        print(f"\n{_hr()}")
        print("  COMBAT RESOLUTION")
        print(_hr())
        result = resolve(p1, spell1, p2, spell2)
        for line in result.log:
            print(line)

        # ⑥ Field mana decay (end of cycle)
        prev1, prev2 = p1.field_mana, p2.field_mana
        p1.decay_field(FIELD_DECAY_RATE)
        p2.decay_field(FIELD_DECAY_RATE)
        print(_hr("-", 56))
        pct = int(FIELD_DECAY_RATE * 100)
        print(
            f"  [Decay -{pct}%]  "
            f"{p1.name} field: {prev1:.2f} → {p1.field_mana:.2f}  |  "
            f"{p2.name} field: {prev2:.2f} → {p2.field_mana:.2f}"
        )

        # ⑦ Win condition check
        if not p1.is_alive() or not p2.is_alive():
            break

        cycle += 1
        input("\n  [Enter to continue] ")

    # ---------------------------------------------------------------- result
    print(f"\n{SEP}")
    print("  GAME OVER")
    print(SEP)
    if not p1.is_alive() and not p2.is_alive():
        print("  DRAW!")
    elif not p1.is_alive():
        print(f"  {p2.name} WINS!")
    else:
        print(f"  {p1.name} WINS!")
    print(f"  Final — {p1.name}: {p1.hp} HP   {p2.name}: {p2.hp} HP")
    print(SEP)
