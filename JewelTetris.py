import sys
import pygame

from JewelSettings import Settings
import JewelGameFunctions as jgf
from pygame.sprite import Group
from random import randint

def run_game():

	pygame.init()
	settings = Settings()
	screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
	screenRe = screen.get_rect()
	screen.fill((150, 150, 150))
	# print('bottom ' + str(screenRe.bottom))
	# print('top ' + str(screenRe.top))
	# print('left ' + str(screenRe.left))
	# print('right ' + str(screenRe.right))

	currentJewelsGroup = Group()

	while True:

		if settings.isFirstIteration:

			settings.isFirstIteration = False
			jgf.funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen)

		else:
			if jgf.checkIfTheJewelGroupReachedBottom(settings):
				jgf.groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup)
				jgf.resetAllTheSettings(settings)
				jgf.funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen)
			else:
				jgf.funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen)


run_game()




