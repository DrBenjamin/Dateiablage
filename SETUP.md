# Setup

Anleitung zum Setup der Entwicklungsumgebung Mini-Projekt "Dateiablage".

## Unternehmensportal besuchen

* Microsoft Visual Studio Code installieren
* Git installieren

## Minianaconda installieren

* Miniconda unter diesem Link [Link](https://www.anaconda.com/download/success#miniconda) installieren
* Setup Einstellung: Next -> I Agree -> "Just Me" muss angeklickt sein -> Next

  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/78733ca3c744ff51aed75c3398c21696936c1972/Images/1.Miniconda_setup.png?raw=true)
* Install ->  Next -> Finish

## Hinweis!: Das VPN macht Probleme bei der Verbindung mit Github
* Zscaler öffnen: Oben rechts : Log Out klicke

![Image](https://github.com/DrBenjamin/Dateiablage/blob/53e19c76fcb661d57c289d234f70ebd361d9699d/Images/2.Zscaler.png?raw=true)

## Visual Code öffnen

* Get Started schließen
* Clone Git Respository wählen
* Oben diesen Link einfügen: [Link](https://github.com/DrBenjamin/Dateiablage?raw=true?raw=true)
* ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/3.Visual_Code.png?raw=true)
* Ordner auswählen: CGM Onedrive -> Doukumente -> Select Respoitory Location klicken
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/4.Ordner%20ausw%C3%A4hlen.png?raw=true)
* open:
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/5.Open_Respository.png?raw=true)
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/6.Accept.png?raw=true)
* Doppelklick: 3 Dateien
* ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/7.Datei_Doppelklick.png?raw=true)
* Unten rechts: auf installieren klicken
* ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/8.Python_Erweiterung.png?raw=true)

## Browser öffnen

* Dieser Link: [GitHub](https://github.com) oder [Dateiablage](https://github.com/DrBenjamin/Dateiablage?raw=true) eingeben
* GitHub Account erstellen, falls noch nicht vorhanden.
* Die angemeldete E-Mail Adresse für diesen Account an Benjamin schicken
* Man bekommt dann eine Mail: 1. View Invitation -> Accept invitation

## Nach der Bestätigung des Links
   ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/9.Github_Home.png?raw=true)
   ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/10.Github_Dateiablage.png?raw=true)
   ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/11.Watch_starred.png?raw=true)

## Visual code öffnen

* Auf diese Weise kann man "Terminal" öffnen
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/12.terminal_offnen.png?raw=true)
* oben rechts Erwriterungen-Symbol klicken: Python eingeben -> Extension Pack installieren
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/13.Python_Erweiterung.png?raw=true)
* Conda Entwicklungsumgebung aktivieren: Oben recht auf Python-Symbol klicken -> conda eingeben -> base -> pfeil klicken
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/14.png?raw=true)
* unten links Einstellung-symbol(Zehnrad) klicken -> Einstellungen
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/15.Einstellung.png?raw=true)
* Im Feld "Einstellung-suche" das Wort "Conda" schreiben
* Conda Path einstellen
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/16.png?raw=true)
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/17.png?raw=true)
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/18.png?raw=true)
* Im Terminal eingeben:
```bash
 conda env create --file=environment.yml
 ```
* Zum Bestätigen:
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/19.Best%C3%A4tigen.png?raw=true)
* Visual code schließen und wieder öffnen
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/20.png?raw=true)
* Pfeli klicken
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/21.png?raw=true)
* Im Terminal eingeben:
```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"
```
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/23.png?raw=true)
* Bei einer Änderung des Codes oder zum Beispiel in README.md Datei -> Speichern -> Commit -> Push
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/24.png?raw=true)
* Im Terminal eingeben: 
```bash
python -m pip install -r .\requirements.txt
```
* Dann Enter-Taste drücken
  ![Image](https://github.com/DrBenjamin/Dateiablage/blob/f8ae2f8215aebd8e1638e083d3a2d11eb6cffb04/Images/22.png?raw=true)
* Im Terminal eingeben: 
```bash
python Dateiablage.py
```