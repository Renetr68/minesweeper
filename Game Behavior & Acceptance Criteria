# Minesweeper – Initial Game Behavior & Acceptance Criteria

# Sprint Goal
Deliver a minimal playable version of Minesweeper with basic game mechanics.

---

# User Stories & Acceptance Criteria

### 1. Board Generation
**User Story:**  
As a player, I want a game board with hidden cells so that I can start a new game.

**Acceptance Criteria:**  
- A grid of fixed size (e.g., 8x8) is generated.  
- A predefined number of mines are placed randomly.  
- Each cell knows the number of mines in its adjacent cells.  
- No duplicate placement of mines.  

---

### 2. Reveal a Cell
**User Story:**  
As a player, I want to click on a cell so that I can see if it’s safe or a mine.

**Acceptance Criteria:**  
- Left-click on a covered cell reveals it.  
- If the cell contains a mine → game ends (lose condition).  
- If the cell does not contain a mine → the number of adjacent mines is displayed.  
- If the cell has zero adjacent mines → all neighboring cells are revealed recursively.  

---

### 3. Display Game State
**User Story:**  
As a player, I want to see which cells are revealed or still hidden so that I can make decisions.

**Acceptance Criteria:**  
- Hidden cells are visibly distinct from revealed cells.  
- Revealed cells show either:
  - A number (adjacent mines count), or  
  - A mine (if clicked).  

---

### 4. Win / Lose Condition
**User Story:**  
As a player, I want to know if I have won or lost so that I can finish the game.

**Acceptance Criteria:**  
- If a mine is revealed → player loses.  
- If all non-mine cells are revealed → player wins.  
- A win or lose message is displayed at the end.  

---

## Definition of Done
- Features are implemented and integrated.  
- All acceptance criteria are met.  
- Code reviewed and tested (unit tests for board generation & mine placement).  
- Documentation updated.  
