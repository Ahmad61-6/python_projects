# 🔧 Developer Guide — Architecture & Modding

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         MAIN GAME LOOP                  │
│  ┌──────────────────────────────────┐  │
│  │  1. Show prompt                  │  │
│  │  2. Parse user input             │  │
│  │  3. Execute action handler       │  │
│  │  4. Call tick()                  │  │
│  │  5. Check win/death conditions   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
        ▲
        │
   Repeat until
   game_over = True
```

---

## State Management

### Player Dictionary
```python
player = {
    "health": 100,           # 0-100
    "sanity": 100,           # 0-100
    "inventory": [],         # Items in bag
    "location": "town_center",  # Current room
    "moves": 0,              # Action counter
    "day": 1,                # Day counter
    "has_talisman_hung": False,  # Safehouse secure?
    "safehouse": None,       # Location key
    "radio_fixed": False,    # Can broadcast?
    "cave_turns": 0,         # Turns in cave
    "in_cave": False,        # Currently in cave?
}
```

### World Dictionary
```python
world = {
    "town_center": {
        "name": "🏙️ Town Center",
        "desc": "...",
        "exits": {"diner": "...", "cave": "..."},
        "items": ["talisman"],
        "npc": None,
    },
    "cave": {
        "name": "🕳️ The Cave",
        "desc": "...",
        "exits": {"town_center": "..."},
        "items": ["battery pack", "signal booster"],
        "is_cave": True,  # Special flag!
    },
    # ... 7 more locations
}
```

---

## Game Flow

```
START
  │
  ├─→ intro_sequence()
  │
  ├─→ create_player()
  │
  ├─→ create_world(random_traitor)
  │
  └─→ MAIN LOOP:
      ├─ show_status()
      ├─ input() → parse_command()
      │   ├─ go [location] → action_go()
      │   ├─ take [item] → action_take()
      │   ├─ search → action_search()
      │   ├─ talk → action_talk()
      │   ├─ hang talisman → action_hang_talisman()
      │   ├─ fix radio → action_fix_radio()
      │   └─ broadcast [code] → action_broadcast()
      │
      ├─ tick(player, world)
      │   ├─ player["moves"] += 1
      │   ├─ Check day/night transition
      │   └─ check_night_danger(player, world)
      │
      ├─ Check win / death
      │   ├─ player["won"] = True → win_screen()
      │   ├─ player["health"] ≤ 0 → game_over()
      │   └─ player["sanity"] ≤ 0 → game_over()
      │
      └─ Repeat
```

---

## ⏰ Time System

```
Move:  1  2  3  4  5  │  6  7  8  9  10  │  11 12 13 14 15
Time:  ☀️ ☀️ ☀️ ☀️ ☀️ │ 🌙 🌙 🌙 🌙 🌙  │ ☀️ ☀️ ☀️ ☀️ ☀️
       ─ DAY 1 ─      │  ─ NIGHT 1 ─   │  ─ DAY 2 ─
```

**Key**: `move % 10` determines day/night
- 0-4: DAY (safe)
- 5-9: NIGHT (monsters active)

---

## 🐛 Known Issues

**Status**: 5 bugs identified. 1 fixed. See [BUG_REPORT.md](BUG_REPORT.md) for fixes.

| Bug | Severity | Solution |
|----|----------|----------|
| `diary_pages` not updated | MEDIUM | Append in `action_take()` |
| `traitor_talked` unused | LOW | Remove variable |
| NPC re-inviting allowed | MEDIUM | Check `already_invited` flag |
| Cave 4th-item grab | LOW | Add return statement |
| Repeat NPC dialogue | LOW | Add `talked_to` flag |

---

## 🔧 Quick Modding Guide

### Add a Location
```python
# In create_world()
"hospital": {
    "name": "🏥 Hospital",
    "desc": "...",
    "exits": {"town_center": "..."},
    "items": ["medicine"],
    "inside": True,
}
```

### Add an NPC
```python
"npc": "Doctor",
"npc_name": "Doctor",
"is_traitor": traitor_name == "Doctor"
```

### Add Custom Item
```python
"items": [..., "skeleton key"]
# Then handle in action_take()
```

### New Command
```python
elif cmd == "pray":
    player["sanity"] = min(100, player["sanity"] + 5)
    tick(player, world)
```

---

## ✅ Testing Checklist

- [ ] All exits connect bidirectionally
- [ ] Talisman protection (safehouse only)
- [ ] Cave 3-turn limit enforced
- [ ] Radio code: 4275 wins, others fail
- [ ] Health/sanity clamped 0-100
- [ ] Day/night at moves 5, 10, 15
- [ ] Free actions don't count
- [ ] Items don't respawn
- [ ] Can't win early

---

## 📚 Resources

- **[en.wikipedia.org/wiki/String_formatting#Python](https://en.wikipedia.org/wiki/String_formatting#Python)** — For f-string syntax
- **[docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html)** — Random module
- **[BUG_REPORT.md](BUG_REPORT.md)** — Detailed issue analysis

---

**Final tip**: Keep backups before major edits! 🎮
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
