import tkinter as tk
import random
import time

class Minesweeper(tk.Frame):
    def __init__(self, master=None, rows=9, cols=9, mines=10):
        super().__init__(master)
        self.master = master
        self.master.title("Minesweeper (Minimal)")
        self.rows, self.cols, self.mines_total = rows, cols, mines

        # Zustand
        self.is_mine = [[False]*self.cols for _ in range(self.rows)]
        self.revealed = [[False]*self.cols for _ in range(self.rows)]
        self.buttons = {}

        # Minen einmalig zufällig setzen
        self._place_mines()

        # Grid erzeugen
        self.grid_frame = tk.Frame(self.master, padx=4, pady=4)
        self.grid_frame.pack()
        self._build_grid()

        # Spiel-/Timer-/Score-Status
        self.started = False
        self.game_over = False
        self.timer_id = None
        self.start_time = None
        self.elapsed_sec = 0
        self.score = 0

        # Topbar für Bedienung & Anzeigen
        self.topbar = tk.Frame(self.master, bg="#2b2d31", padx=8, pady=6)
        self.topbar.pack(fill="x")

        self.btn_new = tk.Button(self.topbar, text="＋ Neues Spiel", command=self.new_game_dialog, bg="#3a3d42",
                                 fg="white", bd=0, padx=10, pady=6, activebackground="#4a4d55")
        self.btn_new.pack(side="left")

        self.btn_restart = tk.Button(self.topbar, text="⟳ Neustart", command=self.restart_game, bg="#3a3d42",
                                     fg="white", bd=0, padx=10, pady=6, activebackground="#4a4d55")
        self.btn_restart.pack(side="left", padx=(8, 0))

        self.score_label = tk.Label(self.topbar, text="Score: 0", fg="white", bg="#2b2d31",
                                    font=("Segoe UI", 11, "bold"))
        self.score_label.pack(side="right")

        self.timer_label = tk.Label(self.topbar, text="Zeit: 0s", fg="white", bg="#2b2d31",
                                    font=("Segoe UI", 11, "bold"))
        self.timer_label.pack(side="right", padx=(0, 16))

    def _build_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.grid_frame,width=2, height=1,text="",relief="raised",font=("Segoe UI", 11, "bold"),bg="#4a4d55",fg="white",activebackground="#5a5e66",activeforeground="white",bd=1,highlightthickness=0,cursor="hand2")
                b.grid(row=r, column=c, padx=1, pady=1)
                b.bind("<Button-1>", lambda e, rr=r, cc=c: self._reveal(rr, cc))
                self.buttons[(r, c)] = b
                self.grid_frame.configure(bg="#1f2125")

    def _reveal(self, r, c):
        if self.revealed[r][c]:
            return
        self.revealed[r][c] = True
        btn = self.buttons[(r, c)]
        if self.is_mine[r][c]:
            btn.config(text="💣", state="disabled", relief="sunken",
                       bg="#E74C3C", fg="white", disabledforeground="white")
        else:
            btn = self.buttons[(r, c)]
            btn.config(text="", state="disabled", relief="sunken", bg="#2b2d31", disabledforeground="white")
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self._check_win()
        if not self.started and not self.game_over:
            self.started = True
            self._start_timer()




    def _place_mines(self):
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_cells = set(random.sample(all_cells, min(self.mines_total, len(all_cells))))
        for r, c in mine_cells:
            self.is_mine[r][c] = True


    # -------- Timer --------
    def _start_timer(self):
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
            # Visuelles Feedback (optional leicht grün färben)
            self.timer_label.config(text=f"Zeit: {self.elapsed_sec}s  ✔")

    # -------- Neustart (gleiche Settings) --------
    def restart_game(self):
        self._stop_timer()
        self.started = False
        self.game_over = False
        self.elapsed_sec = 0
        self.score = 0
        self.timer_label.config(text="Zeit: 0s")
        self.score_label.config(text="Score: 0")
        self._reset_state(self.rows, self.cols, self.mines_total)

    # -------- Neues Spiel Dialog --------
    def new_game_dialog(self):
        win = tk.Toplevel(self.master)
        win.title("Neues Spiel")
        win.resizable(False, False)
        container = tk.Frame(win, padx=10, pady=10)
        container.pack()

        tk.Label(container, text="Zeilen:").grid(row=0, column=0, sticky="e", pady=2)
        tk.Label(container, text="Spalten:").grid(row=1, column=0, sticky="e", pady=2)
        tk.Label(container, text="Minen:").grid(row=2, column=0, sticky="e", pady=2)

        e_rows = tk.Entry(container, width=6)
        e_cols = tk.Entry(container, width=6)
        e_mines = tk.Entry(container, width=6)
        e_rows.grid(row=0, column=1, padx=6, pady=2)
        e_cols.grid(row=1, column=1, padx=6, pady=2)
        e_mines.grid(row=2, column=1, padx=6, pady=2)

        # Default: aktuelle Werte
        e_rows.insert(0, str(self.rows))
        e_cols.insert(0, str(self.cols))
        e_mines.insert(0, str(self.mines_total))

        def apply():
            try:
                nr = max(1, int(e_rows.get()))
                nc = max(1, int(e_cols.get()))
                nm = max(0, int(e_mines.get()))
                nm = min(nm, nr * nc - 1)  # mindestens ein Safe-Feld
            except ValueError:
                win.destroy()
                return
            win.destroy()
            self._apply_new_game(nr, nc, nm)

        tk.Button(container, text="Starten", command=apply).grid(row=3, column=0, columnspan=2, pady=(8, 0))

    # -------- Neues Spiel anwenden --------
    def _apply_new_game(self, rows, cols, mines):
        self._stop_timer()
        self.started = False
        self.game_over = False
        self.elapsed_sec = 0
        self.score = 0
        self.timer_label.config(text="Zeit: 0s")
        self.score_label.config(text="Score: 0")
        self._reset_state(rows, cols, mines)

    # -------- Zustand zurücksetzen + Grid neu bauen --------
    def _reset_state(self, rows, cols, mines):
        # Daten aktualisieren
        self.rows, self.cols, self.mines_total = rows, cols, mines
        self.is_mine = [[False] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.buttons.clear()

        # alte Buttons im Frame entfernen
        for w in self.grid_frame.winfo_children():
            w.destroy()

        # Minen neu legen & Grid neu bauen
        self._place_mines()
        self._build_grid()

def main():
    root = tk.Tk()
    Minesweeper(root, rows=10, cols=10, mines=99)
    root.mainloop()

if __name__ == "__main__":
    main()

