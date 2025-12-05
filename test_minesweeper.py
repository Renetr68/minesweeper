import tkinter as tk
import pytest

from main import Minesweeper

# --- Dummy Label neu

class DummyLabel:
    def __init__(self):
        self.last_config = {}

    def config(self, **kwargs):
        # Im Test machen wir nichts Sichtbares, merken uns nur die Werte
        self.last_config.update(kwargs)


# --- Dummy-Widgets für GUI-abhängige Methoden -----------------------------

class DummyWidget:
    """Ein sehr einfacher Ersatz für Tk-Widgets, der nur .config() kennt."""
    def __init__(self):
        self.last_config = {}

    def config(self, **kwargs):
        self.last_config.update(kwargs)


# --- Pytest-Fixture für die App -------------------------------------------

@pytest.fixture
def app():
    """Erzeugt eine Minesweeper-Instanz ohne sichtbares Fenster."""
    root = tk.Tk()
    root.withdraw()  # kein Fenster anzeigen
    game = Minesweeper(root)
    yield game
    root.destroy()


def _setup_board(app, rows, cols, mines_total=0):
    """
    Hilfsfunktion: Setzt die Logik-Strukturen (is_mine, revealed, flagged,
    adjacent_mines, buttons, timer_label) passend für kleine Test-Boards.
    """
    app.rows = rows
    app.cols = cols
    app.mines_total = mines_total

    app.is_mine = [[False] * cols for _ in range(rows)]
    app.revealed = [[False] * cols for _ in range(rows)]
    app.flagged = [[False] * cols for _ in range(rows)]
    app.adjacent_mines = [[0] * cols for _ in range(rows)]

    # Dummy-Buttons für alle Felder
    app.buttons = {
        (r, c): DummyWidget()
        for r in range(rows)
        for c in range(cols)
    }

    # Dummy-Timer-Label (wird in _handle_mine_click / _check_win benutzt)
    app.timer_label = DummyWidget()


# --- Tests -----------------------------------------------------------------


def test_place_mines_correct_count(app):
    """
    _place_mines soll genau mines_total Minen platzieren.
    """
    _setup_board(app, rows=5, cols=5, mines_total=5)

    app._place_mines()
    mine_count = sum(
        1 for r in range(app.rows) for c in range(app.cols) if app.is_mine[r][c]
    )

    assert mine_count == 5


def test_compute_adjacent_mines_known_pattern(app):
    """
    Prüft _compute_adjacent_mines anhand eines festen 3x3-Boards.
    Layout:
        . M .
        M . M
        . . .

    Erwartete Nachbarzahlen:
        2 - 2
        - 3 -
        1 2 1

    '-' = Mine (adjacent_mines = -1)
    """
    _setup_board(app, rows=3, cols=3, mines_total=3)

    app.is_mine = [
        [False, True,  False],
        [True,  False, True ],
        [False, False, False],
    ]

    app._compute_adjacent_mines()

    expected = [
        [2, -1, 2],
        [-1, 3, -1],
        [1, 2, 1],  # <- hier war vorher 2 statt 1 und hat den Fehler ausgelöst
    ]

    assert app.adjacent_mines == expected


def test_first_click_safe_moves_mine(app):
    """
    _ensure_first_click_safe soll sicherstellen, dass das angeklickte Feld
    keine Mine ist, indem eine evtl. vorhandene Mine verschoben wird.
    """
    _setup_board(app, rows=3, cols=3, mines_total=1)

    # Mine liegt an (1,1)
    app.is_mine[1][1] = True

    app._compute_adjacent_mines()
    app._ensure_first_click_safe(1, 1)

    # Feld (1,1) darf danach keine Mine mehr sein
    assert not app.is_mine[1][1]

    # Insgesamt muss weiterhin genau 1 Mine existieren
    total_mines = sum(
        1 for r in range(app.rows) for c in range(app.cols) if app.is_mine[r][c]
    )
    assert total_mines == 1


def test_reveal_safe_flood_fill(app):
    """
    Prüft Flood-Fill bei _reveal_safe_or_mine:
    Ein Feld mit 0 Nachbarminen deckt alle verbundenen sicheren Felder +
    deren direkte Nachbarn (ohne Minen) auf.
    """
    _setup_board(app, rows=3, cols=3, mines_total=1)

    # 👉 Dummy-Score-Label einhängen, damit _reveal_safe_or_mine nicht crasht
    app.score_label = DummyLabel()

    # Mine oben rechts, Rest sicher
    #   (0,2) = Mine
    app.is_mine = [
        [False, False, True],
        [False, False, False],
        [False, False, False],
    ]

    app._compute_adjacent_mines()

    # Feld (2,0) sollte 0 Nachbarminen haben
    assert app.adjacent_mines[2][0] == 0

    # Aktion: Flood-Fill starten
    app._reveal_safe_or_mine(2, 0)

    # Erwartetes Ergebnis (alle sicheren Felder außer der Mine sind aufgedeckt):
    expected_revealed = [
        [True,  True,  False],
        [True,  True,  True],
        [True,  True,  True],
    ]

    assert app.revealed == expected_revealed


def test_reveal_on_mine_sets_game_over(app):
    """
    Klickt man auf eine Mine, muss game_over = True sein.
    """
    _setup_board(app, rows=2, cols=2, mines_total=1)

    app.is_mine = [
        [True,  False],
        [False, False],
    ]

    app._compute_adjacent_mines()

    # Mine anklicken
    app._reveal_safe_or_mine(0, 0)

    assert app.game_over is True
    assert app.revealed[0][0] is True


def test_check_win_sets_game_over(app):
    """
    Wenn alle sicheren Felder aufgedeckt sind, muss _check_win game_over setzen.
    """
    _setup_board(app, rows=2, cols=2, mines_total=1)

    app.is_mine = [
        [True,  False],
        [False, False],
    ]

    # Sichere Felder: (0,1), (1,0), (1,1) -> alle aufgedeckt
    app.revealed = [
        [False, True],
        [True,  True],
    ]

    app._check_win()

    assert app.game_over is True
