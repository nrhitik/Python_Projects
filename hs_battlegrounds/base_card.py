import random
import config as cfg
from termcolor import colored


class Card:
    def __init__(self, attack: int = None, health: int = None,
                 is_bubbled: bool = False, is_poison: bool = False,
                 is_reborn: bool = False):
        self.attack = attack if attack is not None else random.randint(1, 40)
        self.health = health if health is not None else random.randint(1, 50)

        # if a card is bubbled, it ignores the first time it takes damage
        self.is_bubbled = is_bubbled

        # if a card has poison, it kills any card to which it does damage
        self.is_poison = is_poison

        self.is_reborn = is_reborn

        self.is_dead = False
        self.has_attacked = False
        self.has_lost_hp = False

        self.default_stats = {'attack': self.attack, 'health': self.health,
                              'is_bubbled': self.is_bubbled,
                              'is_poison': self.is_poison,
                              'is_reborn': self.is_reborn}

    def __str__(self):
        '''This function allows us to easily print instances of Card class.
        If the card is bubbled, it adds 'b' after health. If the card has
        poison, it adds 'p' after attack'''

        if self.has_lost_hp:
            hp_str = colored(str(self.health), 'red')
        else:
            hp_str = colored(str(self.health), 'green')

        atk_str = colored(str(self.attack), 'green')

        atk_info = f"{atk_str + 'p' * self.is_poison}"
        hlt_info = f"{hp_str + 'b' * self.is_bubbled}"
        return f"({atk_info: <{cfg.CARD_TXT_SPACE}}|" \
               f"{hlt_info: >{cfg.CARD_TXT_SPACE}})"

    def __repr__(self):
        '''Does the same as __str__'''

        return self.__str__()

    def takes_damage(self, other) -> None:
        '''This function changes the stats of the card based on the other
        card attack'''

        if self.is_bubbled:
            self.is_bubbled = False
            return

        if other.is_poison:
            self.is_dead = True
            return

        self.health -= other.attack
        self.has_lost_hp = True
        if self.health <= 0:
            self.is_dead = True

    def after_death(self):
        if self.is_reborn:
            summon = Card(**self.default_stats)
            summon.is_reborn = False
            summon.health = 1
            return summon
        return None

    def do_attack(self, other) -> None:
        other.takes_damage(self)
        self.takes_damage(other)
