# Test-Manual – Projekt *Minesweeper*

## 1. Allgemeine Informationen

- **Projektname:** Minesweeper (Tkinter)
- **Lehrveranstaltung:** Software Engineering
- **Version des Test-Manuals:** 1.1
- **Datum:** 02.12.2025
- **Tester/in:** Rene Tresek

**Ziel dieses Dokuments:**  
Dieses Test-Manual beschreibt Vorgehensweise, Methoden und konkrete Testfälle zur Qualitätssicherung des Softwareprojekts *Minesweeper*. Es orientiert sich direkt am vorhandenen Python/Tkinter-Code und den implementierten Unit-Tests in `test_minesweeper.py`.

---

## 2. Testobjekt

Testobjekt ist die Python-Anwendung **„Minesweeper“**, implementiert als `Minesweeper`-Klasse in `minesweeper.py`.

### Wichtige Funktionen & Datenstrukturen

- Spielfeldgröße und Minenanzahl:
  - `self.rows`, `self.cols`, `self.mines_total`
- Zustände pro Feld:
  - `self.is_mine[r][c]` – Mine ja/nein
  - `self.revealed[r][c]` – Feld aufgedeckt ja/nein
  - `self.flagged[r][c]` – Flagge gesetzt ja/nein
  - `self.neigh[r][c]` – Anzahl benachbarter Minen
- Zentrale Methoden:
  - `__init__()`, `_reset_board()`, `_place_mines()`, `_neighbors()`, `_check_win()`, `_game_won()`, `_game_lost()`

---

## 3. Testumfang (Scope)

### In-Scope

- **Spiellogik:**
  - Initialisierung des Spielfelds (`_reset_board`)
  - Platzierung der Minen (`_place_mines`)
  - Bestimmung von Nachbarfeldern (`_neighbors`)
  - Erkennung des Spielsieges (`_check_win` → `_game_won`)
- **UI-Nähe (indirekt):**
  - Aufruf von `messagebox.showinfo` bei gewonnenem Spiel (wird in Unit-Tests gemockt)

### Out-of-Scope (für die aktuellen Unit-Tests)

- Vollständige GUI-Darstellung (Farben, Fonts, Layout)
- Komplette Spielinteraktion via Maus (Klick-Events) – wird eher in manuellen Systemtests geprüft
- Timer-Anzeige im Detail

---

## 4. Teststrategie & Testarten

### 4.1 Testebenen

- **Unit-Tests**  
  Über `unittest` in `test_minesweeper.py`.  
  Fokus auf:
  - Korrekte Nachbarlogik (`_neighbors`)
  - Konsistente Board-Initialisierung (`_reset_board`)
  - Richtiges Platzieren von Minen (`_place_mines`)
  - Erkennung des Spielgewinns (`_check_win`)

- **Systemtests (manuell)**  
  Durch Anwenderinteraktion (Klicken, Flaggen setzen, Spiele gewinnen/verlieren).

### 4.2 Testarten

- **Funktionale Tests:**  
  Prüfen, ob sich die internen Datenstrukturen gemäß den Spielregeln verhalten.
- **Negativtests:**  
  Z. B. Randfälle für `_neighbors` (Ecken, Ränder).
- **Regressionstests:**  
  Die Unit-Tests können regelmäßig ausgeführt werden, um sicherzustellen, dass Änderungen keine Fehler einführen.

---

## 5. Testumgebung

- **Hardware:** Standard-PC/Laptop
- **Betriebssystem:** Windows / Linux / macOS
- **Programmiersprache:** Python 3.13
- **Bibliotheken:**
  - `tkinter` (Standard)
  - `unittest`, `unittest.mock` (Standardbibliothek)
- **Ausführung:**
  - Direkt mit `python -m unittest`
  - oder über PyCharm (Test-Runner)

---

## 6. Konkrete Unit-Testfälle

### UT-001 – `_neighbors` für mittlere Zelle

- **Ziel:** Sicherstellen, dass eine Zelle in der Mitte des Spielfelds alle 8 Nachbarn korrekt liefert.
- **Implementierung:** `test_neighbors_center_cell`
- **Vorbedingung:** 5x5-Board.
- **Erwartetes Ergebnis:** 8 Nachbarn, inkl. Diagonalen, exklusive der Zelle selbst.

### UT-002 – `_neighbors` für Ecke

- **Ziel:** Sicherstellen, dass eine Ecke (0,0) genau 3 Nachbarn hat.
- **Implementierung:** `test_neighbors_corner_cell`
- **Erwartetes Ergebnis:** Nur gültige Koordinaten innerhalb des Boards, Anzahl = 3.

### UT-003 – `_reset_board` setzt Zustand zurück

- **Ziel:** Nach `_reset_board(keep_ui=True)` sollen alle Felder:
  - keine Mine sein
  - nicht aufgedeckt sein
  - nicht geflaggt sein
- **Implementierung:** `test_reset_board_initializes_state`
- **Erwartetes Ergebnis:**  
  - `is_mine`, `revealed`, `flagged` bestehen nur aus `False`
  - `game_over = False`, `started = False`
  - `flags_left = mines_total`

### UT-004 – `_place_mines` setzt korrekte Minen und respektiert ersten Klick

- **Ziel:**
  - Minenanzahl entspricht `mines_total`
  - Erste angeklickte Zelle und ihre Nachbarn sind keine Minen
- **Implementierung:** `test_place_mines_respects_first_click_and_neighbors`
- **Besonderheit:** Setzt via `random.seed(42)` einen festen Zufalls-Seed.
- **Erwartetes Ergebnis:**  
  - Anzahl gesetzter Minen = `mines_total`  
  - (first_r, first_c) und alle `_neighbors(first_r, first_c)` sind `False` in `is_mine`.

### UT-005 – `_check_win` erkennt gewonnenes Spiel

- **Ziel:** Wenn alle Nicht-Minen-Felder aufgedeckt sind, muss das Spiel als gewonnen markiert werden.
- **Implementierung:** `test_check_win_sets_game_over_when_all_safe_revealed`
- **Vorbedingung:**  
  - 3x3-Board, 1 Mine (z. B. in der Mitte)  
  - Alle Nicht-Minen-Felder sind in `revealed` = `True`
- **Erwartetes Ergebnis:**  
  - `game_over = True`  
  - `messagebox.showinfo()` wird genau einmal aufgerufen (gemockt).

---

## 7. Fehler- und Änderungsmanagement

- **Fehlererfassung:**  
  - Kurzbeschreibung  
  - Testfall-ID (z. B. UT-004)  
  - Erwartetes vs. tatsächliches Verhalten  
  - Schweregrad (kritisch, mittel, gering)  
  - Status (neu, in Bearbeitung, behoben, geschlossen)

- **Änderungen:**  
  - Anpassung des Codes in `minesweeper.py`  
  - Erneuter Lauf aller Unit-Tests  
  - Ggf. Erweiterung der Testfälle bei neuen Features

---

## 8. Abnahmekriterien (Definition of Done für Tests)

Eine User Story / ein Inkrement gilt als fertig, wenn:

1. Alle relevanten Unit-Tests in `test_minesweeper.py` **grün** sind  
2. Keine offenen kritischen Fehler bestehen  
3. Notwendige Systemtests (manuell) erfolgreich durchgeführt wurden  
4. Dieses Test-Manual und die Testfälle bei Änderungen aktualisiert wurden

---

## 9. Testdokumentation

- `TEST_MANUAL.md` (dieses Dokument)  
- `test_minesweeper.py` (implementierte Unit-Tests)  
