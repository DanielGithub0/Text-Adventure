import os
import random

__location__ = os.path.realpath( #this creates a call for "__location__" as the real path for [this] file
    os.path.join(os.getcwd(), os.path.dirname(__file__))) #anything called using "__location__" will have the directory of this file searched

class fighting_class:
    def __init__(self, name, base_health=0, base_damage=0, base_speed=0, lvl_inc_health=0, lvl_inc_damage=0, lvl_inc_speed=0, att_range=0): 
        """setting the class to be able to create "classes" to set fighting style"""
        self.name = name
        self.base_health = base_health
        self.base_damage = base_damage
        self.base_speed = base_speed
        self.lvl_inc_health = lvl_inc_health
        self.lvl_inc_damage = lvl_inc_damage
        self.lvl_inc_speed = lvl_inc_speed
        self.range = att_range
        
class race:
    def __init__(self, name, base_health=0, base_damage=0, base_speed=0, lvl_inc_health=0, lvl_inc_damage=0, lvl_inc_speed=0, allowed_classes=[]): 
        """defining the race that the player can choose"""
        self.name = name
        self.base_health = base_health
        self.base_damage = base_damage
        self.base_speed = base_speed
        self.lvl_inc_health = lvl_inc_health
        self.lvl_inc_damage = lvl_inc_damage   
        self.lvl_inc_speed = lvl_inc_speed
        self.allowed_classes = allowed_classes  # List to hold allowed fighting classes    

class Bag: 
    """A simple bag class to hold items with a limited capacity."""
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        else:
            return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            return False

    def list_items(self):
        return self.items

class player_Character:
    def __init__(self, name, level, race, fighting_class): 
        """defining the players character class"""
        if fighting_class not in race.allowed_classes:
            raise ValueError(f"{race.name} cannot become {fighting_class.name}")
        self.name = name
        self.level = level
        self.classType = fighting_class.name
        self.health = fighting_class.base_health
        self.damage = fighting_class.base_damage
        self.speed = fighting_class.base_speed
        self.experience = 0
        self.bag = Bag("player_bag", capacity=10)  # Initialize a bag with a capacity of 10 items
    
    def level_up(self):
        """Level up the character, increasing health and damage."""
        self.level += 1
        self.health += (fighting_class.lvl_inc_health + random.randint(-3, 3))  # Randomly increase health by 1 to 3 times the increment
        self.damage += (fighting_class.lvl_inc_damage + random.randint(-3, 3))
        self.speed += (fighting_class.lvl_inc_speed + random.randint(-3, 3))
        self.experience = 0  # Reset experience after leveling up
        print(f"{self.name} has leveled up to level {self.level}!")
        print(f"New stats - \nHealth: {self.health}\nDamage: {self.damage}\nSpeed: {self.speed}")
        
    def lvl_exp_requirement(self):
        """Calculate the experience required for the next level."""
        required_exp = 3 * self.level + (self.level * (self.level ** random.randint(0,2)))
        return required_exp
    
class Attack:
    def __init__(self, character, target, range):
        """Initialize an attack with a character, damage, and range."""
        self.character = character
        self.target = target
        self.range = range
        
        if self.range <= self.character.att_range:
            # Apply damage to the target
            self.target.health -= self.character.damage
            print(f"{self.character.name} attacks {self.target.name} for {self.damage} damage!")
            if self.target.health <= 0:
                print(f"{self.target.name} has been defeated!")
        
      # if the target is within range, apply damage,
      # otherwise, print a message indicating the target is out of range
        
class Battle:
    def __init__(self, player, enemy):
        """Initialize a battle between player and enemy."""
        self.player = player
        self.enemy = enemy

    def start_battle(self): #starting the battle, and all battle logic
        """Start the battle logic."""
        turn = True
        if self.player.speed > self.enemy.speed:
            turn = self.player
        else:
            turn = self.enemy
        
        match turn:
            case self.player:
                self.player_attack()
                print(f"{self.player.name} attacks {self.enemy.name}!")
        

    def end_battle(self):
        """End the battle and return results."""
        # Placeholder for ending battle logic
        pass

class Enemy:
    def __init__(self, name, lvl, race, Fighting_class,):
        """Initialize an enemy with basic attributes."""
        self.name = name
        self.level = lvl
        self.race = race
        self.fighting_class = Fighting_class
        # Calculate enemy attributes based on level and class and race
        self.health = Fighting_class.base_health + ((lvl - 1) * Fighting_class.lvl_inc_health) +((lvl - 1) * race.lvl_inc_health)
        self.damage = Fighting_class.base_damage + ((lvl - 1) * Fighting_class.lvl_inc_damage) + ((lvl - 1) * race.lvl_inc_damage)
        self.speed = Fighting_class.base_speed + ((lvl - 1) * Fighting_class.lvl_inc_speed) + ((lvl - 1) * race.lvl_inc_speed)
        self.att_range = Fighting_class.range  # Attack range of the enemy

    def attack(self, target):
        """Enemy attacks the target."""
        target.health -= self.damage
        return target.health <= 0  # Return True if the target is defeated


"""Classes"""
#fighting classes that the player can choose from
warrior = fighting_class("Warrior", base_health=120, base_damage=20, base_speed=10, lvl_inc_health=15, lvl_inc_damage=5, lvl_inc_speed=1, att_range=1)

ranger = fighting_class("Ranger", base_health=100, base_damage=25, base_speed=15, lvl_inc_health=10, lvl_inc_damage=4, lvl_inc_speed=2, att_range=3)

mage = fighting_class("Mage", base_health=80, base_damage=35, base_speed=8, lvl_inc_health=8, lvl_inc_damage=6, lvl_inc_speed=1, att_range=4)
#adding more fighting classes allowed

"""Races"""
#races that the player can choose from
human = race("Human", base_health=100, base_damage=10, base_speed=10, lvl_inc_health=2, lvl_inc_damage=2, lvl_inc_speed=2, allowed_classes=[warrior, ranger, mage])

elf = race("Elf", base_health=70, base_damage=12, base_speed=12, lvl_inc_health=2, lvl_inc_damage=2, lvl_inc_speed=2, allowed_classes=[ranger, mage])

dragonborn = race("Dragonborn", base_health=120, base_damage=15, base_speed=8, lvl_inc_health=4, lvl_inc_damage=4, lvl_inc_speed=1, allowed_classes=[warrior, mage])

wisp = race("Wisp", base_health=40, base_damage=3, base_speed=18, lvl_inc_health=1, lvl_inc_damage=2, lvl_inc_speed=3, allowed_classes=[mage])
#adding more races allowed

def create_character():
    print("Welcome to the Text Adventure Game!")
    player_name = input("Who are you fellow adventurer? [Enter your name]: ")
    print(f"Hello, {player_name}! Let's create your character.")
    changeName = input("Would you like to change the name for your character or are you confident in who you are? [y/n]: ")
    while changeName.lower() not in ['y', 'n']:
        changeName = input("Please answer with 'y' for yes or 'n' for no: ")
    if changeName.lower() == 'y':
        player_name = input("What would you like to name your character? [Enter a name]: ")
        print(f"Great! Your character's name is now {player_name}.")
    else:
        print(f"Your character's name remains {player_name}.")
    
    print("Now, let's choose your race.")
    print("Available races:")
    print("1. Human. The most average yet versatile race. Can be any class, but not the best at any. \n2. Elf. The nimble and agile race. They excel in ranged combat and magic, but are weaker in melee.\n3. Dragonborn. The strong and resilient people descendants of dragons. They are powerful in melee and magic, but slower.\n4. Wisp. The mystical and ethereal race hailing from the spirit world. They excel in magic and speed, but are fragile.")
    player_race = input("Choose your race (Human, Elf, Dragonborn, Wisp): ")
    changeRace = input(f"You are a {player_race} right? [y/n]: ")
    while changeRace.lower() not in ['y', 'n']:
        changeRace = input("Please answer with 'y' for yes or 'n' for no: ")
    if changeRace.lower() == 'n':
        player_race = input(f"If not a {player_race}, then what: ") 
    match player_race.lower():  
        case "human":
            character_race = human
        case "elf":
            character_race = elf
        case "dragonborn":
            character_race = dragonborn
        case "wisp":
            character_race = wisp
    
    print(f"You have chosen the {character_race.name}.")
    
    player_class = input("Choose your fighting class (Warrior, Ranger, Mage): ")
    while player_class.lower() not in [warrior.name.lower(), ranger.name.lower(), mage.name.lower()]:
        player_class = input("Invalid class. Please choose from Warrior, Ranger, or Mage: ")
    match player_class.lower():
        case "warrior":
            fighting_class = warrior
        case "ranger": 
            fighting_class = ranger
        case "mage":  
            fighting_class = mage
    
    print(f"You have chosen the {fighting_class.name} class.")
    print(f"Thats a great choice, {player_name}! You are now a level 1 {player_race} {player_class}.\nYour starting stats are: \nHealth: {fighting_class.base_health + character_race.base_health}, \nDamage: {fighting_class.base_damage + character_race.base_damage}, \nSpeed: {fighting_class.base_speed + character_race.base_speed}.\nYou will gain:\n{fighting_class.lvl_inc_health + character_race.lvl_inc_health} health, \n{fighting_class.lvl_inc_damage + character_race.lvl_inc_damage} damage, \n{fighting_class.lvl_inc_speed + character_race.lvl_inc_speed} speed per level.")
    print("This will deviate a bit by +/- 3 points per level to add a bit of spice to the game.")
    print(f"You are ready to embark on your adventure {player_name}!")
    player = player_Character(player_name, 1, character_race, fighting_class)  # Create the player character
    starting_adventure()  # Start the adventure after character creation
    
def starting_adventure():
    """Placeholder for the starting adventure logic."""
    print("Your adventure begins now! Explore the world, fight enemies, and level up your character.")
    # Placeholder for adventure logic
    pass
    


if __name__ == "__main__":
    create_character()  # Call the function to create a character  
    
#player creation example
#player = Character("Alice", 1, warrior)
#print(player.health)  # 150
        
        
# Text Adventure Game
""" the original code was a text adventure game that had a welcome message and two choices for the player to make. Very basic. Idea completely changed to a more complex text adventure game with character creation.
# The player could either waste their life away or do something with their life.
welcomeState = open(os.path.join(__location__, "welcome.txt")) #calling the welcome message
 
computerSitting = input(welcomeState.read())
action = False

while action == False:
    if computerSitting == "a":
      print("you wasted your life away")
      action = True
    elif computerSitting == "b":
       print("ur doing something with your life")
       action = True
    else:
       computerSitting = input("you need to answer the question: ")

leaveOff = False
while action == True & leaveOff == False:
    print("loop 2 true")
    officeLeave = input(open(os.path.join(__location__, "office.txt")).read())
    if officeLeave == "a":
        print("fuck youuuu.. you WERE ONE step closer to not being a failure.. but u fucked that up")
        leaveOff = False
        action = False
    elif officeLeave == "b":
        print("you are doing better than yesterday")
        leaveOff = True
    else:
       officeLeave = input("you need to answer the question: ")

"""