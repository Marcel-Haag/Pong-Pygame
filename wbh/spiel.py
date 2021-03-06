### Bibliothek spiel.py
### Stand Mai 2020, Copyright Wilhelm Buechner Hochschule

### Eine Änderung an dieser Datei ist nicht erlaubt!!!

import pygame
import sys


class Einstellungen():
    fps = 60  # Frames pro Sekunde

    # Dimensionen
    fensterBreite = 1600
    fensterHoehe = 1040
    linienDicke = 18
    abstand = 2.85 * linienDicke
    schlaegerBreite = 15
    schlaegerHoehe = 120
    schriftGroesse = 34
    schriftGroessePoints = 20
    ballRadius = 10  # nur fuer runden Ball notwendig

    def __init__(self):
        # Notwendige Initialisierung fuer pygame
        pygame.init()
        pygame.display.set_caption('Pong')
        pygame.mouse.set_visible(0)  # setze Mauszeiger unsichtbar

    def fenster_mitte(self):
        return self.fensterHoehe // 2

    def schlaeger_mitte(self):
        return self.fenster_mitte() - self.schlaegerHoehe // 2

    def linker_rand(self):
        return self.abstand

    def rechter_rand(self):
        return self.fensterBreite - self.schlaegerBreite - self.abstand

    def schrift(self):
        return pygame.font.SysFont('arial', self.schriftGroesse, bold=True)

    def schriftPoints(self):
        return pygame.font.SysFont('arial', self.schriftGroessePoints, bold=True)


'''Idealer Weise waere dies kein globales Objekt'''
config = Einstellungen()


class Form(pygame.sprite.Sprite):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.geschwindigkeit = geschwindigkeit
        self.farbe = farbe


class Rectangle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def draw(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, self.farbe, self.rect)


class Circle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.radius = config.ballRadius

    def draw(self, fensterFlaeche):
        pygame.draw.circle(fensterFlaeche, self.farbe,
                           (self.rect.x, self.rect.y), self.radius)


class Willkommen():
    # Willkommensbildschirm beim Programmstart
    def __init__(self, fensterFlaeche):
        popupFenster = pygame.Rect((config.linker_rand() + 80, config.linker_rand() + 80),
                                   (config.fensterBreite * 2 // 2.35, config.fensterHoehe * 1.85 // 2.35))
        fensterFlaeche.fill(pygame.Color('white'), popupFenster)
        textZeile1 = 'Willkommen zu Pong'
        textZeile2 = 'Spielstart mit beliebiger Taste'
        textWidth1, textHeight1 = config.schrift().size(textZeile1)
        textWidth2, textHeight2 = config.schrift().size(textZeile2)
        zeile1 = config.schrift().render(textZeile1, False, pygame.Color('black'))
        xZeile1 = (config.fensterBreite - textWidth1) // 2
        yZeile1 = (config.fensterHoehe * 2 // 3 - textHeight1) // 2
        zeile2 = config.schrift().render(textZeile2, False, pygame.Color('black'))
        xZeile2 = (config.fensterBreite - textWidth2) // 2
        yZeile2 = (config.fensterHoehe - config.abstand - textHeight2) // 2
        fensterFlaeche.blit(zeile1, (xZeile1, yZeile1))
        fensterFlaeche.blit(zeile2, (xZeile2, yZeile2))


class Spiel():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, spielfeld, spieler, computer, ball, punkteAnzeige):
        self.punkte = 0
        self._fpsTimer = pygame.time.Clock()

        self._spielfeld = spielfeld
        self._fensterFlaeche = pygame.display.set_mode(
            (config.fensterBreite, config.fensterHoehe))
        self._spieler = spieler
        self._computer = computer
        self._ball = ball
        self._allSchlaeger = [self._spieler, self._computer]  # Liste
        self._punkteAnzeige = punkteAnzeige

    def run(self):
        '''
        Spielschleife - Game Loop Pattern, siehe auch:
        http://gameprogrammingpatterns.com/game-loop.html
        '''
        running = False
        # Willkommensbildschirm anzeigen, weiter mit Taste
        while running == False:
            Willkommen(self._fensterFlaeche)
            pygame.display.update()
            # Ueberpruefe ob Taste gedrueckt wurde
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = True
        # Spielschleife
        while running:
            self._ereignisse_behandeln()
            self._update()
            self._zeichnen()
            pygame.display.update()
            self._fpsTimer.tick(config.fps)

    def _ereignisse_behandeln(self):
        # Ereignis abfragen
        for ereignis in pygame.event.get():
            self._behandle(ereignis)

    def _behandle(self, event):
        # Ueberpruefe ob Schliessen-Symbol im Fenster gedrueckt wurde
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return
        # Ueberpruefe ob Maus bewegt wurde
        elif event.type == pygame.MOUSEMOTION:
            self._spieler.move(event.pos)
            return
        return event

    def _update(self):
        self._bewegen()
        self._aufprall_berechnen()

    def _bewegen(self):
        self._ball.move()
        self._computer.move(self._ball)

    def _aufprall_berechnen(self):
        if self._ball.hit_schlaeger(self._computer):
            self._ball.bounce('x')

        elif self._ball.hit_schlaeger(self._spieler):
            self._ball.bounce('x')
            self.punkte += 1

        elif self._ball.trefferComputer():
            self.punkte += 5

        elif self._ball.trefferSpieler():
            self.punkte = 0

    def _zeichnen(self):
        self._spielfeld.draw(self._fensterFlaeche)
        self._ball.draw(self._fensterFlaeche)
        for schlaeger in self._allSchlaeger:
            schlaeger.draw(self._fensterFlaeche)
        self._punkteAnzeige.draw(self.punkte, self._fensterFlaeche)


class Spielfeld():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, farbe=pygame.Color('black')):
        self.farbe = farbe

    def draw(self, fensterFlaeche):
        fensterFlaeche.fill(self.farbe)
        self._umrandung(fensterFlaeche)
        self._mittellinie(fensterFlaeche)

    def _umrandung(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, pygame.Color('white'),
                         ((0, 0), (config.fensterBreite, config.fensterHoehe)),
                         config.linienDicke * 2)

    def _mittellinie(self, fensterFlaeche):
        pygame.draw.line(fensterFlaeche, pygame.Color('white'),
                         (config.fensterBreite // 2, 0),
                         (config.fensterBreite // 2, config.fensterHoehe),
                         config.linienDicke // 4)


class Ball(Rectangle):  # Alternativer Parameter: Circle
    # Pfeiltasten
    LEFT = -1
    RIGHT = 1
    UP = -1
    DOWN = 1

    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.richtungX = self.LEFT
        self.richtungY = self.UP

    # Funktion zum Bewegen des Balls, neue Position setzen
    def move(self):
        self.rect.x += (self.richtungX * self.geschwindigkeit)
        self.rect.y += (self.richtungY * self.geschwindigkeit)

        # Pruefe Kollision mit Wand
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('y')
        if self.hit_wall():
            self.bounce('x')

    # Richtungsaenderung fuer Ball
    def bounce(self, axis):
        if axis == 'x':
            self.richtungX *= -1
        elif axis == 'y':
            self.richtungY *= -1

    # Treffen von Ball auf Schlaeger
    def hit_schlaeger(self, schlaeger):
        return pygame.sprite.collide_rect(self, schlaeger)

    # Treffen von Ball auf Wand links oder rechts
    def hit_wall(self):
        return (
                (self.richtungX == -1
                 and self.rect.left <= self.breite) or
                (self.richtungX == 1
                 and self.rect.right >= config.fensterBreite - self.breite)
        )

    # Treffen von Ball auf Decke
    def hit_ceiling(self):
        return self.richtungY == -1 and self.rect.top <= self.breite

    # Treffen von Ball auf Boden
    def hit_floor(self):
        return (self.richtungY == 1
                and self.rect.bottom >= config.fensterHoehe - self.breite)

    def trefferSpieler(self):
        return self.rect.left <= self.breite

    def trefferComputer(self):
        return self.rect.right >= config.fensterBreite - self.breite


class Schlaeger(Rectangle):
    # Funktion zum Zeichnen des Schlaegers
    def draw(self, fensterFlaeche):
        # Stoppt Schlaeger am unteren Spielfeldrand
        if self.rect.bottom > config.fensterHoehe - config.linienDicke:
            self.rect.bottom = config.fensterHoehe - config.linienDicke
        # Stoppt Schlaeger am oberen Spielfeldrand
        elif self.rect.top < config.linienDicke:
            self.rect.top = config.linienDicke + 1  # randkorrektur

        super().draw(fensterFlaeche)

    # Funktion zum Bewegen des Schlaegers mit Maus
    def move(self, pos):
        self.rect.y = pos[1]


class AutoSchlaeger(Schlaeger):
    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, ball, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self._ball = ball

    # Automatische Bewegung, richtet sich nach dem Ball
    def move(self, pos):
        # Wenn Ball sich vom Schlaeger wegbewegt, zentriere ihn
        if self._ball.richtungX == -1:
            self._zentrieren()
        # Wenn Ball sich auf Schlaeger zubewegt, beoachte seine Bewegung
        elif self._ball.richtungX == 1:
            self._beobachten()

    def _beobachten(self):
        if self.rect.centery < self._ball.rect.centery:
            self.rect.y += self.geschwindigkeit
        else:
            self.rect.y -= self.geschwindigkeit

    def _zentrieren(self):
        if self.rect.centery < config.fenster_mitte():
            self.rect.y += self.geschwindigkeit
        elif self.rect.centery > config.fenster_mitte():
            self.rect.y -= self.geschwindigkeit


class PunkteAnzeige():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, punkte, x, y, schrift, farbe=pygame.Color('white')):
        self.punkte = punkte
        self.x = x
        self.y = y
        self.schrift = schrift
        self.farbe = farbe

    # Schreibe aktuellen Punktestand an den Bildschirm
    def draw(self, punkte, fensterFlaeche):
        self.punkte = punkte
        result_surf = self.schrift.render('Punkte: %s' % (self.punkte), True, self.farbe)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        fensterFlaeche.blit(result_surf, rect)
