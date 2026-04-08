# 🧟‍♂️ Normie Survival

An intense, highly-optimized arena survival shooter built entirely from scratch in Python and Pygame. 

Survive the relentless horde for 3 minutes, level up your arsenal, and defeat the Boss. Featuring a custom Entity-Component-System (ECS), a dynamic AI Director, and an engine optimized to handle hundreds of active entities at a locked 60 FPS.

![Gameplay Screenshot] (readme_files/screenshot.png)

## ✨ Key Features

* **Dynamic AI Director:** Enemy spawn rates scale relentlessly with time, featuring "Aggro Spikes" that dynamically punish overpowered players to maintain tension.
* **Mastery System:** Deep, stacking upgrade pool featuring branching weapon types (Shotguns, Piercing Snipers), AOE Tesla coils, temporary shields, and physics-based magnetism.
* **Boss Encounters:** Elite enemies with custom states, including Gravity Well paralysis and Dash attacks.
* **Juicy Combat Feedback:** Screen shake, hit-flashing, dynamic blood/spark particle systems, and multi-segmented jagged lightning generation.
* **Endless Mode:** Defeat the boss to claim the Mega Gem, or choose to do a "Victory Lap" and fight indefinitely.

## ⚙️ Technical Architecture (The Engine)

This game isn't just a massive `while` loop. It runs on a custom-built, highly decoupled engine designed to squeeze maximum performance out of Python:

* **Entity-Component-System (ECS):** Pure separation of data and logic. Systems (Movement, Collision, Combat, Rendering) process data arrays independently, preventing "spaghetti code."
* **Flow-Field Pathfinding:** Instead of $A^*$ calculating 200 individual paths per frame, the engine calculates a single, unified "gravity map" once per second, allowing the entire horde to navigate perfectly around the player at a fraction of the CPU cost.
* **Hardware-Accelerated UI Caching:** To prevent Pixel Fill-Rate bottlenecks, 1080p UI panels are generated, scaled, and cached into memory via a "Dirty Flag" system, reducing UI rendering time from 40ms to 0.1ms per frame.
* **Spatial Hashing:** Collision detection operates on a dynamic grid system, dropping complexity from $O(N^2)$ to near $O(1)$, ensuring smooth frame rates even when the arena is completely flooded.

## 🚀 Installation & How to Play

### Prerequisites
* Python 3.x
* Pygame

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/Normie-Survival.git](https://github.com/YourUsername/Normie-Survival.git)
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```
3. Run the engine:
   ```bash
   python main.py
   ```

## 🎮 Controls

* **WASD / Arrow Keys:** Move your character.
* **Mouse:** Aim your weapons.
* **Auto-Fire:** Weapons fire automatically based on their individual cooldown stats.
* **ESC:** Pause Game / Access Settings (Toggle Music, Sound, Screen Shake).

## 🛠️ Profiling & Optimization Notes
This engine was heavily profiled using `cProfile`. If you are a developer looking to fork this:
* Toggle the live, unobtrusive FPS counter in the top-left to monitor performance drops.
* Keep an eye on `ParticleManager.py` if altering the `lightning_bolts` life-cycle, as it relies on jagged interpolation.

## 📜 Credits
* **Developer:** Xavier
* **Engine:** Pygame
