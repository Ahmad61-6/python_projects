
"""
╔══════════════════════════════════════════════════════════════════╗
║              THE ENDLESS ROAD - A Text Adventure               ║
║                   Grade 9 Python Project                       ║
║          Storyline, Decision Paths & Survival Mechanics        ║
╚══════════════════════════════════════════════════════════════════╝

HOW TO RUN THIS GAME:
    python the_endless_road.py


CONTROLS:
    - Type commands and press ENTER
    - The game will always show you your options
    - Commands are NOT case-sensitive (so 'DINER' = 'diner')
"""

import random
import time
import sys
import os

# ─────────────────────────────────────────────
#   UTILITY FUNCTIONS (The Helper Tools)
# ─────────────────────────────────────────────

def slow_print(text, delay=0.03):
    """Prints text letter by letter for dramatic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def box_print(text, width=60):
    """Prints text inside a neat box."""
    lines = text.split('\n')
    print("╔" + "═" * (width - 2) + "╗")
    for line in lines:
        padded = line.center(width - 2)
        print("║" + padded + "║")
    print("╚" + "═" * (width - 2) + "╝")

def section_break():
    print("\n" + "─" * 60 + "\n")

def pause(seconds=1.5):
    time.sleep(seconds)

def clear():
    """Clears the screen so things feel fresh."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Shows the game title banner."""
    print("""
\033[91m
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌲  T H E   E N D L E S S   R O A D  🌲                 ║
║                                                              ║
║         You drove in. Now can you drive OUT?                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
\033[0m""")

# ─────────────────────────────────────────────
#   GAME STATE (The Brain of the Game)
# ─────────────────────────────────────────────

def create_player():
    """Creates a brand new player with all starting stats."""
    return {
        "name": "",
        "health": 100,
        "sanity": 100,
        "inventory": [],
        "location": "town_center",
        "moves": 0,          # Every command = 1 move; 5 moves = night falls
        "day": 1,
        "inside": False,     # Is the player in a building?
        "has_talisman_hung": False,  # Is talisman on the door of safehouse?
        "safehouse": None,   # Which building is the player's safe house?
        "diary_pages": [],   # Collected diary pages for the radio puzzle
        "radio_fixed": False,
        "survived_nights": 0,
        "cave_turns": 0,     # Tracks turns inside the cave (max = 3!)
        "in_cave": False,
        "traitor_invited": False,
        "game_over": False,
        "won": False,
        "items_looted": [],  # Tracks what was already taken from each spot
    }

def create_world(traitor_name):
    """
    Builds the entire game world — all locations, items, NPCs.
    The traitor is randomly chosen each playthrough!
    """
    world = {
        "town_center": {
            "name": "🏙️  Town Center",
            "desc": (
                "You're standing in the middle of a tiny, deserted town. "
                "Old shop signs creak in the wind. A broken fountain "
                "drips rusty water. There's graffiti on the wall that says: "
                "'DON\'T TRUST THE SMILES.' Roads lead in every direction, "
                "but they ALL loop back here..."
            ),
            "exits": {
                "diner": "Go to the Old Diner",
                "church": "Go to the Abandoned Church",
                "gas station": "Go to the Gas Station",
                "forest": "Go into the Dark Forest",
                "hill": "Go to the Radio Tower Hill",
                "cave": "Go to the Cave Entrance",
                "sheriff": "Go to the Sheriff's Office",
                "house": "Go to the Old Farmhouse (Safe House)",
            },
            "npc": None,
            "items": ["crumpled map"],
        },

        "diner": {
            "name": "🍽️  The Rusty Spoon Diner",
            "desc": (
                "The diner smells like burnt coffee and old grease. "
                "Booths are ripped, menus are faded. A ceiling fan spins slowly. "
                "Behind the counter, a stout cook with flour on their apron "
                "stares at you with a smile that's just a little too wide."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": "Cook" if traitor_name == "Cook" else "Cook (Friendly)",
            "items": ["canned food", "bandages", "diary page 2"],
            "npc_name": "Cook",
            "is_traitor": traitor_name == "Cook",
            "searched": False,
            "inside": True,
        },

        "church": {
            "name": "⛪  Abandoned Church",
            "desc": (
                "The wooden church looks half-eaten by rot. "
                "Pews are overturned. Stained glass windows let in dusty light. "
                "On the altar you can see something GLOWING softly... "
                "Could that be the Talisman everyone's been whispering about?"
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["talisman", "diary page 1"],
            "searched": False,
            "inside": True,
        },

        "gas_station": {
            "name": "⛽  Abandoned Gas Station",
            "desc": (
                "Rusty pumps stand like old soldiers. The shop window is smashed. "
                "Inside, shelves are knocked over, but some stuff is still intact. "
                "You spot some wires hanging from the ceiling and a toolbox "
                "kicked into the corner."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["copper wire", "bandages", "diary page 3"],
            "searched": False,
            "inside": True,
        },

        "forest": {
            "name": "🌲  The Dark Forest",
            "desc": (
                "The trees are so tall they block the sky. It's eerily quiet "
                "except for the sound of something breathing just outside your sight. "
                "Broken branches and strange footprints litter the ground. "
                "You find old supplies left by someone who clearly ran away fast."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["antenna piece", "canned food"],
            "searched": False,
            "inside": False,
            "is_dangerous": True,
        },

        "hill": {
            "name": "📡  Radio Tower Hill",
            "desc": (
                "You hike up the steep hill to find a rusted old radio tower. "
                "Most of it is broken and overgrown with vines. "
                "There's a control panel at the base — scratched and beaten up, "
                "but maybe it can still WORK if someone was smart enough to fix it..."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["old manual"],
            "searched": False,
            "inside": False,
        },

        "cave": {
            "name": "🕳️  The Cave Entrance",
            "desc": (
                "A dark crack in the hillside. Cold air breathes out of it "
                "like the cave is alive. You can hear... snoring? Deep, rumbling, "
                "WRONG-sounding snoring. That must be the monsters sleeping. "
                "You could sneak in and grab rare items — but you MUST leave "
                "within 3 turns or they wake up. GAME OVER."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["battery pack", "signal booster", "extra health kit", "bonus rations"],
            "searched": False,
            "inside": True,
            "is_cave": True,
        },

        "sheriff": {
            "name": "🚔  Sheriff's Office",
            "desc": (
                "The sheriff's office looks surprisingly tidy compared to everything else. "
                "A tall person in a dusty uniform sits at a desk, writing something. "
                "They look up and give you a calm, friendly nod. "
                "'You look lost,' they say. 'This town... it does things to people.'"
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": "Sheriff" if traitor_name == "Sheriff" else "Sheriff (Friendly)",
            "npc_name": "Sheriff",
            "items": ["diary page 4", "first aid kit"],
            "is_traitor": traitor_name == "Sheriff",
            "searched": False,
            "inside": True,
        },

        "house": {
            "name": "🏚️  The Old Farmhouse",
            "desc": (
                "A creaky, worn-down farmhouse at the edge of town. "
                "The windows are grimy but the doors have thick wooden bars. "
                "If you could hang a Talisman on that door... "
                "this place might just be safe enough to survive the night."
            ),
            "exits": {"town_center": "Go back to Town Center"},
            "npc": None,
            "items": ["matches", "diary page 5"],
            "searched": False,
            "inside": True,
            "is_safehouse": True,
        },
    }
    return world

# ─────────────────────────────────────────────
#   DIARY PAGES (Clues to solve the puzzle)
# ─────────────────────────────────────────────

DIARY_PAGES = {
    "diary page 1": (
        "📖 DIARY PAGE 1 — Found in the Church:\n"
        "   '...the old preacher said the frequency would save us all.\n"
        "    He said the FIRST number is the number of crows\n"
        "    that sat on the fallen tree. I counted them myself.\n"
        "    There were FOUR of them. I am certain of it...'"
    ),
    "diary page 2": (
        "📖 DIARY PAGE 2 — Found in the Diner:\n"
        "   '...the cook told me the SECOND number before the monsters\n"
        "    took her. She whispered it between sobs: TWO.\n"
        "    She said it twice, like it mattered. Maybe it does.'"
    ),
    "diary page 3": (
        "📖 DIARY PAGE 3 — Found in the Gas Station:\n"
        "   '...scrawled on the gas pump in red marker:\n"
        "    THE THIRD NUMBER IS THE NUMBER OF DAYS A WEEK.\n"
        "    I think someone left this on purpose. SEVEN.'"
    ),
    "diary page 4": (
        "📖 DIARY PAGE 4 — Found in the Sheriff's Office:\n"
        "   '...the Sheriff told me about the radio — how it only works\n"
        "    on one specific channel. The FOURTH number, he said,\n"
        "    is the number of fingers on one hand. FIVE.\n"
        "    The full code: ????. You have all the pieces now.'"
    ),
    "diary page 5": (
        "📖 DIARY PAGE 5 — Found in the Farmhouse:\n"
        "   '...if you are reading this, you found my hiding spot.\n"
        "    The radio frequency is FOUR DIGITS. You must find all four.\n"
        "    Broadcast it and help will come. I am almost out of time.\n"
        "    Do NOT trust everyone in this town. One of them is not human.'"
    ),
}

# The secret radio code = 4275 (crow=4, diner=2, week days=7, fingers=5)
RADIO_CODE = "4275"

# ─────────────────────────────────────────────
#   NPC DIALOGUE
# ─────────────────────────────────────────────

def npc_dialogue(npc_name, is_traitor, player, world_location):
    """Handles what NPCs say when you talk to them."""
    print()
    if npc_name == "Cook":
        if is_traitor:
            slow_print("🧑‍🍳 Cook: 'Oh sweetie, you poor thing! You must be SO scared.'")
            slow_print("         'You should set up your safe house at the farmhouse.'")
            slow_print("         'I'd LOVE to come stay with you. Keep you company...'")
            slow_print("         Their smile seems to flicker for just a second.")
            slow_print("         [You can INVITE them to your safehouse — but should you?]")
        else:
            slow_print("🧑‍🍳 Cook: 'Listen to me carefully. Don't go out at night. Ever.'")
            slow_print("         'The Talisman in the church — GET IT. It's real.'")
            slow_print("         'And fix that radio tower on the hill. It's your only way out.'")
            slow_print("         'I heard the frequency code is hidden in diary pages around town.'")

    elif npc_name == "Sheriff":
        if is_traitor:
            slow_print("🚔 Sheriff: 'Well hey there, traveller. You seem smart.'")
            slow_print("            'I know all the safe spots in town. Trust me.'")
            slow_print("            'You should let me into your safehouse tonight.'")
            slow_print("            'I can... keep an eye on things.' *long pause* 'For you.'")
            slow_print("            [You can INVITE them to your safehouse — but should you?]")
        else:
            slow_print("🚔 Sheriff: 'Son/Ma'am, I ain't gonna sugarcoat this.'")
            slow_print("            'This town is cursed. Those THINGS come out at night.'")
            slow_print("            'The only escape is the radio tower up on the hill.'")
            slow_print("            'You need parts: wire, antenna, battery, and a signal booster.'")
            slow_print("            'And don't trust everyone who smiles at you.'")
    print()

# ─────────────────────────────────────────────
#   STATUS DISPLAY
# ─────────────────────────────────────────────

def show_status(player):
    """Shows the player their current stats — always visible."""
    time_of_day = get_time_of_day(player)
    time_color = "\033[91m" if time_of_day == "🌙 NIGHT" else "\033[93m"
    reset = "\033[0m"

    health_bar = make_bar(player["health"], 100, 20, "❤️")
    sanity_bar = make_bar(player["sanity"], 100, 20, "🧠")

    print(f"\n{'─'*60}")
    print(f"  👤 {player['name']}  |  📅 Day {player['day']}  |  {time_color}{time_of_day}{reset}")
    print(f"  ❤️  Health:  {health_bar} {player['health']}/100")
    print(f"  🧠  Sanity:  {sanity_bar} {player['sanity']}/100")
    print(f"  🎒  Bag:     {', '.join(player['inventory']) if player['inventory'] else '(empty)'}")
    print(f"  📍 Location: {player['location'].replace('_', ' ').title()}")
    moves_left = max(0, 5 - (player['moves'] % 5))
    print(f"  ⏳ Moves until dark: {moves_left}")
    if player["in_cave"]:
        print(f"  ⚠️  CAVE TURNS LEFT: {3 - player['cave_turns']} (GET OUT BEFORE 0!)")
    print(f"{'─'*60}\n")

def make_bar(value, maximum, length, emoji):
    """Creates a visual progress bar."""
    filled = int((value / maximum) * length)
    empty = length - filled
    return f"[{'█' * filled}{'░' * empty}]"

def get_time_of_day(player):
    """Figures out if it's day or night based on move count."""
    # Night falls every 5 moves
    cycle = player["moves"] % 10
    if cycle < 5:
        return "☀️  DAY"
    else:
        return "🌙 NIGHT"

def is_night(player):
    return player["moves"] % 10 >= 5

# ─────────────────────────────────────────────
#   NIGHT ATTACK SYSTEM
# ─────────────────────────────────────────────

def check_night_danger(player, world):
    """
    If it's night and the player is outside without protection —
    the monsters come. This runs after every move.
    """
    if not is_night(player):
        return  # Safe! It's daytime.

    loc = world.get(player["location"], {})
    is_inside = loc.get("inside", False)
    has_talisman_protection = player["has_talisman_hung"] and player["safehouse"] == player["location"]

    if is_inside and has_talisman_protection:
        # FULLY SAFE
        return

    elif is_inside and not has_talisman_protection:
        # Inside but no talisman — monsters can still get in
        slow_print("\n😰 You're inside, but you have NO Talisman on the door...")
        slow_print("   You hear scratching on the walls. Sniffing at the windows.")

        if player["sanity"] < 50:
            slow_print("   Wait... is that a child crying outside? Should you let them in?")
            slow_print("   (Your sanity is LOW — your mind is playing tricks on you!)")
        else:
            slow_print("   Something slams against the door. HARD.")

        damage = random.randint(15, 30)
        player["health"] -= damage
        player["sanity"] -= 10
        slow_print(f"   A claw rakes through the window! You lose {damage} health! 😱")

    else:
        # Outside at night = very dangerous
        slow_print("\n🌑 You're OUTSIDE after dark. This is extremely dangerous!")
        slow_print("   You hear footsteps. Close. Then... laughter. Wrong laughter.")
        slow_print("   A figure steps into the moonlight, smiling too wide...")

        if player["sanity"] < 50:
            slow_print("   Wait, is that your friend? They look so friendly...")
            slow_print("   (WARNING: LOW SANITY is making you see them differently!)")
        else:
            slow_print("   Its eyes are WRONG. Its smile doesn't reach its eyes.")
            slow_print("   You RUN. You barely escape — but not without damage.")

        damage = random.randint(25, 40)
        sanity_loss = random.randint(15, 25)
        player["health"] -= damage
        player["sanity"] -= sanity_loss
        slow_print(f"   You lose {damage} health and {sanity_loss} sanity! 😰")

    check_death(player)

def check_death(player):
    """Checks if the player is dead or has lost their mind."""
    if player["health"] <= 0:
        player["health"] = 0
        slow_print("\n\n💀 Your health has reached ZERO...")
        slow_print("   Everything goes dark.")
        slow_print("   The town has claimed another soul.")
        pause(2)
        game_over_screen(player, reason="health")
        player["game_over"] = True

    elif player["sanity"] <= 0:
        player["sanity"] = 0
        slow_print("\n\n🌀 Your sanity has shattered completely...")
        slow_print("   You start laughing for no reason. Then crying.")
        slow_print("   Then you walk to the edge of the woods and just... keep going.")
        slow_print("   The smiling figures welcome you. You smile back. You're one of them now.")
        pause(2)
        game_over_screen(player, reason="sanity")
        player["game_over"] = True

# ─────────────────────────────────────────────
#   GAME OVER / WIN SCREENS
# ─────────────────────────────────────────────

def game_over_screen(player, reason="health"):
    clear()
    print("\n\033[91m")
    box_print("💀  G A M E   O V E R  💀")
    print("\033[0m")
    print(f"\n  You survived {player['day']} day(s) and took {player['moves']} actions.")
    print(f"  Items collected: {', '.join(player['inventory']) if player['inventory'] else 'None'}")

    if reason == "health":
        slow_print("  You fought hard but the darkness was too much to bear.")
    elif reason == "sanity":
        slow_print("  The town broke your mind before it broke your body.")
    elif reason == "cave":
        slow_print("  You got greedy in the cave. The monsters woke up. That was your last mistake.")
    elif reason == "traitor":
        slow_print("  You trusted the wrong person. They opened a window in the night.")
    elif reason == "trapped":
        slow_print("  You never fixed the radio. The town swallowed you whole.")

    print("\n  Better luck next time. The road goes on forever...")
    print("\n  (Run the game again to try a new playthrough — traitor is random each time!)\n")

def win_screen(player):
    clear()
    print("\n\033[92m")
    box_print("🎉  Y O U   E S C A P E D !  🎉")
    print("\033[0m")
    slow_print(f"\n  🚁 The helicopter descends through the morning fog...")
    slow_print("  The pilot stares at the town below as you climb in.")
    slow_print("  'What IS this place?' they ask.")
    slow_print("  You just shake your head and look forward. Never back.")
    print()
    print(f"  📊 Final Stats:")
    print(f"     ❤️  Health Remaining: {player['health']}/100")
    print(f"     🧠  Sanity Remaining: {player['sanity']}/100")
    print(f"     📅  Days Survived:    {player['day']}")
    print(f"     👣  Total Moves:      {player['moves']}")
    print(f"     🎒  Items Collected:  {', '.join(player['inventory'])}")
    print()

    # Give a rating based on performance
    score = player["health"] + player["sanity"] + (player["day"] * 5)
    if score > 180:
        rating = "⭐⭐⭐  MASTER SURVIVOR — You barely broke a sweat."
    elif score > 120:
        rating = "⭐⭐    SURVIVOR — Close calls, but you made it!"
    else:
        rating = "⭐     BARELY MADE IT — One more scare and it was over."

    print(f"  🏆 Rating: {rating}")
    print("\n  The Endless Road has been beaten. For now.\n")

# ─────────────────────────────────────────────
#   MOVE TICK (happens after every player action)
# ─────────────────────────────────────────────

def tick(player, world):
    """
    Called after every player action.
    Counts moves, switches day/night, triggers events.
    """
    if player["game_over"] or player["won"]:
        return

    player["moves"] += 1

    # Check for new night or new day
    cycle = player["moves"] % 10
    if cycle == 5:
        player["day"] += 1
        player["survived_nights"] += 1
        slow_print("\n\n🌙 The sun has set. The streets go quiet. TOO quiet...")
        slow_print("   You can hear something moving in the woods at the edge of town.")
        slow_print("   The monsters are WAKING UP. Get inside with a Talisman — FAST!\n")
        pause(2)
    elif cycle == 0 and player["moves"] > 0:
        slow_print("\n\n☀️  A new day dawns. The monsters slink back into their caves.")
        slow_print("   You have survived another night. But the clock is ticking.\n")
        pause(1.5)

    # Random creepy events (keep the player on edge)
    if random.random() < 0.15:
        creepy_event(player)

    # Night danger check
    check_night_danger(player, world)

def creepy_event(player):
    """Random atmospheric events to freak the player out."""
    events = [
        "👁️  You notice scratch marks on the door of a nearby building. They look... FRESH.",
        "🐦  A crow lands next to you and stares. It doesn't blink. It NEVER blinks.",
        "📻  A radio somewhere crackles with static, then whispers your name. Then silence.",
        "🌫️  The fog thickens suddenly. You can only see a few feet ahead.",
        "🚶  In the corner of your eye, you see a figure wave at you from a window. When you look — nobody's there.",
        "🩸  You find a handprint on a wall. Still wet.",
    ]

    if player["sanity"] < 50:
        low_sanity_events = [
            "🌀  You hear laughter from behind you. When you spin around — nothing. Just your reflection in a window. But it kept laughing.",
            "😊  A smiling figure beckons to you from the tree line. They look so FRIENDLY... snap out of it! Your sanity is low!",
            "🪞  For a moment, you see the town as a beautiful paradise. Then you blink. It's still a ruin. What's happening to your mind?",
        ]
        events.extend(low_sanity_events)

    chosen = random.choice(events)
    slow_print(f"\n  {chosen}")
    player["sanity"] = max(0, player["sanity"] - 5)

# ─────────────────────────────────────────────
#   ACTION HANDLERS
# ─────────────────────────────────────────────

def action_look(player, world):
    """Look around your current location."""
    loc_key = player["location"]
    loc = world[loc_key]
    print()
    box_print(loc["name"].replace("🍽️ ", "").replace("⛪ ", "").replace("⛽ ", "").strip())
    slow_print(f"\n  {loc['desc']}")

    # Show items still available here
    items_here = [i for i in loc.get("items", []) if i not in player["items_looted"]]
    if items_here:
        print(f"\n  🔍 You can see: {', '.join(items_here)}")
    else:
        print("\n  🔍 Nothing useful left here.")

    # Show NPC if present
    if loc.get("npc"):
        print(f"\n  👤 NPC here: {loc['npc']}")

    # Show exits
    print("\n  🚪 Exits:")
    for direction, description in loc.get("exits", {}).items():
        clean_direction = direction.replace("_", " ")
        print(f"    → {description} (type: '{clean_direction}')")

    # Cave warning
    if loc.get("is_cave"):
        print("\n  ⚠️  CAVE WARNING: You have exactly 3 turns inside before monsters wake up!")

def action_go(player, world, destination):
    """Move the player to a new location."""
    loc = world[player["location"]]
    exits = loc.get("exits", {})

    # Handle gas station key name
    if destination == "gas station":
        destination = "gas station"

    # Find the exit (flexible matching)
    matched = None
    for exit_key in exits:
        clean_exit = exit_key.replace("_", " ")
        if destination in clean_exit or clean_exit in destination or destination in exit_key:
            matched = exit_key
            break

    # Map destination names to world keys
    key_map = {
        "town center": "town_center",  
        "center": "town_center",
        "diner": "diner",
        "church": "church",
        "gas station": "gas_station",
        "gas_station": "gas_station",
        "forest": "forest",
        "hill": "hill",
        "cave": "cave",
        "sheriff": "sheriff",
        "house": "house",
    }

    target_key = key_map.get(destination) or key_map.get(matched)

    if target_key and target_key in world:
        # Cave-specific logic
        if player["in_cave"]:
            if target_key != "cave":
                # Leaving cave
                player["in_cave"] = False
                player["cave_turns"] = 0
                slow_print("\n🕳️  You stumble out of the cave, blinking in the light. You're safe... for now.")

        if target_key == "cave":
            if is_night(player):
                slow_print("\n🌙 The cave is even MORE dangerous at night. You can't go in now.")
                return
            player["in_cave"] = True
            player["cave_turns"] = 0

        old_location = player["location"]
        player["location"] = target_key
        loc_data = world[target_key]

        slow_print(f"\n  ➡️  You make your way to {loc_data['name']}...")

        # Update inside/outside status
        player["inside"] = loc_data.get("inside", False)

        # Forest danger during day
        if target_key == "forest" and not is_night(player):
            if random.random() < 0.4:
                slow_print("\n  🌲 A branch snaps you in the face! You trip on a root!")
                damage = random.randint(5, 15)
                player["health"] -= damage
                slow_print(f"  You lose {damage} health from clumsy stumbling!")

        tick(player, world)
    else:
        slow_print(f"\n  ❌ You can't go '{destination}' from here. Check your exits!")

def action_take(player, world, item_name):
    """Pick up an item from the current location."""
    loc_key = player["location"]
    loc = world[loc_key]
    items_here = [i for i in loc.get("items", []) if i not in player["items_looted"]]

    # Find item (flexible matching)
    found = None
    for item in items_here:
        if item_name in item or item in item_name:
            found = item
            break

    if found:
        player["inventory"].append(found)
        player["items_looted"].append(found)
        slow_print(f"\n  ✅ You picked up: {found}!")

        # Cave turn tracking
        if player["in_cave"]:
            player["cave_turns"] += 1
            remaining = 3 - player["cave_turns"]
            if remaining > 0:
                slow_print(f"  ⚠️  CAVE ALERT: {remaining} turn(s) left before monsters wake!")
            else:
                slow_print("  ⚠️  That's 3 items from the cave. You should LEAVE NOW!")

        # Special item messages
        if "talisman" in found.lower():
            slow_print("  ✨ The Talisman glows warmly in your hand. This will protect you...")
        elif "diary" in found.lower():
            slow_print(f"\n  {DIARY_PAGES.get(found, 'A cryptic diary page.')}")

        # Special: if player tries to grab a 4th cave item
        tick(player, world)

    else:
        slow_print(f"\n  ❌ You can't find '{item_name}' here.")
        if items_here:
            slow_print(f"  Items you CAN take: {', '.join(items_here)}")

def action_search(player, world):
    """Search the current location thoroughly."""
    loc_key = player["location"]
    loc = world[loc_key]

    if loc.get("searched"):
        slow_print("\n  🔍 You've already searched here thoroughly. Nothing new to find.")
        tick(player, world)
        return

    slow_print(f"\n  🔍 You carefully search {loc['name']}...")
    pause(1)
    items_here = [i for i in loc.get("items", []) if i not in player["items_looted"]]

    if items_here:
        slow_print(f"  You find: {', '.join(items_here)}")
        slow_print("  Type 'take [item name]' to pick things up!")
    else:
        slow_print("  You search every corner but find nothing useful.")

    loc["searched"] = True
    tick(player, world)

def action_hang_talisman(player, world):
    """Hang the talisman on the safehouse door."""
    if "talisman" not in player["inventory"]:
        slow_print("\n  ❌ You don't have the Talisman! Find it in the Abandoned Church first.")
        return

    loc_key = player["location"]
    loc = world[loc_key]

    if not loc.get("inside", False):
        slow_print("\n  ❌ You need to be INSIDE a building to hang the Talisman.")
        return

    if not loc.get("is_safehouse", False):
        slow_print("\n  ⚠️  This building could work as a safehouse...")
        slow_print("  You hang the Talisman here. This is now your safe house!")
        loc["is_safehouse"] = True  # Allow any inside building

    player["has_talisman_hung"] = True
    player["safehouse"] = loc_key
    slow_print(f"\n  ✨ You carefully hang the Talisman on the door of {loc['name']}.")
    slow_print("  It glows with a soft golden light. The monsters won't get through this.")
    slow_print("  This is now your SAFE HOUSE. Return here before night falls!")
    tick(player, world)

def action_use_health_kit(player, item_name):
    """Use a health/first aid item."""
    heal_items = {
        "bandages": 20,
        "first aid kit": 40,
        "extra health kit": 50,
    }

    for item, heal_amount in heal_items.items():
        if item in item_name or item_name in item:
            if item in player["inventory"]:
                player["health"] = min(100, player["health"] + heal_amount)
                player["inventory"].remove(item)
                slow_print(f"\n  💊 You use the {item}. Health restored by {heal_amount}!")
                slow_print(f"  ❤️  Health is now {player['health']}/100.")
                return
            else:
                slow_print(f"\n  ❌ You don't have {item} in your bag.")
                return

    slow_print(f"\n  ❌ '{item_name}' isn't something you can use for healing.")

def action_talk(player, world):
    """Talk to the NPC in the current location."""
    loc_key = player["location"]
    loc = world[loc_key]

    if not loc.get("npc"):
        slow_print("\n  👤 There's nobody here to talk to.")
        return

    npc_name = loc.get("npc_name")
    is_traitor = loc.get("is_traitor", False)

    npc_dialogue(npc_name, is_traitor, player, loc)
    tick(player, world)

def action_invite(player, world):
    """Invite the NPC to your safehouse — RISKY if they're the traitor!"""
    loc_key = player["location"]
    loc = world[loc_key]

    if not loc.get("npc"):
        slow_print("\n  👤 There's nobody here to invite.")
        return

    if not player["safehouse"]:
        slow_print("\n  ❌ You don't have a safe house yet! Set one up first.")
        return

    npc_name = loc.get("npc_name")
    is_traitor = loc.get("is_traitor", False)

    slow_print(f"\n  You invite {npc_name} to shelter in your safe house tonight...")
    player["traitor_invited"] = is_traitor

    if is_traitor:
        slow_print(f"  {npc_name} grins widely. 'Of course. I'd be... delighted.'")
        slow_print("  Something about that smile makes your stomach drop. But you push the feeling away.")

        # Traitor event triggers at night
        if is_night(player):
            slow_print(f"\n⚠️  That night, you wake to the sound of a window being opened...")
            slow_print(f"  {npc_name} stands there, window wide, smiling at the darkness outside.")
            slow_print("  The monsters pour through the gap like smoke. You never had a chance.")
            pause(2)
            game_over_screen(player, reason="traitor")
            player["game_over"] = True
    else:
        slow_print(f"  {npc_name} nods gratefully. 'Thank you. I'll keep watch while you sleep.'")
        slow_print("  You feel safer. Sanity restored by 10.")
        player["sanity"] = min(100, player["sanity"] + 10)

    tick(player, world)

def action_fix_radio(player, world):
    """Try to fix the radio tower — need all 4 parts!"""
    if player["location"] != "hill":
        slow_print("\n  📡 You need to be at the Radio Tower Hill to fix the radio!")
        return

    required_parts = ["copper wire", "antenna piece", "battery pack", "signal booster"]
    missing = [part for part in required_parts if part not in player["inventory"]]

    if missing:
        slow_print("\n  🔧 You try to fix the radio, but you're missing parts!")
        slow_print(f"  Still need: {', '.join(missing)}")
        slow_print("  Check the gas station, forest, and cave for parts.")
        return

    slow_print("\n  🔧 You have ALL the parts! You start wiring them in...")
    slow_print("  Copper wire... check. Antenna piece... check.")
    slow_print("  Battery pack... check. Signal booster... check.")
    slow_print("\n  The old radio tower GROANS and CRACKLES to life!")
    slow_print("  Static fills the air. But which frequency do you use?")

    # Check diary pages collected
    pages_found = [p for p in player["diary_pages"] if p in player["inventory"]]
    diary_count = len([i for i in player["inventory"] if "diary page" in i])
    if diary_count < 4:
        slow_print(f"\n  📖 You've only found {diary_count}/4 diary page clues.")
        slow_print("  The pages are hidden across town — find them all to learn the code!")

    player["radio_fixed"] = True
    slow_print("\n  ✅ Radio fixed! Now use 'broadcast [4-digit code]' to call for help!")
    tick(player, world)

def action_broadcast(player, code_attempt):
    """Try to broadcast the distress signal with the correct frequency."""
    if not player["radio_fixed"]:
        slow_print("\n  📡 The radio isn't fixed yet! Find the parts and fix it first.")
        return

    if player["location"] != "hill":
        slow_print("\n  📡 You need to be at the Radio Tower to broadcast!")
        return

    slow_print(f"\n  📡 You tune the dial to frequency {code_attempt}...")

    if code_attempt == RADIO_CODE:
        slow_print("  The static clears. A voice crackles through!")
        slow_print("  'Unknown signal received. Location locked. Sending rescue.'")
        slow_print("  'Helicopter ETA: Sunrise. Hold tight.'")
        slow_print("\n  You did it. You actually did it.")
        slow_print("  You sit down on the hill and wait, watching the horizon.")
        slow_print("  For the first time since you arrived, you smile.")
        pause(2)
        player["won"] = True
    else:
        slow_print("  Nothing but static. That's not the right frequency.")
        slow_print("  Read your diary pages carefully — the clues are all there!")
        player["sanity"] = max(0, player["sanity"] - 5)

def action_cave_extra(player):
    """Tries to grab a 4th item from the cave — GAME OVER!"""
    if not player["in_cave"]:
        slow_print("\n  You're not in the cave.")
        return

    if player["cave_turns"] >= 3:
        slow_print("\n  🕳️  You reach greedily for one more item...")
        slow_print("  Then — SILENCE. The snoring stops.")
        slow_print("  Slowly, one by one, eyes open in the darkness. Red eyes. LOTS of them.")
        slow_print("  You scream. Nobody outside hears it.")
        pause(2)
        game_over_screen(player, reason="cave")
        player["game_over"] = True

def action_inventory(player):
    """Show detailed inventory."""
    print("\n  🎒 YOUR BACKPACK:")
    if not player["inventory"]:
        slow_print("  (empty — you haven't found anything yet!)")
    else:
        for item in player["inventory"]:
            if "diary page" in item:
                print(f"   📖 {item}")
            elif item in ["copper wire", "antenna piece", "battery pack", "signal booster"]:
                print(f"   🔧 {item}  ← radio part!")
            elif item == "talisman":
                print(f"   ✨ {item}  ← protect safehouse with 'hang talisman'")
            elif item in ["bandages", "first aid kit", "extra health kit"]:
                print(f"   💊 {item}  ← use with 'use {item}'")
            else:
                print(f"   🎁 {item}")
    print()

def action_read_diary(player, page_name):
    """Read a diary page that's in your inventory."""
    found = None
    for item in player["inventory"]:
        if page_name in item or item in page_name or "diary" in page_name:
            if "diary page" in item:
                found = item
                break

    if found and found in DIARY_PAGES:
        slow_print(f"\n  {DIARY_PAGES[found]}")
    elif found:
        slow_print(f"\n  {found}: A crumpled page. Too damaged to read clearly.")
    else:
        slow_print("\n  ❌ You don't have that diary page. Find them across town!")

def action_help(player, world):
    """Show all available commands."""
    print("""
  ╔══════════════════════════════════════════════════╗
  ║             📋 COMMAND CHEAT SHEET              ║
  ╠══════════════════════════════════════════════════╣
  ║ MOVEMENT                                        ║
  ║   go [place]     → Move to a location           ║
  ║   look / l       → Describe where you are       ║
  ╠══════════════════════════════════════════════════╣
  ║ ITEMS                                           ║
  ║   take [item]    → Pick up an item              ║
  ║   search / s     → Search the area              ║
  ║   inventory / i  → Check your bag               ║
  ║   use [item]     → Use health/bandages           ║
  ║   read diary     → Read a diary page            ║
  ╠══════════════════════════════════════════════════╣
  ║ SURVIVAL                                        ║
  ║   hang talisman  → Protect your safehouse       ║
  ║   fix radio      → Repair the radio tower       ║
  ║   broadcast XXXX → Send distress signal         ║
  ╠══════════════════════════════════════════════════╣
  ║ NPCs                                            ║
  ║   talk           → Speak to someone             ║
  ║   invite         → Invite NPC to safehouse      ║
  ║                    (⚠️ One of them is a TRAITOR!)║
  ╠══════════════════════════════════════════════════╣
  ║ OTHER                                           ║
  ║   status         → Show your full stats         ║
  ║   help / h       → Show this menu               ║
  ║   quit           → Exit the game                ║
  ╚══════════════════════════════════════════════════╝

  🎯 YOUR GOAL: Find radio parts → Fix the tower → Solve the code → ESCAPE!
  ⚠️  SURVIVE: Get inside with a Talisman before night (every 5 moves)!
""")

# ─────────────────────────────────────────────
#   INPUT PARSER (Understands what you type)
# ─────────────────────────────────────────────

def parse_command(raw_input, player, world):
    """
    Takes whatever the player typed and figures out what to do.
    This is the BRAIN of the game's input system.
    """
    cmd = raw_input.strip().lower()

    if not cmd:
        return  # Ignore empty input

    # ── LOOK / DESCRIBE ──────────────────────
    if cmd in ["look", "l", "look around", "describe", "where am i"]:
        action_look(player, world)

    # ── MOVEMENT ─────────────────────────────
    elif cmd.startswith("go ") or cmd.startswith("move ") or cmd.startswith("head to ") or cmd.startswith("walk to "):
        destination = cmd.replace("go ", "").replace("move ", "").replace("head to ", "").replace("walk to ", "").strip()
        action_go(player, world, destination)

    # Shortcut: just type the place name
    elif cmd in ["town center", "town_center", "center"]:
        action_go(player, world, "town_center")
    elif cmd in ["diner", "the diner", "rusty spoon"]:
        action_go(player, world, "diner")
    elif cmd in ["church", "the church", "abandoned church"]:
        action_go(player, world, "church")
    elif cmd in ["gas station", "gas", "petrol station"]:
        action_go(player, world, "gas_station")
    elif cmd in ["forest", "the forest", "woods"]:
        action_go(player, world, "forest")
    elif cmd in ["hill", "radio hill", "tower", "tower hill"]:
        action_go(player, world, "hill")
    elif cmd in ["cave", "the cave", "cave entrance"]:
        action_go(player, world, "cave")
    elif cmd in ["sheriff", "sheriff office", "sheriff's office", "police"]:
        action_go(player, world, "sheriff")
    elif cmd in ["house", "farmhouse", "safe house", "safehouse"]:
        action_go(player, world, "house")

    # ── SEARCH ───────────────────────────────
    elif cmd in ["search", "s", "look around", "examine", "scout"]:
        action_search(player, world)

    # ── TAKE ITEM ────────────────────────────
    elif cmd.startswith("take ") or cmd.startswith("grab ") or cmd.startswith("pick up "):
        item = cmd.replace("take ", "").replace("grab ", "").replace("pick up ", "").strip()
        action_take(player, world, item)

    # ── USE ITEM ─────────────────────────────
    elif cmd.startswith("use ") or cmd.startswith("eat "):
        item = cmd.replace("use ", "").replace("eat ", "").strip()
        action_use_health_kit(player, item)

    # ── INVENTORY ────────────────────────────
    elif cmd in ["inventory", "i", "bag", "backpack", "items"]:
        action_inventory(player)

    # ── TALISMAN ─────────────────────────────
    elif cmd in ["hang talisman", "place talisman", "use talisman", "put up talisman"]:
        action_hang_talisman(player, world)

    # ── TALK ─────────────────────────────────
    elif cmd in ["talk", "speak", "chat", "talk to npc", "talk to person", "speak to person"]:
        action_talk(player, world)

    # ── INVITE ───────────────────────────────
    elif cmd in ["invite", "invite npc", "invite person", "let them in", "bring them"]:
        action_invite(player, world)

    # ── FIX RADIO ────────────────────────────
    elif cmd in ["fix radio", "repair radio", "build radio", "fix tower", "work on radio"]:
        action_fix_radio(player, world)

    # ── BROADCAST ────────────────────────────
    elif cmd.startswith("broadcast ") or cmd.startswith("transmit ") or cmd.startswith("radio "):
        code = cmd.split()[-1]  # Last word = the code they entered
        if code.isdigit() and len(code) == 4:
            action_broadcast(player, code)
        else:
            slow_print("\n  📡 The code must be exactly 4 digits! (e.g., 'broadcast 1234')")

    # ── CAVE GREED ───────────────────────────
    elif cmd in ["grab one more", "take one more", "be greedy", "just one more"]:
        action_cave_extra(player)

    # ── READ DIARY ───────────────────────────
    elif cmd.startswith("read diary") or cmd.startswith("read page") or cmd == "read":
        if "read diary page" in cmd:
            num = cmd.replace("read diary page ", "").strip()
            action_read_diary(player, f"diary page {num}")
        else:
            # Read any diary page in inventory
            found_any = False
            for item in player["inventory"]:
                if "diary page" in item:
                    slow_print(f"\n  {DIARY_PAGES.get(item, 'Unreadable.')}")
                    found_any = True
            if not found_any:
                slow_print("\n  📖 You don't have any diary pages yet. Search the town!")

    # ── STATUS ───────────────────────────────
    elif cmd in ["status", "stats", "check", "how am i"]:
        show_status(player)

    # ── HELP ─────────────────────────────────
    elif cmd in ["help", "h", "commands", "what can i do", "?"]:
        action_help(player, world)

    # ── QUIT ─────────────────────────────────
    elif cmd in ["quit", "exit", "q", "leave", "stop"]:
        slow_print("\n  Thanks for playing The Endless Road. The town will miss you... 👁️")
        player["game_over"] = True

    # ── WAIT (Risky! Wastes a move) ──────────
    elif cmd in ["wait", "rest", "sleep", "do nothing"]:
        slow_print("\n  ⏳ You stand there, doing nothing. Time passes...")
        if is_night(player):
            slow_print("  Not smart to wait at night. Something cold brushes past you...")
            player["sanity"] = max(0, player["sanity"] - 10)
        tick(player, world)

    # ── UNKNOWN ──────────────────────────────
    else:
        responses = [
            f"  🤔 Not sure what '{cmd}' means. Type 'help' for commands.",
            f"  ❓ Hmm, '{cmd}'? Try 'look' to see where you are, or 'help' for all commands.",
            f"  💭 The town doesn't respond to '{cmd}'. Try 'search', 'go [place]', or 'help'.",
        ]
        slow_print(f"\n{random.choice(responses)}")

# ─────────────────────────────────────────────
#   INTRO SEQUENCE (The Opening Cutscene)
# ─────────────────────────────────────────────

def intro_sequence():
    """The opening story — sets the scene dramatically."""
    clear()
    banner()
    pause(1)

    slow_print("  The sun is low. Orange light bleeds across the highway.")
    slow_print("  You're driving home — music on, windows down, totally normal day.")
    pause(1)
    slow_print("\n  Then the road ends.")
    pause(0.5)
    slow_print("\n  Not 'construction' ends. Not 'detour' ends.")
    slow_print("  ENDS ends — blocked by a massive tree that must have fallen an hour ago.")
    slow_print("  And on its branches... crows. FOUR of them. Still as statues.")
    slow_print("  All staring at you.")
    pause(1.5)

    slow_print("\n  You take the only dirt road on the left.")
    slow_print("  It's a half hour of bumps and potholes before you reach a little town.")
    slow_print("  Faded sign reads: 'MILLHAVEN CROSSING — Population: 312'")
    pause(1)

    slow_print("\n  You drive straight through... and emerge back in the center of town.")
    slow_print("  You try again. And again. And AGAIN.")
    slow_print("  Every road leads back to the same place.")
    slow_print("  You are not going anywhere.")
    pause(1.5)

    slow_print("\n  A hand-painted sign nailed to the fountain reads:")
    slow_print("  'STOP TRYING TO LEAVE. FIND THE RADIO. SURVIVE THE NIGHT.'")
    slow_print("  And at the bottom, in smaller letters:")
    slow_print("  'DON\'T TRUST THE SMILES.'")
    pause(2)

    section_break()
    slow_print("  You get out of the car. The sun is getting lower.")
    slow_print("  Time to figure out what's going on — FAST.")
    section_break()
    pause(1.5)

# ─────────────────────────────────────────────
#   TUTORIAL HINTS (For first-time players)
# ─────────────────────────────────────────────

def tutorial_hints():
    """Quick tips so players know what to do."""
    print("""
  ╔══════════════════════════════════════════════════╗
  ║           🎓 QUICK START GUIDE                 ║
  ╠══════════════════════════════════════════════════╣
  ║  1. Type 'look' to see your surroundings       ║
  ║  2. Type 'go [place]' to move around           ║
  ║  3. Type 'search' to hunt for items            ║
  ║  4. Type 'take [item]' to pick things up       ║
  ║  5. Find the TALISMAN (church) and set up       ║
  ║     a safehouse BEFORE night falls!            ║
  ║  6. Collect 4 radio parts to fix the tower     ║
  ║  7. Find diary pages to learn the radio code   ║
  ║  8. Solve the puzzle, broadcast, and ESCAPE!   ║
  ║                                                ║
  ║  ⏳ Night falls every 5 moves — PLAN AHEAD!   ║
  ║  👁️  One NPC is a TRAITOR — trust carefully!  ║
  ║  🕳️  Cave has rare items but only 3 turns!    ║
  ╚══════════════════════════════════════════════════╝
""")

# ─────────────────────────────────────────────
#   MAIN GAME LOOP
# ─────────────────────────────────────────────

def main():
    """The main function — this runs the entire game."""
    clear()

    # ── Title Screen ─────────────────────────
    banner()
    print("  Press ENTER to begin your adventure...")
    input()

    # ── Intro Story ──────────────────────────
    intro_sequence()

    # ── Player Name ──────────────────────────
    print()
    while True:
        name = input("  What's your name, traveller? → ").strip()
        if name:
            break
        print("  (You need to enter a name!)")

    print(f"\n  Welcome to Millhaven Crossing, {name}.")
    slow_print("  Try not to die.")
    pause(1)

    # ── Setup Game ───────────────────────────
    traitor = random.choice(["Cook", "Sheriff"])  # Random traitor every playthrough!
    player = create_player()
    player["name"] = name
    world = create_world(traitor)

    # Quick hint
    tutorial_hints()
    input("  Press ENTER to start playing → ")
    clear()

    # ── Initial Look ─────────────────────────
    action_look(player, world)
    show_status(player)
    print("  Type 'help' to see all commands, or just start exploring!\n")

    # ── Main Game Loop ────────────────────────────────────────────────────
    while not player["game_over"] and not player["won"]:

        # Show prompt — with location and time
        time_str = "☀️ DAY" if not is_night(player) else "🌙 NIGHT"
        prompt = f"\n  [{time_str} | {player['location'].replace('_', ' ').title()}] > "

        try:
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Game interrupted. Goodbye!")
            break

        parse_command(user_input, player, world)

        # ── Win Check ────────────────────────
        if player["won"]:
            win_screen(player)
            break

        # ── Death Check ──────────────────────
        if player["health"] <= 0 or player["sanity"] <= 0:
            if not player["game_over"]:
                check_death(player)

        # ── Show status every so often ───────
        if player["moves"] > 0 and player["moves"] % 3 == 0:
            show_status(player)

    # ── Play Again? ──────────────────────────
    print()
    again = input("  Would you like to play again? (yes/no) → ").strip().lower()
    if again in ["yes", "y", "yeah", "yep", "sure"]:
        main()  
    else:
        print("\n  Thanks for playing THE ENDLESS ROAD. 🛣️")
        print("  The town remembers you. Always.\n")

# ─────────────────────────────────────────────
#   ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()