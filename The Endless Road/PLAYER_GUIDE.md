# 🌲 THE ENDLESS ROAD — Player's Complete Guide

## Overview

**The Endless Road** is a survival adventure game where you're trapped in a cursed town called Millhaven Crossing. Every action counts. Every choice matters. Can you gather the right items, fix the radio tower, and escape before the monsters get you?

---

## 🎮 Core Game Mechanics

### Time System: Day/Night Cycle

The game operates on a **Day/Night cycle**:
- **Every 5 action commands** = One time period passes
- **Action commands** = `go`, `take`, `search`, `talk`, `invite`, `hang talisman`, `fix radio`, `broadcast`
- **Free actions** (do NOT advance time) = `look`, `inventory`, `status`, `help`

**Critical Rule**: You have **5 moves per day**. After move 5, the sun sets and monsters emerge. You MUST be:
1. Inside a building, AND
2. Have hung the Talisman on the door

### Health System

- **Starting Health**: 100
- **Night Dangers**: Attacks deal 15-40 damage (depending on your location and preparation)
- **Cave Dangers**: Monsters wake up if you're inside for 3+ turns
- **Medical Items**: 
  - `bandages` = +20 health
  - `first aid kit` = +40 health  
  - `extra health kit` = +50 health
- **Death Threshold**: Health ≤ 0 = Game Over

### Sanity System

- **Starting Sanity**: 100
- **Sanity Loss Sources**:
  - Night attacks without protection: -10 to -25
  - Being outside at night: -15 to -25
  - Creepy atmospheric events: -5 per event
  - Waiting/resting at night: -10
- **Critical Threshold**: Sanity < 50 = **HALLUCINATION MODE**
  - Text descriptions become unreliable
  - NPCs look friendly even if they're the Traitor
  - Horror descriptions are softened to confuse you
- **Death Threshold**: Sanity ≤ 0 = Game Over (you lose your mind)

### The Traitor Mechanic

One of two NPCs is the **Traitor** (a monster in disguise):
- **The Cook** or **The Sheriff** — one is human, one is NOT
- They are randomly chosen at the start of each playthrough
- **Betrayal Detection**: 
  - Humans give helpful advice about items and survival
  - Traitors speak strangely and invite you to your safehouse (to let monsters in at night)
- **Inviting the Traitor**: If you use `invite [traitor]` and it becomes night, they open a window to the monsters = **INSTANT GAME OVER**

---

## 🗺️ World Map & Locations

### Town Center
- **Description**: The hub of Millhaven Crossing. All roads connect here.
- **Danger**: Very dangerous at night (no shelter)
- **Visible Items**: `talisman` ⭐ (GRAB THIS FIRST!)
- **NPCs**: None
- **Exits**: Diner, Church, Gas Station, Forest, Hill, Cave, Sheriff, House

### The Old Farmhouse (House)
- **Description**: Your ideal safehouse — sturdy with thick wooden bars
- **Inside**: Yes (protected during day)
- **Visible Items**: None
- **Hidden Items** (use `search`): `matches`, `diary page 5`
- **Special**: This is the **Perfect Safehouse** — use `hang talisman` here
- **Exits**: Town Center

### The Abandoned Church
- **Description**: Half-eaten by rot. The talisman GLOWS here
- **Inside**: Yes
- **Visible Items**: `talisman` ⭐⭐ (ESSENTIAL), `diary page 1`
- **Exits**: Town Center
- **Strategy**: This is usually your FIRST MOVE — grab the talisman immediately

### The Diner (Rusty Spoon)
- **Description**: Burnt coffee smell, ripped booths, a stout cook with an unsettling smile
- **Inside**: Yes
- **Characters**: **The Cook** (human or Traitor?)
- **Visible Items**: `canned food`, `bandages`
- **Hidden Items** (use `search`): `diary page 2`
- **Exits**: Town Center

### Gas Station (Abandoned)
- **Description**: Rusty pumps, smashed windows, overturned shelves
- **Inside**: Yes
- **Visible Items**: `copper wire` 🔧 (RADIO PART #2)
- **Hidden Items** (use `search`): `diary page 3`, `bandages`
- **Exits**: Town Center
- **Strategy**: Essential for fixing the radio

### The Dark Forest
- **Description**: Impossibly tall trees, breathing sounds, broken footprints
- **Inside**: No (exposed)
- **Visible Items**: `antenna piece` 🔧 (RADIO PART #4), `canned food`
- **Danger**: You might take 5-15 damage from tripping during day (random)
- **Exits**: Town Center
- **Strategy**: Only visit during the day

### The Cave Entrance
- **Description**: Cold, dark, MONSTERS ARE SLEEPING HERE
- **Inside**: Technically yes, but dangerous
- **Visible Items**: `battery pack` 🔧 (RADIO PART #1), `signal booster` 🔧 (RADIO PART #3), `extra health kit`, `bonus rations`
- **CRITICAL MECHANIC**: 
  - You have **EXACTLY 3 TURNS** inside the cave
  - Each item taken = 1 turn
  - If you try to grab a 4th item = MONSTERS WAKE UP = **INSTANT GAME OVER**
  - Cannot enter at night
- **Strategy**: Plan carefully. You need 2 items from here, so 2 turns max. Get in, grab what you need, GET OUT.
- **Exits**: Town Center

### Sheriff's Office
- **Description**: Tidy compared to other buildings. A calm, friendly Sheriff sits at a desk
- **Inside**: Yes
- **Characters**: **The Sheriff** (human or Traitor?)
- **Visible Items**: `first aid kit`, `diary page 4`
- **Exits**: Town Center

### Radio Tower Hill
- **Description**: Steep climb with a rusted old radio tower covered in vines
- **Inside**: No
- **Purpose**: **THIS IS YOUR FINISH LINE**
- **Actions**:
  - `fix radio` (when you have all 4 parts)
  - `broadcast 4275` (the correct code)
- **Notes**: This location has no items or danger
- **Exits**: Town Center

---

## 🔧 The Quest: Fixing the Radio

### Step 1: Collect the 4 Radio Parts

The radio tower needs exactly 4 parts to work:

| Part | Location | How to Get | Difficulty |
|------|----------|-----------|-----------|
| 🔋 **Battery Pack** | Cave | `take battery pack` | Risky (cave has 3-turn limit) |
| 🔌 **Copper Wire** | Gas Station | `take copper wire` | Easy (just grab it) |
| 📡 **Signal Booster** | Cave | `take signal booster` | Risky (cave has 3-turn limit) |
| 📶 **Antenna Piece** | Forest | `take antenna piece` | Medium (daytime only) |

### Step 2: Learn the Radio Code from Diary Pages

You need to find **4 diary pages** scattered across town. Each page contains one digit of the radio code:

| Page | Location | Digit | Clue |
|------|----------|-------|------|
| 📖 Page 1 | Church | **4** | "...the number of crows that sat on the fallen tree. I counted them myself. There were FOUR of them." |
| 📖 Page 2 | Diner | **2** | "...the cook told me the SECOND number... She whispered it between sobs: TWO." |
| 📖 Page 3 | Gas Station | **7** | "THE THIRD NUMBER IS THE NUMBER OF DAYS A WEEK. ...SEVEN." |
| 📖 Page 4 | Sheriff | **5** | "...the FOURTH number, he said, is the number of fingers on one hand. FIVE." |
| 📖 Page 5 | House | Context | Explains you need 4 digits and warns about the Traitor |

**The Code**: `4275` (collected from all four diary pages)

### Step 3: Go to the Hill and Fix the Radio
```
go hill
fix radio
```

You'll get a confirmation that the radio is working.

### Step 4: Broadcast the Correct Frequency
```
broadcast 4275
```

If correct: A helicopter arrives at sunrise and you ESCAPE!
If incorrect: Static. You lose 5 sanity. Try again.

---

## 📋 Complete Command Reference

### Movement (1 move each)
```
go [location]        Go to a new area (e.g., "go cave", "go town center")
```

### Items & Inventory (1 move each)
```
take [item]          Pick up an item (e.g., "take talisman", "take battery pack")
search               Search the current location for hidden items
inventory / i        Check what's in your backpack (FREE - no move cost)
use [item]           Use a medical item (bandages, first aid kit, etc.)
```

### Survival Actions (1 move each)
```
hang talisman        Place the talisman on your safehouse door (REQUIRED for night protection)
fix radio            Repair the radio tower (need all 4 parts, must be at Hill)
broadcast [code]     Send distress signal (need correct 4-digit code, must be at Hill)
```

### NPCs (1 move each)
```
talk                 Speak to an NPC in the current room
invite               Invite an NPC to your safehouse (⚠️ RISKY if they're the Traitor!)
```

### Information (FREE - no move cost)
```
look / l             See the room description and items again
status               Check health, sanity, current day, and moves remaining
help / h             Display the command cheat sheet
```

### Other (1 move each)
```
wait / rest          Do nothing for a move (⚠️ risky at night)
quit / exit          Exit the game
```

---

## 🎯 Winning Strategy (Non-Speedrun)

### Day 1: Secure the Safehouse
- `go church` → `take talisman` → `go house` → `hang talisman`
- `take matches` (from searching house)
- This gives you a safe place to sleep tonight

### Night 1: Safe Exploration
- Search the house for `diary page 5`
- Spend remaining moves searching and resting safely

### Day 2-5: Gather Radio Parts
- Day 2: Go to cave, take ONE part (battery pack)
- Day 3: Go to gas station, take copper wire
- Day 4: Go to cave again, take signal booster (2nd cave visit)
- Day 5: Go to forest, take antenna piece

### Throughout: Collect Diary Pages
- Search each location as you visit to find diary pages
- Once you have 4 pages, you know the code is `4275`

### Day 6: The Escape
- Go to hill with all 4 parts
- `fix radio`
- `broadcast 4275`
- ESCAPE! 🎉

---

## ⚠️ Common Mistakes to Avoid

### Mistake #1: Not Getting the Talisman First
- If you're inside a building at night WITHOUT the talisman hung, monsters can still attack
- Always grab it from the church first and hang it at your safehouse

### Mistake #2: Staying Outside at Night
- Staying outside after move 5 causes massive damage (25-40) and sanity loss
- Always plan to be inside YOUR SAFEHOUSE before night falls

### Mistake #3: Getting Greedy in the Cave
- The cave only allows 3 items taken before monsters wake up
- You need battery pack AND signal booster = 2 items
- If you try a 3rd, you're pushing it. A 4th = INSTANT DEATH

### Mistake #4: Inviting the Wrong NPC
- If you invite the Traitor, they open a window at night
- Monsters pour through and you die immediately
- Only invite an NPC if you're sure they're human (talk to them first for clues)

### Mistake #5: Not Collecting Diary Pages
- You need all 4 pages to know the radio code
- Without them, you'll have to guess the broadcast frequency (very risky)

### Mistake #6: Wasting Moves
- Every move counts. Don't waste time at risky locations during the day
- Plan your day: which locations you'll visit, in what order, before starting

### Mistake #7: Ignoring Your Sanity
- When sanity drops below 50, descriptions become unreliable
- An NPC that looks friendly might actually be the Traitor!
- Below 50 sanity = hallucinations start corrupting your perception

---

## 📊 Status Bar Explained

```
──────────────────────────────────────────────────────
  👤 Name  |  📅 Day 1  |  ☀️ DAY
  ❤️  Health:  [████████████████████] 100/100
  🧠  Sanity:  [████████████████████] 100/100
  🎒  Bag:    (empty)
  📍 Location: Town Center
  ⏳ Moves until dark: 5
──────────────────────────────────────────────────────
```

- **Health/Sanity Bars**: Visual representation. Full = safe, empty = danger
- **Moves until dark**: How many actions before night falls (every 5)
- **Bag**: What items you're carrying
- **Time**: ☀️ DAY = safe to explore, 🌙 NIGHT = GET INSIDE

---

## 💡 Pro Tips

1. **Map Memorization**: Learn the layout so you don't waste moves on navigation
2. **Item Tracking**: Keep notes of where each diary page is located
3. **NPC Investigation**: Talk to BOTH NPCs early to get clues about who's the Traitor
4. **Sanity Management**: If sanity gets low, invite a human NPC for +10 restoration
5. **Cave Efficiency**: Plan your cave visit to grab both parts in 2 moves max
6. **Inventory Management**: Check `inventory` frequently to track what you have
7. **Free Actions**: Use `look` and `status` liberally — they don't cost moves!
8. **Tie-Breaking**: If you're unsure who's the Traitor, trust the one who talks about the RADIO and ESCAPE

---

## 🎊 Winning!

When you successfully broadcast the code:
```
📡 The code 4275 is correct!
   'Helicopter ETA: Sunrise. Hold tight.'
   
🚁 The helicopter descends through the morning fog...
   The pilot stares at the town as you climb in.
   You escaped! The town remembers you. Always.
```

Your final score is calculated based on:
- Remaining health
- Remaining sanity
- Days survived
- Items collected

⭐⭐⭐ **MASTER SURVIVOR** — Score > 180
⭐⭐ **SURVIVOR** — Score > 120
⭐ **BARELY MADE IT** — Score < 120

---

**Good luck, traveler. The Endless Road awaits...** 🛣️👁️
