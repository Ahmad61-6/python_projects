# 🔧 The Endless Road — Developer & Modder Documentation

## Architecture Overview

The game is built as a single-file Python text adventure using a state-machine architecture. All game state is tracked in a `player` dictionary and a `world` dictionary.

### Key Components

1. **Game State** (`player` dict) — Tracks health, sanity, inventory, location, time
2. **World Definition** (`world` dict) — Describes all locations, NPCs, items
3. **Command Parser** (`parse_command()`) — Converts user input to game actions
4. **Action Handlers** — Functions like `action_take()`, `action_go()` that modify state
5. **Tick System** (`tick()`) — Advances time and triggers events after each move
6. **Safety Functions** — `check_night_danger()`, `check_death()` for consequences

---

## Player State Dictionary

```python
player = {
    "name": "",                      # Player's name (string)
    "health": 100,                   # HP 0-100
    "sanity": 100,                   # Sanity 0-100
    "inventory": [],                 # List of item strings
    "location": "town_center",       # Current room key
    "moves": 0,                      # Total action count
    "day": 1,                        # Day counter
    "inside": False,                 # In building? (bool)
    "has_talisman_hung": False,      # Talisman on safehouse? (bool)
    "safehouse": None,               # Safehouse location key
    "diary_pages": [],               # ⚠️ UNUSED! (BUG #1)
    "radio_fixed": False,            # Radio tower usable? (bool)
    "survived_nights": 0,            # Night counter
    "cave_turns": 0,                 # Turns spent in cave (max 3)
    "in_cave": False,                # Currently in cave? (bool)
    "traitor_talked": False,         # ⚠️ UNUSED! (BUG #2)
    "traitor_invited": False,        # Invited traitor to safehouse?
    "game_over": False,              # Game ended? (bool)
    "won": False,                    # Game won? (bool)
    "items_looted": [],              # Items already taken (for deduplication)
}
```

### State Variables with Known Issues

1. **`diary_pages`** — Initialized but NEVER updated when diary pages are taken
   - Status: **NOT TRACKED PROPERLY**
   - Used in: Line 944 in `action_fix_radio()`
   - Impact: The check `diary_count = len([i for i in player["inventory"] if "diary page" in i])` works instead, making `diary_pages` redundant

2. **`traitor_talked`** — Initialized but completely unused
   - Status: **VESTIGIAL CODE**
   - Could be used to: Track if player has talked to traitor before
   - Impact: No impact, just dead code

3. **`traitor_invited`** — Set but only used for one-time traitor event
   - Status: **SINGLE-USE STATE**
   - Used in: `action_invite()` and night danger check
   - Impact: Works correctly, but could allow re-inviting

---

## World Dictionary Structure

Each location is a dict with these keys:

```python
location_dict = {
    "name": str,                     # Display name with emoji (e.g., "🏚️  The Old Farmhouse")
    "desc": str,                     # Long description for `look` command
    "exits": {key: str, ...},        # Adjacent rooms and descriptions
    "npc": str,                      # NPC name or None
    "items": [str, ...],             # Items available here
    "searched": bool,                # Has player searched? (optional)
    "inside": bool,                  # Is it a building? (optional)
    "is_safehouse": bool,            # Can be safehouse? (optional)
    "is_cave": bool,                 # Is this the cave? (optional)
    "is_traitor": bool,              # Is NPC the traitor? (optional)
    "npc_name": str,                 # NPC name for dialogue (optional)
}
```

### Location Keys
- `town_center` — Hub connecting all areas
- `diner` — Has Cook NPC
- `church` — Has talisman
- `gas_station` — Has copper wire
- `forest` — Has antenna piece
- `hill` — Radio tower (finish line)
- `cave` — Monster lair with 3-turn limit
- `sheriff` — Has Sheriff NPC
- `house` — Default safehouse

---

## 🐛 IDENTIFIED STATE-TRACKING BUGS

### BUG #1: Diary Pages List Never Updated
**Severity**: MEDIUM  
**Location**: `action_take()` function (line ~830)  
**Issue**: When player takes a diary page, it's added to inventory but NOT to `player["diary_pages"]`

```python
# Current code (BUGGY):
def action_take(player, world, item_name):
    # ... item adding code ...
    if found:
        player["inventory"].append(found)  # ✓ This is correct
        player["items_looted"].append(found)  # ✓ This is correct
        # ❌ Missing: player["diary_pages"].append(found)
```

**Impact**: 
- `action_fix_radio()` checks `player["diary_pages"]` but it's always empty
- Code falls back to: `diary_count = len([i for i in player["inventory"] if "diary page" in i])`
- This workaround works, but the original intent is broken

**Fix**:
```python
if "diary page" in found.lower():
    player["diary_pages"].append(found)  # Add this line
    slow_print(f"\n  {DIARY_PAGES.get(found, 'A cryptic diary page.')}")
```

---

### BUG #2: Traitor Talked Flag Never Used
**Severity**: LOW  
**Location**: Player state initialization (line ~74)  
**Issue**: `traitor_talked` is initialized but never set or checked anywhere

```python
"traitor_talked": False,  # ❌ VESTIGIAL — NEVER CHANGED
```

**Impact**: 
- No functional impact (dead code)
- Suggests incomplete feature intent
- Code smell for maintenance

**Fix**: Either remove it or implement NPC dialogue caching:
```python
# Option 1: Remove entirely
# (Delete from player dict initialization)

# Option 2: Prevent repeat dialogues
if npc_name == "Cook":
    if player["traitor_talked"]:
        slow_print(f"  Cook: 'Look, we've talked enough...'")
        return
    player["traitor_talked"] = True
    # Then show dialogue...
```

---

### BUG #3: No Protection Against Inviting Same NPC Twice
**Severity**: MEDIUM  
**Location**: `action_invite()` function (line ~950)  
**Issue**: Player can invite the same NPC multiple times

```python
# Current logic:
def action_invite(player, world):
    # ... finds NPC ...
    player["traitor_invited"] = is_traitor  # Overwrites previous value
    # Should check: if already invited, deny second invitation
```

**Impact**:
- If player invites human, leaves, comes back, invites them again
- "Sanity +10" is triggered multiple times (potential exploit)
- Design-wise, should only get +10 once per human

**Fix**:
```python
def action_invite(player, world):
    loc_key = player["location"]
    loc = world[loc_key]
    
    if not loc.get("npc"):
        slow_print("\n  👤 There's nobody here to invite.")
        return
    
    npc_name = loc.get("npc_name")
    
    # ✓ NEW: Check if already invited
    if loc.get("already_invited"):
        slow_print(f"  {npc_name}: 'I'm already coming, remember?'")
        return
    
    loc["already_invited"] = True  # ✓ NEW: Mark as invited
    
    # ... rest of function ...
```

---

### BUG #4: Cave Turns Allow 4th Item Grab (Brief Window)
**Severity**: LOW  
**Location**: `action_take()` function (line ~838)  
**Issue**: After taking 3 items, player is warned but CAN still attempt a 4th

```python
# Current logic:
if player["cave_turns"] >= 3:
    slow_print("  ⚠️  That's 3 items from the cave. You should LEAVE NOW!")
    # But the item WAS still successfully taken
    # Player can then try: "grab one more", "take one more", etc.
```

**Impact**:
- Intended behavior: 3 items max, then must leave
- Actual behavior: Can grab 3, warned, but game doesn't force exit
- Player must follow warning (or intentionally trigger Game Over)

**Fix** (if stricter enforcement is desired):
```python
if player["in_cave"]:
    if player["cave_turns"] >= 3:
        slow_print(f"\n  ❌ You've already grabbed 3 items from the cave!")
        slow_print(f"  The monsters are stirring. You must LEAVE NOW.")
        return  # Prevent taking more
    
    player["cave_turns"] += 1
    remaining = 3 - player["cave_turns"]
    if remaining > 0:
        slow_print(f"  ⚠️  CAVE ALERT: {remaining} turn(s) left before monsters wake!")
```

---

### BUG #5: NPC Dialogue Repeats Without Variation
**Severity**: LOW  
**Location**: `action_talk()` and `npc_dialogue()` functions (line ~330)  
**Issue**: Talking to same NPC repeatedly shows identical dialogue

```python
def action_talk(player, world):
    # ... gets NPC ...
    npc_dialogue(npc_name, is_traitor, player, loc)
    tick(player, world)
    # No check for repeat talks
```

**Impact**:
- Minor immersion issue
- NPCs should either: refuse repeat talks, or give different dialogue
- Doesn't break gameplay, just repetitive

**Fix**:
```python
def action_talk(player, world):
    loc_key = player["location"]
    loc = world[loc_key]

    if not loc.get("npc"):
        slow_print("\n  👤 There's nobody here to talk to.")
        return

    # ✓ NEW: Check if already talked
    if loc.get("talked_to"):
        npc_name = loc.get("npc_name")
        slow_print(f"\n  {npc_name}: 'Look, I've already told you everything I know.'")
        tick(player, world)
        return
    
    npc_name = loc.get("npc_name")
    is_traitor = loc.get("is_traitor", False)
    
    loc["talked_to"] = True  # ✓ NEW: Mark as talked
    npc_dialogue(npc_name, is_traitor, player, loc)
    tick(player, world)
```

---

## 🎮 Time System Logic

### Move Counting & Cycles

```python
def tick(player, world):
    player["moves"] += 1
    
    cycle = player["moves"] % 10
    # Cycle 0-4 = Day
    # Cycle 5-9 = Night
    
    if cycle == 5:
        # Sun sets - monsters wake
        player["day"] += 1
        player["survived_nights"] += 1
        
    elif cycle == 0 and player["moves"] > 0:
        # Sun rises - new day
```

### Move Allocation Per Day

- **5 moves = 1 day interval**
- Every action (go, take, search, talk, invite, hang talisman, fix radio, broadcast) = 1 move
- Free actions (look, inventory, status, help) = 0 moves

### Optimal Move Usage

**Day 1 Challenge** (5 moves):
```
Move 1: take talisman      (from Town Center)
Move 2: go house           (to Old Farmhouse)
Move 3: hang talisman      (on safehouse door)
Move 4: search             (find matches & diary page 5)
Move 5: take matches       (sun sets immediately after)
       → Night falls, safe inside with talisman hung
```

---

## 🌙 Night Danger System

### check_night_danger() Logic

Called after every `tick()`. Checks three conditions:

1. **Is it night?** `player["moves"] % 10 >= 5`
2. **Is player inside?** `location.get("inside")`  
3. **Is safehouse protected?** `player["has_talisman_hung"] and player["safehouse"] == location`

### Outcome Matrix

| Inside | Talisman Hung | Location | Result |
|--------|---------------|----------|--------|
| No | No | Outside | VERY DANGEROUS (25-40 dmg, -15-25 sanity) |
| No | Yes | Outside | VERY DANGEROUS (talisman only protects safe house) |
| Yes | No | Inside | DANGEROUS (15-30 dmg, -10 sanity) |
| Yes | Yes | Safehouse | ✓ SAFE (no damage) |

---

## 🎯 Win Condition Logic

### Victory Path (Sequences Required)

```
1. Collect 4 radio parts:
   - battery pack (cave)
   - copper wire (gas station)
   - signal booster (cave)
   - antenna piece (forest)

2. Collect 4 diary pages (from any location):
   - Page 1: Church (digit 4)
   - Page 2: Diner (digit 2)
   - Page 3: Gas station (digit 7)
   - Page 4: Sheriff's office (digit 5)

3. Be at "hill" location
4. Execute: fix radio
5. Execute: broadcast 4275
   → If code correct: player["won"] = True
   → If code wrong: -5 sanity, must try again
```

### Code Validation

```python
def action_broadcast(player, code_attempt):
    if code_attempt == RADIO_CODE:  # RADIO_CODE = "4275"
        player["won"] = True
        # Win screen triggers
    else:
        player["sanity"] -= 5
        # Try again message
```

---

## 🧩 Item System

### Item Categories

**Radio Parts** (Required 4):
- `battery pack` → Cave
- `copper wire` → Gas Station
- `signal booster` → Cave
- `antenna piece` → Forest

**Diary Pages** (4 needed for code):
- `diary page 1` → Church
- `diary page 2` → Diner
- `diary page 3` → Gas Station
- `diary page 4` → Sheriff's Office
- `diary page 5` → Old Farmhouse (context)

**Key Item**:
- `talisman` → Church (must grab, must hang)

**Health Items** (Optional but helpful):
- `bandages` (+20 health)
- `first aid kit` (+40 health)
- `extra health kit` (+50 health)

**Flavor Items** (No mechanical use):
- `matches`
- `canned food`
- `bonus rations`
- `crumpled map`
- `old manual`

### Item Deduplication System

```python
player["items_looted"] = []  # Tracks ALL taken items globally

# In action_take():
items_here = [i for i in loc.get("items", []) if i not in player["items_looted"]]
# Only shows items not in this list

# When taken:
player["items_looted"].append(found)  # Prevents item respawn

# When searched:
if item in player["items_looted"]:
    # Won't show in "You find:" message
```

**Note**: This system is global. Once taken, an item is gone forever (no respawning).

---

## 🧟 NPC & Traitor Logic

### NPC Setup

At game start:
```python
traitor = random.choice(["Cook", "Sheriff"])  # Randomized each playthrough
world = create_world(traitor)  # Builds world with traitor assigned
```

### NPC State in World

```python
"diner": {
    "npc": "Cook",  # or "Cook (Friendly)" based on traitor
    "npc_name": "Cook",
    "is_traitor": True,  # or False
    # ...
}
```

### Dialogue Logic

```python
def npc_dialogue(npc_name, is_traitor, player, world_location):
    if is_traitor:
        # Speaks strangely, invites to safehouse
        slow_print("Cook: 'Oh sweetie...' [smile flickers]")
    else:
        # Gives helpful advice
        slow_print("Cook: 'Don't go out at night. Get the Talisman.'")
```

### Traitor Betrayal

```python
def action_invite(player, world):
    # ...
    if is_traitor:
        player["traitor_invited"] = is_traitor
        
        # Traitor event triggers ONLY at night
        if is_night(player):
            # Window opens, monsters pour in
            # GAME OVER
```

---

## 🎨 Text & Atmosphere System

### Visual Elements

- **Emoji usage**: Every location and item class has a primary emoji
- **Color codes**: Health/Sanity use `\033[91m` (red), `\033[92m` (green), etc.
- **Formatting**: Box borders using `╔═╗║╚` characters
- **Pacing**: `slow_print()` introduces dramatic delays

### Hallucination Mode (Sanity < 50)

When sanity drops below 50, atmospheric messages change:
- Friendly descriptions become unsettling
- NPCs appear more dangerous
- Creepy events become more frequent
- Check in `creepy_event()` function (line ~620)

```python
if player["sanity"] < 50:
    low_sanity_events = [
        "🌀  You hear laughter from behind you...",
        "😊  A smiling figure beckons to you...",
        "🪞  For a moment, you see the town as...
    ]
```

---

## 📊 Modding Guide

### Adding a New Location

1. **Create location dict** in `create_world()`:
```python
"abandoned_warehouse": {
    "name": "🏭 Abandoned Warehouse",
    "desc": "A massive rusted warehouse...",
    "exits": {"town_center": "Go back to Town Center"},
    "npc": None,
    "items": ["mysterious artifact"],
    "searched": False,
    "inside": True,
},
```

2. **Add exit from Town Center**:
```python
"town_center": {
    # ...
    "exits": {
        # ... existing exits ...
        "warehouse": "Go to the Abandoned Warehouse",
    },
},
```

3. **Handle input parsing** in `parse_command()`:
```python
elif cmd in ["warehouse", "the warehouse"]:
    action_go(player, world, "abandoned_warehouse")
```

### Adding a New NPC

1. **Add to location**:
```python
"npc": "Stranger" if traitor_name == "Stranger" else "Stranger (Friendly)",
"npc_name": "Stranger",
"is_traitor": traitor_name == "Stranger",
```

2. **Add dialogue case**:
```python
elif npc_name == "Stranger":
    if is_traitor:
        slow_print("Stranger: 'Welcome to my domain...'")
    else:
        slow_print("Stranger: 'Get out of here while you still can!'")
```

### Adding a New Item Type

1. **Add to world location** `items` list
2. **Add special handling** in `action_take()`:
```python
if "mysterious artifact" in found.lower():
    slow_print("  ✨ The artifact pulses with energy...")
    player["sanity"] = max(0, player["sanity"] - 5)
```

3. **Add to inventory display** if needed:
```python
elif item == "mysterious artifact":
    print(f"   🎭 {item}  ← ancient and unsettling")
```

---

## 🔓 Save/Load System (Not Implemented)

Currently the game has NO persistence. Each play is fresh.

**To add save functionality:**

```python
import json

def save_game(player, world, filename="save.json"):
    # Only save player state (world can be regenerated)
    with open(filename, 'w') as f:
        json.dump(player, f, indent=2)

def load_game(filename="save.json"):
    with open(filename, 'r') as f:
        return json.load(f)
```

Then add commands:
```python
elif cmd == "save":
    save_game(player, world)
    slow_print("Game saved!")
```

---

## 🧪 Testing Checklist

- [ ] Day/night cycle shifts at move 5 and 10
- [ ] Talisman protection only works at safehouse, not other buildings
- [ ] Diary counters correctly (need all 4 before fix radio)
- [ ] Cave 3-turn limit enforced
- [ ] Traitor event triggers only if invited + night
- [ ] Radio code validation (4275 wins, others lose sanity)
- [ ] Health/sanity properly clamped 0-100
- [ ] All exits properly connected
- [ ] Free actions don't advance turn counter
- [ ] Items don't respawn after taking them
- [ ] NPC dialogues display correctly

---

**Happy modding!** 🎮
