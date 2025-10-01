# Minesweeper – Requirements

## 1. Functional Requirements
These describe the **core features** the game must support:

1. **Game Board**
   - The game must generate a grid of cells (e.g., Beginner 8×8, Intermediate 16×16, Expert 30×16).
   - The board must contain a predefined number of mines, placed randomly.

2. **Cell Interaction**
   - The player must be able to reveal a cell (left-click).
   - The game must display:
     - A number if adjacent mines exist.
     - Empty space if no adjacent mines exist (with recursive reveal).
     - A mine if the clicked cell contains one (game over).
   - The player must be able to mark a suspected mine with a flag (right-click).

3. **Game States**
   - The game must detect win/lose conditions.
   - The game must display a message when the player wins or loses.

4. **Difficulty Levels**
   - The game must support at least 3 difficulty levels (different grid sizes and mine counts).

5. **User Interface**
   - The board must clearly show hidden, revealed, and flagged cells.
   - A timer and mine counter should be displayed.

6. **Persistence (Optional / Advanced)**
   - The game should allow storing high scores.
   - The game should allow restarting or resetting.

---

## 2. Non-Functional Requirements
These describe **quality attributes** of the game:

1. **Performance**
   - Board generation and reveal actions must occur instantly (under 0.5s).

2. **Usability**
   - The interface must be intuitive and responsive.
   - Clear visual distinction between hidden, revealed, and flagged cells.

3. **Portability**
   - The game should run in a standard browser or as a standalone desktop app.

4. **Reliability**
   - The game must ensure fair random placement of mines.
   - No two mines may occupy the same cell.

5. **Testability**
   - Core logic (board generation, reveal, win/loss detection) must be covered by automated tests.

---

## 3. Constraints
- Development must follow Scrum methodology (sprints, backlog, increments).  
- The initial version must be playable with basic features by Sprint 2.  
- The project must be implemented in the chosen technology stack (e.g., Java, Python, or JavaScript + framework).  
