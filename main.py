import tkinter as tk
import random

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

    def _build_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.grid_frame, width=2, height=1, text="")
                b.grid(row=r, column=c, padx=1, pady=1)
                b.bind("<Button-1>", lambda e, rr=r, cc=c: self._reveal(rr, cc))
                self.buttons[(r, c)] = b

    def _reveal(self, r, c):
        if self.revealed[r][c]:
            return
        self.revealed[r][c] = True
        btn = self.buttons[(r, c)]
        if self.is_mine[r][c]:
            btn.config(text="💣", state="disabled", relief="sunken", disabledforeground="black")
        else:
            btn.config(text="", state="disabled", relief="sunken")

    def _place_mines(self):
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_cells = set(random.sample(all_cells, min(self.mines_total, len(all_cells))))
        for r, c in mine_cells:
            self.is_mine[r][c] = True

def main():
    root = tk.Tk()
    Minesweeper(root, rows=9, cols=9, mines=10)
    root.mainloop()

if __name__ == "__main__":
    main()

