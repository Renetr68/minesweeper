import tkinter as tk
import random
import time

# Vordefinierte Schwierigkeitsgrade: (Zeilen, Spalten, Minen)
DIFFICULTIES = {
    "Einfach": (9, 9, 10),
    "Mittel": (16, 16, 40),
    "Schwer": (16, 30, 99),
}

# Farben für Zahlen entsprechend der Minenanzahl
NUMBER_COLORS = {
    1: "#3498DB",
    2: "#2ECC71",
    3: "#E67E22",
    4: "#9B59B6",
    5: "#E74C3C",
    6: "#1ABC9C",
    7: "#F1C40F",
    8: "#95A5A6",
}


class Minesweeper(tk.Frame):
    # Hauptklasse für das Spiel
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Minesweeper")

        # Feste Fenstergröße, zentriert, nicht resizable, einheitlicher Hintergrund
        width, height = 900, 700
        sw, sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        x, y = (sw - width) // 2, (sh - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.minsize(width, height)
        self.master.resizable(False, False)
        self.master.configure(bg="#15171a")

        # Basiszustand-Variablen
        self.rows = 0
        self.cols = 0
        self.mines_total = 0
        self.is_mine = []          # boolean pro Feld: Mine ja/nein
        self.revealed = []         # boolean pro Feld: bereits aufgedeckt
        self.flagged = []          # boolean pro Feld: Flagge gesetzt
        self.adjacent_mines = []   # int pro Feld: Anzahl angrenzender Minen
        self.buttons = {}          # (r, c) -> Button-Widget

        self.started = False       # wurde bereits geklickt (für Timer + first-click-safe)
        self.game_over = False
        self.timer_id = None
        self.start_time = None
        self.elapsed_sec = 0
        self.score = 0
        self.current_difficulty = None  # aktuell gewählter Schwierigkeitsgrad (String)

        # Starte im Startmenü
        self._build_menu()

    # ===========================================================
    # Startmenü / Navigation
    # ===========================================================
    def _build_menu(self):
        """Erzeugt das Startmenü mit den Schwierigkeits-Buttons."""
        self._stop_timer()
        self.started = False
        self.game_over = False

        # Alle bisherigen Widgets entfernen (Spielfeld, Topbar, etc.)
        for w in self.master.winfo_children():
            w.destroy()

        # Hintergrund-Frame (füllt gesamtes Fenster)
        menu_frame = tk.Frame(self.master, bg="#15171a")
        menu_frame.pack(expand=True, fill="both")

        # Zentrierte "Card" für ein elegantes Menü
        inner = tk.Frame(menu_frame, bg="#1f2125", padx=30, pady=30)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            inner, text="Minesweeper",
            fg="white", bg="#1f2125",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(0, 16))

        tk.Label(
            inner, text="Wähle einen Schwierigkeitsgrad",
            fg="#bdc3c7", bg="#1f2125",
            font=("Segoe UI", 12)
        ).pack(pady=(0, 20))

        # Buttons für die vordefinierten Schwierigkeitsgrade
        for level in ("Einfach", "Mittel", "Schwer"):
            tk.Button(
                inner,
                text=level,
                command=lambda lvl=level: self._start_from_menu(lvl),
                bg="#3a3d42",
                fg="white",
                bd=0,
                padx=20,
                pady=10,
                activebackground="#4a4d55",
                activeforeground="white",
                font=("Segoe UI", 11, "bold"),
                cursor="hand2",
                width=14,
            ).pack(pady=6)

        # Info-Leiste für Steuerung
        tk.Label(
            inner,
            text="Linksklick: Feld öffnen   |   Rechtsklick: Flagge 🚩 setzen/entfernen",
            fg="#7f8c8d",
            bg="#1f2125",
            font=("Segoe UI", 9),
        ).pack(pady=(16, 0))

    def _start_from_menu(self, level: str):
        """Startet ein neues Spiel mit dem im Menü gewählten Schwierigkeitsgrad."""
        self.current_difficulty = level
        rows, cols, mines = DIFFICULTIES[level]
        self._start_game(rows, cols, mines)

    def _start_game(self, rows: int, cols: int, mines: int):
        """Initialisiert Spiellogik und UI für ein neues Spiel."""
        self._stop_timer()

        # Spielzustand zurücksetzen / initialisieren
        self.rows, self.cols, self.mines_total = rows, cols, mines
        self.is_mine = [[False] * cols for _ in range(rows)]
        self.revealed = [[False] * cols for _ in range(rows)]
        self.flagged = [[False] * cols for _ in range(rows)]
        self.adjacent_mines = [[0] * cols for _ in range(rows)]
        self.buttons.clear()
        self.started = False
        self.game_over = False
        self.timer_id = None
        self.start_time = None
        self.elapsed_sec = 0
        self.score = 0

        # Alte Widgets entfernen
        for w in self.master.winfo_children():
            w.destroy()

        # Hauptcontainer
        main = tk.Frame(self.master, bg="#15171a")
        main.pack(expand=True, fill="both")

        # Topbar oben
        top = tk.Frame(main, bg="#1f2125", padx=12, pady=8)
        top.pack(fill="x")

        # Button: zurück zum Menü
        tk.Button(
            top, text="🏠 Menü", command=self._back_to_menu,
            bg="#3a3d42", fg="white", bd=0, padx=10, pady=6,
            activebackground="#4a4d55", activeforeground="white", cursor="hand2",
        ).pack(side="left")

        # Button: Neustart mit gleichem Schwierigkeitsgrad
        tk.Button(
            top, text="⟳ Neustart", command=self.restart_game,
            bg="#3a3d42", fg="white", bd=0, padx=10, pady=6,
            activebackground="#4a4d55", activeforeground="white", cursor="hand2",
        ).pack(side="left", padx=(8, 0))

        # Anzeige des aktuellen Modus (Einfach/Mittel/Schwer)
        mode_text = f"Modus: {self.current_difficulty}" if self.current_difficulty else "Modus"
        tk.Label(
            top, text=mode_text,
            fg="#bdc3c7", bg="#1f2125",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(16, 0))

        # Score-Anzeige
        self.score_label = tk.Label(
            top, text="Score: 0",
            fg="white", bg="#1f2125",
            font=("Segoe UI", 11, "bold"),
        )
        self.score_label.pack(side="right")

        # Timer-Anzeige
        self.timer_label = tk.Label(
            top, text="Zeit: 0s",
            fg="white", bg="#1f2125",
            font=("Segoe UI", 11, "bold"),
        )
        self.timer_label.pack(side="right", padx=(0, 16))

        # Inhalt: das Spielfeld zentriert im Fenster
        content = tk.Frame(main, bg="#15171a")
        content.pack(expand=True, fill="both")

        self.grid_frame = tk.Frame(content, padx=8, pady=8, bg="#1f2125")
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Minen platzieren & Nachbarzahlen berechnen
        self._place_mines()
        self._compute_adjacent_mines()
        self._build_grid()

    def _back_to_menu(self):
        """Zurück ins Startmenü (z. B. nach Klick auf 'Menü')."""
        self._build_menu()

    # ===========================================================
    # Grid / Buttons
    # ===========================================================
    def _build_grid(self):
        """Erzeugt die Buttons des Spielfelds und bindet Klick-Events."""
        # Zellengröße abhängig von Spaltenanzahl (damit Einfach/Mittel gut lesbar)
        if self.cols <= 10:
            cell_width, font_size = 4, 13
        elif self.cols <= 16:
            cell_width, font_size = 3, 12
        else:
            cell_width, font_size = 2, 10

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.grid_frame,
                    width=cell_width,
                    height=1,
                    text="",
                    relief="flat",
                    font=("Segoe UI", font_size, "bold"),
                    bg="#2f343f",
                    fg="white",
                    activebackground="#4b5160",
                    activeforeground="white",
                    bd=0,
                    highlightthickness=0,
                    cursor="hand2",
                )
                btn.grid(row=r, column=c, padx=1, pady=1)

                # Linksklick: Feld öffnen
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self._reveal(rr, cc))
                # Rechtsklick: Flagge setzen / entfernen
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self._toggle_flag(rr, cc))

                self.buttons[(r, c)] = btn

    # ===========================================================
    # Eingabe-Handling (Reveal & Flaggen)
    # ===========================================================
    def _reveal(self, r: int, c: int):
        """Öffnet ein Feld per Linksklick (inkl. first-click-safe und Timerstart)."""
        if self.game_over:
            return
        if self.flagged[r][c]:
            # Geflaggte Felder können nicht geöffnet werden
            return

        # Erster Klick: Feld muss garantiert sicher sein
        if not self.started:
            self._ensure_first_click_safe(r, c)
            self.started = True
            self._start_timer()

        self._reveal_safe_or_mine(r, c)

    def _toggle_flag(self, r: int, c: int):
        """Setzt oder entfernt eine Flagge per Rechtsklick."""
        if self.game_over:
            return
        if self.revealed[r][c]:
            # Bereits aufgedeckte Felder können nicht geflaggt werden
            return

        self.flagged[r][c] = not self.flagged[r][c]
        btn = self.buttons[(r, c)]

        if self.flagged[r][c]:
            # Flagge setzen
            btn.config(text="🚩", fg="#F1C40F", bg="#2f343f")
        else:
            # Flagge entfernen, zurück zum verdeckten Standardzustand
            btn.config(text="", fg="white", bg="#2f343f")

    def _ensure_first_click_safe(self, r: int, c: int):
        """Stellt sicher, dass das erste angeklickte Feld keine Mine ist."""
        if not self.is_mine[r][c]:
            return

        # Finde ein anderes, nicht-minen Feld, auf das die Mine verschoben werden kann
        candidates = [
            (rr, cc)
            for rr in range(self.rows)
            for cc in range(self.cols)
            if not self.is_mine[rr][cc] and (rr, cc) != (r, c)
        ]

        if candidates:
            nr, nc = random.choice(candidates)
            self.is_mine[r][c] = False
            self.is_mine[nr][nc] = True
        else:
            # Fallback: wenn keine Kandidaten existieren, einfach Mine entfernen
            self.is_mine[r][c] = False

        # Nach Anpassung Nachbarzahlen neu berechnen
        self._compute_adjacent_mines()

    # ===========================================================
    # Reveal-Logik & Flood-Fill
    # ===========================================================
    def _reveal_safe_or_mine(self, r: int, c: int):
        """Kernlogik: Feld öffnen, bei 0 Flood-Fill, ansonsten Zahl anzeigen."""
        if self.revealed[r][c]:
            return

        # Falls doch eine Mine (nach first-click-safe nur möglich bei späteren Klicks)
        if self.is_mine[r][c]:
            self._handle_mine_click(r, c)
            return

        # Iterative Flood-Fill für Performance
        queue = [(r, c)]
        while queue:
            cr, cc = queue.pop()
            if self.revealed[cr][cc]:
                continue
            if self.is_mine[cr][cc]:
                continue
            if self.flagged[cr][cc]:
                # Geflaggte Felder nicht auto-öffnen
                continue

            self.revealed[cr][cc] = True
            btn = self.buttons[(cr, cc)]
            count = self.adjacent_mines[cr][cc]

            if count > 0:
                # Zahl anzeigen mit passender Farbe
                color = NUMBER_COLORS.get(count, "white")
                btn.config(
                    text=str(count),
                    state="disabled",
                    relief="flat",
                    bg="#262a33",
                    fg=color,
                    disabledforeground=color,
                )
            else:
                # Leeres Feld (keine benachbarten Minen)
                btn.config(
                    text="",
                    state="disabled",
                    relief="flat",
                    bg="#262a33",
                    disabledforeground="white",
                )
                # Alle Nachbarn in die Queue aufnehmen (sofern noch nicht revealed / Mine / Flagge)
                for nr in range(max(0, cr - 1), min(self.rows, cr + 2)):
                    for nc in range(max(0, cc - 1), min(self.cols, cc + 2)):
                        if (
                            not self.revealed[nr][nc]
                            and not self.is_mine[nr][nc]
                            and not self.flagged[nr][nc]
                        ):
                            queue.append((nr, nc))

            # Score für jedes neu aufgedeckte sichere Feld erhöhen
            self.score += 1

        # Score-Anzeige aktualisieren und prüfen, ob gewonnen
        self.score_label.config(text=f"Score: {self.score}")
        self._check_win()

    def _handle_mine_click(self, r: int, c: int):
        """Behandelt den Klick auf eine Mine (Game Over, Endscreen bleibt)."""
        self.game_over = True
        self.revealed[r][c] = True
        self._stop_timer()

        # Getroffene Mine hervorheben
        self.buttons[(r, c)].config(
            text="💣",
            state="disabled",
            relief="flat",
            bg="#E74C3C",
            fg="white",
            disabledforeground="white",
        )

        # Alle übrigen Minen anzeigen
        self._reveal_all_mines()
        self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s  ✖")

    def _reveal_all_mines(self):
        """Zeigt nach Game Over alle Minen und sperrt alle Buttons."""
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[(r, c)]
                if self.is_mine[r][c]:
                    if not self.revealed[r][c]:
                        btn.config(
                            text="💣",
                            state="disabled",
                            relief="flat",
                            bg="#E74C3C",
                            fg="white",
                            disabledforeground="white",
                        )
                else:
                    btn.config(state="disabled")

    # ===========================================================
    # Minen & Nachbarn
    # ===========================================================
    def _place_mines(self):
        """Platziert zufällig self.mines_total Minen auf dem Spielfeld."""
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        for r, c in random.sample(cells, min(self.mines_total, len(cells))):
            self.is_mine[r][c] = True

    def _compute_adjacent_mines(self):
        """Berechnet für jedes Feld die Anzahl angrenzender Minen."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_mine[r][c]:
                    self.adjacent_mines[r][c] = -1
                    continue
                count = 0
                for rr in range(max(0, r - 1), min(self.rows, r + 2)):
                    for cc in range(max(0, c - 1), min(self.cols, c + 2)):
                        if self.is_mine[rr][cc]:
                            count += 1
                self.adjacent_mines[r][c] = count

    # ===========================================================
    # Timer
    # ===========================================================
    def _start_timer(self):
        """Startet den Sekundentimer ab dem ersten Klick."""
        if self.timer_id is not None:
            return
        self.start_time = time.perf_counter()
        self._tick()

    def _tick(self):
        """Timer-Tick: aktualisiert jede Sekunde die Zeit-Anzeige."""
        if self.game_over:
            return
        self.elapsed_sec = int(time.perf_counter() - (self.start_time or time.perf_counter()))
        self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s")
        self.timer_id = self.after(1000, self._tick)

    def _stop_timer(self):
        """Stoppt den Timer, falls aktiv."""
        if self.timer_id is not None:
            try:
                self.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

    # ===========================================================
    # Gewinn-Check & Neustart
    # ===========================================================
    def _check_win(self):
        """Prüft, ob alle sicheren Felder aufgedeckt wurden (Gewinnbedingung)."""
        safe_cells = self.rows * self.cols - self.mines_total
        revealed_safe = sum(
            1
            for r in range(self.rows)
            for c in range(self.cols)
            if self.revealed[r][c] and not self.is_mine[r][c]
        )
        if revealed_safe >= safe_cells:
            self.game_over = True
            self._stop_timer()
            self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s  ✔")

    def restart_game(self):
        """Startet ein neues Spiel mit dem aktuellen Schwierigkeitsgrad."""
        if not self.current_difficulty:
            self._back_to_menu()
            return
        rows, cols, mines = DIFFICULTIES[self.current_difficulty]
        self._start_game(rows, cols, mines)


# Einstiegspunkt
def main():
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()