# SNOMAST 2.2

Dieses Python-Projekt stellt den ausführbaren Prototyp von S.Kunz & C.Zgraggen 
im Rahmen der BSc Thesis '22 über "NLP zur Unterstützung von SNOMED-CT Codierung" dar.

Das Projekt wurde als pipenv Projekt entworfen und somit können die Abhängigkeiten virtuell geladen werden.
Dieses README bietet die Einführung, wie der Prototyp zum laufen gebracht werden kann.

Die Nutzung des Projektes bedingt, dass auf dem Rechner der anzuwendenden Person ein Python
Interpreter installiert ist und ein Packageverwaltungssystem (pip)zur Verfügung steht.

Das Projekt wurde unter der Python Version 3.8 entwickelt. Unter dieser Version wurde auch die
Lauffähigkeit getestet. Unter Python Versionen > 3.8 sollte der Code jedoch auch funktionieren. Hierfür
muss jedoch im Pipfile die Version unter dem Punkt [requires] angepasst werden.

Für die Übersetzung von Texten in die englische Sprache wird ein Authentifikations-Schlüssel von DeepL
benötigt. Dieser ist im Python-Script "business_logic_control" unter DEEPL_AUTH_KEY auf Zeile 10
hinterlegt.
Aktuell ist nur ein freier Schlüssel hinterlegt, bei welchem die Kapazitätsgrenze für Übersetzungen
zur Neige gehen könnte oder nicht mehr aktuell ist. Die maximale Übersetzungskapazität ist bei einem
freien Schlüssel 500’000 Zeichen im Monat. Daher ist es sinnvoll, diesen mit einem eigenen Schlüssel
zu ersetzen. Dies kann problemlos in einem Texteditor gemacht werden. Er muss in Anführungszeichen
eingeschlossen werden.

Um die virtuelle Packageverwaltung zu nutzen, muss zuerst pipenv global installiert werden. Unter pip
ist dies mittels "pip install pipenv" zu bewerkstelligen und muss nur einmalig ausgeführt werden.

Um das GUI zu starten, muss mittels Kommandozeile in den Projektordner navigiert werden.
Im Projektordner kann mit dem Befehl "pipenv shell" die virtuelle Packageverwaltung aufgerufen
werden.

In der virtuellen Umgebung werden mittels "pipenv install" alle benötigten Packages und
Abhängigkeiten installiert.

Um das GUI zu starten, muss in der virtuellen Umgebung "python snomast.py" ausgeführt werden.
Nun startet sich das GUI auf und steht für die Verwendung zur Verfügung.

Nach der Benutzung, wenn das Fenster des GUI geschlossen wurde, muss mittels "exit" in der
Kommandozeile die virtuelle Umgebung geschlossen werden
