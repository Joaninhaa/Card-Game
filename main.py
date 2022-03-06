import pygame
from random import choice

pygame.init()
pygame.font.init()

WHITE = (240, 240, 200)
BLACK = (20, 20, 20)
PINK = (255, 190, 210)
GREEN = (190, 255, 180)
BLUE = (190, 255, 255)
GRAY = (150, 150, 150)
PURPLE = (230, 160, 255)
DARKRED = (180, 60, 80)

FPS = 60
TAM = 32
RES = [900//TAM*TAM, 600//TAM*TAM]
CARDNAMES = ["defense", "heal"]
CARDS = {
    #name : [heal, damage, defense, cost]
    "defense": [0, 0, 2, 1],
    "heal" : [2, 0, 0, 1]
}

class Button():
    def __init__(self, y, text, width=TAM*3, height=TAM):
        self.x = RES[0]-width-TAM
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text

    def draw(self, surf, font):
        pygame.draw.rect(surf, WHITE, self.rect)
        txt  = font.render(self.text, True, DARKRED)

        surf.blit(txt, (self.x, self.y))
    
    def clickCheck(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            print(f'Uau vc clicou em {self.text}')

class Enemy():
    def __init__(self, x, y, width=TAM, height=TAM*2):
        self.health = 5
        self.damage = 1
        self.defense = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def drawHUD(self, font, surf):
        txtHealth = font.render(str(self.health), True, GREEN)
        txtDefense = font.render(str(self.defense), True, GRAY)

        surf.blit(txtHealth, (self.x, self.y-txtHealth.get_height()))
        surf.blit(txtDefense, (self.x+self.width-txtDefense.get_width(), self.y-txtDefense.get_height()))

    def draw(self, font, surf):
        pygame.draw.rect(surf, DARKRED, self.rect)
        self.drawHUD(font, surf)


class Player():
    def __init__(self, x, y, width=TAM, height=TAM*2):
        self.health = 10
        self.damage = 1
        self.defense = 0
        self.mana = 100
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.turn = True
    
    def drawHud(self, font, surface):
        txtHealth = font.render("Health: " +  str(self.health), True, GREEN)
        txtMana = font.render("Mana: " +  str(self.mana), True, BLUE)
        txtDamage = font.render("Damage: " +  str(self.damage), True, PINK)
        txtDefense = font.render("Defense: " +  str(self.defense), True, GRAY)

        surface.blit(txtHealth, (RES[0]-txtHealth.get_width(), 0))
        surface.blit(txtMana, (RES[0]-txtMana.get_width(), txtHealth.get_height()))
        surface.blit(txtDamage, (RES[0]-txtDamage.get_width(), txtMana.get_height() + txtHealth.get_height()))
        surface.blit(txtDefense, (RES[0]-txtDefense.get_width(), txtDamage.get_height() +txtHealth.get_height() + txtMana.get_height()))

    def draw(self, surface):
        pygame.draw.rect(surface, PURPLE, self.rect)    


class Card():
    def __init__(self, x, y, width=TAM*2, height=TAM*4):
        self.x = x
        self.y = y 
        self.widthO = width
        self.heightO = height
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.name = choice(CARDNAMES)

        self.heal = CARDS[self.name][0]
        self.damage = CARDS[self.name][1]
        self.defense = CARDS[self.name][2]
        self.cost = CARDS[self.name][3]
        
    def drawHUD(self, font, surf):
        txtName = font.render(self.name.capitalize(), True, PURPLE)
        txtDamage = font.render(str(self.damage), True, PINK)
        txtCost = font.render(str(self.cost), True, BLUE)
        txtHeal = font.render(str(self.heal), True, GREEN)
        txtDefense = font.render(str(self.defense), True, GRAY)
        

        surf.blit(txtName, (self.x, self.y-txtName.get_height()))
        surf.blit(txtDamage, (self.x, self.y))
        surf.blit(txtCost, (self.x+self.width-txtCost.get_width(), self.y))
        surf.blit(txtHeal, (self.x, self.y+self.height-txtHeal.get_height()))
        surf.blit(txtDefense, (self.x+self.width-txtDefense.get_width(), self.y+self.height-txtDefense.get_height()))
    
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height
    
    def clickCheck(self, player, deck):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if player.mana > self.cost and player.turn:
                player.mana -= self.cost
                player.health += self.heal
                player.damage += self.damage
                player.defense += self.defense
                deck.cards.remove(self)


class Deck():
    def __init__(self):
        self.cards = []
        self.border = TAM
    
    def newCards(self, num):
        if len(self.cards) + num <= 7:
            for i in range(num):
                self.cards.append(Card(0, RES[1]-TAM*4))
    
    def displayCards(self, surface):
        i = 0
        for card in self.cards:
            card.x = (TAM*2 + self.border) * i
            card.rect.x = (TAM*2 + self.border) * i
            pygame.draw.rect(surface, (80, 80,80),  card.rect)
            i += 1


 
def hud(font, surf, clock):
    txtFps = font.render("Fps: " +  str(int(clock.get_fps())), True, WHITE)

    surf.blit(txtFps, (0, 0))
                

def main():
    run = True

    player = Player(TAM*5, TAM*7)

    enemy = Enemy(TAM*20, TAM*7)

    deck = Deck()
    myFont = pygame.font.SysFont("Comic Sans MS", TAM//2)
    
    btnPassTurn = Button(RES[1]-TAM*3, "Pass Turn")

    win = pygame.display.set_mode((RES[0], RES[1]))
    pygame.display.set_caption("AYAYAYAYAY :3")
    clock = pygame.time.Clock()

    while run:
        win.fill(BLACK)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_p:
                    deck.newCards(3)

        
        player.drawHud(myFont, win)
        player.draw(win)

        enemy.draw(myFont, win)

        hud(myFont, win, clock)

        btnPassTurn.draw(win, myFont)
        btnPassTurn.clickCheck()

        deck.displayCards(win)
        for card in deck.cards:
            card.drawHUD(myFont, win)
            card.clickCheck(player, deck)

        pygame.display.update()
        clock.tick(FPS)
        

main()