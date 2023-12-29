import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))  # Window
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100
SHIP_MASS = 50
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

WHITE = (255, 255, 255) # Background
RED = (255, 0, 0) # Ship
BLUE = (0, 0, 255) # Planet
BLACK = (0, 0, 0)

BG = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("images/Planet.png"), (PLANET_SIZE * 2 , PLANET_SIZE * 2))
#PLANET_2 = pygame.transform.scale(pygame.image.load("images/Planet_2.png"), (PLANET_SIZE * 2 , PLANET_SIZE * 2))
obj = pygame.transform.scale(pygame.image.load("images/Ship.png"), (OBJ_SIZE * 4 , OBJ_SIZE * 4))
font = pygame.font.Font('freesansbold.ttf', 20)
explosion = pygame.transform.scale(pygame.image.load("images/explosion.gif"), (OBJ_SIZE * 5 , OBJ_SIZE * 2))



class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))
        

#class Planet_2:
    #def __init__(self, x, y, mass):
        #self.x = x
        #self.y = y
        #self.mass = mass

    #def draw(self):
        #win.blit(PLANET_2, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))
        


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.angle = 0
    
    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)   # Calculate distance between ship and planet
        force = (G * self.mass * planet.mass) / distance ** 2 # Calculate force

        acceleration = force / self.mass # Calculate acceleration
        angle = math.atan2(planet.y - self.y, planet.x - self.x) # Calculate angle
        
        acceleration_x = acceleration * math.cos(angle) # Calculate acceleration x
        acceleration_y = acceleration * math.sin(angle) # Calculate acceleration y
       
        self.angle = math.degrees(angle) # Calculate angle in degrees

        self.vel_x += acceleration_x  # Calculate velocity  
        self.vel_y += acceleration_y 

        self.x += self.vel_x  # Calculate position
        self.y += self.vel_y  
    
    def draw(self):
        rotated_image = pygame.transform.rotate(obj, self.angle)
        win.blit(rotated_image, (self.x - OBJ_SIZE, self.y - OBJ_SIZE))

def create_ship(location, mouse):
    t_x, t_y = location # Target x and y
    m_x, m_y = mouse # Mouse x and y
    vel_x = (m_x - t_x) / VEL_SCALE # Calculate velocity x
    vel_y = (m_y - t_y) / VEL_SCALE # Calculate velocity y  
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS) 

    return obj


def text_box(acceleration):
    text = font.render(f'Accelertaion: ' + acceleration  + ' Velocity: ', True, WHITE, None)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 1.15, HEIGHT // 10)
    win.blit(text, textRect)

def main():
    running = True
    clock = pygame.time.Clock()
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    #planet_2 = Planet_2(WIDTH // 4, HEIGHT // 2, PLANET_MASS)
    objects = []
    object_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if object_pos:
                    obj = create_ship(object_pos, mouse_pos)
                    objects.append(obj)
                    object_pos = None
                else:   
                    object_pos = mouse_pos  # Set object position to mouse position
        
        win.blit(BG, (0, 0)) # Draw background
        
        if object_pos:
            pygame.draw.line(win, WHITE, object_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, object_pos, OBJ_SIZE)
        
                
        planet.draw()
        
        for obj in objects:
            obj.draw()
            obj.move(planet)
            #obj.move(planet_2)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collide = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
            #collide_2 = math.sqrt((obj.x - planet_2.x)**2 + (obj.y - planet_2.y)**2) <= PLANET_SIZE
            if off_screen or collide: #collide_2
                objects.remove(obj)
                win.blit(explosion, (obj.x - OBJ_SIZE, obj.y - OBJ_SIZE))

                
            else:
                acceleration = round(math.sqrt(obj.vel_x**2 + obj.vel_y**2), 2)
                text_box(str(acceleration))
        
        pygame.display.update() # Update display
               
        
    pygame.quit()
            

if __name__ == "__main__":
    main()  # Run main function