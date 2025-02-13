"""Part 4 electric boogaloo"""
import random

def display_player_status(player_health):
    """health check!"""
    print(f"Your current health: {player_health}")

def handle_path_choice(player_health):
    """Path choice return health"""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health = min(player_health + 10, 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_health = max(player_health - 15, 0)
        if player_health == 0:
            print("You are barely alive!")
    return player_health

def player_attack(monster_health):
    """return monster health"""
    print("You strike the monster for 15 damage!")
    return max(monster_health - 15, 0)

def monster_attack(player_health):
    """return player health"""
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        player_health = max(player_health - 20, 0)
    else:
        print("The monster hits you for 10 damage!")
        player_health = max(player_health - 10, 0)
    return player_health

def combat_encounter(player_health, monster_health, has_treasure):
    """monster fight"""
    while player_health > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        if monster_health == 0:
            print("You defeated the monster!")
            return player_health, has_treasure

        player_health = monster_attack(player_health)
        display_player_status(player_health)

        if player_health == 0:
            print("Game Over!")
            return player_health, False

    return player_health, False

def check_for_treasure(has_treasure):
    """check if monster has treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """add item to inventory"""
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """show invantory"""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for idx, item in enumerate(inventory, start=1):
            print(f"{idx}. {item}")

def enter_dungeon(player_health, inventory, dungeon_rooms):
    """handle dungeon and rooms"""
    print("\nEntering the dungeon...\n")
    for room in dungeon_rooms:
        # immutability
        try:
            room[1] = "modified"
        except TypeError:
            print("Error: Cannot modify room tuple. Tuples are immutable.")

        room_description, item, challenge_type, challenge_outcome = room
        print(f"\nRoom: {room_description}")

        # add item
        if item is not None:
            print(f"You found a {item} in the room.")
            if item == "treasure":
                inventory.insert(0, item)
                print("You found a treasure and it's so valuable, you keep it at the top "
                      "of your inventory!")
            else:
                acquire_item(inventory, item)

        # chalanges based on room typee
        if challenge_type == "puzzle":
            print("You encounter a puzzle!")
            choice = input("Do you want to solve or skip the puzzle? ").strip().lower()
            if choice == "solve":
                success = random.choice([True, False])
                success_message, failure_message, health_change = challenge_outcome
                if success:
                    print(success_message)
                    player_health += health_change
                else:
                    print(failure_message)
                    player_health += health_change
            else:
                print("You chose to skip the puzzle. No changes occur.")
        elif challenge_type == "trap":
            print("You see a potential trap!")
            choice = input("Do you want to disarm or bypass the trap? ").strip().lower()
            if choice == "disarm":
                success = random.choice([True, False])
                success_message, failure_message, health_change = challenge_outcome
                if success:
                    print(success_message)
                    player_health += health_change
                else:
                    print(failure_message)
                    player_health += health_change
            else:
                print("You chose to bypass the trap. You proceed with caution.")
        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")

        # alive check!
        if player_health < 0:
            player_health = 0
            print("You are barely alive!")

        # skeet skeet pop pop
        if player_health < 50 and "healing potion" in inventory:
            index = inventory.index("healing potion")
            inventory.pop(index)
            print("Your health is low. You used a healing potion from your inventory!")
            player_health = min(player_health + 20, 100)

        display_inventory(inventory)
        print(f"Current health: {player_health}")

    print(f"\nYou exit the dungeon with {player_health} health.")
    return player_health, inventory


def main():
    """main main main main main main"""
    # init var
    player_health = 100
    monster_health = 70
    inventory = []
    has_treasure = random.choice([True, False])

    # path choice
    player_health = handle_path_choice(player_health)
    player_health, treasure_obtained_in_combat = combat_encounter(
        player_health, monster_health, has_treasure
    )

    check_for_treasure(treasure_obtained_in_combat)

    # dungeon rooms
    if player_health > 0:
        dungeon_rooms = [
            ("A dusty old library", "key", "puzzle",
             ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
            ("A narrow passage with a creaky floor", None, "trap",
             ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
            ("A grand hall with a shimmering pool", "healing potion", "none", None),
            ("A small room with a locked chest", "treasure", "puzzle",
             ("You cracked the code!", "The chest remains stubbornly locked.", -5))
        ]
        player_health, inventory = enter_dungeon(player_health, inventory,
                                                 dungeon_rooms)

    print("\nFinal Player Status:")
    display_player_status(player_health)
    display_inventory(inventory)


if __name__ == "__main__":
    main()
