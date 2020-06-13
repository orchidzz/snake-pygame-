import pygame
import sys
import os
import random
import math

'''set up'''
pygame.init()

#height and width of the screen
worldx = 400
worldy = 400
global background

#multiple screens
startScr = True
playScr = False
loseScr = False
running = True # main loop of game

#grids for the play screen
grid_list = []
'''
	[[0][0][0]...]
	[[0][0][0]...]
	...
'''
SIDE_LENGTH = 18 #the length of the grid
MARGIN = 2 #the width of the margin
	
#set initial direction of snake to be up/north
head_direction = "K_UP"

clock = pygame.time.Clock()

'''objects'''
#func to draw the grid for background
def setUpBoard():
	background = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
	background_color = [0,0,0]
	background.fill(background_color)
	for row in range(int(worldy/(SIDE_LENGTH+MARGIN))):
		grid_list.append([])
		for column in range(int(worldx/(SIDE_LENGTH+MARGIN))):
			x_coord = (MARGIN + SIDE_LENGTH) * column + MARGIN #x-coord of the grid 
			y_coord = (MARGIN + SIDE_LENGTH) * row + MARGIN # y-coord of the grid
			grid_list[row].append([x_coord + int(SIDE_LENGTH/2), y_coord +int(SIDE_LENGTH/2)]) #append the center of the square according to that grid --> needed to spawn the food which is a circle
			pygame.draw.rect(background, [80,80,80],[x_coord, y_coord,SIDE_LENGTH,SIDE_LENGTH])

snake_parts_list = []	
class Snake(pygame.sprite.Sprite):
	#list of pixels to move coord of snake by according to the pressed key
	global DIRECTION_LIST
	DIRECTION_LIST = {"K_LEFT": (- MARGIN - SIDE_LENGTH, 0), "K_RIGHT": (MARGIN + SIDE_LENGTH, 0), "K_DOWN": (0, MARGIN + SIDE_LENGTH), "K_UP": (0, -MARGIN - SIDE_LENGTH)}
	
	def __init__(self, num):
		pygame.sprite.Sprite.__init__(self)
		self.number = num #id for each snake's part
		self.rect = 0
		self.position = 0
		snake_parts_list.append(self) #add to snake parts list to control its growth
		
		self.posList = [] #store the part's position coords whenever it moves
	
	def draw(self, x_coord, y_coord):
		self.sprite = pygame.draw.rect(background, [0,255,0], [x_coord,y_coord, SIDE_LENGTH+MARGIN,SIDE_LENGTH+MARGIN])
		self.rect = pygame.Rect(x_coord,y_coord, SIDE_LENGTH+MARGIN,SIDE_LENGTH+MARGIN)
		
		self.position = [x_coord,y_coord]
		
	def move_(self, new_direction):
		#reset background in order to redraw rect to make it "move"
		grid_list.clear()
		setUpBoard()
		
		#change position of snake's head when it moves
		self.position[0] += new_direction[0]
		self.position[1] += new_direction[1]
		
		#redraw rect at new position
		self.sprite = pygame.draw.rect(background, [0,255,0], [self.position[0],self.position[1], SIDE_LENGTH+MARGIN,SIDE_LENGTH+MARGIN])
		self.rect = self.sprite
		
		#delete unnecessary stored positions except the last two when a new part is added to follow the prev part
		if len(snake_parts_list)-1 > self.number:
			del self.posList[0:len(self.posList)-1]
		
		position_element = tuple(self.position) #make it a tuple to not change it when appended as self.position changes continuously which causes the position_element stored to change
		self.posList.append(position_element)
	
	def collides_with(self, sprite):
		return self.rect.collidepoint(sprite)
	
	def coords(self, indexNum):
		return self.position[indexNum] #as a list [x,y]
	
	def crashed_into_its_parts(self):
		if self.rect.collidelist(snake_parts_list[1:len(snake_parts_list)-1]) == -1:
			return False
		else:
			return True

class SnakeParts(Snake):
	def __init__(self, num):
		super().__init__(num)
		
	def follow(self, followPos):
		self.followPosList = followPos
		pos = self.followPosList[0]
		self.position = pos #update its own position --> a tuple
		
		#delete unnecessary stored positions except the last two when a new part is added to follow the prev part
		if (len(snake_parts_list)-1) > self.number:
			del self.posList[0:len(self.posList)-1] #exclusive of the last element
		
		#redraw the part at new position
		self.sprite = pygame.draw.rect(background, [0,255,0], [ pos[0],pos[1], SIDE_LENGTH+MARGIN,SIDE_LENGTH+MARGIN ])
		self.rect = self.sprite
		
		self.posList.append(self.position)	#add the new position to its list

class Food(pygame.sprite.Sprite):
	global FOOD_group
	FOOD_group = pygame.sprite.GroupSingle()
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.position = 0
		
	def spawn(self, position):
		self.sprite = pygame.draw.circle(background, [255,255,0], position, 10)
		FOOD_group.add(self)
		#pygame.display.update()
		
		#coords of the upper left corner of grid the target(a circle) is in equals to the center of circle minus radius
		self.position = position
		for i in self.position:
			i = i - SIDE_LENGTH/2
	def eaten(self):
		setUpBoard()
		#pygame.display.update()
		self.kill()
	def coords(self):
		return self.position # as a list

'''instantiate objects'''
target = Food()
head = Snake(0)

'''main loop'''
while running:
	#start screen
	while startScr == True:
		background = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
		background.fill([0,0,0])
		FONT = pygame.font.SysFont('Arial', 50)
		text1 = FONT.render("Start???", True, [255, 255, 255])
		text2 = FONT.render("click the screen", True, [255, 255, 255])
		background.blit(text1, (0,250))
		background.blit(text2, (0,300))
		pygame.display.update()
		#when user quits, ends the loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				startScr = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				playScr = True
				startScr = False
		
	#play screen
	while playScr == True:
		#draw grids for background when game screen starts 
		#draw once
		if len(grid_list) == 0:
			setUpBoard()
			head.draw(int(worldx/2), int(worldy/2))
			
		#check events
		for event in pygame.event.get():
			#when arrow keys are pressed, move the head of the snake according to direction (if the direction is not the same as the current direction of the snake's head)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and head_direction != "K_UP" and head_direction != "K_DOWN":
					#prev_direction = head_direction
					head_direction = "K_DOWN"
				elif event.key == pygame.K_UP and head_direction != "K_DOWN" and head_direction != "K_UP":
					#prev_direction = head_direction
					head_direction = "K_UP"
				elif event.key == pygame.K_LEFT and head_direction != "K_RIGHT" and head_direction != "K_LEFT":
					#prev_direction = head_direction
					head_direction = "K_LEFT"
				elif event.key == pygame.K_RIGHT and head_direction != "K_LEFT" and head_direction != "K_RIGHT":
					#prev_direction = head_direction
					head_direction = "K_RIGHT"
				#else:
					#prev_direction = head_direction
				#direction_list.append(prev_direction)
			#when user quits, end the loop
			if event.type == pygame.QUIT:
				running = False
				playScr = False
		
		#move the head
		head.move_(DIRECTION_LIST[head_direction])
		
		#when snake's head goes out of bound, end game & set lose screen
		if  head.coords(0) > worldx or head.coords(0) < -10 or head.coords(1) > worldy or head.coords(1) < -10:
			loseScr = True
			playScr = False
			break

		#when snake's head collides with snake's body parts
		if head.crashed_into_its_parts():
			loseScr = True
			playScr = False
			break
			
		#spawn the food
		if not FOOD_group.has(target):
			food_position = (grid_list[random.randint(0, int(worldx/(SIDE_LENGTH+MARGIN)-1))][random.randint(0, int(worldy/(SIDE_LENGTH+MARGIN)-1))])
			target.spawn(food_position)
		else:
			target.spawn(food_position)
		
		#move the snake parts one by one, excluding the head (index 0)
		for part in range(1, len(snake_parts_list)):
			last_part = snake_parts_list[part-1]
			snake_parts_list[part].follow(getattr(last_part, "posList"))	
		
		#when snake eats the food, delete the food + snake grows
		if head.collides_with(target.coords()):
			target.eaten() #delete food
			
			last_part = snake_parts_list[len(snake_parts_list)-1] #locate the snake's last part in the list
			new_part = SnakeParts(len(snake_parts_list)) #create new instance
			#get last position of the last instance/snake part
			last_part_x = getattr(last_part, "posList")[len(head.posList)-2][0] 
			last_part_y = getattr(last_part, "posList")[len(head.posList)-2][1]
			#draw new snake part
			new_part.draw(last_part_x, last_part_y)
		
		#frame update
		pygame.display.update()
		clock.tick_busy_loop(5) # num of frames per second
		
	#lose screen --> ask for replay
	while loseScr == True:
		#need to create replay button
		background = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
		background.fill([0,0,0])
		
		FONT = pygame.font.SysFont('Arial', 50)
		text1 = FONT.render("play again???", True, [255, 255, 255])
		text2 = FONT.render("click the screen", True, [255, 255, 255])
		background.blit(text1, (0,250))
		background.blit(text2, (0,300))
		pygame.display.update()
		#check events
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				startScr = True
				loseScr = False
				#reset everything
				grid_list.clear()
				del snake_parts_list[1:len(snake_parts_list)]
				
			#when user quits, ends the loop
			elif event.type == pygame.QUIT:
				running = False
				loseScr = False
				
			
#end the program
pygame.quit()


'''need to 
'''