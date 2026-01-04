# Test-Manual und Testpolitik  
## Projekt *Minesweeper*  
Lehrveranstaltung *Software Engineering*

---

## 1. Einleitung und Zielsetzung

Dieses Dokument stellt eine umfassende Testdokumentation für das im Rahmen der Lehrveranstaltung *Software Engineering* entwickelte Projekt *Minesweeper* dar. Ziel dieses Test-Manuals ist es nicht, lediglich formale Testfälle aufzulisten, sondern den gesamten Testprozess reflektiert, nachvollziehbar und erfahrungsbasiert darzustellen.

Der Fokus liegt dabei insbesondere auf der Testpolitik, der gewählten Teststrategie, den gemachten Erfahrungen während des Testens sowie den Erkenntnissen, die aus Tests, Code Reviews und Refactoring gewonnen wurden. Damit folgt dieses Dokument bewusst den Vorgaben des Lektors, der den Schwerpunkt der Bewertung auf inhaltliche Tiefe, Sinnhaftigkeit der Tests und reflektierte Gedankenarbeit legt.

---

## 2. Projektüberblick

### 2.1 Projektbeschreibung

Im Projekt wurde das klassische Spiel *Minesweeper* in der Programmiersprache Python umgesetzt. Als grafisches Framework kam Tkinter zum Einsatz. Das Spiel bildet die bekannten Kernfunktionen des Originals ab, darunter:

- zufällige Platzierung von Minen  
- Berechnung benachbarter Minen  
- First-Click-Safety (der erste Klick darf keine Mine auslösen)  
- Flood-Fill-Logik bei Feldern ohne benachbarte Minen  
- Setzen und Entfernen von Flaggen  
- Erkennung von Gewinn- und Verlustbedingungen  
- grafische Darstellung des Spielfelds  

Das Projekt eignete sich besonders gut, um sowohl Spiellogik als auch GUI-nahe Programmierung zu kombinieren und dabei verschiedene Testansätze zu erproben.

---

### 2.2 Technischer Überblick

Die Anwendung basiert auf einer zentralen `Minesweeper`-Klasse, welche sowohl Spiellogik als auch große Teile der GUI-Steuerung beinhaltet. Bereits früh zeigte sich, dass Logik und Benutzeroberfläche stark miteinander gekoppelt sind. Diese Architekturentscheidung hatte später erheblichen Einfluss auf die Teststrategie und die Umsetzung der Unit-Tests.

---

## 3. Teamorganisation und Vorgehensmodell

### 3.1 Rollen im Projektteam

Das Projekt wurde in einem Team mit klar definierten Rollen umgesetzt:

- Product Owner  
- Requirements Engineer  
- Developer  
- Tester  
- Scrum Master  

Diese Rollenverteilung sollte einen realitätsnahen Softwareentwicklungsprozess abbilden und Verantwortlichkeiten klar trennen.

---

### 3.2 Scrum im Projekt

Scrum wurde im Projekt „im Bereich des Möglichen streng gelebt“. Das bedeutet, dass zentrale Scrum-Prinzipien wie iterative Entwicklung, regelmäßige Abstimmungen und klare Aufgabenverteilung umgesetzt wurden, jedoch pragmatisch an den Projektumfang angepasst.

Der Fokus lag nicht auf formalen Scrum-Artefakten, sondern auf funktionierender Zusammenarbeit und kontinuierlichem Fortschritt.

---

## 4. Rolle des Testers im Projekt

### 4.1 Verständnis der Testerrolle

Die Rolle des Testers beschränkte sich nicht auf das Schreiben von Testfällen. Vielmehr war der Tester aktiv in alle Phasen des Projekts eingebunden, insbesondere in:

- die Ableitung von Tests aus Requirements  
- die Diskussion von Implementierungsentscheidungen  
- Code Reviews  
- Refactoring-Überlegungen  

Dadurch entwickelte sich Testen zu einem integralen Bestandteil des Entwicklungsprozesses.

---

### 4.2 Verantwortung und Aufgaben

Zu den zentralen Aufgaben des Testers zählten:

- Planung und Durchführung von Tests  
- Bewertung der Testbarkeit des Codes  
- Rückmeldung an Entwickler  
- Dokumentation von Testergebnissen  
- Reflexion des gesamten Testprozesses  

Diese Aufgaben erforderten sowohl technisches Verständnis als auch kommunikative Fähigkeiten.

---

## 5. Testpolitik

### 5.1 Ziel der Testpolitik

Die Testpolitik definierte den Rahmen für alle Testaktivitäten im Projekt. Ziel war es, eine ausreichende Qualität der Spiellogik sicherzustellen, ohne eine vollständige Testabdeckung zu erzwingen.

Qualität wurde dabei als stabile, nachvollziehbare und konsistente Spiellogik verstanden.

---

### 5.2 Qualitätskriterien

Im Fokus standen folgende Qualitätskriterien:

- korrekte Spiellogik  
- konsistente Zustandsübergänge  
- reproduzierbares Verhalten  
- verständlicher und wartbarer Code  

Nicht angestrebt wurden vollständige Fehlerfreiheit oder automatisierte GUI-Tests.

---

### 5.3 Testen als Erkenntnisgewinn

Eine zentrale Erkenntnis des Projekts war, dass Tests nicht nur Fehler aufdecken, sondern auch Designschwächen sichtbar machen und Refactoring anstoßen. Testen wurde somit als Werkzeug zur Wissens- und Qualitätssteigerung verstanden.

---

## 6. Teststrategie

### 6.1 Strategischer Ansatz

Die Teststrategie setzte auf eine Kombination aus:

- automatisierten Unit-Tests  
- manuellen End-to-End-Tests  
- Code Reviews  
- Refactoring  

Diese Kombination erwies sich als besonders effektiv für den Projektkontext.

---

### 6.2 Entscheidung gegen automatisierte GUI-Tests

Auf automatisierte GUI-Tests wurde bewusst verzichtet, da der Aufwand den Nutzen überstiegen hätte. Tkinter bietet nur begrenzte Möglichkeiten für UI-Testautomatisierung, und der Lernfokus lag klar auf der Spiellogik.

---

## 7. Testdesign

### 7.1 Ableitung aus Requirements

Testfälle wurden aus den zuvor abgestimmten Requirements abgeleitet. Typische Anforderungen waren:

- Der erste Klick darf keine Mine auslösen  
- Felder ohne Nachbarminen müssen angrenzende Felder automatisch öffnen  
- Ein Spiel muss korrekt als gewonnen oder verloren erkannt werden  

---

### 7.2 Nutzung von ChatGPT

Zur Unterstützung bei der Testfallfindung wurde ChatGPT eingesetzt. Die generierten Vorschläge dienten als Inspiration, mussten jedoch stets manuell geprüft und angepasst werden. Ohne diese Nachbearbeitung wären viele Testfälle zu allgemein geblieben.

---

## 8. Automatisierte Unit-Tests

### 8.1 Ziel der Unit-Tests

Die Unit-Tests sollten ausschließlich die Spiellogik absichern. GUI-Aspekte wurden bewusst nicht getestet.

---

### 8.2 Testframework pytest

Als Testframework kam pytest zum Einsatz. Die Tests wurden in `test_minesweeper.py` implementiert und deckten unter anderem folgende Funktionen ab:

- Minenplatzierung  
- Nachbarberechnung  
- First-Click-Safety  
- Flood-Fill-Logik  
- Gewinn- und Verlustbedingungen  

---

### 8.3 Umgang mit GUI-Abhängigkeiten

Da viele Methoden GUI-Elemente referenzieren, wurden DummyWidgets und DummyLabels verwendet. Diese ermöglichten das Testen der Logik trotz starker GUI-Kopplung.

---

## 9. Manuelle End-to-End-Tests

### 9.1 Motivation

Manuelle End-to-End-Tests waren unverzichtbar, um das Spiel aus Sicht eines echten Nutzers zu bewerten. Dabei wurden komplette Spielabläufe getestet.

---

### 9.2 Typischer Testpfad

Ein typischer End-to-End-Test bestand aus:

1. Start des Spiels  
2. Erster Klick  
3. Beobachtung der Flood-Fill-Logik  
4. Setzen von Flaggen  
5. Öffnen weiterer Felder  
6. Spielende durch Gewinn oder Verlust  

---

### 9.3 Erkenntnisse

Viele Auffälligkeiten, insbesondere in der Benutzerführung und im Zustandsmanagement, wurden erst durch manuelles Spielen sichtbar.

---

## 10. Gefundene Bugs

Während des Projekts wurden mehrere kleinere Bugs identifiziert, unter anderem:

- fehlerhafte Flood-Fill-Randfälle  
- inkonsistente First-Click-Safety  
- falsche Nachbarzählung in Sonderfällen  
- doppelte Definition von Farbwerten  
- unvollständige Prüfung des Game-Over-Zustands  

Diese Bugs waren lehrreich und führten zu gezielten Verbesserungen.

---

## 11. Code Reviews

Code Reviews ergänzten die Tests sinnvoll. Sie halfen, strukturelle Schwächen, Code-Duplikate und Magic Numbers zu identifizieren. Besonders die doppelte Definition von Farbwerten wurde durch Reviews erkannt.

---

## 12. Refactoring

Refactoring war meist eine direkte Folge von Tests oder Code Reviews. Ziel war es, den Code lesbarer, wartbarer und testbarer zu machen, ohne das Verhalten zu verändern.

---

## 13. Grenzen der Tests

Nicht getestet wurden:

- grafisches Layout  
- Farben und Design  
- Performance  
- Usability im Detail  

Diese Einschränkungen wurden bewusst akzeptiert.

---

## 14. Lessons Learned

Tests verbesserten nicht nur die Codequalität, sondern auch das Verständnis der Spiellogik. Besonders komplexe Logiken wurden erst durch Tests vollständig verstanden.

---

## 15. Persönliche Reflexion

Die Rolle des Testers erwies sich als anspruchsvoll, aber sehr lehrreich. Testen war nicht nur eine technische Aufgabe, sondern auch ein analytischer und kommunikativer Prozess.

---

## 16. Verbesserungsvorschläge

Für zukünftige Projekte wird empfohlen:

- Logik und GUI frühzeitig zu trennen  
- Tests früher zu beginnen  
- Testergebnisse kontinuierlich zu dokumentieren  

---

## 17. Qualitätsbewertung

Die gewählte Teststrategie war für den Projektumfang angemessen. Die wichtigsten Spielfunktionen konnten zuverlässig abgesichert werden.

---

## 18. Risikoanalyse

Risiken bestanden vor allem in:

- starker GUI-Kopplung  
- begrenzter Testabdeckung  
- fehlender Performanceanalyse  

Diese Risiken wurden bewusst in Kauf genommen.

---

## 19. Zusammenfassung

Die Kombination aus Tests, Code Reviews und Refactoring führte zu einem stabilen und nachvollziehbaren Ergebnis.

---

## 20. Fazit

Das Projekt zeigte, dass Testen ein zentraler Bestandteil moderner Softwareentwicklung ist. Tests halfen nicht nur beim Finden von Fehlern, sondern auch beim Verständnis, der Strukturierung und der Qualitätsverbesserung des Codes.

Dieses Test-Manual dokumentiert nicht nur, was getestet wurde, sondern vor allem warum und mit welchen Erkenntnissen.
