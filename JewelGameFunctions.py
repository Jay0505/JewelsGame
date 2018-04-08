import sys
import pygame

from pygame.sprite import Group
from random import randint
from rectangle import Rectangle


################################# Settings #################################################
'''
-- Whenever a jewelGroup reached bottom, we have to create a new jewelGroup without disturbing the earlier jewelGroup which
reached the bottom of the screen.

-- So, before creating a new jewelGroup, we reset the important settings which are responsible for the behaviour and creation
of the jewels.
'''
def resetAllTheSettings(settings):
	# Jewel settings
	settings.jewels.empty()
	settings.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
	settings.jewelType = 1
	settings.jewelsLimit = 4
	settings.jewelDirection = 1
	settings.jewelMovingRight = False
	settings.jewelMovingLeft = False
	settings.anyJewelReachedEdge = False
	settings.anyJewelReachedBottom = False
	settings.numberOfJewels = 0
	del settings.listOfJewels[:]
	settings.count = 0



######################################## KEY EVENTS ###########################################

def checkEvents(settings, screen, jewels, currentJewelsGroup):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			keyDownEvents(settings, screen, event, jewels, currentJewelsGroup)

		elif event.type == pygame.KEYUP:
			keyUpEvents(settings, screen, event, jewels)

########
'''
-- If the user presses the right arrow key down, then the jewels should move right, in other words the x-coordinate
should increase. Therefore, we check for the settings.jewelDirection variable for whether it is positive or negative.
If it is negative and the key pressed is right arrow, we change the direction value to a positive value.

-- If the user presses the left arrow key down, then the jewels should move left, in other words the x-coordinate
should decrease. Therefore, we check for the settings.jewelDirection variable for whether it is positive or negative.
If it is positive and the key pressed is left arrow, we change the direction value to a negative value.

-- Also, we change the jewelMovingRight to True if the right arrow key pressed likewise we set jewelMovingLeft to True
if the left arrow key is pressed.

'''
def keyDownEvents(settings, screen, event, jewels, currentJewelsGroup):
	if event.key == pygame.K_RIGHT:
		settings.jewelMovingRight = True
		#settings.jewelMovingLeft = False
		if settings.jewelDirection == -1:
			settings.jewelDirection = 1 

		determineRightOrLeftForEachJewel(settings)

	elif event.key == pygame.K_LEFT:
		settings.jewelMovingLeft = True
		#settings.jewelMovingRight = False
		if settings.jewelDirection == 1:
			settings.jewelDirection = -1

		determineRightOrLeftForEachJewel(settings)

	elif event.key == pygame.K_UP:
		up = 1
		changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, up)


	elif event.key == pygame.K_DOWN:
		down = 0
		changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, down)


	



#########
'''
-- If the left arrow key is released, then we set the jewelMovingLeft to false likewise if the right arrow key is 
just released, we set the jewelMovingRight to false.
'''

def keyUpEvents(settings, screen, event, jewels):
	if event.key == pygame.K_LEFT:
		settings.jewelMovingLeft = False

	elif event.key == pygame.K_RIGHT:
		settings.jewelMovingRight = False





####################### JEWEL FUNCTIONS ########################################################


def determineTheProbableXCoordinatesForTheNewlyFormedJewels(settings):
	numberOfSegments = determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings)
	AcceptableXCoordinates = []
	for number in range(numberOfSegments):
		AcceptableXCoordinates.append((number * settings.jewelWidth))

	return AcceptableXCoordinates


def determineTheXCoordinateOfTheNewlyFormedJewel(settings):
	AcceptableXCoordinates = determineTheProbableXCoordinatesForTheNewlyFormedJewels(settings)
	numberOfSegments = determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings)
	indexOfTheXCoordinate = randint(0, numberOfSegments - 1)
	xCoordinate = AcceptableXCoordinates[indexOfTheXCoordinate]

	return xCoordinate


############################################
def determineJewelType(settings):
	settings.jewelType = randint(1, settings.jewelType)

	
############################################
def determineVerticallyOrHorizontallyAlignedJewels(settings):
	settings.jewelVerticalOrHorizontal = randint(0, settings.jewelVerticalOrHorizontal)
	

############################################
def determineJewelTypeAlignmentAndThenCreateJewelGroup(settings, screen):

	determineJewelType(settings)
	determineVerticallyOrHorizontallyAlignedJewels(settings)
	createJewelGroup(settings, screen)

############################################
def funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen):
	jewelType = settings.jewelType
	jewelVerticalOrHorizontal = settings.jewelVerticalOrHorizontal
	jewels = settings.jewels
	checkEvents(settings, screen, jewels, currentJewelsGroup) # Checks for any key press or release events
	forwardJewels(settings, jewels, jewelType, currentJewelsGroup) # move the jewels in the downward direction
	moveJewels(settings, screen, jewels, currentJewelsGroup) # move the jewels either right or left based upon the key pressed
	updateScreen(settings, screen, jewelType, jewels, currentJewelsGroup) # updates the screen with the latest positions of the jewels

############################################
def funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen):
	determineJewelTypeAlignmentAndThenCreateJewelGroup(settings, screen)
	funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen)


############################################
def createJewelGroup(settings, screen):
	jewelType = settings.jewelType
	jewelVerticalOrHorizontal = settings.jewelVerticalOrHorizontal
	jewels = settings.jewels
	if jewelVerticalOrHorizontal == 1:
		createHorizontallyAlignedJewels(settings, screen, jewelType, jewels)
	else:
		settings.jewelVerticalOrHorizontal = 0
		createVerticallyAlignedJewels(settings, screen, jewelType, jewels)


############################################
def createVerticallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	# yCoordinate = 0
	#xCoordinate = 250
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	# for number in range(numberOfJewels - 1, -1, -1):
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.y = 0
		else:
			# We add '+1' to create some space between jewels so as to create a boundary between jewels
			# rectangle.rect.y = (number * rectangle.height) + (2 * number) 
			rectangle.rect.y = (number * rectangle.height)

		rectangle.myNumber = number
		rectangle.rect.x = xCoordinate
		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)


############################################
def createHorizontallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	settings.numberOfJewels = numberOfJewels
	yCoordinate = 0
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.x = xCoordinate 
		else:
			# We add '(2 * number)' to create some space between jewels so as to create a boundary between jewels
			#rectangle.rect.x = xCoordinate + (number * rectangle.width) + (2 * number)
			rectangle.rect.x = xCoordinate + (number * rectangle.width)
		rectangle.myNumber = number
		rectangle.rect.y = yCoordinate
		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)



############################################
def fixTheNumberOfJewelsToBeFormed(settings):
	numberOfJewels = randint(1, settings.jewelsLimit)
	return numberOfJewels

############################################--------------------------------------------#####################################################

'''
-- This function is responsible for the downward movement of the jewel. Update is the method in the respective jewel class.
If we write jewels.update(), then the update method is applied on each and every jewel in the jewels group.
'''
def forwardJewels(settings, jewels, jewelType, currentJewelsGroup):
	#changeTheSettingsOfTheJewelsIfCollided(settings, currentJewelsGroup)
	updateJewel(settings, currentJewelsGroup)

############################################
def updateJewel(settings, currentJewelsGroup):
	
	for jewel in settings.jewels.sprites():
		if jewel.moveDown and not jewel.reachedBottom:
			jewel.update()
			checkCollisionOfEachJewelWithCurrentJewelsGroup(jewel, settings, currentJewelsGroup)

'''
-- A collision between two entities is determined by comparing the rect attributes (xCoordinate and yCoordinate) of both the entities

-- In our case, two jewels are said to be collided if they both have same rect attributes. Now let us say, we have two jewels moving downwards
and the co-ordinates of those jewels are (100, 200), (100, 220) (height of each jewel is 20). Now, these two jewels are affixed to each other like
the jewels in our game which are affixed vertically when they are vertically aligned.

-- Let us suppose that, JewelA has co-ordinates (100, 200) and JewelB has co-ordinates (100, 220). let us say, we have a jewel which has already
reached bottom and stationed at the co-ordinates (100, 300) and lets call this jewel, JewelC

-- Now, we say, JewelB is collided with JewelC on when they both have same rect attributes. In other words, when the jewelA and JewelB are moving
downwards and when both JewelB and JewelC are perfectly interposed with each other. In this case, JewelB and JewelC - (100, 300) 
																											 JewelA - (100, 280)

-- But, in our game, when a jewel is collided with each other, the movement of the jewels should be stopped and ideally after a collision is detected,
the co-ordinates of the three jewels should be as following:
					JewelC - (100, 300)
					JewelB - (100, 280)
					JewelA - (100, 260) But, both JewelC and JewelB are interposed and JewelA is 20 steps (which is equal to height of the jewels) than
					it should be.

-- To rectify this error, the bottom of the moving Jewels is decremented by the speed factor (or height of the jewel, both are equal in our game). 
  			Before collision                        AfterCollision
  			JewelC - (100, 300)						JewelC - (100, 300)
													JewelB - (100, 300)
													JewelA - (100, 280)
			JewelB - (100, 220)
			JewelA - (100, 200)

		but after decrementing the bottom by the speed factor, the co-ordinates would be JewelC (100, 300), JewelB (100, 280) and JewelA (100, 260) 
		Thus creating the required effect (moving jewels immediately stopping when collided with any stationed jewel)
'''			

def checkCollisionOfEachJewelWithCurrentJewelsGroup(jewel, settings, currentJewelsGroup):
	collidedJewelsList = pygame.sprite.spritecollide(jewel, currentJewelsGroup, False)
	if len(collidedJewelsList) != 0:
		
		if settings.jewelVerticalOrHorizontal == 0:
			bottom = collidedJewelsList[0].rect.top
			changeTheSettingsOfTheJewelsCollidedWhenVerticallyAligned(settings, bottom)
		else:
			jewel.moveDown = False
			jewel.reachedBottom = True
			jewel.movingRight = False
			jewel.movingLeft = False
			jewel.rect.bottom = collidedJewelsList[0].rect.top
			jewel.blitme()
			currentJewelsGroup.add(jewel)
			settings.jewels.remove(jewel)



def auxillaryCollisionFunctionWhileMovingRightOrLeft(jewel, settings, currentJewelsGroup):
	collidedJewelsList = pygame.sprite.spritecollide(jewel, currentJewelsGroup, False)
	return collidedJewelsList
	#if len(collidedJewelsList) != 0:
		# if settings.jewelVerticalOrHorizontal == 0:
		# 	if settings.jewelDirection == 1:
		# 		jewel.movingRight = False
		# 		jewel.rect.x -= settings.jewelWidth
		# 		jewel.blitme()

		# 		# for jewel in settings.jewels.sprites():
		# 		# 	jewel.movingRight = False
		# 		# 	jewel.rect.x -= settings.jewelWidth
		# 		# 	jewel.blitme()

		# 	else:
		# 		jewel.movingLeft = False
		# 		jewel.rect.x += settings.jewelWidth
		# 		jewel.blitme()
		# else:
		# 	for jewel in settings.jewels.sprites():
		# 		if settings.jewelDirection == 1:
		# 			jewel.movingRight = False
		# 			jewel.rect.x -= settings.jewelWidth

		# 		else:
		# 			jewel.movingLeft = False
		# 			jewel.rect.x += settings.jewelWidth

		# 		#jewel.rect.x += (settings.jewelDirection * settings.jewelWidth)
		# 		jewel.blitme()

			# for jewel in settings.jewels.sprites():
			# 	jewel.movingLeft = False
			# 	jewel.rect.x += settings.jewelWidth
			# 	jewel.blitme()
	# if len(collidedJewelsList) != 0:
	# 	print(str(collidedJewelsList[0].rect.x) + "  X  " +  str(jewel.rect.x))
	# 	print(str(collidedJewelsList[0].rect.y) + "  Y  " +  str(jewel.rect.y))
	# 	print(str(collidedJewelsList[0].rect.top) + "  top  " +  str(jewel.rect.top))
	# 	print(str(collidedJewelsList[0].rect.bottom) + "  bottom  " +  str(jewel.rect.bottom))


def auxillaryFunctionVerticalCollidedWhileMovingLeftOrRight(jewel, settings):
	if settings.jewelDirection == 1:
		jewel.movingRight = False
		jewel.rect.x -= settings.jewelWidth
		#jewel.blitme()

		# for jewel in settings.jewels.sprites():
		# 	jewel.movingRight = False
		# 	jewel.rect.x -= settings.jewelWidth
		# 	jewel.blitme()

	else:
		jewel.movingLeft = False
		jewel.rect.x += settings.jewelWidth
	jewel.blitme()


def auxillaryFunctionHorizontalCollidedWhileMovingLeftOrRight(currentJewl, settings):
	# for jewel in settings.jewels.sprites():
	# 	#if jewel.rect.x == currentJewl.rect.x and jewel.rect.y == currentJewl.rect.y:
	# 	if settings.jewelDirection == 1:
	# 		jewel.movingRight = False
	# 		jewel.rect.x -= settings.jewelWidth

	# 	else:
	# 		jewel.movingLeft = False
	# 		jewel.rect.x += settings.jewelWidth
	# 	jewel.blitme()


	for jewel in settings.jewels.sprites():
		jewel.rect.x -= (settings.jewelDirection * settings.jewelWidth)
		if settings.jewelDirection == 1:
			jewel.movingRight = False
		else:
			jewel.movingLeft = False
		jewel.blitme()


		# else:
		# 	if settings.jewelDirection == 1:
		# 		jewel.movingRight = False
				

		# 	else:
		# 		jewel.movingLeft = False

		# if settings.jewelDirection == 1:
		# 	jewel.movingRight = False
		# 	jewel.rect.x -= settings.jewelWidth

		# else:
		# 	jewel.movingLeft = False
		# 	jewel.rect.x += settings.jewelWidth

		# jewel.blitme()
				

		#jewel.rect.x += (settings.jewelDirection * settings.jewelWidth)
		


def changeTheSettingsOfTheJewelsCollidedWhenVerticallyAligned(settings, bottom):
	settings.anyJewelReachedBottom = True
	for jewel in settings.jewels.sprites():
		jewel.moveDown = False
		jewel.reachedBottom = True
		jewel.movingRight = False
		jewel.movingLeft = False
		jewel.rect.bottom -= settings.jewelSpeedFactor
		jewel.blitme()

		

############################################--------------------------------------------#####################################################
'''
-- This function is used to change the positions of the jewels when UP arrow key is pressed.
-- 
'''
def changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, upOrDown):

	if upOrDown == 1:
		changeTheJewelPositionsWhenUpArrowKeyPressed(settings, screen, currentJewelsGroup)

	if upOrDown == 0:
		changeTheJewelPositionsWhenDownArrowKeyPressed(settings, screen, currentJewelsGroup)
	

############################################
'''
-- If the up arrow key pressed, then change the positions of the jewels in the clockwise direction. In other words, jewel at 
index 1 should be move to index 0, index 2 to index 1, index 3 to index 2 ......index 0 to index n - 1

-- 'n' being number of jewels in the list
'''

def changeTheJewelPositionsWhenUpArrowKeyPressed(settings, screen, currentJewelsGroup):
	numberOfJewels = len(settings.listOfJewels)
	jewels = settings.listOfJewels

	indexOneRectangleshape = jewels[0].shape
	colorOfTheJewelInRGB = jewels[0].jewelColor
	screenOfTheIndexOneJewel = jewels[0].screen
	for index in range(1, numberOfJewels):
		screen = jewels[index].screen
		shape = jewels[index].shape
		colorValueInRGB = jewels[index].jewelColor
		drawTheShapeAtTheNewCoordinates(screen, jewels[index - 1], shape, colorValueInRGB)

	drawTheShapeAtTheNewCoordinates(screenOfTheIndexOneJewel, jewels[numberOfJewels - 1], indexOneRectangleshape, colorOfTheJewelInRGB)
	updateScreen(settings, screen, 1, settings.jewels, currentJewelsGroup)



############################################
'''
-- If the up arrow key pressed, then change the positions of the jewels in the clockwise direction. In other words, jewel at 
index n should be move to index n - 1, index n - 1 to index n - 2, index n - 2 to index n - 3 ......index n  to index 0

-- 'n' being number of jewels in the list
'''

def changeTheJewelPositionsWhenDownArrowKeyPressed(settings, screen, currentJewelsGroup):
	numberOfJewels = len(settings.listOfJewels)
	jewels = settings.listOfJewels

	lastRectangleshape = jewels[numberOfJewels - 1].shape
	colorOfThelastJewel = jewels[numberOfJewels - 1].jewelColor
	screenOfTheLastJewel = jewels[numberOfJewels - 1].screen
	for index, jewel in reversed(list(enumerate(jewels))):
		if index != numberOfJewels - 1:
			screen = jewels[index].screen
			shape = jewels[index].shape
			colorValueInRGB = jewels[index].jewelColor
			drawTheShapeAtTheNewCoordinates(screen, jewels[index + 1], shape, colorValueInRGB)

	drawTheShapeAtTheNewCoordinates(screenOfTheLastJewel, jewels[0], lastRectangleshape, colorOfThelastJewel)
	updateScreen(settings, screen, 1, settings.jewels, currentJewelsGroup)


def drawTheShapeAtTheNewCoordinates(screen, jewel, shapeOfTheJewel, colorOfTheJewelInRGB):
	if shapeOfTheJewel == "rectangle":
		jewel.jewelColor = colorOfTheJewelInRGB
		jewel.shape = shapeOfTheJewel
	




############################################--------------------------------------------#####################################################

def moveJewels(settings, screen, jewels, currentJewelsGroup):
	didJewelGroupReachedBottom = checkIfTheJewelGroupReachedBottom(settings)
	if not didJewelGroupReachedBottom:

		

		screenRect = screen.get_rect()
		anyJewelAtTheEdge = anyJewelReachedEdge(settings, screen, jewels)

		isMovingRightOrLeft = settings.jewelMovingRight or settings.jewelMovingLeft

		for jewel in settings.jewels.sprites():
			if isMovingRightOrLeft and (not anyJewelAtTheEdge) and (jewel.movingRight or jewel.movingLeft):
				jewel.rect.x += (settings.jewelWidth * settings.jewelDirection)
				collidedJewelsList = auxillaryCollisionFunctionWhileMovingRightOrLeft(jewel, settings, currentJewelsGroup)
				if len(collidedJewelsList) != 0:
					# print(str(collidedJewelsList[0].rect.x) + "  X  " +  str(jewel.rect.x))
					# print(str(collidedJewelsList[0].rect.y) + "  Y  " +  str(jewel.rect.y))
					# print(str(collidedJewelsList[0].rect.top) + "  top  " +  str(jewel.rect.top))
					# print(str(collidedJewelsList[0].rect.bottom) + "  bottom  " +  str(jewel.rect.bottom))
					# print(str(collidedJewelsList[0].rect.right) + "  right  " +  str(jewel.rect.right))
					# print(str(collidedJewelsList[0].rect.left) + "  left  " +  str(jewel.rect.left))
					if settings.jewelVerticalOrHorizontal == 0:
						auxillaryFunctionVerticalCollidedWhileMovingLeftOrRight(jewel, settings)
					else:
						auxillaryFunctionHorizontalCollidedWhileMovingLeftOrRight(jewel, settings)
						break
						 
						





def determineRightOrLeftForEachJewel(settings):
	if settings.jewelDirection == 1:
		for jewel in settings.jewels.sprites():
			jewel.movingRight = True
			jewel.movingLeft = False
	else:
		for jewel in settings.jewels.sprites():
			jewel.movingLeft = True
			jewel.movingRight = False


def whenCollidedSetTheAppropriateRightOrLeftValuesForJewels(settings, collidedJewels):
	if len(collidedJewels) != 0:
		if settings.jewelVerticalOrHorizontal == 1: # if horizontally aligned
			if settings.jewelDirection == 1:
				for jewel in settings.jewels.sprites():
					jewel.movingRight = False
			else:
				for jewel in settings.jewels.sprites():
					jewel.movingLeft = False

		else:									    # If vertically aligned
			for movingJewel, stationaryJewels in collidedJewels.items():
				if movingJewel.movingRight:
					movingJewel.movingRight = False
				else:
					movingJewel.movingLeft = False
		#movingJewel.movingRight = False if movingJewel.movingRight else movingJewel.movingLeft = False





				

############################################
def anyJewelReachedEdge(settings, screen, jewels):
	screenRect = screen.get_rect()
	returnValue = False
	for jewel in jewels.sprites():
		if jewel.rect.right > screenRect.right - settings.jewelWidth:
			if settings.jewelDirection != -1:
				returnValue = True
				break

		elif jewel.rect.left < settings.jewelWidth:
			if settings.jewelDirection != 1:
				returnValue = True
				break

	return returnValue

############################################
def checkIfTheJewelGroupReachedBottom(settings):
	reachedBottom = False
	numberOfJewelsReachedBottomIfHorizontallyAligned = 0

	if settings.jewelVerticalOrHorizontal == 0:
		for jewel in settings.jewels.sprites():
			if jewel.reachedBottom:
				reachedBottom = True
				break

		return reachedBottom

	else:
		for jewel in settings.jewels.sprites():
			if jewel.reachedBottom:
				numberOfJewelsReachedBottomIfHorizontallyAligned += 1

		if len(settings.jewels) == numberOfJewelsReachedBottomIfHorizontallyAligned:
			reachedBottom = True
		
		return reachedBottom



############################################
def groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup):
	for jewel in settings.jewels.sprites():
		currentJewelsGroup.add(jewel)







			

######################################################## SCREEN UPDATES ####################################################

'''
-- To give the notion of a free movement of jewels, after jewels making a movement (either downwards or sidewards) we fill the 
screen again with the background color.

-- During that time, jewels which were present earlier would be cleared and we would be offered a clear empty screen.

-- To prevent the game from this, after filling the screen with backgroud color, we blit (draw) the jewels in the jewelsGroup with 
the recent and updated co-ordinates using blit method

-- whenever a jewelGroup reached the bottom, they would be saved in the currentJewelsGroup present in NewValuesForNewJewels class

-- pygame.display.flip() method updates the screen with the recent updates.
'''

def updateScreen(settings, screen, jewelType, jewels, currentJewelsGroup):
	screen.fill(settings.backgroundColor)
	if jewelType == 1:
		for rectangle in jewels.sprites():
			rectangle.blitme()

		if len(currentJewelsGroup) != 0:
			for rectangle in currentJewelsGroup.sprites():
				rectangle.blitme()

	pygame.time.delay(100)
	pygame.display.flip()



############################################
def determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings):
	numberOfSegments = int((settings.screenWidth)  / settings.jewelWidth)
	return numberOfSegments	


			





