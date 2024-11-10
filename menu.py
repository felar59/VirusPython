import pygame
pygame.init()

screen = pygame.display.set_mode((1920, 1080))

def afficher_menu(stop):
    terrains = [
        [["x", "x", "car", "d"], ["x", "x", "car"], ["x", "g", "g", "d"], ["x", "0", "x"], ["0", "x", "x", "x"], ["x", "x", "x"], ["x", "x", "x", "x"]], #Lvl 1
        [["x", "x", "x", "x"], ["x", "x", "x"], ["d", "x", "0", "v"], ["g", "g", "x"], ["d", "g", "car", "v"], ["d", "x", "car"], ["0", "x", "x", "v"]], #Lvl 2
        [["x", "x", "car", "x"], ["g", "0", "car"], ["g", "x", "x", "x"], ["g", "x", "d"], ["x", "x", "d", "x"], ["0", "x", "x"], ["x", "x", "x", "x"]], #Lvl 3
        [["x", "x", "x", "x"], ["x", "x", "x"], ["d", "x", "0", "v"], ["g", "x", "x"], ["d", "car", "v", "x"], ["x", "car", "g"], ["0", "x", "x", "x"]], #Lvl 4
        [["y", "w", "w", "x"], ["x", "x", "x"], ["y", "w", "u", "g"], ["u", "u", "g"], ["x", "x", "d", "d"], ["x", "car", "d"], ["x", "x", "car", "x"]], #Lvl 5
    ]
    # Chargement et affichage de l'arrière-plan
    image = pygame.image.load("./PygameAssets/bgLevelSelect.png")
    image_agrandie = pygame.transform.scale(image, (1920, 1080))
    screen.blit(image_agrandie, (0, 0))
    # Dictionnaire de dictionnaire pour stocker les boutons et leurs positions
    if stop == 0:
        boutons = {
            1: {"image": pygame.image.load("./PygameAssets/Buttons/NIVEAUX.png"), "position": (870, 450)},
            2: {"image": pygame.image.load("./PygameAssets/Buttons/RULES.png"), "position": (870, 520)},
        }
    elif stop == 1:
        boutons = {
            1: {"image": pygame.image.load("./PygameAssets/Buttons/STARTER.png"), "position": (750, 450)},
            2: {"image": pygame.image.load("./PygameAssets/Buttons/JUNIOR.png"), "position": (990, 450)},
            3: {"image": pygame.image.load("./PygameAssets/Buttons/EXPERT.png"), "position": (750, 520)},
            4: {"image": pygame.image.load("./PygameAssets/Buttons/MASTER.png"), "position": (990, 520)},
            5: {"image": pygame.image.load("./PygameAssets/Buttons/WIZARD.png"), "position": (1920//2 - 218//2, 590)},
            6: {"image": pygame.image.load("./PygameAssets/Buttons/MENU.png"), "position": (1920//2 - 218//2, 680)},
        }
    # Affichage de tous les boutons + gestion des événement pour définire le niveau
    for key, bouton in boutons.items():
        screen.blit(bouton["image"], bouton["position"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False  

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            for key, bouton in boutons.items():
                rect = bouton["image"].get_rect(topleft=bouton["position"])
                if rect.collidepoint(mouse_pos):

                    if stop == 0:
                        if key == 1:
                            stop = 1 # Change stop pour passer à la selection de niveau
                    elif stop == 1:
                        if key == 6:
                            stop = 0
                        else:
                            terrain = terrains[key - 1]  # Retourne le terrain sélectionné
                            print(terrain)
                            stop = 2  # Change stop pour passer au jeu
                            return stop, terrain

    return stop, None