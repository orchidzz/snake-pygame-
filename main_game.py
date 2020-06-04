import pygame
import sys
import os
import random
import math

'''set up'''
pygame.init()

#height and width of the screen
worldx = 1000
worldy = 700

#multiple screens
startScr = True
playScr = False
loseScr = False
running = True # main loop of game

#grids for the play screen
grid_list = []
''' 
	[0][0][0]...
	[0][0][0]...
	...
'''
SIDE_LENGTH = 18 #the length of the grid
MARGIN = 2 #the width of the margin

#pixels to move coord of snake by according to the pressed key
DIRECTION_LIST = {"K_LEFT": (- MARGIN - SIDE_LENGTH, 0), "K_RIGHT": (MARGIN + SIDE_LENGTH, 0), "K_DOWN": (0, MARGIN + SIDE_LENGTH), "K_UP": (0, -MARGIN - SIDE_LENGTH)}
	
#set initial direction of snake to be up/north
head_direction = "K_UP"

clock = pygame.time.Clock()

'''objects'''
#snake_body = pygame.sprite.Group()
snake_parts_list = []
class Snake(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
	def draw(self, backgound, x_coord, y_coord):
		self.sprite = pygame.draw.rect(background, [0,255,0], [x_coord,y_coord, SIDE_LENGTH+MARGIN,SIDE_LENGTH+MARGIN])
		self.rect = pygame.Rect(self.sprite)
		snake_parts_list.append(self)
		self.position = [x_coord,y_coord]
		
	def move_(self, new_direction):
		
		self.rect.move_ip(new_direction)
		
		
		#change position of snake's head when it moves
		self.position[0] += new_direction[0]
		self.position[1] += new_direction[1]
		
		pygame.display.flip()
	
	def follow(self, old_direction, new_direction, snake_head):
		if not self.coords() == snake_head.coords():
			self.move_(DIRECTION_LIST[old_direction])

		self.direction = new_direction
		self.move_(DIRECTION_LIST[new_direction])
	#def die(cls):
		#cls.()
	#need func to erase the snake when lose
	def collides_with(self, sprite):
		return self.rect.collidepoint(sprite)
	
	def coords(self, num):
		return self.position[num] #as a list
		
FOOD_group = pygame.sprite.GroupSingle()
class Food(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
	def spawn(self, background, position):
		self.sprite = pygame.draw.circle(background, [255,255,0], position, 10)
		FOOD_group.add(self)
		pygame.display.update()
		
		#coords of the upper left corner of grid the target(a circle) is in equals to the center of circle minus radius
		self.position = position
		for i in self.position:
			i = i - SIDE_LENGTH/2
	def eaten(self, background, color):
		self.sprite = pygame.draw.circle(backgound, color, self.position, 10)
		pygame.display.update()
		self.kill()
	def coords(self):
		return self.position # as a list

'''instantiate objects'''
target = Food()
head = Snake()

'''main loop'''
while running:
	#start screen
	while startScr == True:
		background = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
		background.fill([0,0,0])
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
		#draw grids for background
		#remember to change range when change side length/ margin/ or screen width/height values
		#draw once
		if len(grid_list) == 0:
			background = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
			background_color = [0,0,0]
			background.fill(background_color)
			for row in range(35):
				grid_list.append([])
				for column in range(50):
					x_coord = (MARGIN + SIDE_LENGTH) * column + MARGIN #x-coord of the grid 
					y_coord = (MARGIN + SIDE_LENGTH) * row + MARGIN # y-coord of the grid
					grid_list[row].append([x_coord + int(SIDE_LENGTH/2), y_coord +int(SIDE_LENGTH/2)]) #append the center of the square according to that grid --> needed to spawn the food which is a circle
					pygame.draw.rect(background, [80,80,80],[x_coord, y_coord,SIDE_LENGTH,SIDE_LENGTH])
		
			head.draw(background, 500, 500)
		
		
		head.move_(DIRECTION_LIST[head_direction])
		
		
		#check events
		for event in pygame.event.get():
			#when arrow keys are pressed, move the head of the snake according to direction (if the direction is not the same as the current direction of the snake's head)
			if event.type == pygame.KEYDOWN:
				if event.key in DIRECTION_LIST and event.key != head_direction:
					head.move_(DIRECTION_LIST[event.key])
					prev_direction = head_direction
					head_direction = event.key
				#snake's body parts follow the head
					for part in snake_parts_list:
						part.follow(prev_direction, head_direction, head)	
			
			#when user quits, end the loop
			if event.type == pygame.QUIT:
				running = False
				playScr = False
		
		#when food disappears, spawn the food at random grid
		if not FOOD_group.has(target):
			target.spawn(background, (grid_list[random.randint(0, 34)][random.randint(0, 49)]))
		
		#when snake eats the food, delete the food + snake grows
		#need fix
		if head.collides_with(target.coords()):
			target.eaten(background, background_color) #delete food
			
			#grows??
			'''
				list append name
				name.Snake()
				find direction of next to last part
				position name part at (next to last part's position - direction)
				name.follow()
			'''	
			new_part = "part" + str(snake_parts_list.length())
			snake_parts_list.append(x)
			new_part = Snake()
			last_part = snake_parts_list[length-1]
			coords = last_part.coords()
			last_part_direction = DIRECTION_LIST[last_part.getattr(direction)] 
			new_part_x = coords[0] - last_part_direction[0]
			new_part_y = coords[1] - last_part_direction[1]
			new_part.draw(background, new_part_x, new_part_y)
			new_part.follow(prev_direction,head_direction, head)
			
		#when snake's head goes out of bound, end game & set lose screen
		if  head.coords(0) >1000 or head.coords(0) < 0 or head.coords(1) > 1000 or head.coords(1) < 0:
			loseScr = True
			playScr = False
		print("hi")
		
		pygame.display.update()
		clock.tick(2) # num of frames per second
		
	#lose screen --> ask for replay
	while loseScr == True:
		#need to create replay button
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				startScr = True
				loseScr = False
		#when user quits, ends the loop
			if event.type == pygame.QUIT:
				running = False
				loseScr = False
				
			
#ends the program
pygame.quit()


'''need to make the snake move'''