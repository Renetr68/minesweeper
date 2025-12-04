import tkinter as tk
import random
import time

# Neue Konstante: Vordefinierte Schwierigkeitsgrade (Zeilen, Spalten, Minen)
DIFFICULTIES = {
    "Einfach": (9, 9, 10),
    "Mittel": (16, 16, 40),
    "Schwer": (16, 30, 99),
}

# Neue Konstante: Farben für die Zahlenanzeige nach Minesweeper-Konvention
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
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Minesweeper")

        # Neue Layout-Einstellung: Feste Fenstergröße, nicht veränderbar, zentriert und einheitlicher Hintergrund
        width, height = 900, 700
        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.minsize(width, height)
        self.master.resizable(False, False)  # Neue Einstellung: Fenstergröße fixieren
        self.master.configure(bg="#15171a")

        # Grundzustand für Board & Spielvariablen
        self.rows = 0
        self.cols = 0
        self.mines_total = 0
        self.is_mine = []
        self.revealed = []
        self.adjacent_mines = []
        self.buttons = {}

        self.started = False
        self.game_over = False
        self.timer_id = None
        self.start_time = None
        self.elapsed_sec = 0
        self.score = 0
        self.current_difficulty = None

        self.topbar = None
        self.grid_frame = None
        self.menu_frame = None
        self.score_label = None
        self.timer_label = None

        # Neue Initialisierung: Startmenü anstelle direkter Spielfeldanzeige
        self._build_menu()

    def _build_menu(self):
        # Neue Funktion: Baut ein Startmenü mit zentriertem „Card“-Layout für die Schwierigkeitswahl
        self._stop_timer()
        self.started = False
        self.game_over = False

        # Alle bisherigen Widgets (z. B. Spielfeld) entfernen
        for w in self.master.winfo_children():
            w.destroy()

        # Hintergrund-Container
        self.menu_frame = tk.Frame(self.master, bg="#15171a")
        self.menu_frame.pack(expand=True, fill="both")

        # Card in der Mitte
        inner = tk.Frame(self.menu_frame, bg="#1f2125", padx=30, pady=30)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            inner,
            text="Minesweeper",
            fg="white",
            bg="#1f2125",
            font=("Segoe UI", 24, "bold"),
        )
        title.pack(pady=(0, 16))

        subtitle = tk.Label(
            inner,
            text="Wähle einen Schwierigkeitsgrad",
            fg="#bdc3c7",
            bg="#1f2125",
            font=("Segoe UI", 12),
        )
        subtitle.pack(pady=(0, 20))

        # Buttons für die drei Schwierigkeitsgrade
        for level in ("Einfach", "Mittel", "Schwer"):
            btn = tk.Button(
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
            )
            btn.pack(pady=6)

        # Fußzeile / Info
        footer = tk.Label(
            inner,
            text="Linksklick: Feld öffnen",
            fg="#7f8c8d",
            bg="#1f2125",
            font=("Segoe UI", 9),
        )
        footer.pack(pady=(16, 0))

    def _start_from_menu(self, level):
        # Neue Funktion: Startet ein neues Spiel basierend auf gewählter Difficulty
        self.current_difficulty = level
        rows, cols, mines = DIFFICULTIES[level]
        self._start_game(rows, cols, mines)

    def _start_game(self, rows, cols, mines):
        # Neue Funktion: Setzt alle Spielzustände zurück und baut Spielfeld & Topbar auf
        self._stop_timer()

        self.rows, self.cols, self.mines_total = rows, cols, mines
        self.is_mine = [[False] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.adjacent_mines = [[0] * self.cols for _ in range(self.rows)]
        self.buttons = {}
        self.started = False
        self.game_over = False
        self.timer_id = None
        self.start_time = None
        self.elapsed_sec = 0
        self.score = 0

        # Alle bisherigen Widgets (z. B. Menü) entfernen
        for w in self.master.winfo_children():
            w.destroy()

        # Haupt-Container: Hält Topbar oben und Spielfeld zentriert darunter
        self.main_frame = tk.Frame(self.master, bg="#15171a")
        self.main_frame.pack(expand=True, fill="both")

        # Topbar
        self.topbar = tk.Frame(self.main_frame, bg="#1f2125", padx=12, pady=8)
        self.topbar.pack(fill="x")

        # Button: Zurück zum Menü
        self.btn_menu = tk.Button(
            self.topbar,
            text="🏠 Menü",
            command=self._back_to_menu,
            bg="#3a3d42",
            fg="white",
            bd=0,
            padx=10,
            pady=6,
            activebackground="#4a4d55",
            activeforeground="white",
            cursor="hand2",
        )
        self.btn_menu.pack(side="left")

        # Button: Neustart mit aktuellem Schwierigkeitsgrad
        self.btn_restart = tk.Button(
            self.topbar,
            text="⟳ Neustart",
            command=self.restart_game,
            bg="#3a3d42",
            fg="white",
            bd=0,
            padx=10,
            pady=6,
            activebackground="#4a4d55",
            activeforeground="white",
            cursor="hand2",
        )
        self.btn_restart.pack(side="left", padx=(8, 0))

        # Anzeige des aktuellen Modus
        mode_text = f"Modus: {self.current_difficulty}" if self.current_difficulty else "Modus"
        self.mode_label = tk.Label(
            self.topbar,
            text=mode_text,
            fg="#bdc3c7",
            bg="#1f2125",
            font=("Segoe UI", 10),
        )
        self.mode_label.pack(side="left", padx=(16, 0))

        # Score-Label
        self.score_label = tk.Label(
            self.topbar,
            text="Score: 0",
            fg="white",
            bg="#1f2125",
            font=("Segoe UI", 11, "bold"),
        )
        self.score_label.pack(side="right")

        # Timer-Label
        self.timer_label = tk.Label(
            self.topbar,
            text="Zeit: 0s",
            fg="white",
            bg="#1f2125",
            font=("Segoe UI", 11, "bold"),
        )
        self.timer_label.pack(side="right", padx=(0, 16))

        # Content-Container: Zentriert das Spielfeld
        self.content_frame = tk.Frame(self.main_frame, bg="#15171a")
        self.content_frame.pack(expand=True, fill="both")

        # Grid-Frame als „Card“ in der Mitte
        self.grid_frame = tk.Frame(self.content_frame, padx=8, pady=8, bg="#1f2125")
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Minen setzen und Nachbarzahlen berechnen
        self._place_mines()
        self._compute_adjacent_mines()
        self._build_grid()

    def _back_to_menu(self):
        # Neue Funktion: Bringt den Benutzer zurück ins Startmenü (Anfangsstate)
        self._stop_timer()
        self.started = False
        self.game_over = False
        self._build_menu()

    def _build_grid(self):
        # Neue Anpassung: Zellengröße dynamisch je nach Spaltenanzahl für bessere Lesbarkeit
        if self.cols <= 10:
            cell_width = 4
            font_size = 13
        elif self.cols <= 16:
            cell_width = 3
            font_size = 12
        else:
            cell_width = 2
            font_size = 10

        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(
                    self.grid_frame,
                    width=cell_width,
                    height=1,
                    text="",
                    relief="flat",  # moderner Look
                    font=("Segoe UI", font_size, "bold"),
                    bg="#2f343f",
                    fg="white",
                    activebackground="#4b5160",
                    activeforeground="white",
                    bd=0,
                    highlightthickness=0,
                    cursor="hand2",
                )
                b.grid(row=r, column=c, padx=1, pady=1)
                b.bind("<Button-1>", lambda e, rr=r, cc=c: self._reveal(rr, cc))
                self.buttons[(r, c)] = b

    def _reveal(self, r, c):
        # Guard: Keine weitere Interaktion, wenn das Spiel bereits beendet ist
        if self.game_over:
            return

        # Neuer Schritt: Erster Klick wird garantiert sicher gemacht
        if not self.started:
            # Neue Funktion: Sichert, dass das erste angeklickte Feld keine Mine enthält
            self._ensure_first_click_safe(r, c)
            self.started = True
            self._start_timer()

        # Zentrale Reveal-Logik
        self._reveal_safe_or_mine(r, c)

    def _ensure_first_click_safe(self, r, c):
        # Neue Funktion: Stellt sicher, dass das erste Feld keine Mine ist (Mine ggf. umsetzen)
        if not self.is_mine[r][c]:
            return

        # Alle Kandidaten, die keine Mine sind und nicht das geklickte Feld sind
        candidates = [
            (rr, cc)
            for rr in range(self.rows)
            for cc in range(self.cols)
            if not self.is_mine[rr][cc] and not (rr == r and cc == c)
        ]

        if candidates:
            new_r, new_c = random.choice(candidates)
            self.is_mine[r][c] = False
            self.is_mine[new_r][new_c] = True
        else:
            # Edge-Case: Falls keine Kandidaten vorhanden, Mine einfach entfernen
            self.is_mine[r][c] = False

        # Nach der Veränderung die Nachbarzahlen neu berechnen
        self._compute_adjacent_mines()

    def _reveal_safe_or_mine(self, r, c):
        # Funktion: Effizientes Aufdecken (inkl. Zahlenanzeige und Flood-Fill bei 0)
        if self.revealed[r][c]:
            return
        if self.is_mine[r][c]:
            self._handle_mine_click(r, c)
            return

        # Iteratives Flood-Fill zur Performance-Optimierung
        queue = [(r, c)]
        while queue:
            cr, cc = queue.pop()
            if self.revealed[cr][cc]:
                continue
            if self.is_mine[cr][cc]:
                continue

            self.revealed[cr][cc] = True
            btn = self.buttons[(cr, cc)]
            count = self.adjacent_mines[cr][cc]

            if count > 0:
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
                btn.config(
                    text="",
                    state="disabled",
                    relief="flat",
                    bg="#262a33",
                    disabledforeground="white",
                )
                # Nur wenn 0 benachbarte Minen: angrenzende Felder in Queue
                for nr in range(max(0, cr - 1), min(self.rows, cr + 2)):
                    for nc in range(max(0, cc - 1), min(self.cols, cc + 2)):
                        if not self.revealed[nr][nc] and not self.is_mine[nr][nc]:
                            queue.append((nr, nc))

            # Score pro neu aufgedecktem sicheren Feld erhöhen
            self.score += 1

        # Score-Anzeige aktualisieren und Gewinn prüfen
        self.score_label.config(text=f"Score: {self.score}")
        self._check_win()

    def _handle_mine_click(self, r, c):
        # Funktion: Behandelt Game-Over bei Klick auf eine Mine (Endscreen bleibt stehen)
        self.game_over = True
        self.revealed[r][c] = True
        self._stop_timer()

        btn = self.buttons[(r, c)]
        btn.config(
            text="💣",
            state="disabled",
            relief="flat",
            bg="#E74C3C",
            fg="white",
            disabledforeground="white",
        )
        self._reveal_all_mines()
        self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s  ✖")
        # Kein automatischer Rücksprung – Endscreen bleibt sichtbar

    def _reveal_all_mines(self):
        # Funktion: Zeigt nach Game Over alle Minen und sperrt alle Felder
        for rr in range(self.rows):
            for cc in range(self.cols):
                btn = self.buttons[(rr, cc)]
                if self.is_mine[rr][cc]:
                    if not self.revealed[rr][cc]:
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

    def _place_mines(self):
        # Zufälliges Platzieren der Minen
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_cells = set(random.sample(all_cells, min(self.mines_total, len(all_cells))))
        for r, c in mine_cells:
            self.is_mine[r][c] = True

    def _compute_adjacent_mines(self):
        # Hilfsfunktion: Berechnet die Anzahl angrenzender Minen pro Feld
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

    # -------- Timer --------
    def _start_timer(self):
        # Fix: Timer nur starten, wenn keiner läuft
        if self.timer_id is not None:
            return
        self.start_time = time.perf_counter()
        self._tick()

    def _tick(self):
        if self.game_over:
            return
        self.elapsed_sec = int(time.perf_counter() - (self.start_time or time.perf_counter()))
        self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s")
        self.timer_id = self.after(1000, self._tick)

    def _stop_timer(self):
        # Fix: Timer sauber stoppen und Timer-ID zurücksetzen
        if self.timer_id is not None:
            try:
                self.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

    # -------- Gewonnen? --------
    def _check_win(self):
        total = self.rows * self.cols
        safe_cells = total - self.mines_total
        revealed_safe = 0
        for rr in range(self.rows):
            for cc in range(self.cols):
                if self.revealed[rr][cc] and not self.is_mine[rr][cc]:
                    revealed_safe += 1

        if revealed_safe >= safe_cells:
            self.game_over = True
            self._stop_timer()
            self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s  ✔")
            # Endscreen bleibt sichtbar, Restart/ Menü über Buttons

    # -------- Neustart --------
    def restart_game(self):
        # Neue Logik: „Neustart“ startet direkt ein neues Spiel mit aktuellem Schwierigkeitsgrad
        if self.current_difficulty is None:
            self._back_to_menu()
            return
        rows, cols, mines = DIFFICULTIES[self.current_difficulty]
        self._start_game(rows, cols, mines)


def main():
    root = tk.Tk()
    # Startet mit Startmenü, Difficulty wird dort gewählt
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()