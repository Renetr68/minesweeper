# Test-Manual – Projekt *Minesweeper* (Tkinter + Pytest)

## 1. Allgemeine Informationen

- **Projektname:** Minesweeper (Tkinter)
- **Lehrveranstaltung:** Software Engineering
- **Version des Test-Manuals:** 2.0
- **Datum:** 02.12.2025
- **Tester/in:** Rene Tresek

**Ziel dieses Dokuments:**  
Dieses Test-Manual beschreibt die Vorgehensweise, Methoden und konkreten Testfälle zur Qualitätssicherung des Softwareprojekts *Minesweeper*.  
Es basiert **direkt auf der finalen Minesweeper-Implementierung in `main.py`** und dem **pytest-Testpaket `test_minesweeper.py`**, welches Dummy-Widgets nutzt, um GUI-Interaktionen ohne echtes Fenster zu testen.

---

## 2. Testobjekt

Das Testobjekt ist die Python-Anwendung **„Minesweeper“**, umgesetzt als Klasse `Minesweeper` in `main.py`.

### Wichtige Spiellogik-Komponenten

- Spielfeldkonfiguration:
  - `rows`, `cols`, `mines_total`
- Board-Zustände (2D-Listen):
  - `is_mine[r][c]` – Mine ja/nein  
  - `revealed[r][c]` – Feld aufgedeckt  
  - `flagged[r][c]` – Flagge gesetzt  
  - `adjacent_mines[r][c]` – Anzahl benachbarter Minen
- GUI-Elemente (für Tests ersetzt durch Dummy-Klassen):
  - `buttons[(r, c)]`
  - `score_label`
  - `timer_label`
- Zentrale Methoden:
  - `_place_mines()`
  - `_compute_adjacent_mines()`
  - `_ensure_first_click_safe()`
  - `_reveal_safe_or_mine()`
  - `_check_win()`

---

## 3. Testumfang (Scope)

### In-Scope

- **Spiellogik:**
  - Minenverteilung
  - Berechnung von Nachbarzahlen
  - Flood-Fill-Aufdecken sicherer Felder
  - Reaktion beim Klicken auf eine Mine
  - Erkennen eines gewonnenen Spiels

- **UI-abhängige Logik (über Dummy-Klassen getestet):**
  - Zugriff auf Buttons via `buttons[(r,c)].config()`
  - Aktualisierung von Labels (`score_label`, `timer_label`)

### Out-of-Scope

- Grafische Darstellung (Farben, Fonts, Layout)
- Animationen oder Sound
- Nutzerinteraktion über echte Mausklicks
- Timer-Funktionalität im Detail

---

## 4. Teststrategie & Testarten

### 4.1 Testebenen

- **Unit-Tests (pytest)**
  - Prüfen interne Logik unabhängig von der GUI.
  - Verwendung von Dummy-Widgets zur Entkopplung von Tkinter.

- **Systemtests (manuell)**
  - echtes Spielen über die Benutzeroberfläche
  - Tests von UX, Layout, Buttons, Spielfluss.

### 4.2 Testarten

- **Funktionale Tests**  
  Stellen sicher, dass die Spiellogik den Minesweeper-Regeln entspricht.

- **Negativtests**  
  Testen Verhalten in Randfällen (z. B. Klick auf bereits aufgedecktes Feld).

- **Regressionstests**  
  Durch erneutes Ausführen aller Pytest-Testfälle nach Codeänderungen.

---

## 5. Testumgebung

- **Hardware:** Standard-PC/Laptop
- **Betriebssystem:** Windows 10/11, macOS, Linux
- **Programmiersprache:** Python 3.11+
- **Bibliotheken:**
  - `tkinter` (GUI)
  - `pytest` (Test-Framework)
- **Tools:**
  - PyCharm Community / Professional
  - Windows Terminal / PowerShell

---

## 6. Konkrete Unit-Testfälle

Die Testfälle entsprechen **1:1** den implementierten Tests in `test_minesweeper.py`.

---

### **UT-001 – Korrektes Platzieren von Minen**

- **Methode:** `_place_mines`
- **Fixture:** `_setup_board(5,5,5)`
- **Test:** `test_place_mines_correct_count`
- **Ziel:** Anzahl gesetzter Minen entspricht `mines_total`.
- **Erwartetes Ergebnis:** `mine_count == 5`

---

### **UT-002 – Berechnung von Nachbarminen (3×3 Muster)**

- **Methode:** `_compute_adjacent_mines`
- **Test:** `test_compute_adjacent_mines_known_pattern`
- **Board:**  
. M .
M . M
. . .

- **Erwartete Matrix:**
2 -1 2
-1 3 -1
1 2 1

---

### **UT-003 – First-Click-Safe**

- **Methode:** `_ensure_first_click_safe`
- **Test:** `test_first_click_safe_moves_mine`
- **Ziel:**  
- Das erste Feld darf keine Mine enthalten.
- Gesamtzahl der Minen bleibt gleich.

---

### **UT-004 – Flood-Fill Funktion (0-er Feld aufdecken)**

- **Methode:** `_reveal_safe_or_mine`
- **Test:** `test_reveal_safe_flood_fill`
- **Setup:**  
- Mine nur in (0,2)
- Feld (2,0) hat 0 Nachbarminen
- **Erwartetes Feld nach Aufdecken (`revealed`):**

T T F
T T T
T T T


---

### **UT-005 – Klick auf Mine löst Game Over aus**

- **Methode:** `_reveal_safe_or_mine`
- **Test:** `test_reveal_on_mine_sets_game_over`
- **Erwartetes Ergebnis:**  
- `game_over == True`  
- getroffenes Feld wird `revealed == True`

---

### **UT-006 – Gewinnbedingung**

- **Methode:** `_check_win`
- **Test:** `test_check_win_sets_game_over`
- **Setup:**  
- 2×2 Board, 1 Mine  
- Alle sicheren Felder sind `revealed == True`
- **Erwartetes Ergebnis:**  
- `game_over == True`

---

## 7. Fehler- und Änderungsmanagement

### Erfassung eines Fehlers

Jeder Fehler wird dokumentiert mit:

1. **Testfall-ID** (z. B. UT-004)
2. **Kurzbeschreibung**
3. **Erwartetes Verhalten**
4. **Tatsächliches Verhalten**
5. **Schweregrad**
6. **Status**

### Vorgehen bei Änderungen

1. Code in `main.py` anpassen  
2. `pytest` erneut ausführen  
3. Bei neuen Features → neue Tests erstellen  
4. Dieses Manual aktualisieren

---

## 8. Definition of Done (DoD) für Tests

Ein Increment gilt als fertig, wenn:

- Alle Pytest-Testfälle **grün** sind  
- Keine kritischen Fehler offen sind  
- Manuelle Systemtests erfolgreich  
- Dokumentation (inkl. Test-Manual) aktualisiert wurde  

---

## 9. Testdokumentation

- **TEST_MANUAL.md** – dieses Dokument  
- **test_minesweeper.py** – automatisierte pytest-Tests  
- **main.py** – getestete Minesweeper-Implementierung  

