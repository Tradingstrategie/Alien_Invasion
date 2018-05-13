import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialisiert Pygame, das Einstellungs- und das Bildschirm-Objekt.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Erstellt die Play-Schaltfläche.
    play_button = Button(ai_settings, screen, "Play")

    # Erstellt eine Instanz zur Speicherung von Spielstatistiken und eine An zeigetafel zu erstellen.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Erstellt ein Schiff.
    ship = Ship(ai_settings, screen)

    # Erstellt eine Gruppe zur Speicherung der Geschosse.
    bullets = Group()

    # Erstellt die Aliens.
    aliens = Group()

    # Erstellt die Invasionsflotte.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Startet die Hauptschleife des Spiels.
    while True:
         # Lauscht auf Tastatur- und Mausereignisse.
         gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

         if stats.game_active:
             # Schiffsupdate
             ship.update()
             # Geschossupdate
             gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
             # Aliensupdate
             gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
         # Bildschirmupdate
         gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()

