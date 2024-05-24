# Benfords Gesetz

Benfords Gesetz ist ein Gesetz zur relativen Häufigkeit von Ziffern (0-9) als Anfangsziffer. Es kann benutzt werden um Betrug in Datensetzen zu finden. Wenn zum Beispiel ein großer Datensatz von Finanzdaten nicht diesem Gesetz folgt, kann Betrug vorliegen, man sollte sich den Datensatz aber immer nochmal selber anschauen und den Grund für die Abweichung herausfinden. [https://de.wikipedia.org/wiki/Benfordsches_Gesetz](Link zu Wikipedia)

Dies ist ein Pytohnscript zur Visualisierung von Benfords Gesetz. 

Die benötigtesn Bibliotheken zu diesem Projekt sind in dem requirements.txt file.

Die Datensätze müssen in einem Ordner `data` liegen, der auf dem selben Level wie das Script sein muss. Die Datensätze müssen eine .csv datei sein.

# Parameter 

Beim Ausführen gibt es Parameter, die das Script benötigt (Die Parameter werden über die konsole übergeben):

| Kürzel | Beschreibung
| - | - |
|-d | Datensatzname (z.B. Fibonacci) (Muss immer angegeben werden, die anderen sind optional) |
|-s | Startzeile (wo das Programm anfangen soll zu zählen) |
|-e | Endzeile (wo das Programm aufhören soll zu zählen)  |
|-c | Spalte (aus welcher Spalte die Daten kommen sollen) (default = 1) |
|-l | um sich die letzte Ziffer anzuschauen |
|-p | um die Daten in einem Graph zeichnen zu lassen |
|-z | n-te Ziffer |
|-a | Wie viele Zahlen angeschaut werden sollen (z.B die ersten beiden Zahlen) |
|-t | Um Werte zusammenzufassen (z.B. 2, dann fasst das Programm 1 und 2 zu einem Wert zusammen und 3 und 4) |
|-i | Um Die Benfords-Gesetz Kurve auszublenden |

Beispiele:
py benfords_law.py -d fibonacci -s 0 -c 0 -p
py benfords_law.py -d fibonacci -s 0 -c 0 -p -a 2

# Funktionen

## check_data

Prüft ob die angegebenen Daten richtig sind

## get_probability

Berechnet die relative Häufigkeit nach Benfords-Gesetz für die angegeben Konfiguration.
! Letzte Ziffern sollten einfach nur Zufällig verteilt sein. !

## calculate

Zählt die Ziffern an der angegebenen Stelle in dem Datensatz und berechnet und gibt die relative Häufigkeit der Ziffern aus.

# Beitragen

Beiträge zu diesem Projekt sind gerne wilkommen.