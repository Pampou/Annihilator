from functions import *
import sfml as sf
import random
import math

#Enemy
class Enemy():
	def __init__(self, x, y, name="default"):
		self._x = x
		self._y = y
		
		self._sprite = sf.Sprite(ENEMY1_TEX)
		self._sprite = setOriginToCenter(self._sprite)
		
		self.health = random.randint(2,4)
		self._direction = "left"
		self._speed = 2
		
		self._timer = sf.Clock()
	def shoot(self):
		if self._timer.elapsed_time.milliseconds > ENEMY_SHOOT_RATE:
			self._timer.restart()
			if random.randint(0, 100) > 50:
				return True
			else:
				return False
		else:
			return False
	def damage(self, dmg):
		self.health -= dmg
	def getPos(self):
		return (self._x, self._y)
	def update(self, window):
		if self._direction == "left":
			self._x -= self._speed

		self._sprite.position = (self._x, self._y)
		self._sprite.rotate(-2)
		self._sprite.color = sf.Color(MAIN_COLOR[0],MAIN_COLOR[1],MAIN_COLOR[2],255)
		window.draw(self._sprite)

#Explosion class
class Explosion():
	def __init__(self, x, y, particlesCount):
		self._x = x
		self._y = y
		
		self._particles = []
		self._particlesCount = particlesCount
		
		self._timer = sf.Clock()
		self._lifetime = 2500
		for particle in range(1, self._particlesCount):
			self._particles.append(Particle(self._x, self._y))
	def getTime(self):
		return self._timer
	def getLifetime(self):
		return self._lifetime
	def update(self, window):
		for particle in self._particles:
			particle.update(window)

#Particle
class Particle():
	def __init__(self, x, y):
		self._sprite = sf.Sprite(PARTICLE_TEX)
		self._sprite = setOriginToCenter(self._sprite)
				
		self._alpha = 255
		self._x = x
		self._y = y
		
		angle = random.uniform(0, math.pi*2)
		speed = random.uniform(0.1, 5)
		self._xVel = math.cos(angle) * speed
		self._yVel = math.sin(angle) * speed
	def update(self, window):
		self._x += self._xVel
		self._y += self._yVel
		
		self._alpha -= 5
		if self._alpha < 0:
			self._alpha = 0
		
		self._sprite.position = (self._x, self._y)
		self._sprite.color = sf.Color(MAIN_COLOR[0],MAIN_COLOR[1],MAIN_COLOR[2],self._alpha)
		window.draw(self._sprite)

#Smoke particles
class SmokeParticle():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		self.texture = SMOKE_TEX[random.randint(0,1)]
		self.sprite = sf.Sprite(self.texture)
		self.sprite = setOriginToCenter(self.sprite)
		
		self.sprite.position = (self.x,self.y)
		self.timer = sf.Clock()
		
		self.alpha = 255
		self._speed = random.uniform(1,3)
	def update(self, window):
		self.y -= self._speed
		self.x -= 2
		self.alpha -= 1.5
		if self.alpha < 0:
			self.alpha = 0

		self.sprite.position = (self.x,self.y)
		self.sprite.color = sf.Color(MAIN_COLOR[0],MAIN_COLOR[1],MAIN_COLOR[2],self.alpha)
		
		window.draw(self.sprite)
	def lifetime(self):
		if self.timer.elapsed_time.milliseconds > SMOKE_PARTICLES_LIFETIME:
			return True
		else:
			return False

#Player
class Player():
	def __init__(self, x, y):
		self._sprite = sf.Sprite(sf.Texture.from_file("img/player.png"))
		self._sprite = setOriginToCenter(self._sprite)
		
		self._x = x
		self._y = y
		
		self._health = 100
		self._lives = 3
		self._sprite.position = (self._x, self._y)
	def getPos(self):
		return (self._x, self._y)
	def getHealth(self):
		return self._health
	def getLives(self):
		return self._lives
	def move(self, xVel, yVel):
		self._x += xVel
		self._y += yVel
		
		self._sprite.position = (self._x, self._y)
	def respawn(self, x, y):
		self._x = x
		self._y = y
		
		self._sprite.position = (self._x, self._y)
		self._health = 100
		self._lives -= 1
	def update(self, window):
		window.draw(self._sprite)
	def damage(self, dmg):
		self._health -= dmg

#Bullet
class Bullet():
	def __init__(self, x, y, playerSource=True):
		self._sprite = sf.Sprite(sf.Texture.from_file("img/bullet1.png"))
		self._sprite = setOriginToCenter(self._sprite)
		
		self._x = x
		self._y = y
		
		self._sprite.position = (self._x, self._y)
		self._playerSource = playerSource
		if not self._playerSource:
			self._sprite.color = sf.Color(MAIN_COLOR[0],MAIN_COLOR[1],MAIN_COLOR[2], 255)
	def getPos(self):
		return (self._x, self._y)
	def update(self, window):
		if self._playerSource:
			self._x += 14
		else:
			self._x -= 14
		
		self._sprite.position = (self._x, self._y)
		window.draw(self._sprite)

#CONFIG
WIDTH = 800
HEIGHT = 600

FRAMERATE = 60

SPEED = 8

SMOKE_PARTICLES_MAX = 50
SMOKE_PARTICLES_RATE = 100
SMOKE_PARTICLES_LIFETIME = 4000

PLAYER_SHOOT_RATE = 100
ENEMY_SHOOT_RATE = 1500

SMOKE_TEX = [sf.Texture.from_file("img/smoke1.png"), sf.Texture.from_file("img/smoke2.png")]
PARTICLE_TEX = sf.Texture.from_file("img/particle.png")

ENEMY1_TEX = sf.Texture.from_file("img/enemy1.png")

MAIN_COLOR = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

#Main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "Annihilation")
window.framerate_limit = FRAMERATE

font = sf.Font.from_file("fnt/jupiter.ttf")

#Instance smoke particles
smokeParticles = []
smokeParticlesClock = sf.Clock()

#Player
player = Player(50, HEIGHT/2)
playerShootTime = sf.Clock()

#Player Bullets
playerBullets = []

#All effects
effects = []

#Sounds buf
explodeSnd1Buf = sf.SoundBuffer.from_file("snd/explode1.ogg")
hitSndBuf = sf.SoundBuffer.from_file("snd/hit.ogg")
deathSndBuf = sf.SoundBuffer.from_file("snd/death.wav")

#Sounds
exp1Sound = sf.Sound(explodeSnd1Buf)
hitSound = sf.Sound(hitSndBuf)
deathSound = sf.Sound(deathSndBuf)

#Enemies
enemies = []
enemiesSpawnTick = sf.Clock()

#Enemies bullets
enemiesBullet = []

#Health text
healthText = sf.Text("", font, 24)
healthText.color = sf.Color(255,255,255,255)
healthText.position = sf.Vector2(10,window.height - 74)

#Lives text
livesText = sf.Text("", font, 24)
livesText.color = sf.Color(255,255,255,255)
livesText.position = sf.Vector2(10,window.height - 54)

#Score text
score = 0
scoreText = sf.Text("", font, 24)
scoreText.color = sf.Color(255,255,255,255)
scoreText.position = sf.Vector2(10,window.height - 34)


while window.is_open:
	#Handle smoke particles
	if smokeParticlesClock.elapsed_time.milliseconds > SMOKE_PARTICLES_RATE:
		if len(smokeParticles) < SMOKE_PARTICLES_MAX:
			smokeParticle = SmokeParticle(random.randint(0, WIDTH), 800)
			smokeParticles.append(smokeParticle)
		smokeParticlesClock.restart()
	
	if enemiesSpawnTick.elapsed_time.milliseconds > 500:
		enemies.append(Enemy(WIDTH, random.randint(0, HEIGHT)))
		enemiesSpawnTick.restart()
	
	#Events
	for event in window.events:
		# close window: exit
		if type(event) is sf.CloseEvent:
			window.close()
	
	#Player move
	pos = player.getPos()
	if sf.Keyboard.is_key_pressed(sf.Keyboard.UP) and pos[1] > 0:
		yVel = -SPEED
	elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) and pos[1] < HEIGHT:
		yVel = SPEED
	else:
		yVel = 0
	
	if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) and pos[0] > 0:
		xVel = -SPEED
	elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) and pos[0] < WIDTH:
		xVel = SPEED
	else:
		xVel = 0
	
	player.move(xVel, yVel)

	if sf.Keyboard.is_key_pressed(sf.Keyboard.SPACE):
		if playerShootTime.elapsed_time.milliseconds > PLAYER_SHOOT_RATE:
			playerBullets.append(Bullet(player.getPos()[0]- 10, player.getPos()[1]+18))
			
			playerShootTime.restart()
			
	if player.getHealth() <= 0:
		effects.append(Explosion(player.getPos()[0], player.getPos()[1], 1000))
		player.respawn(50, HEIGHT/2)
		deathSound.play()
	
	if player.getLives() <= 0:
		window.close()
		
	#Clear screen
	window.clear()
	
	#Background smoke
	for smokeParticle in smokeParticles:
		if smokeParticle.lifetime():
			smokeParticles.remove(smokeParticle)
		else:
			smokeParticle.update(window)
	
	#Player
	player.update(window)
	
	#Enemies
	for enemy in enemies:
		if enemy.health <= 0:
			effects.append(Explosion(enemy.getPos()[0], enemy.getPos()[1], 70))
			exp1Sound.play()
			enemies.remove(enemy)
			score += 10
		else:
			if enemy.getPos()[0] < 0:
				enemies.remove(enemy)
			else:
				#Collisions with player
				if collision(player, enemy, 32):
					enemy.health = 0
					player.damage(25)
				else:
					if enemy.shoot():
						enemiesBullet.append(Bullet(enemy.getPos()[0], enemy.getPos()[1],False))
					enemy.update(window)
	
	#Player shots
	for playerBullet in playerBullets:
		#Checking collisions with enemies
		for enemy in enemies:
			if collision(playerBullet, enemy):
				effects.append(Explosion(playerBullet.getPos()[0], playerBullet.getPos()[1], 4))
				playerBullets.remove(playerBullet)
				enemy.damage(1)
				score += 1
				hitSound.play()
		if playerBullet.getPos()[0] < WIDTH + 64:
			playerBullet.update(window)
		else:
			playerBullets.remove(playerBullet)
	
	#Enemies shots
	for enemyBullet in enemiesBullet:
		if collision(enemyBullet, player, 32):
			player.damage(random.randint(1, 3))
			effects.append(Explosion(enemyBullet.getPos()[0], enemyBullet.getPos()[1], 4))
			hitSound.play()
			enemiesBullet.remove(enemyBullet)
		if enemyBullet.getPos()[0] < 0:
			enemiesBullet.remove(enemyBullet)
		else:
			enemyBullet.update(window)
	
	#Effects
	for effect in effects:
		if effect.getTime().elapsed_time.milliseconds < effect.getLifetime():
			effect.update(window)
		else:
			effects.remove(effect)
	
	#Text
	healthText.string = "Health : " + str(player.getHealth())
	livesText.string = "Lives : " + str(player.getLives())
	scoreText.string = "Score : " + str(score)
	
	window.draw(healthText)
	window.draw(livesText)
	window.draw(scoreText)
	
	#Window update
	window.display() 