import pygame
import menu
import time
import random

pygame.init()

# Classe Terrain pour gérer les éléments du terrain, Génération / Affichage
class Terrain:
    def __init__(self):
        self.terrain = None # Definie après avoir selectionné le niveau
        self.load_assets()
            
    def load_assets(self):
        # Charger les images et redimensionner
        self.virus_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/carte-mere.png"), (100, 100))
        self.virus_back_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/carte-mere-back.png"), (102, 102))
        self.vide_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/vide.png"), (100, 100))
        self.Globule_Back_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/Globule_Back.png"), (102, 102))
        
        self.back_empty = pygame.transform.scale(pygame.image.load("./PygameAssets/BACK_EMPTY.png"), (1920, 1080))
        
        self.Globules = self.load_globules() #pour tout ce qui n'est pas cases_vide/virus/block_solid utilisé des texure de virus pareille de diferante couleur
        self.block = pygame.transform.scale(pygame.image.load("./PygameAssets/ai-cerveau.png"), (100, 100))

    def load_globules(self):
        # Avec les 6 images de globules je les ranges dans un dictionnaire en fesant une boucle for pour pas prendre trop de place
        globules = {}
        for x in range(1, 7):
            globule_path = f"./PygameAssets/Globule_{x}.png" # Nom des fichier numérotés de 1 à 6 Globule_1, 2 ...
            globule = pygame.image.load(globule_path)
            globules[x] = pygame.transform.scale(globule, (100, 100))
        return globules
    
    def draw(self, screen, selected, tab_index):
        screen.blit(self.back_empty, (0,0)) # Fond du menu mais en écarter pour laisser de la place pour le jeu

        for i in range(len(self.terrain)):
            for y in range(len(self.terrain[i])):
                # Le modulo 4 c'est car le terrain c'est une liste de liste qui alter de taille 4, 3, donc en fonction de si c'est 4 ou 3 ils sont placés differament
                if len(self.terrain[i]) % 4 != 0:
                    self.draw_element(screen, selected, tab_index, i, y, 770, 240)
                else:
                    self.draw_element(screen, selected, tab_index, i, y, 700, 240)
    
    def draw_element(self, screen, selected, tab_index, i, y, x, z):
        # Mettre un fond blanc derrière le globule/virus déplacable, de 2px plus grand donc je décale de 1 px d'ou le -1
        if selected[tab_index] == self.terrain[i][y]:
            if selected[tab_index] == "car":
                screen.blit(self.virus_back_agrandie, ((y * 140 + x -1), (i * 75 + z -1)))
            else:
                screen.blit(self.Globule_Back_agrandie, ((y * 140 + x -1), (i * 75 + z -1)))
        # Mettre image de case vide si il y a "x" en [i][y]
        if self.terrain[i][y] == "x":
            screen.blit(self.vide_agrandie, (y * 140 + x, i * 75 + z))
        # Mettre image de block_solid si il y a "0" en [i][y]
        elif self.terrain[i][y] == "0":
            screen.blit(self.block, (y * 140 + x, i * 75 + z))
        # Mettre image de virus si il y a "car" en [i][y]
        elif self.terrain[i][y] == "car":
            screen.blit(self.virus_agrandie, (y * 140 + x, i * 75 + z))
        else:
            # Pour la longueur du nombre de globule qui n'est pas le virus prendre une texture de globule
            for v in range(len(selected)):
                if selected[v] == self.terrain[i][y]:
                    screen.blit(self.Globules[v], (y * 140 + x, i * 75 + z))

# Classe Game pour gérer le jeu
class Game:
    def __init__(self):
        # Initialisation de variables
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.terrain = Terrain()
        self.running = True
        self.stop = 0
        self.tab = 0

        self.directionListe = 0

        # Initialisation du module de mixage (son)
        pygame.mixer.init()

        # Chargement des fichier audio (.wav)
        self.bloop1 = pygame.mixer.Sound('sounds/bloop1.wav')
        self.bloop2 = pygame.mixer.Sound('sounds/bloop2.wav')
        self.bloop3 = pygame.mixer.Sound('sounds/bloop3.wav')
        self.randBloop = [self.bloop1,self.bloop2,self.bloop3]

        backgroundSong = pygame.mixer.Sound('sounds/EdgeOfSanity.wav')
        backgroundSong.play(loops=50)

        self.stopTemps = 0
        self.startTemps = 0
        self.nbrCoup = 0

        self.otherPiece, self.alreadyTest = [], []

        self.allgood = False

        self.selected = {}

    def run(self):
        # Boucle principale 
        while self.running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if self.terrain.terrain is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.terrain.terrain[0][0] == "car" and self.terrain.terrain[1][0] == "car":
                        mouse_pos = event.pos
                        if self.rect.collidepoint(mouse_pos):
                            self.stop, self.stopTemps, self.startTemps, self.nbrCoup = 0, 0, 0, 0 #met le menu reset le temps et le nbr de coup
                            
            self.mettreajour_screen()
            pygame.display.flip()

    def mettreajour_screen(self):
        keys = pygame.key.get_pressed()
        self.screen.fill((0, 0, 0))

        # Si pas de niveau séléctionne afficher menu
        if self.stop == 0 or self.stop == 1 or self.stop == 3:
            self.stop, self.terrain.terrain = menu.afficher_menu(self.stop)
            if self.terrain.terrain is not None:
                self.selected = self.element_select()

        # Si niveau séléctionnne afficher terrain
        if self.stop == 2 and self.terrain.terrain is not None:

            if self.startTemps == 0:
                self.startTemps = time.time()

            self.mouvement(keys, self.selected, self.tab)
            self.terrain.draw(self.screen, self.selected, self.tab)

            # Si le virus est dans le coin en haut à gauche afficher "you win"
            if self.terrain.terrain[0][0] == "car" and self.terrain.terrain[1][0] == "car":
    
                self.endTemps = time.time()

                #  image de fond
                self.screen.blit(pygame.transform.scale(pygame.image.load("./PygameAssets/TableauScore.png"), (550, 600)), (1920//2 - 550/2, 1080//2 - 600/2))

                # écriture ta gagné
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textWin = self.font.render('GG', True, (173,216,230))
                self.text_rect = self.textWin.get_rect(center=(1920 // 2, 1080 // 2 - 200))
                self.screen.blit(self.textWin, self.text_rect)

                # écriture nbr de coup
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textCoup = self.font.render(f'Nombre de move : {self.nbrCoup}', True, (173,216,230))
                self.text_rect_Coup = self.textCoup.get_rect(center=(1920 // 2, 1080 // 2 - 50))
                self.screen.blit(self.textCoup, self.text_rect_Coup)

                # écriture temps
                if self.stopTemps == 0:
                    self.tempstotal = self.endTemps - self.startTemps
                    self.stopTemps += 1
                    if self.tempstotal > 60:
                        self.ecrieTempstotal = f"{self.tempstotal//60:.0f} min {self.tempstotal%60:.3f} sec"
                    else:
                        self.ecrieTempstotal = f"{self.tempstotal:.3f} sec"
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textTemps = self.font.render(f'Temps : {self.ecrieTempstotal}', True, (173,216,230))
                self.text_rect_Temsp = self.textTemps.get_rect(center=(1920 // 2, 1080 // 2 + 100))
                self.screen.blit(self.textTemps, self.text_rect_Temsp)

                # bouton menu
                self.screen.blit(pygame.image.load("./PygameAssets/Buttons/MENU.png"), (1920//2 - 218//2, 730))
                self.rect = pygame.image.load("./PygameAssets/Buttons/MENU.png").get_rect(topleft=(1920//2 - 218//2, 730))


    def element_select(self):
        '''
        Permet de séléctionner les élément qui sont bougable dans un dictionnaire, en fonction du niveau qui est choisis 
        ( parcour le terrain et vois si c'est differant de 0 et x (cases solid et vide))
        Variable qui sera utiliser pour séléctionner la "piece" qu'on veut bouger
        '''
        x = 1
        selected_index = {0: "car"}
        for i in range(len(self.terrain.terrain)):
            for y in range(len(self.terrain.terrain[i])):
                if self.terrain.terrain[i][y] not in ["x", "0", "car"] and self.terrain.terrain[i][y] not in selected_index.values():
                    selected_index[x] = self.terrain.terrain[i][y]
                    x += 1
        return selected_index

    def mouvement(self, keys, selected, tab):
        '''
        Pour chaque déplacement appele la fonction moveMolecule
        Pour tab juste change la variable tab
        Variable Good sert a faire que si j'appuie une fois sa compte comme 1 fois et pas itére plusieurs fois l'action
        '''
        if keys[pygame.K_a] and self.Good == True:
            self.directionListe = 0 
            self.allgood = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [-1, -1, -1, 0], 1)
            self.Good = False

        if keys[pygame.K_z] and self.Good == True:
            self.directionListe = 0
            self.allgood = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [-1, 0, -1, 1], 1)
            self.Good = False

        if keys[pygame.K_q] and self.Good == True:
            self.directionListe = -1
            self.allgood = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [1, -1, 1, 0], 1)
            self.Good = False

        if keys[pygame.K_s] and self.Good == True:
            self.directionListe = -1
            self.allgood = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [1, 0, 1, 1], 1)
            self.Good = False

        # Si aucun bouton est pressé Good = True donc une action peux être refaite
        if not any(keys):
            self.Good = True

        if keys[pygame.K_TAB] and self.Good == True:
            if len(selected) - 1 == tab:
                self.tab = 0
                self.Good = False
            else:
                self.tab += 1
                self.Good = False

    def moveMolecule(self, select, posxy_xy2, makeAmove = 0):
        '''
        select c'est pour savoir quel element bouger
        posxy_xy2[0], posxy_xy2[1] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x]
           [x, x, x ,x] on cherche a déplacer un element ici en haut ou en bas
            [x, x, x]
        posxy_xy2[2], posxy_xy2[3] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x, x]
              [x, x, x] on cherche a déplacer un element ici en haut ou en bas
            [x, x, x, x]
        directionListe c'est pour parcourir le terrain soit d'en haut si on vas en haut sinon d'en bas si on vers le bas (pour éviter un déplacement qui se répéte en boucle, j'ai pris du temps a trouvé ce probleme..)
        '''
        if self.allvalid(select, posxy_xy2): # Vérifie si le déplacement est possible

            if makeAmove == 1:
                self.randBloop[random.randint(-1,2)].play()
                self.nbrCoup += 1

            for w in range(0, len(self.terrain.terrain), 1) if self.directionListe == 0 else range(len(self.terrain.terrain) - 1, -1, -1): # Parcours le terrain de haut ou de bas en haut en fonction de z
                for q in range(len(self.terrain.terrain[w])):
                    if self.terrain.terrain[w][q] == select:
                        if len(self.terrain.terrain[w]) % 4 == 0:
                            self.terrain.terrain[w + posxy_xy2[0]][q + posxy_xy2[1]] = select
                            self.terrain.terrain[w][q] = "x"
                        else:
                            self.terrain.terrain[w + posxy_xy2[2]][q + posxy_xy2[3]] = select
                            self.terrain.terrain[w][q] = "x"

    def allvalid(self, select, posxy_xy2):
        '''
        Vérifie que pour chaque élément qui compose le globule il puisse se déplacer dans la direction voulue
        en fonction return True ou False
        '''
        p, v = 0, 0
        for m in range(len(self.terrain.terrain)):
            for n in range(len(self.terrain.terrain[m])):
                if self.terrain.terrain[m][n] == select:
                    # Vérifie les conditions de déplacement pour chaque élément en fonction de leur pose
                    if (len(self.terrain.terrain[m]) % 4 == 0 and self.isvalid(select, m + posxy_xy2[0], n + posxy_xy2[1])) or (len(self.terrain.terrain[m]) % 4 != 0 and self.isvalid(select, m + posxy_xy2[2], n + posxy_xy2[3])):
                        p += 1
                    v += 1

        if p == v:
            if self.poussageRecursife(select, posxy_xy2):
                return True
        else:
            self.allgood = False

        return False
    
    def isvalid(self, select, x, y):
        # Vérifie si l'élément peux aller vers la direction souhaité (si il dépasse pas de la map et ne fonce pas dans autre chose)
        if len(self.terrain.terrain) > x > -1 and len(self.terrain.terrain[x]) > y > -1:
            # Permet de voir si l'élément après est dans selected (élément bougable) pour le bouger et le bouger si possible
            if self.terrain.terrain[x][y] in self.selected.values() and self.terrain.terrain[x][y] != select and self.terrain.terrain[x][y] not in self.otherPiece:
                self.otherPiece.append(self.terrain.terrain[x][y]) 
            # vérifie si il peux se déplacer
            if self.terrain.terrain[x][y] == "x" or self.terrain.terrain[x][y] in self.selected.values():
                    return True
        return False

    def poussageRecursife(self, select, posxy_xy2):    
        self.alreadyTest.append(select)
        if self.alreadyTest != self.otherPiece:
            for molecule in self.otherPiece:
                # Appeler moveMolecule uniquement si nécessaire
                if molecule not in self.alreadyTest:
                    self.alreadyTest.append(molecule)
                    self.moveMolecule(molecule, posxy_xy2)
                
        if self.allgood:
            return True
        else: 
            return False
# Initialiser et lancer le jeu
game = Game()
game.run()

pygame.quit()
