# Setup-Anleitung für Git & PyCharm

## 1. PyCharm installieren (Entwickler)

Lade PyCharm von [jetbrains.com](https://www.jetbrains.com/pycharm/) herunter und installiere es.

---

## 2. Git installieren (alle)

Download-Link: [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)

Verwende die **Default-Einstellungen** außer bei:  
- *Override the default branch name for new repositories*  
- *Use Windows' default console window*

---

## 3. GitHub Konto registrieren (alle)

Lege ein Konto auf [github.com](https://github.com) an.

---

## 4. Git Repository lokal klonen

1. Öffne die **cmd** im gewünschten Speicherort.  
   Beispiel:
   ```bash
   C:\Users\renet\OneDrive\Dokumente\FH Master TM>git clone https://github.com/Renetr68/minesweeper.git
   ```

2. Mit GitHub-Konto einloggen und Git-Ökosystem autorisieren.  
3. Das Repository ist nun im gewählten Ordner verfügbar.

---

## 5. Python installieren

Lade Python von [python.org](https://www.python.org/downloads/) herunter und installiere es.

---

## 6. Projekt in PyCharm öffnen (Entwickler)

Öffne den geklonten Projektordner in PyCharm.

---

# Git Grundlagenbefehle

- `git add` – markiert Änderungen an Dateien für den nächsten Commit.  
- `git commit -m "Nachricht"` – speichert die markierten Änderungen dauerhaft mit Kommentar.  
- `git status` – zeigt den aktuellen Stand der Dateien und Commits an.  
- `git log` – listet die bisherigen Commits mit Details auf.  
- `git clone <URL>` – kopiert ein bestehendes Repository auf den lokalen Rechner.  
- `git pull` – holt Änderungen vom Remote-Repository und integriert sie lokal.  
- `git push` – überträgt lokale Commits ins Remote-Repository.  
