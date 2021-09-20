### Spiel Pong erweitert (programmiert mit Python und Bibliotheken pygame und spiel)
### Vorlage fuer B-Aufgabe INF-L
### Stand Mai 2020, Copyright Wilhelm Buechner Hochschule

from wbh.spiel import *


## Klasse ColoredBall
## die Klasse erbt von Ball,
## initalisiert den Ball ueber den Konstruktor der Superklasse
## und setzt das Attribut farbe 
class ColoredBall(Ball):
    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.farbe = farbe


## Klasse TastaturSchlaeger
## die Klasse erbt von Schlaeger und fuegt die Methode movekey hinzu
class TastaturSchlaeger(Schlaeger):
    # Funktion zum Bewegen des Schlaegers mit Tastatur
    def movekey(self, pos):
        self.rect.y = self.rect.y + (pos * self.geschwindigkeit)


## hier ist der Rumpf der Klasse SpielErweiterung
class SpielErweitert(Spiel):
    '''Erweiterung des Spiels um Tastatureingaben und
       Tastatursteuerung des Schlaegers'''

    # Erweiterung des Spiels um Tastatureingaben und
    # Tastatursteuerung des Schlaegers
    def _behandle(self, event):
        # Ueberpruefe ob Schliessen-Symbol im Fenster gedrueckt wurde
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return
        # Ueberpruefe ob Tastatur verwendet wurde
        elif event.type == pygame.KEYDOWN:
            self._behandle_tastatur(event)
        return event

    # Methode zur Tastensteuerung
    def _behandle_tastatur(self, event):
        if event.key == pygame.K_UP:
            self._spieler.movekey(-10)
            return
        elif event.key == pygame.K_DOWN:
            self._spieler.movekey(10)
            return


# das Hauptprogramm, Einstiegspunkt fuer den Aufruf vom Betriebssystem
def main():
    ## Objekt ball von Klasse ColoredBall
    ## mit Parametern (x, y, breite, hoehe, geschwindigkeit, farbe) initialisiert
    ball = Ball(
        x=config.fensterBreite // 2 - 20,
        y=config.fensterHoehe // 2 - 20,
        breite=config.linienDicke,
        hoehe=config.linienDicke,
        geschwindigkeit=10,
    )

    ## Objekt spielerSchlaeger von Klasse TastaturSchlaeger angelegt
    ## mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisiert
    ## analog zur vorherigen Version
    spielerSchlaeger = TastaturSchlaeger(
        x=config.linker_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=5
    )

    ## die folgenden Objekte sind vorgegeben (id. zur anderen Vorlage)
    spielfeld = Spielfeld()

    computerSchlaeger = AutoSchlaeger(
        x=config.rechter_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=10,
        ball=ball
    )

    punkteAnzeige = PunkteAnzeige(
        punkte=0,
        x=config.fensterBreite - 250,
        y=45,
        schrift=config.schriftPoints()
    )

    ## Aufruf der Methode run der Klasse SpielErweitert
    SpielErweitert(spielfeld, spielerSchlaeger, computerSchlaeger, ball, punkteAnzeige).run()


# Aufruf der Main-Funktion
if __name__ == '__main__':
    main()
