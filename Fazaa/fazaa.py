# Fazaa
# Music by Trevor Lentz (Deus Ex Tempus)
# Graphics by Kenney (www.kenney.nl)

# Imports
import pygame
import random
from os import path
import sys
import os

# Executable stuff
def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

# Initialize pygame modules
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

# Screen Setup
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Fazaa')

# FPS clock
clock = pygame.time.Clock()

# Background
background = pygame.image.load(find_data_file('background.png')).convert()
background = pygame.transform.scale(background, (800, 800))
bg1DrawHeight = 0
background2 = pygame.image.load(find_data_file('background2.png')).convert()
background2 = pygame.transform.scale(background2, (800, 800))
bg2DrawHeight = -800

# Function for drawing text to screen
def drawText(screen, text, size, x, y):
    font = pygame.font.Font(find_data_file('kenvector_future.ttf') , size)
    textSurface = font.render(text, True, (255, 255, 255))
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    screen.blit(textSurface, textRect)

# Function for creating a new meteor
def createMeteor():
    meteor = Meteor()
    allSprites.add(meteor)
    meteors.add(meteor)

# Function for drawing health
def drawHealth(screen, x, y, health):
    if health < 0:
        health = 0
    barLength = 150
    barHeight = 10
    fill = (health / 100) * barLength
    outlineRect = pygame.Rect(x, y, barLength, barHeight)
    fillRect = pygame.Rect(x, y, fill, barHeight)
    pygame.draw.rect(screen, (255, 0, 0), fillRect)
    pygame.draw.rect(screen, (255, 255, 255), outlineRect, 2)

def drawLives(screen, x, y, lives):
    for i in range(lives):
        image = playerLifeSprite
        imageRect = playerLifeSprite.get_rect()
        imageRect.x = x + 30 * i
        imageRect.y = y
        screen.blit(playerLifeSprite, imageRect)

def gameOverScreen():
    drawText(screen, "Fazaa", 64, WIDTH / 2, HEIGHT / 4)
    drawText(screen, "Arrow Keys To Move, Space To Shoot, Q To Quit", 18, WIDTH / 2, HEIGHT / 2)
    drawText(screen, "Press A Key To Begin", 18, WIDTH / 2, HEIGHT * 4 / 7)
    drawText(screen, "Developed by Haroon", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                else:
                    waiting = False

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerSprite
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.thrust = Thrust(self.rect.centerx, self.rect.bottom)
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hiddenTimer = pygame.time.get_ticks()
        self.shootMode = 0
        self.shootModeTime = pygame.time.get_ticks()
        self.shieldMode = 0
        self.shieldModeTime = pygame.time.get_ticks()

    def update(self):
        # Unhide if player is hidden
        if self.hidden and pygame.time.get_ticks() - self.hiddenTimer > 3000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 50)
        # Stand still if no buttons are pressed
        self.xSpeed = 0
        self.ySpeed = 0
        # Remove thrust sprite if no forward movement
        self.thrust.kill()
        # Timeout shootMode
        if self.shootMode == 1 and pygame.time.get_ticks() - self.shootModeTime > 10000:
            self.shootMode = 0
            self.shootModeTime = pygame.time.get_ticks()
        # Timeout shieldMode
        if self.shieldMode == 1 and pygame.time.get_ticks() - self.shieldModeTime > 10000:
            self.shieldMode = 0
            self.shieldModeTime = pygame.time.get_ticks()

        # Check for pressed buttons
        pressed = pygame.key.get_pressed()

        # Movement and thrust animation for forward movement
        if pressed[pygame.K_LEFT]:
            self.xSpeed = -7
        if pressed[pygame.K_RIGHT]:
            self.xSpeed = 7
        if pressed[pygame.K_UP]:
            self.ySpeed = -7
            self.thrust.rect.midtop = (self.rect.centerx, self.rect.bottom)
            allSprites.add(self.thrust)
        if pressed[pygame.K_DOWN]:
            self.ySpeed = 7


        # Fix speed of diagonal movement
        if self.xSpeed != 0 and self.ySpeed != 0:
            self.xSpeed /= 1.414
            self.ySpeed /= 1.414

        # Move
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

        # Movement boundaries
        if self.rect.right > WIDTH + self.rect.width / 2:
            self.rect.right = WIDTH + self.rect.width / 2
        if self.rect.left < 0 - self.rect.width / 2:
            self.rect.left = 0 - self.rect.width / 2
        if self.rect.bottom > HEIGHT + self.rect.height / 2 and not self.hidden:
            self.rect.bottom = HEIGHT + self.rect.height / 2
        if self.rect.top < 0 - self.rect.height / 2:
            self.rect.top = 0 - self.rect.height / 2

    def shoot(self):
        # Shoot laser
        if not self.hidden and self.shootMode == 0:
            pygame.mixer.Channel(3).play(laserSound)
            laser = Laser(self.rect.centerx, self.rect.top)
            allSprites.add(laser)
            lasers.add(laser)
        if not self.hidden and self.shootMode == 1:
            pygame.mixer.Channel(3).play(laserSound)
            laser1 = Laser(self.rect.centerx, self.rect.top)
            laser2 = Laser(self.rect.left, self.rect.centery)
            laser3 = Laser(self.rect.right, self.rect.centery)
            allSprites.add(laser1)
            allSprites.add(laser2)
            allSprites.add(laser3)
            lasers.add(laser1)
            lasers.add(laser2)
            lasers.add(laser3)


    def hide(self):
        # Hide the player temporarily when dead
        self.hidden = True
        self.hiddenTimer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 3000)

    def tripleGun(self):
        # Shoot three lasers
        self.shootMode = 1
        self.shootModeTime = pygame.time.get_ticks()

    def shield(self):
        # Create shield
        if self.shieldMode == 1:
            self.shieldModeTime = pygame.time.get_ticks()
        else:
            self.shieldMode = 1
            self.shieldModeTime = pygame.time.get_ticks()
            playerShield = Shield()
            allSprites.add(playerShield)

# Laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laserSprite
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.ySpeed = -10

    def update(self):
        # Move laser straight up the screen and remove it, if it goes off the screen
        self.rect.y += self.ySpeed
        if self.rect.bottom < 0:
            self.kill()     

# Thrust
class Thrust(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = thrustSprite
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)

# Shield
class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shieldSprite
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center

    def update(self):
        # Make shield follow player
        self.rect.center = player.rect.center 
        # Remove shield if timeout
        if player.shieldMode == 0:
            self.kill()

# Meteor
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageOriginal = random.choice(meteorSprites)
        self.image = self.imageOriginal.copy()
        self.imageOriginal.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -150)
        self.ySpeed = random.randrange(2, 15)
        self.xSpeed = random.randrange(-2, 3)
        self.rotation = 0
        self.rotationSpeed = random.randrange(-8, 9)
        self.lastUpdate = pygame.time.get_ticks()

    # Rotation
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 17:
            self.lastUpdate = now
            self.rotation = (self.rotation + self.rotationSpeed) % 360
            newImage = pygame.transform.rotate(self.imageOriginal, self.rotation)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter


    def update(self):
        # Rotate
        self.rotate()
        # Move
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        # Remove meteor if it goes off the screen and create a new one 
        if self.rect.top > HEIGHT + 10 or self.rect.right < -10 or self.rect.left > WIDTH + 10:
            self.kill()
            meteor = Meteor()
            allSprites.add(meteor)
            meteors.add(meteor)

# Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosionAnimation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = -1
        self.lastUpdate = pygame.time.get_ticks()
        self.frameRate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > self.frameRate:
            self.lastUpdate = now
            self.frame += 1
            if self.frame == len(explosionAnimation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionAnimation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Powerup
class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerupSprites[self.type]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.ySpeed = 2

    def update(self):
        # Move powerups slowly down the screen
        self.rect.y += self.ySpeed
        if self.rect.top > HEIGHT:
            self.kill()  

# Load sounds
laserSound = pygame.mixer.Sound(find_data_file('laser.wav'))

explosionSounds = []
for sound in ('explosion.ogg', 'explosion2.ogg'):
    explosionSounds.append(pygame.mixer.Sound(find_data_file(sound)))
explosionSounds = tuple(explosionSounds)

playerExplosionSound = pygame.mixer.Sound(find_data_file('booms.ogg'))

# Music
pygame.mixer.music.load(find_data_file('Deus_Ex_Tempus.mp3'))

# Load sprites
playerSprite = pygame.image.load(find_data_file('redPlayer.png')).convert()
playerSprite = pygame.transform.smoothscale(playerSprite, (66, 50))
playerSprite.set_colorkey((0, 0, 0))

playerLifeSprite = pygame.image.load(find_data_file('redLife.png')).convert()
playerLifeSprite = pygame.transform.smoothscale(playerSprite, (12, 10))
playerLifeSprite.set_colorkey((0, 0, 0))

laserSprite = pygame.image.load(find_data_file('redLaser.png')).convert()
laserSprite = pygame.transform.smoothscale(laserSprite, (4, 27))
laserSprite.set_colorkey((0, 0, 0))

thrustSprite = pygame.image.load(find_data_file('thrust.png')).convert()
thrustSprite = pygame.transform.smoothscale(thrustSprite, (7, 15))
thrustSprite.set_colorkey((0, 0, 0))

shieldSprite = pygame.image.load(find_data_file('shield.png')).convert()
shieldSprite = pygame.transform.smoothscale(shieldSprite, (144, 137))
shieldSprite.set_colorkey((0, 0, 0))
shieldSprite.set_alpha(50)

meteorSprites = []
meteorList = ('bigbrown1.png', 'bigbrown2.png', 'bigbrown3.png', 'bigbrown4.png', 'biggrey1.png', 'biggrey2.png',
    'biggrey3.png', 'biggrey4.png', 'medbrown1.png', 'medbrown2.png', 'medgrey1.png', 'medgrey2.png', 'smallbrown1.png',
    'smallbrown2.png', 'smallgrey1.png', 'smallgrey2.png', 'tinybrown1.png', 'tinybrown2.png', 'tinygrey1.png',
    'tinygrey2.png')
for sprite in meteorList:
    meteorSprites.append(pygame.image.load(find_data_file(sprite)).convert())
meteorSprites = tuple(meteorSprites)

powerupSprites = {}
powerupSprites['shield'] = pygame.image.load(find_data_file('shieldPower.png')).convert()
powerupSprites['gun'] = pygame.image.load(find_data_file('gunPower.png')).convert()

# Animations
explosionAnimation = {}
explosionAnimation['lg'] = []
explosionAnimation['sm'] = []
explosionAnimation['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    image = pygame.image.load(find_data_file(filename)).convert()
    image.set_colorkey((0, 0, 0))
    imageLarge = pygame.transform.smoothscale(image, (80, 80))
    explosionAnimation['lg'].append(imageLarge)
    imageSmall = pygame.transform.smoothscale(image, (32, 32))
    explosionAnimation['sm'].append(imageSmall)

    filename = 'sonicExplosion0{}.png'.format(i)
    image = pygame.image.load(find_data_file(filename)).convert()
    image.set_colorkey((0, 0, 0))
    explosionAnimation['player'].append(image)


# Play music
pygame.mixer.music.play(loops = -1)

# Game over flag
gameOver = True

# Game loop flag
done = False
 
# -------- Game Loop -----------
while not done:    
    # --- 60 FPS
    clock.tick(60)

    # Game over
    if gameOver:
        gameOverScreen()
        gameOver = False
        
        # Sprite groups
        allSprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        lasers = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # Create player
        player = Player()
        allSprites.add(player)

        # Create meteors
        for i in range(15):
            createMeteor()

        # Score variable
        score = 0
    
    # --- Events loop (inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_q:
                pygame.quit()

    # --- Game logic
    allSprites.update()

    # Meteor and player collisions
    collisions = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for collision in collisions:
        pygame.mixer.Channel(1).play(random.choice(explosionSounds))
        explosion = Explosion(collision.rect.center, 'sm')
        allSprites.add(explosion)
        if player.shieldMode == 0:
            player.health -= collision.radius * 2
        createMeteor()
        if player.health <= 0:
            pygame.mixer.Channel(2).play(playerExplosionSound)
            playerExplosion = Explosion(player.rect.center, 'player')
            allSprites.add(playerExplosion)
            player.hide()
            player.lives -= 1
            player.health = 100
    
    # Wait for player explosion animation to finish after death
    if player.lives == 0 and not playerExplosion.alive():
        player.kill()
        if not pygame.mixer.get_busy():
            gameOver = True
    
    # Meteor and laser collisions
    collisions = pygame.sprite.groupcollide(meteors, lasers, True, True)
    for collision in collisions:
        random.choice(explosionSounds).play()
        explosion = Explosion(collision.rect.center, 'lg')
        allSprites.add(explosion)
        if random.random() > 0.97:
            powerup = Powerup(collision.rect.center)
            allSprites.add(powerup)
            powerups.add(powerup)
        score += 100 - collision.radius
        createMeteor()

    # Player and powerup collisions
    collisions = pygame.sprite.spritecollide(player, powerups, True)
    for collision in collisions:
        if collision.type == 'shield':
            player.shield()
        if collision.type == 'gun':
            player.tripleGun()

    # --- Screen-clearing (background)
    if bg1DrawHeight >= 800:
        bg1DrawHeight = -800
    if bg2DrawHeight >= 800:
        bg2DrawHeight = -800
    screen.blit(background, (0, bg1DrawHeight))
    screen.blit(background2, (0, bg2DrawHeight))
    bg1DrawHeight += 1
    bg2DrawHeight += 1
 
    # --- Drawing/rendering
    allSprites.draw(screen)
    drawText(screen, str(score), 26, WIDTH / 2, 20)
    drawHealth(screen, 20, 20, player.health)
    drawLives(screen, WIDTH - 100, 20, player.lives)
 
    # --- Flip
    pygame.display.flip()
 
 
# Quit
pygame.quit()