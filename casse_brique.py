import pygame
from pygame.locals import *
import time
from math import acos, degrees, sqrt, cos
from random import randint

class Niveau:
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generer(self):
        
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for lettre in ligne:
                    if lettre != '':
                        ligne_niveau.append(lettre)
                structure_niveau.append(ligne_niveau)
            self.structure = structure_niveau
    def afficher(self, fenetre):
        
        self.infinie = pygame.image.load("images/brique_noire.png")
        self.rouge = pygame.image.load("images/brique_final.png")
        self.noire = pygame.image.load("images/brique_noire.png")
        self.blanc = pygame.image.load("images/brique_blanche.png")

        num_ligne = 0

        self.infinieX = []
        self.infinieY = []

        self.rougeX = []
        self.rougeY = []
        
        self.blancX = []
        self.blancY = []

        self.noireX = []
        self.noireY = []

        self.Dx = self.rouge.get_width()
        self.Dy = self.rouge.get_height()
        
        for ligne in self.structure:
            num_case = 0
            for lettre in ligne:
                x = num_case * 60
                y = num_ligne * 30

                if lettre == "r":
                    self.rougeX.append(x)
                    self.rougeY.append(y)

                if lettre == "n":         
                    self.noireX.append(x)
                    self.noireY.append(y)

                if lettre == "b":    
                    self.blancX.append(x)
                    self.blancY.append(y)

                if lettre == 'i':
                    self.infinieX.append(x)
                    self.infinieY.append(y)
                num_case += 1
            num_ligne += 1

class Paddle:
    """Classe définissant le comportement de l'objet Paddle"""

    def __init__(self, coord=(0, 0), vitesse=10, images=[]):

        self.vitesse = vitesse
        self.images = [pygame.image.load(img) for img in images]
        self.rect = self.images[0].get_rect()
        self.rect.center = coord

    def affiche(self, fenetre, num_img):
        fenetre.blit(self.images[num_img], self.rect)

    def glisse_left(self, lim_gauche=85):
        if self.rect.left + self.vitesse > lim_gauche :
            self.rect = self.rect.move(-self.vitesse, 0)

    def glisse_right(self, lim_droite=540):
        if self.rect.left + self.vitesse < lim_droite:
            self.rect = self.rect.move((self.vitesse, 0))



class Balle:
    """Classe définissant la balle"""

    def __init__(self, coord=(0, 0), vitesse=0.1, images=[]):
        
        self.images = [pygame.image.load(img) for img in images]
        self.rect = self.images[0].get_rect()
        self.Dx = self.images[0].get_width()
        self.Dy = self.images[0].get_height()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.vecteur = (0, 0)
        self.vitesse = vitesse
        global transfert
        self.count = 0
        self.score = 0 + transfert
        self.v = (50, 0)

        
    def ramdom_vecteur(self, vitesse=0.1):
        
        self.randomx = randint(-2, 2)
        while self.randomx == 0:
            self.randomx = randint(-2, 2)
        self.randomy = randint(2, 5)

    def affiche(self, fenetre, num_img):
        fenetre.blit(self.images[num_img], self.rect)

    def deplace(self):
        self.collision()
        self.rect = self.rect.move(self.vecteur)
        self.ramdom_vecteur()
        liste_key = pygame.key.get_pressed()
        """if liste_key[K_s]:
            self.rect = self.rect.move(0,10)
        if liste_key[K_a]:
            self.rect = self.rect.move(-10, 0)
        if liste_key[K_d]:
            self.rect = self.rect.move(10, 0)
        if liste_key[K_w]:
            self.rect = self.rect.move(0,-10)"""
        if liste_key[K_SPACE]:
            if self.rect.center == (360, 647):
                self.vecteur = (self.randomx, self.randomy)

    def collision(self):

        if self.rect.bottom >= 720:
            self.vecteur = (0,0)
            global continuer_jeu
            global choix
            global transfert
            continuer_jeu = 0
            choix = 0
            transfert = 0
        
        elif pygame.sprite.collide_rect(barre, balle) == True:

            if self.vecteur[0] < 0 and self.vecteur[0] > -6:
                x = self.vecteur[0] - 0.35
            elif self.vecteur[0] > 0 and self.vecteur[0] < 6:
                x = self.vecteur[0] + 0.35

            if self.vecteur[1] < 0 and self.vecteur[1] > -6:
                y = self.vecteur[1] - 0.35
            elif self.vecteur[1] > 0 and self.vecteur[1] < 6:
                y = self.vecteur[1] + 0.35
            else:
                x = self.vecteur[0]
                y = self.vecteur[1]
            self.vecteur = (x, y)      
            self.vecteur = (self.vecteur[0], -self.vecteur[1])
            balle.rect.bottom = barre.rect.top - 5
            self.count = self.count + 1

        if self.rect.collidelist(brique.collision_infinie) != -1:

            self.z = self.rect.collidelist(brique.collision_infinie)
            self.balletobrique = (((brique.collision_infinie[self.z][0] + (niveau.Dx/2)) - (self.rect[0] + (self.Dx/2))), 
                ((brique.collision_infinie[self.z][1] + (niveau.Dy/2)) - (self.rect[1] + (self.Dy/2))))

        elif self.rect.collidelist(brique.collision_rouge) != -1:

            self.z = self.rect.collidelist(brique.collision_rouge)
            self.score = self.score + 10
            self.balletobrique = (((brique.collision_rouge[self.z][0] + (niveau.Dx/2)) - (self.rect[0] + (self.Dx/2))), 
                ((brique.collision_rouge[self.z][1] + (niveau.Dy/2)) - (self.rect[1] + (self.Dy/2))))

        elif self.rect.collidelist(brique.collision_noire) != -1:

            self.z = self.rect.collidelist(brique.collision_noire)
            self.score = self.score + 10
            self.balletobrique = (((brique.collision_noire[self.z][0] + (niveau.Dx/2)) - (self.rect[0] + (self.Dx/2))),
                ((brique.collision_noire[self.z][1] + (niveau.Dy/2)) - (self.rect[1] + (self.Dy/2))))

        elif self.rect.collidelist(brique.collision_blanc) != -1:

            self.z = self.rect.collidelist(brique.collision_blanc)      
            self.score = self.score + 10
            self.balletobrique = (((brique.collision_blanc[self.z][0] + (niveau.Dx/2)) - (self.rect[0] + (self.Dx/2))),
                ((brique.collision_blanc[self.z][1] + (niveau.Dy/2)) - (self.rect[1] + (self.Dy/2))))

        if self.rect.collidelist(brique.collision_infinie) != -1 or self.rect.collidelist(brique.collision_blanc) != -1 or self.rect.collidelist(brique.collision_rouge) != -1 or self.rect.collidelist(brique.collision_noire) != -1:

            self.Nballetobrique = sqrt((self.balletobrique[0]**2) + (self.balletobrique[1]**2))
            self.Ni = sqrt((self.v[0]**2) + (self.v[1]** 2))
            self.scalaire = (((self.balletobrique[0] * self.v[0]) + (self.balletobrique[1] * self.v[1]))/ (self.Nballetobrique * self.Ni))

            self.cos = 2*(degrees(acos(self.scalaire)))
            print(self.cos)
            if self.cos > 0 and self.cos < 60 or self.cos > 294 and self.cos < 360:
                self.vecteur = (-self.vecteur[0], self.vecteur[1])
            elif self.cos > 60 and self.cos < 294:
                self.vecteur = (self.vecteur[0], -self.vecteur[1])


            if self.rect.collidelist(brique.collision_rouge) != -1:
                del brique.collision_rouge[self.z]
                del brique.rX[self.z]
                del brique.rY[self.z]
            elif self.rect.collidelist(brique.collision_noire) != -1:

                del brique.collision_noire[self.z]
                del brique.nX[self.z]
                del brique.nY[self.z]

            elif self.rect.collidelist(brique.collision_blanc) != -1:

                del brique.collision_blanc[self.z]
                del brique.bX[self.z]
                del brique.bY[self.z]

class Brique:
    def __init__(self):
        self.rX = niveau.rougeX
        self.rY = niveau.rougeY
        
        self.bX = niveau.blancX
        self.bY = niveau.blancY

        self.nX = niveau.noireX
        self.nY = niveau.noireY

        self.iX = niveau.infinieX
        self.iY = niveau.infinieY

        self.collision_rouge = []
        for i in range(len(self.rY)):
            x = self.rX[i]
            y = self.rY[i]
            self.collision_rouge.append([x, y, niveau.Dx, niveau.Dy])

        self.collision_blanc = []
        for i in range(len(self.bX)):
            x = self.bX[i]
            y = self.bY[i]
            self.collision_blanc.append([x, y, niveau.Dx, niveau.Dy])
        
        self.collision_noire = []
        for i in range(len(self.nX)):
            x = self.nX[i]
            y = self.nY[i]
            self.collision_noire.append([x, y, niveau.Dx, niveau.Dy])
        
        self.collision_infinie = []
        for i in range(len(self.iX)):
            x = self.iX[i]
            y = self.iY[i]
            self.collision_infinie.append([x, y, niveau.Dx, niveau.Dy])
            
    def affiche_brique(self):
        
        for i in range(len(self.rX)):
            x = self.rX[i]
            y = self.rY[i]
            fenetre.blit(niveau.rouge, (x, y))
        for i in range(len(self.bX)):
            x = self.bX[i]
            y = self.bY[i]
            fenetre.blit(niveau.blanc, (x, y))
        for i in range(len(self.nX)):
            x = self.nX[i]
            y = self.nY[i]
            fenetre.blit(niveau.noire, (x, y))
        for i in range(len(self.iX)):
            x = self.iX[i]
            y = self.iY[i]
            fenetre.blit(niveau.infinie, (x, y))
            
class Bonus:
    def __init__(self, coord, images, vitesse):
        
        self.vitesse = vitesse
        self.images = [pygame.image.load(img) for img in images]
        self.rect = self.images[0].get_rect()
        self.rect.center = coord
        self.vecteur = (0, 0)
        self.seconde = 1
        self.stop = 0 
        self.time2 = 0
        self.replay = 1

    def affiche(self, fenetre, num_img):
        fenetre.blit(self.images[num_img], self.rect)

    def temps(self):
        global time
        if balle.rect.center != (self.rect.x, self.rect.y):
            #DECLENCHE AU BOUT DE 5SEC          
            if self.seconde < 5 and self.seconde > 0:
                if pygame.time.get_ticks() >= time:
                    time += 1000
                    self.seconde += 1
            elif self.seconde >= 5:
                self.vecteur = (0,2)  
            else : 
                self.vecteur = (0, 0)
                self.arret()
            #DECLENCHE AVEC NOMBRE DE REBONDS
            """if self.replay == 0:
                self.arret()
            if balle.count >= 1 and self.replay == 1:
                self.vecteur = (0, 2)
            
            elif balle.count == 0:
                self.vecteur = (0, 0)"""
 
    def move(self):
        self.temps()
        self.colision()
        self.rect = self.rect.move( self.vecteur[0], self.vecteur[1])
    
    def colision(self):  
        global image
        if pygame.sprite.collide_rect(fleche, barre) == True:
            self.coord = barre.rect.center
            image = 1
            barre.rect = barre.images[1].get_rect()
            barre.rect.center = self.coord
            self.seconde = 0
            self.replay = 0
            self.time2 = pygame.time.get_ticks() + 1000
            balle.count = 0
            self.vecteur=(0,0)
            self.rect.center = (-10, -10)

        elif self.rect.bottom > 720:
            balle.count = 0
            self.seconde = 0
            self.replay = 0
            self.vecteur = (0, 0)
            self.rect.center = (-10, -10)

    def arret(self):
        global time
        global image
        if self.stop < 5:
            if pygame.time.get_ticks() >= self.time2:
                self.time2 += 1000
                self.stop += 1
        else:
            self.coord = barre.rect.center
            image = 0
            barre.rect = barre.images[0].get_rect()
            barre.rect.center = self.coord

pygame.init()
pygame.display.set_caption("Break My Breaks")
pygame.key.set_repeat(1, 15)
choix = 0
continuer = 1

transfert = 0

while continuer:

    Xjouer = 160
    Yjouer = 500
    
    Xquitter = 370
    Yquitter = 500
    
    tailleX = 195
    tailleY = 54

    fenetre = pygame.display.set_mode((720, 720))

    titre = pygame.image.load("images/menu_final.png").convert()

    jouer = pygame.image.load("images/jouer_final.png").convert_alpha()
    quitter = pygame.image.load("images/quitter_final.png").convert_alpha()

    fenetre.blit(titre, (0, 0))
    
    pygame.display.flip()

    continuer_accueil = 1
    
           
    while continuer_accueil == 1:

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
                choix = 0
                

            elif event.type == KEYDOWN:
                if event.key == K_F1:
                    continuer_accueil = 0
                    continuer_jeu = 1
                    choix = 2
                if event.key == K_F2:
                    continuer_accueil = 0
                    continuer_jeu = 1
                    choix = 3

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= Xjouer and x <= Xjouer + tailleX:
                    if y >= Yjouer and y <= Yjouer + tailleY:
                        continuer_accueil = 0
                        continuer_jeu = 1
                        choix = 1

            if event.type == MOUSEBUTTONDOWN:
                if x >= Xquitter and x <= Xquitter + tailleX:
                    if y >= Yquitter and y <= Yquitter + tailleY:
                        continuer_accueil = 0
                        continuer_jeu = 0
                        continuer = 0
                        choix = 0
        
        fenetre.blit(jouer, (Xjouer, Yjouer))
        fenetre.blit(quitter, (Xquitter, Yquitter))

        pygame.display.update()
        
        if choix != 0:
            continuer_accueil = 0
            continuer_jeu = 1
            image = 0

        #GENERATION NIVEAU
            niveau = Niveau(str(choix))
            niveau.generer()
            niveau.afficher(fenetre)
        #BARRE        
            barre = Paddle(coord=(360, 670), images=["images/barre_simple_final.png","images/barre_double_final.png"], vitesse=20)
            barre.affiche(fenetre, 0)
        #BALLE
            balle = Balle(coord=(348, 635), images=["images/balle_final.png"], vitesse=0.1)
            balle.affiche(fenetre, 0)

            fleche = Bonus(coord=(randint(80, 640), -10), images=["images/fleche_final.png"], vitesse=0.1)

            brique = Brique()

            color = [0, 0, 0]
        
    while continuer_jeu == 1:

        if balle.vecteur == (0, 0):
            time = pygame.time.get_ticks() + 1000

        balle.deplace()    
        fleche.move()
        brique.affiche_brique()

        if len(brique.collision_rouge) == 0 and len(brique.collision_noire) == 0 and len(brique.collision_blanc) == 0:
            continuer_jeu = 0
            transfert = balle.score
            if choix < 3 :
                choix = choix + 1                
            elif choix >= 3 :
                choix = 0
                continuer = 0
                print("Vous avez gagné ! Score : {}".format(balle.score))
        
        if len(brique.collision_rouge) +  len(brique.collision_noire) + len(brique.collision_blanc) <= 3: color = [10, 150, 10] 
        elif len(brique.collision_rouge) +  len(brique.collision_noire) + len(brique.collision_blanc) <= 5: color = [255, 145, 0]
        elif len(brique.collision_rouge) + len(brique.collision_noire) + len(brique.collision_blanc) <= 10: color = [193, 23, 0]
              
#KEY 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                continuer_jeu = 0
                choix = 0
                transfert = 0
            if event.type == KEYDOWN:
                liste_key = pygame.key.get_pressed()
                if liste_key[K_RIGHT]:
                        barre.glisse_right()
                if liste_key[K_LEFT]:
                        barre.glisse_left()

                pygame.display.update()
        
        
        fenetre.fill(color)
        barre.affiche(fenetre, image)
        balle.affiche(fenetre, 0)       
        niveau.afficher(fenetre)        
        brique.affiche_brique()
        fleche.affiche(fenetre, 0)
        pygame.display.flip()
        pygame.display.update()
        
        pygame.display.set_caption(str(balle.score))
        pygame.time.wait(1)


pygame.quit()
