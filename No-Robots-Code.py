import random
import sys


class Item:
    def __init__(self, name, item_type, effect):
        self.name = name
        self.item_type = item_type  # 'usable' or 'permanent'
        self.effect = effect  # 'health_boost', 'strength_boost', 'magic_boost', etc.

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"You obtained a {item.name}.")

    def list_items(self):
        if not self.items:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.items:
                print(f"- {item.name}")

    def find_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class.lower()
        self.inventory = Inventory()
        
        if self.char_class == "warrior":
            self.health = 120
            self.strength = 30
            self.agility = 5
            self.magic = 1
            self.dodge_chance = 1 / 10
        elif self.char_class == "mage":
            self.health = 80
            self.strength = 5
            self.agility = 5
            self.magic = 20
            self.dodge_chance = 1 / 4
        elif self.char_class == "rogue":
            self.health = 100
            self.strength = 20
            self.agility = 15
            self.magic = 5
            self.dodge_chance = 1 / 2
        else:
            raise ValueError("Invalid character class")

    def is_alive(self):
        return self.health > 0

    def try_dodge(self):
        return random.random() < self.dodge_chance

    def use_item(self, item, checkpoint_function):
        choice = get_valid_input(f"Do you want to [Use] the {item.name} or [Keep] it? ", ["use", "keep"]).lower()
        if choice == "use":
            if item.effect == "health_boost":
                self.health += 30
                print("You feel your health increase!")
            elif item.effect == "strength_boost":
                self.strength += 5
                print("You feel a surge of power!")
            elif item.effect == "magic_boost":
                self.magic += 5
                print("You feel your magical power intensify!")
            self.inventory.items.remove(item)
        else:
            print(f"You kept the {item.name} for later.")
        checkpoint_function(self)

class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def is_alive(self):
        return self.health > 0

    def attack(self):
        return random.randint(self.attack_power - 2, self.attack_power + 2)

    def try_dodge(self):
        return random.random() < 1 / 12

class Dragon(Enemy):
    def __init__(self, name="Dragon"):
        super().__init__(name, random.randint(100, 120), random.randint(10, 20))

class Golem(Enemy):
    def __init__(self, name="Ancient Crystal Golem"):
        super().__init__(name, random.randint(100, 125), random.randint(20, 30))

class Wraith(Enemy):
    def __init__(self, name="Phantom Wraith"):
        super().__init__(name, random.randint(110, 130), random.randint(15, 30))

class Serpent(Enemy):
    def __init__(self, name="Colossal Serpent"):
        super().__init__(name, random.randint(100, 175), random.randint(5, 12))

def combat(player, enemies):
    if len(enemies) == 1:
        print(f"{len(enemies)} Enemy appears! Combat begins!")
    elif len(enemies) > 1:
        print(f"{len(enemies)} Enemies appear! Combat begins!")
    for enemy in enemies:
        while player.is_alive() and enemy.is_alive():
            if not enemy.try_dodge():
                action = get_valid_input(f"Choose an action: [Attack], Use [Magic], [Defend], or [Escape] this battle: ", ["attack", "magic", "defend", "escape"]).lower()
                
                if action == "attack":
                    damage = random.randint(player.strength - 2, player.strength + 2)
                    enemy.health -= damage
                    print(f"You attacked the {enemy.name} for {damage} damage. Enemy health: {enemy.health}")
                elif action == "defend":
                    player.health += random.randint(3, 7)
                    print("You brace yourself, gaining a small amount of health.")
                elif action == "magic":
                    if player.magic > 0:
                        damage = random.randint(player.magic + 3, player.magic + 7)
                        enemy.health -= damage
                        player.magic -= 5
                        print(f"You cast a spell, dealing {damage} damage to the {enemy.name}. Enemy health: {enemy.health}")
                    else:
                        print("You have no magic points left! Please choose another action.")
                        continue
                elif action == "escape":
                    escape_chance = random.random()
                    if escape_chance < 0.2:
                        print("You successfully escaped the battle!")
                        return
                    else:
                        print("Escape failed! The enemy attacks as you try to flee.")
                        damage = enemy.attack()
                        player.health -= damage
                        print(f"You took {damage} damage while trying to escape. Your health: {player.health}")
                        continue

                if enemy.is_alive():
                    damage = enemy.attack()
                    player.health -= damage
                    print(f"The {enemy.name} attacks! You took {damage} damage. Your health: {player.health}")
            else:
                print(f"The {enemy.name} dodged your attack!")

        if not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

    print(f"You defeated all enemies!\n")

def final_boss_battle(player):
    print("\nYou've entered the Fortress, and the Final Boss appears!")
    final_boss = FinalBoss("Fortress Guardian", 120, 8)
    combat(player, [final_boss])
    if player.is_alive():
        print("You have defeated the Fortress Guardian!")
        final_reward = Item("Fortress Guardian's Crown", "permanent", "strength_boost")
        player.inventory.add_item(final_reward)
        print("The Fortress Guardian drops a powerful crown, granting you greater strength!")
        player.use_item(final_reward, lambda p=player: end_game(p))
    else:
        print("You were defeated by the Fortress Guardian. Better luck next time!")
        sys.exit()

def haunted_forest(player):
    print("\nYou enter the haunted forest, the trees twist and groan with dark magic.")
    print("Strange creatures lurk in the shadows, but you press on.")
    # You may encounter small random battles here (could be creatures or minor enemies)
    encounter = random.choice(["ghost", "wild_plant", "shadow_creature"])
    print(f"You are confronted by a {encounter}!")
    
    enemy = Enemy(encounter.capitalize(), 30, 5)
    combat(player, [enemy])
    if player.is_alive():
        print("You manage to defeat the creature and continue your journey through the forest.")
        print("After a few more hours, you arrive at the Dark Temple.")
        final_boss_battle(player)
    else:
        print("You were overwhelmed in the haunted forest. Better luck next time!")
        sys.exit()

def get_valid_input(prompt, valid_choices):
    """Repeatedly prompts the user for input until they choose a valid option."""
    while True:
        choice = input(prompt).lower()
        if choice in valid_choices:
            return choice
        else:
            print(f"Invalid input. Please choose one of the following options: {', '.join(valid_choices)}")

def start_story(player):
    print(f"Intro... You are {name}, a {char_class}, with a daring adventure ahead. You found yourself trapped in a dragons den. In this game you have options to explore different areas, all eding with a boss fight. In combat you have 4 choices: Attack, using your strenght to take down your enemies; Magic, where you cast a powerful spell to damage your enemies. Be careful as you have a certain amount of magic points, which are required to use a magic attack. You can defend, where you have the chance to gain 3-7 health back, and Escape, where you have a 10% chance of escaping. If you fail to escape, you take damage and your turn ends. Enjoy.")
    choice = input("Would you like to continue? (y/n): ")
    if choice == "y":
        print("\nYou are trapped in the dragon's den. You see a dragon egg nearby and a small opening you can escape through.")
        choice = get_valid_input("Do you [Steal] the dragon egg or [Escape]? ", ["steal", "escape"])
        
        if choice == "steal":
            print("You took the egg, but two raiders ambush you!")
            raider1 = Enemy("Raider 1", 30, 5)
            raider2 = Enemy("Raider 2", 30, 5)
            combat(player, [raider1, raider2])
            if player.is_alive():
                print("You escaped with the dragon egg!")
                health_potion = Item("Health Potion", "usable", "health_boost")
                player.inventory.add_item(health_potion)
                player.use_item(health_potion, lambda p=player: post_dragon_den(p))
        elif choice == "escape":
            print("You escape through the opening, leaving the egg behind.")
            post_dragon_den(player)
    elif choice == "c":
        cave_entrance(player)
    elif choice == "n":
        print("Okay, farewell adventurer!")

def post_dragon_den(player):
    mystic_herb = Item("Mystic Herb", "usable", "health_boost")
    player.inventory.add_item(mystic_herb)
    player.use_item(mystic_herb, lambda p=player: village_or_tower(p))

def village_or_tower(player):
    print("\nYou emerge from the dragon's den. You can head north to a fishing village or south to the Fortress.")
    choice = get_valid_input("Do you go [North] to the village or [South] to the Fortress? ", ["north", "south"])

    if choice == "north":
        village_encounter(player)
    elif choice == "south":
        haunted_forest(player)

def village_encounter(player):
    print("\nYou arrive at a fishing village under attack!")
    choice = get_valid_input("Do you want to [Sneak] away or [Defend] the village? ", ["sneak", "defend"])

    if choice == "sneak":
        print("You manage to sneak away without being seen. As you flee, you find a Magic Potion.")
        magic_potion = Item("Magic Potion", "usable", "magic_boost")
        player.inventory.add_item(magic_potion)
        player.use_item(magic_potion, lambda p=player: castle_or_return_south(p))

    elif choice == "defend":
        print("You choose to defend the village from the raiders!")
        raider1 = Enemy("Raider 1", 30, 5)
        raider2 = Enemy("Raider 2", 30, 5)
        raider3 = Enemy("Raider 3", 30, 5)
        combat(player, [raider1, raider2, raider3])
        if player.is_alive():
            print("You saved the villagers and receive a Health Potion as a reward.")
            health_potion = Item("Health Potion", "usable", "health_boost")
            player.inventory.add_item(health_potion)
            player.use_item(health_potion, lambda p=player: castle_or_return_south(p))

def cave_exploration(player):
    cave_gaurd = random.choice(["Crystal Golem", "Luminous Bat", "Enchanted Spider"])
    if cave_gaurd == "Crystal Golem":
        gaurds_item = "Crystal Shard"
    if cave_gaurd == "Luminous Bat":
        gaurds_item = "Crystal Shard"
    if cave_gaurd == "Enchanted Spider":
        gaurds_item = "Glowing Eye"
    print(f"While you were exploring, you ran into the {cave_gaurd}!")

    creature = Enemy(cave_gaurd.capitalize(), 35, 5)
    combat(player, [creature])

    if player.is_alive():
        print(f"You defeated the {cave_gaurd} and found the {gaurds_item}")
        final_cave_boss(player)
    elif not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

def final_cave_boss(player):
    cave_boss = random.choice(["Anchent Crystal Golem", "Phantom Wraith", "Collosal Serpent"])

    if cave_boss == "Anchent Crystal Golem":
        print("You encountered the Anchent Crystal Golem, a golem 3x larger than any seen before. It's eyes made of purple crystals, and massive blue shards the size of a horse sticking out all over it's body... Prepare for the fight of a life time!")
        bosss = Golem(cave_boss.capitalize())
        combat(player, [bosss])
        if player.is_alive():
            print(f"You defeated the {cave_boss} and found the Great Purple Crystal, the eye of the beast! Congratulations and farewell {name}!")
            sys.exit()
        elif not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

    elif cave_boss == "Phantom Wraith":
        print("You encountered the Phantom Wraith, a ghost with features difficult to make out. It has a ragged old cloak thats been torn up through it's previous battles. You see the destroyed bodies of a couple of Crystal Golems; ferocious battles occured here... Now its your turn. Prepare for the fight of a life time!")
        bosss = Wraith(cave_boss.capitalize())
        combat(player, [bosss])
        if player.is_alive():
            print(f"You defeated the {cave_boss} and found the Cloak of Shadows, the prized possession of the beast is now yours! Congratulations and farewell {name}!")
            sys.exit()
        elif not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

    elif cave_boss == "Collosal Serpent":
        print("You encountered the Collosal Serpent, the serpent capible of destroying cities. It's fangs larger than the greatest warriors sword. Despite it's size, the Serpent is the one of the most agile creatures, and if you aren't careful, it will take you out with ease. As a child you heard the stored of how your ancestors drove the snake away from the city and underground. Now, its time for you to finish what they started... Prepare for the fight of a life time!")
        bosss = Serpent(cave_boss.capitalize())
        combat(player, [bosss])
        if player.is_alive():
            print(f"You defeated the {cave_boss} and found the Great Serpent Fang, the weapon of the beast used to terrorize your ancestors is now yours! Congratulations and farewell {name}!")
            sys.exit()
        elif not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

def dragon_boss_battle(player):
    dragon = "Dragon"
    print("You travled back to the den, but to your horror, the dragon is now awake. You must prepare and fight this beast, and save your land... Prepare for the battle of a lifetime!")
    bosss = Dragon(dragon.capitalize())
    combat(player, [bosss])
    if player.is_alive():
        print(f"The Dragon is dead, the egg is yours and the land is free of the fear of the dragon. Congratulations and farewell {name}!")
        sys.exit()
    elif not player.is_alive():
            print("You died. Farewell, adventurer.")
            sys.exit()

def cave_entrance(player):
    print('You arrive at the Mystic Cave. Do you want to enter or continue exploring: ("village", "dragon", "fortress" or "cave")')
    choice = input("Choose where you want to go: ")
    if choice == "cave":
        cave_exploration(player)
    elif choice == "village":
        village_encounter(player)
    elif choice == "dragon":
        dragon_boss_battle(player)
    elif choice == "fortress":
        haunted_forest(player)
def castle_or_return_south(player):
    choice = get_valid_input("Do you want to continue [North] to the castle or head [West] to the ? ", ["north", "west"])

    if choice == "north":
        print("You arrive at the castle and face the final challenge!")
        final_boss_battle(player)
    elif choice == "west":
        print("You head west to the Mystic Cave.")
        cave_entrance(player)

# Start the game
name = input("Enter your character's name: ")
char_class = input("Choose your class (Warrior, Mage, Rogue): ").capitalize()

player = Character(name, char_class)
start_story(player)

def end_game(player):
    print(f"\n{player.name}, you've completed your journey!")
    print("Thanks for playing!")
    sys.exit()  # Exit the game
