import pygame as pg
import random

width, height = 576, 1024
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Flappy Bird")

pg.font.init()
pg.mixer.init()

scroll = 0
score = 0
pipe_height = [700, 500, 600]

red_bird = pg.image.load("./flappy-bird/sprites/redbird-2.png").convert_alpha()
red_bird = pg.transform.scale2x(red_bird)
red_bird_rect = red_bird.get_rect(center=(width//2, height//2))

yellow_bird = pg.image.load("./flappy-bird/sprites/yellowbird-2.png").convert_alpha()
yellow_bird = pg.transform.scale2x(yellow_bird)
yellow_bird_rect = yellow_bird.get_rect(center=(width//4, height//2))

blue_bird = pg.image.load("./flappy-bird/sprites/bluebird-2.png").convert_alpha()
blue_bird = pg.transform.scale2x(blue_bird)
blue_bird_rect = blue_bird.get_rect(center=(width * 3 //4, height//2))


jump_fx = pg.mixer.Sound("./flappy-bird/audio/wing.wav")
jump_fx.set_volume(0.5)
hit_fx = pg.mixer.Sound("./flappy-bird/audio/die.wav")
hit_fx.set_volume(0.5)
		
def draw_bg(scroll):
	bg = pg.image.load("./flappy-bird/sprites/background-day.png").convert_alpha()
	bg = pg.transform.scale2x(bg)

	screen.blit(bg, (0, 0))

def draw_ground(scroll):
	ground = pg.image.load("./flappy-bird/sprites/base.png").convert_alpha()
	ground = pg.transform.scale2x(ground)
	ground_width = ground.get_width()
	ground_height = ground.get_height()
	screen.blit(ground, (scroll, height - ground_height))
	screen.blit(ground, (scroll + ground_width, height - ground_height))

class Bird:
	def __init__(self, bird):
		self.images = []
		self.index = 0
		self.animate(bird)
		self.img = self.images[self.index]
		self.rect = self.img.get_rect(center=(100, height // 2))
		self.gravity = 0.25
		self.movement = 0
	def animate(self, bird):
		for i in range(1, 4):
			img = pg.image.load(f"./flappy-bird/sprites/{bird}-{i}.png").convert_alpha()
			self.images.append(img)
	def handle_animations(self):
		self.index += 0.1
		if self.index > len(self.images):
			self.index = 0
		self.img = self.images[int(self.index)]
	def draw(self):
		screen.blit(self.img, self.rect)
	def jump(self, key):
		if key[pg.K_SPACE]:
			jump_fx.play()
			self.movement = 0
			self.movement = -8
		self.movement += self.gravity
		self.rect.centery += self.movement

class Pipe:
	def __init__(self):
		self.img = pg.image.load("./flappy-bird/sprites/pipe-green.png").convert_alpha()
		self.pipes = []
	def spawn(self):
		self.y = random.choice(pipe_height)
		bottom_pipe = self.img.get_rect(midbottom=(700, self.y - 300))
		top_pipe = self.img.get_rect(midtop=(700, self.y))
		return top_pipe, bottom_pipe 
	def draw(self):
		for pipe in self.pipes:
			if pipe.bottom >= 800:
				screen.blit(self.img, pipe)
			else:
				flipped = pg.transform.flip(self.img, False, True)
				screen.blit(flipped, pipe)

	def move(self):
		for pipe in self.pipes:
			pipe.centerx -= 5
			
	def check_collisions(self):
		for pipe in self.pipes:
			if bird.rect.colliderect(pipe):
				hit_fx.play()
				return "lose"

		if bird.rect.x <= 0 or bird.rect.bottom >= 800:
			hit_fx.play()
			return "lose"

		return "play"


pipe = Pipe()

clock = pg.time.Clock()
FPS = 60
game_status = "menu"

spawn_pipe = pg.USEREVENT
pg.time.set_timer(spawn_pipe, 1200)

run = True
while run:

	scroll -= 2
	score += 0.01

	draw_bg(scroll)
	if scroll <= -576:
		scroll = 0

	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		if event.type == spawn_pipe:
			pipe.pipes.extend(pipe.spawn())

	pos = pg.mouse.get_pos()
	pressed = pg.mouse.get_pressed()[0]
	if game_status == "menu":
		screen.fill((146,244,255))
		font = pg.font.SysFont("comicsans", 50)
		surf = font.render("Choose a player", False, "brown")
		rect = surf.get_rect(center=(width // 2, 300))

		screen.blit(surf, rect)
		screen.blit(red_bird, red_bird_rect)
		screen.blit(yellow_bird, yellow_bird_rect)
		screen.blit(blue_bird, blue_bird_rect)

		if red_bird_rect.collidepoint(pos) and pressed:
			bird = Bird("redbird")
			game_status = "play"
		if yellow_bird_rect.collidepoint(pos) and pressed:
			bird = Bird("yellowbird")
			game_status = "play"
		if blue_bird_rect.collidepoint(pos) and pressed:
			bird = Bird("bluebird")
			game_status = "play"

	if game_status == "play":

		bird.handle_animations()
		bird.draw()
		key = pg.key.get_pressed()
		bird.jump(key)

		pipe.move()
		pipe.draw()

		draw_ground(scroll)

		game_status = pipe.check_collisions()

		font = pg.font.SysFont("comicsans", 50)
		surf = font.render(f"score : {int(score)}", False, "white")
		rect = surf.get_rect(center=(width // 2, 200))
		screen.blit(surf, rect)

	if game_status == "lose":
		message = pg.image.load("./flappy-bird/sprites/message.png").convert_alpha()
		message_rect = message.get_rect(center=(width // 2, height // 2))

		game_over = pg.image.load("./flappy-bird/sprites/gameover.png").convert_alpha()
		game_over_rect = game_over.get_rect(center=(width // 2, 200))

		screen.blit(message, message_rect)
		screen.blit(game_over, game_over_rect)

		if message_rect.collidepoint(pos) and pressed:
			game_status = "play"
			bird.rect.center = (100, 512)
			pipe.pipes.clear()
			bird.movement = 0
			score = 0

	pg.display.update()
	clock.tick(FPS)