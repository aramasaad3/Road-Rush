# Road Rush: Comprehensive Technical Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 1: The Big Picture & Game Engine Basics

If a teacher asks you how your game works, you don't need to recite code. You just need to show them that you understand the **three fundamental concepts** that drive almost all 2D games, including *Road Rush*. 

### Concept 1: The Coordinate System (X and Y)
In math class, the origin `(0, 0)` is usually at the bottom-left of a graph.
In computers and game development (using Pygame), **`0, 0` is the top-left corner of the screen.**

*   **X-Axis:** Moves left to right. (`X=0` is the left edge, `X=480` is the right edge).
*   **Y-Axis:** Moves from top to bottom. (`Y=0` is the very top edge, `Y=800` is the bottom edge).
*   *Why this matters:* When your car drives "forward," the program actually subtracts from the Y-coordinate. When obstacles (like the Red Car) move toward you, the game *adds* to their Y-coordinate to make them fall down the screen.

### Concept 2: The Game Loop & Frames Per Second (FPS)
A video game is just a flipbook. It draws a picture, erases it, moves the objects slightly, and draws the next picture. It does this extremely fast. Our game runs at **60 Frames Per Second (FPS)**. 

If someone asks what a **"Game Loop"** is, explain that it is an infinite `while True` loop that does three things exactly 60 times every second:
1.  **Event Handling:** Did the player press the Left arrow key this frame? Did they press ESC?
2.  **Update State:** We see they pressed Left, so we update the car's `X` position. We update the timer. We move the enemy cars down by a few pixels.
3.  **Render (Draw):** We paint the screen entirely black, and then we paint the road, the car, the enemies, and the UI text at their *new* positions. 

### Concept 3: MVC Architecture (Model-View-Controller)
When building small scripts, people often put all their code into one massive file. Since *Road Rush* has AI enemies, persistent saving, UI overlays, and physics, doing that would make the code impossible to read.

Instead, we decided to build the game using **MVC Architecture**, which is an industry-standard software design pattern. If a teacher asks why you have so many folders, this is the answer: it keeps the code strictly organized by its *purpose*.

Here is how MVC is broken down in our game:

#### 1. Models (`models/` folder) - "The Data and The Rules"
*   **What it does:** Models only care about data. A car model knows its `X` and `Y` position, its color, and its lane. It does *not* know how to draw itself on the computer screen. It only handles facts.
*   **Examples:** `entities.py` (the factual properties of cars), `resources.py` (how many coins you have), `physics.py` (the math for overlapping rectangles).

#### 2. Views (`views/` folder) - "The Visuals and Sounds"
*   **What it does:** Views are blind and deaf. They only do what they are told. They take the Data from the Models and draw the pixels onto the screen, or play sounds out of the speakers.
*   **Examples:** `hud.py` (draws the yellow coins), `sound.py` (plays music), `feedback.py` (draws the "Game Over" text).

#### 3. Controllers (`controllers/` folder) - "The Middleman / The Brain"
*   **What it does:** Controllers bridge the gap. They listen to the player's keyboard, they change the Models, and they tell the Views what to show.
*   **Examples:** `collision.py` (it actively checks if a car Model hit a wall Model, and if so, it changes the Health Model), `traffic.py` (it decides when to spawn a new enemy Model), `controls.py` (handles the physical keyboard arrow keys).

---

### Project Map Summary
Here is exactly what you see when you open the main game folder:

```text
Road Rush/
├── assets/             # The raw physical `.mp3` and `.wav` media files
├── controllers/        # The Managers (Controls, Spawners, Physics collision logic)
├── models/             # The Data (Cars, Health, Road math, High-score logic)
├── views/              # The Display (Drawing screens, drawing UI, playing sound files)
├── main.py             # THE ENGINE. It glues the MVC together and runs the Game Loop.
├── settings.py         # THE RULES. Global constants like WIDTH=480, GRAY=(50,50,50).
├── strip_comments.py   # Utility script to clean up the code. (We ran it and are done with it).
├── buildozer.spec      # Instructions on how to turn this Python code into an Android APK.
└── RoadRush.spec       # Instructions on how to turn this Python code into a Windows EXE.
```
