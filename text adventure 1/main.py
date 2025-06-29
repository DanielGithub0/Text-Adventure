import os
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk as ImageTK

__location__ = os.path.realpath( #this creates a call for "__location__" as the real path for [this] file
    os.path.join(os.getcwd(), os.path.dirname(__file__))) #anything called using "__location__" will have the directory of this file searched

class game_Window:
    def __init__(self, title="Text Adventure Game", width=960, height=540):
        """Initialize the game window with a title and size."""
        self.window = tk.Tk()
        self.window.geometry(f"{width}x{height}")
        self.window.title(title)
        
        # Load and set the icon
        icon_path = os.path.join(__location__, "githubLogo.jpg")
        if os.path.exists(icon_path):
            icon = ImageTK.PhotoImage(Image.open(icon_path))
            self.window.iconphoto(True, icon)
        else:
            print("Icon file not found.")
        self.window.config(bg="#001373")
        
    def run(self):
        """Run the main loop of the game window."""
        self.window.mainloop()
        
    def print_onto_window(self, text):
        """Print text onto the game window."""
        label = tk.Label(self.window, text=text, bg="#001373", fg="white", font=("Arial", 14), padx=20, pady=20)
        label.pack()
        
class fighting_Class:
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

class bag: 
    """A simple bag class to hold items with a limited capacity."""
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.gold_amount = 0  # Initialize gold amount
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        else:
            print(f"{self.name} is full! Cannot add {item}.")
            return False
    
    def add_gold(self, amount):
        """Add gold to the bag."""
        if amount > 0:
            self.gold_amount += amount
            print(f"{amount} gold added to {self.name}. Total gold: {self.gold_amount}")
            return True
        else:
            print("Invalid amount of gold to add.")
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
        if fighting_Class not in race.allowed_classes:
            raise ValueError(f"{race.name} cannot become {fighting_Class.name}")
        self.name = name
        self.level = level
        self.race = race
        self.classType = fighting_Class.name
        self.health = fighting_Class.base_health + race.base_health  # Calculate health based
        self.damage = fighting_Class.base_damage + race.base_damage  # Calculate damage
        self.speed = fighting_Class.base_speed + race.base_speed  # Calculate speed
        self.range = fighting_Class.range  # Attack range of the player
        self.health_increment = fighting_Class.lvl_inc_health + race.lvl_inc_health  # Health increment per level
        self.damage_increment = fighting_Class.lvl_inc_damage + race.lvl_inc_damage  # Damage increment per level
        self.speed_increment = fighting_Class.lvl_inc_speed + race.lvl_inc_speed  # Speed increment per level
        self.experience_required = 0  
        self.experience = 0
        self.bag = bag(f"{self.name}'s Backpack", capacity=10)  # Initialize a bag with a capacity of 10 items
        self.wallet = bag(f"{self.name}'s Wallet", capacity=300)  # Initialize a wallet with a capacity of 5 items
    
    def level_up(self):
        """Level up the character, increasing health and damage."""
        self.level += 1
        self.health += (fighting_Class.lvl_inc_health + random.randint(-3, 3))  # Randomly increase health by 1 to 3 times the increment
        self.damage += (fighting_Class.lvl_inc_damage + random.randint(-3, 3))
        self.speed += (fighting_Class.lvl_inc_speed + random.randint(-3, 3))
        self.experience = 0  # Reset experience after leveling up
        print(f"{self.name} has leveled up to level {self.level}!")
        print(f"New stats - \nHealth: {self.health}\nDamage: {self.damage}\nSpeed: {self.speed}")
        self.lvl_exp_requirement()  # Recalculate experience required for the next level
        
    def lvl_exp_requirement(self):
        """Calculate the experience required for the next level."""
        required_exp = 3 * self.level + (self.level * (self.level ** random.randint(0,2)))
        self.experience_required = required_exp
    
class attack:
    def __init__(self, character, target, range):
        global battle_over
        """Initialize an attack with a character, damage, and range."""
        self.character = character
        self.target = target
        self.range = range
        
        """Execute the attack logic."""
        if self.range <= self.character.range:  # Check if the target is within range
            # Apply damage to the target
            self.target.health -= self.character.damage
            print(f"{self.character.name} attacks {self.target.name} for {self.character.damage} damage!")
            match self.target.health:
                case health if health > 0:
                    print(f"{self.target.name} has {self.target.health} health remaining.\n")
                case heath if health <= 0:
                    print(f"{self.target.name} has 0 health remaining.")
                    print(f"{self.target.name} has been defeated!")
                    battle_over = True  # End the battle if the target is defeated
        else:
            # Print a message indicating the target is out of range
            print(f"{self.target.name} is out of range for {self.character.name}'s attack!")
            pass
        
      # if the target is within range, apply damage,
      # otherwise, print a message indicating the target is out of range
        
class battle:
    def __init__(self, player, enemy):
        """Initialize a battle between player and enemy."""
        self.player = player
        self.enemy = enemy

    def start_battle(self): #starting the battle, and all battle logic
        global battle_over
        """Start the battle logic."""
        turn = True
        battle_over = False
        if self.player.speed > self.enemy.speed:
            turn = self.player
        else:
            turn = self.enemy
        
        """Default distance is being used (need to be changed to use a dynamic range changing on the location of the characters)
        Can be implemented using an array for locations (kinda like a DND map) and then using the distance between the two characters to determine if they are in range of each other"""
        range = 2 
        
        while not battle_over:
            match turn:
                case self.player:
                    attack.__call__(self.player, self.enemy, range)  # Player attacks first if they have higher speed
                    turn = self.enemy  # Switch turn to enemy
                case self.enemy:
                    attack(self.enemy, self.player, range)  # Enemy attacks first if they have higher speed
                    turn = self.player  # Switch turn to player
        

    def end_battle(self):
        """End the battle and return results."""
        # Placeholder for ending battle logic
        pass

class enemy:
    def __init__(self, name, lvl, race, Fighting_class,):
        """Initialize an enemy with basic attributes."""
        self.name = name
        self.level = lvl
        self.race = race
        self.fighting_class = Fighting_class
        self.range = Fighting_class.range  # Attack range of the enemy
        # Calculate enemy attributes based on level and class and race
        self.health = Fighting_class.base_health + ((lvl - 1) * Fighting_class.lvl_inc_health) +((lvl - 1) * race.lvl_inc_health)
        self.damage = Fighting_class.base_damage + ((lvl - 1) * Fighting_class.lvl_inc_damage) + ((lvl - 1) * race.lvl_inc_damage)
        self.speed = Fighting_class.base_speed + ((lvl - 1) * Fighting_class.lvl_inc_speed) + ((lvl - 1) * race.lvl_inc_speed)
        self.att_range = Fighting_class.range  # Attack range of the enemy

    def attack(self, target):
        """Enemy attacks the target."""
        target.health -= self.damage
        return target.health <= 0  # Return True if the target is defeated

class item:
    def __init__(self, name, description, value):
        """Initialize an item with basic attributes."""
        self.name = name
        self.description = description
        self.value = value  # Value can be gold or other resources
        self.is_equipped = False  # Track if the item is equipped

    def equip(self):
        """Equip the item."""
        self.is_equipped = True
        print(f"{self.name} has been equipped.")

    def unequip(self):
        """Unequip the item."""
        self.is_equipped = False
        print(f"{self.name} has been unequipped.")
        
class guild_Quest:
    def __init__(self, name, description, level_requirement, reward):
        """Initialize a guild quest with basic attributes."""
        self.name = name
        self.description = description
        self.level_requirement = level_requirement
        self.reward = reward  # Reward can be experience, or gold (a list of [experience, gold] in numerical number)
        self.completed_quest = False  # Track if the quest is completed

    def is_available(self, player):
        """Check if the quest is available for the player."""
        if player.level < self.level_requirement and self.completed_quest == False:
            if self.completed_quest == True:
                print(f"Quest '{self.name}' is already completed.")
            else:
                print(f"Quest '{self.name}' is not available. You need to be at least level {self.level_requirement} to take this quest.")
            return False
        else:
            return True
    
    def give_reward(self, player, completed=True):
        """Give the reward to the player."""
        if self.completed_quest == True:
            if isinstance(self.reward, list) and len(self.reward) == 2:
                player.experience += self.reward[0]  # Add experience to the player
                if self.reward[1] != 0:
                    player.wallet.add_gold(self.reward[1])  # Add gold to the player's wallet


"""Classes"""
#fighting classes that the player can choose from
warrior = fighting_Class("Warrior", base_health=120, base_damage=20, base_speed=10, lvl_inc_health=15, lvl_inc_damage=5, lvl_inc_speed=1, att_range=1)

ranger = fighting_Class("Ranger", base_health=100, base_damage=25, base_speed=15, lvl_inc_health=10, lvl_inc_damage=4, lvl_inc_speed=2, att_range=3)

mage = fighting_Class("Mage", base_health=80, base_damage=35, base_speed=8, lvl_inc_health=8, lvl_inc_damage=6, lvl_inc_speed=1, att_range=4)
#adding more fighting classes allowed

"""Races"""
#races that the player can choose from
human = race("Human", base_health=100, base_damage=10, base_speed=10, lvl_inc_health=2, lvl_inc_damage=2, lvl_inc_speed=2, allowed_classes=[warrior, ranger, mage])

elf = race("Elf", base_health=70, base_damage=12, base_speed=12, lvl_inc_health=2, lvl_inc_damage=2, lvl_inc_speed=2, allowed_classes=[ranger, mage])

dragonborn = race("Dragonborn", base_health=120, base_damage=15, base_speed=8, lvl_inc_health=4, lvl_inc_damage=4, lvl_inc_speed=1, allowed_classes=[warrior, mage])

wisp = race("Wisp", base_health=40, base_damage=3, base_speed=18, lvl_inc_health=1, lvl_inc_damage=2, lvl_inc_speed=3, allowed_classes=[mage])
#adding more races allowed

"""Starting Quests"""

slimes_quest = guild_Quest("Slime Hunt", "Defeat 5 slimes in the nearby forest.", 1, [50, 10])  # 50 experience and 10 gold reward")

def create_character():
    global player
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
            fighting_Class_Choice = warrior
        case "ranger": 
            fighting_Class_Choice = ranger
        case "mage":  
            fighting_Class_Choice = mage
    
    print(f"You have chosen the {fighting_Class_Choice.name} class.")
    print(f"Thats a great choice, {player_name}! You are now a level 1 {player_race} {player_class}.\nYour starting stats are: \nHealth: {fighting_Class_Choice.base_health + character_race.base_health}, \nDamage: {fighting_Class_Choice.base_damage + character_race.base_damage}, \nSpeed: {fighting_Class_Choice.base_speed + character_race.base_speed}.\nYou will gain:\n{fighting_Class_Choice.lvl_inc_health + character_race.lvl_inc_health} health, \n{fighting_Class_Choice.lvl_inc_damage + character_race.lvl_inc_damage} damage, \n{fighting_Class_Choice.lvl_inc_speed + character_race.lvl_inc_speed} speed per level.")
    print("This will deviate a bit by +/- 3 points per level to add a bit of spice to the game.")
    print(f"You are ready to embark on your adventure {player_name}!")
    player = player_Character(player_name, 1, character_race, fighting_Class_Choice) #Creates the character
    player.lvl_exp_requirement() #calculates the experience required for the next level
    starting_adventure()  # Start the adventure after character creation
    
def starting_adventure():
    """Placeholder for the starting adventure logic."""
    print("Your adventure begins now! Explore the world, fight enemies, and level up your character.")
    # Placeholder for adventure logic
    
    """"print("You encounter a lone bandit on the road.")
    bandit = Enemy("Bandit", 1, human, warrior)  # Create an enemy for the player to fight
    print(player.range)
    Battle(player, bandit).start_battle()  # Start the battle with the bandit
    #first check for battle logic.. Works
    """
    
    
    print("""In the Inn of the small village of Treiten. Waking up in the 
          unfamiliar room you find yourself in, you look around to notice
          nothing in particular. Walking out of the Inn the Innkeeper reminds
          you that last night was the last night of your stay. He wishes you
          luck on your journey and tells you to come back if you need a place
          to stay. 
          
          In need of money, you decide to head to the adventurers guild. 
          But with your level 1 character, you know that you won't be able to 
          take any high paying jobs.
          
          You walk into the guild and see the Adventure Board (As its called) with
          all of the jobs available. 
          
          there are 3 available jobs for your current level.""")
    
    
if __name__ == "__main__":
    create_character()  # Call the function to create a character
'''
if __name__ == "__main__":
    game = game_Window()  # Create an instance of the game window
    game.run()  # Run the game window
    game.print_onto_window("Welcome to the Text Adventure Game!")  # Print welcome message onto the window
    create_character()  # Call the function to create a character  
    '''
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
        print("fuck you.. you WERE ONE step closer to not being a failure.. but u fucked that up")
        leaveOff = False
        action = False
    elif officeLeave == "b":
        print("you are doing better than yesterday")
        leaveOff = True
    else:
       officeLeave = input("you need to answer the question: ")

"""