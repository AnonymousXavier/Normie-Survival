markdown
# 🧟‍♂️ Normie Survival

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-CE-green?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Custom_ECS-8A2BE2?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.3-FFD700?style=for-the-badge)

> **An intense, highly-optimized arena survival shooter built entirely from scratch in Python. Features a custom Entity-Component-System (ECS), bespoke flow-field pathfinding, and a hardware-accelerated UI caching engine to maintain a locked 60 FPS.**

![Gameplay Banner / Title Screen](docs/gameplay.gif)

## 📖 The Hook

The horde doesn't stop, and neither do you. 

You are dropped into an infinite grid with nothing but a base weapon and a strict timer. As you decimate the swarm, you collect experience gems to augment your physical stats, bolt on retaliation tech, and expand your arsenal. 

But the AI Director is watching. As time ticks down, spawn rates multiply and elite enemies drop into the arena. Survive the onslaught, trigger the boss fight, and claim the Mega Gem—or die trying.

---

## 🔥 What's New in v1.3 (The "Game Feel" Update)
* **The Active Dodge:** A high-risk, high-reward tactical dash granting temporary I-Frames, leaving behind a fading electrical "Ghost Trail."
* **Hit-Stop Time Manipulation:** The engine now literally freezes for 80ms–150ms during heavy impacts (taking damage, Boss hits, Boss deaths), simulating immense physical friction and weight.
* **The "Donut of Death" Spawner:** Enemies now utilize targeted edge-spawning (Frustum Spawning) combined with an aggressive background "Leash" garbage collector, ensuring maximum horde density exactly where the player is looking without wasting CPU cycles.
* **Polynomial RPG Scaling:** Rebalanced the entire game economy away from exponential grind-walls, implementing a smooth polynomial XP curve and time-based enemy scaling.

---

## 📸 Visual Showcase

### 1. The Arsenal (Weapon Mastery)
![Combat](docs/combat.gif)

### 2. The Active Dodge (Run/Dash Mechanic)
![Active Dodge](docs/dash.gif)

### 3. The Tesla Web (Area of Effect)
![Tesla Web](docs/tesla_web.gif)

### 4. The Boss Encounter
![Boss Fight](docs/boss.gif)

---

## 🛠️ Technical Architecture (The Engine)

This game isn't just a massive `while` loop. It runs on a custom-built, highly decoupled engine designed to squeeze maximum performance out of Python without relying on pre-built physics nodes.

* **Entity-Component-System (ECS):** Pure separation of data and logic. Systems (Movement, Collision, Combat, Rendering) process data arrays independently, preventing spaghetti code and allowing for massive scalability.
* **Two-Pass Rendering System:** The pipeline separates static background elements (shadows, grids, auras) from dynamic actors (sprites, UI), ensuring perfect Z-index sorting so high-priority boss shadows never render on top of overlapping mobs.
* **Flow-Field Pathfinding:** Instead of A* calculating 200 individual paths per frame, the engine calculates a single, unified "gravity map" once per second, allowing the entire horde to navigate perfectly around the player at a fraction of the CPU cost.
* **Hardware-Accelerated UI Caching:** To prevent Pixel Fill-Rate bottlenecks, 1080p UI panels are generated, scaled, and cached into memory via a "Dirty Flag" system, reducing UI rendering time from 40ms to 0.1ms per frame.
* **Spatial Hashing:** Collision detection operates on a dynamic discrete grid system, dropping complexity from O(N^2) to near O(1), ensuring smooth frame rates even when the arena is completely flooded.

---

## 🚀 Installation & How to Play

### Prerequisites
* Python 3.x
* Pygame-CE

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/AnonymousXavier/Normie-Survival.git](https://github.com/AnonymousXavier/Normie-Survival.git)
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame-ce
   ```
3. Run the engine:
   ```bash
   python main.py
   ```

---

## 🎮 Controls

* **[W, A, S, D]** or **[Arrow Keys]** - Move your character.
* **[Mouse]** - Aim your weapons.
* **[SPACE]** or **[SHIFT]** - Active Dodge (Dash / I-Frames).
* **[Auto-Fire]** - Weapons fire automatically based on their individual cooldown stats.
* **[ESC]** - Pause Game / Access System Options (Toggle Music, Sound, Screen Shake).

---

## 📊 Profiling & Optimization Notes
This engine was heavily profiled using `cProfile`. If you are a developer looking to fork or study the architecture:
* Toggle the live, unobtrusive FPS counter in the top-left to monitor performance under heavy load.
* Keep an eye on the `Spatial Hashing` logic and `Misc.get_entities_on_screen` for examples of aggressive frustum culling.

## 📜 Credits
* **Developer:** Xavier
* **Engine:** Pygame-CE
