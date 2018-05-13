import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    ###Klasse Raumschiff.###


    def __init__(self, ai_settings, screen):
        ###Initialize the ship and set its starting position.###
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Lädt das Bild des Schiffs und ruft dessen umgebendes Rechteck ab.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Platziert jedes neue Schiff mittig am unteren Bildschirmrand.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Speichert einen Fließkommawert für den Schiffsmittelpunkt.
        self.center = float(self.rect.centerx)

        # Bewegungsflags
        self.moving_right = False
        self.moving_left = False


    def update(self):
        ###Update the ships position based on the movement flags.###
        # Aktualisiert den Wert für den Mittelpunkt des Schiffs, nicht des Rechtecks.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Aktualisiert das rect-Objekt auf der Grundlage von self.center.
        self.rect.centerx = self.center


    def blitme(self):
        ###Draw the ship at its current location.###
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        ###Center the Ship on the Screen.###
        self.center = self.screen_rect.centerx

