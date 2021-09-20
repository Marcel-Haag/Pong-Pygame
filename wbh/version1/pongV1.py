### Spiel Pong programmiert mit Python und Bibliotheken pygame und spiel
### Vorlage fuer B-Aufgabe INF-L
### Stand Mai 2020, Copyright Wilhelm Buechner Hochschule


# das Hauptprogramm, Einstiegspunkt fuer den Aufruf vom Betriebssystem
from wbh.spiel import *


def main():
    ## Objekt ball von Klasse Ball
    ## mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisiert
    ball = Ball(
        x=config.fensterBreite // 2 - 20,
        y=config.fensterHoehe // 2 - 20,
        breite=config.linienDicke,
        hoehe=config.linienDicke,
        geschwindigkeit=10
    )

    ## Objekt spielerSchlaeger von Klasse Schlaeger
    ## mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisiert
    spielerSchlaeger = Schlaeger(
        x=config.linker_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=5
    )

    ## Objekt spielfeld von Klasse Spielfeld (keine Parameter)
    spielfeld = Spielfeld()

    ## Objekt computerSchlaeger von Klasse AutoSchlaeger ist schon angelegt
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisiert
    ## Objekt ball wird uebergeben, damit computerSchlaeger dem Ball folgen kann
    computerSchlaeger = AutoSchlaeger(
        x=config.rechter_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=10,
        ball=ball
    )

    ## Objekt punkteAnzeige von Klasse PunkteAnzeige ist schon angelegt
    ## und mit Parametern (punkte, x, y, schrift) initialisiert
    punkteAnzeige = PunkteAnzeige(
        punkte=0,
        x=config.fensterBreite - 250,
        y=45,
        schrift=config.schriftPoints()
    )

    ## Aufruf der Methode run der Klasse Spiel ist ebenfalls vorgegeben
    Spiel(spielfeld, spielerSchlaeger, computerSchlaeger, ball, punkteAnzeige).run()


# Aufruf der Main-Funktion
if __name__ == '__main__':
    main()
