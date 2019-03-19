import pygame, sys

#initialisation de pygame
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)


#Initialisation des differentes musiques du menu:
musique_pause = pygame.mixer.Sound("sons\Pause_On.wav")
musique_survol = pygame.mixer.Sound("sons\Pause_Bouton.wav")
musique_continue = pygame.mixer.Sound("sons\\Continue_Click.wav")
musique_retry = pygame.mixer.Sound("sons\\Retry_Click.wav")
musique_quit = pygame.mixer.Sound("sons\\Quit_Click.wav")


#Variables utiles dans les fonctions
NULL, zone, glow=0, 0, 0
RUNNING, PAUSE = 0, 1
survol=[0,0]


#Definition d'une classe "bouton" pour les images des boutons du menu
class bouton:
    x=NULL
    y=NULL
    image=NULL



#AFFICHAGE########################################################################
#Fonction d'affichage du menu
def pause(fenetre, musique):
    global glow
    fenetre.fill((0,0,0))   #fond noir

 #son ouverture du menu SSI: menu n'était pas déja ouvert (musique=1 lors de l'ouverture du menu et 0 a la sortie)
    if musique==0:
        musique_pause.play()

 #affichage bouton "continue"
    bouton_select=bouton()
    if glow == 1:
        bouton_select.image = pygame.image.load("images\\continue_glow.jpg").convert_alpha()
    else:
        bouton_select.image = pygame.image.load("images\\continue.jpg").convert()
    bouton_select.image = pygame.transform.scale(bouton_select.image, (240, 95))
    bouton_select.x, bouton_select.y=30, 10
    fenetre.blit(bouton_select.image, (bouton_select.x, bouton_select.y))

 #affichage bouton "retry"
    bouton_retry=bouton()
    if glow == 2:
        bouton_retry.image = pygame.image.load("images\\retry_glow.jpg").convert_alpha()
    else:
        bouton_retry.image = pygame.image.load("images\\retry.jpg").convert()
    bouton_retry.image = pygame.transform.scale(bouton_retry.image, (240, 95))
    bouton_retry.x, bouton_retry.y=30, 105
    fenetre.blit(bouton_retry.image, (bouton_retry.x, bouton_retry.y))

 #affichage bouton "quit"
    bouton_quit=bouton()
    if glow == 3:
        bouton_quit.image = pygame.image.load("images\\quit_glow.jpg").convert_alpha()
    else:
        bouton_quit.image = pygame.image.load("images\\quit.jpg").convert()
    bouton_quit.image = pygame.transform.scale(bouton_quit.image, (240, 95))
    bouton_quit.x, bouton_quit.y=30, 200
    fenetre.blit(bouton_quit.image, (bouton_quit.x, bouton_quit.y))

#ALGO CHANTIER: adaptation de la taille des boutons en fonction de la taille de la fenetre
'''
def pause(fenetre, stop):

    bouton_select=bouton()
    if stop > 1:
        bouton_select.image = pygame.image.load("images\\continue.jpg").convert()
        resize(bouton_select.image)

    bouton_select.x, bouton_select.y=30, 30
    fenetre.blit(bouton_select.image, (bouton_select.x, bouton_select.y))


def resize(image):

    scale_x=300/1920
    scale_y=300/1080

    size_x= int((pygame.Surface.get_width(image))*scale_x)
    size_y= int((pygame.Surface.get_height(image))*scale_y)

    print(size_x, "    &     ", size_y)

    size_x=int(size_x*scale_x)
    size_y=int(size_y*scale_y)

    print(size_x, "    &     ", size_y)

    image = pygame.transform.scale(image, (size_x, size_y))
'''


#DEPLACEMENTS######################################################################
#Gestion des clicks
def click(e, state):
    global zone

    if e.type == pygame.MOUSEBUTTONDOWN and state==PAUSE:
        if e.pos[1]<100 and e.button==1:
            #Reprendre la partie
            state=continuer(state)
            return state
        elif e.pos[1]>=100 and e.pos[1]<200 and e.button==1:
            #Recommencer une partie
            retry()
            return state
        elif e.pos[1]>=200 and e.button==1:
            #Quitter le jeu (vers un menu principal ?)
            quit()
        else:
            return state

    if e.type == pygame.KEYDOWN and state==PAUSE:
        if zone==1:
            #Reprendre la partie
            state=continuer(state)
            return state
        elif zone==2:
            #Recommencer une partie
            retry()
            return state
        elif zone==3:
            #Quitter le jeu (vers un menu principal ?)
            quit()
        else:
            return state




#Gestion déplacement menu via touches
def menu_touches(e, state, fenetre):
    global glow, zone

    if glow == 0:
        if e.key == pygame.K_UP and state==PAUSE:
            zone=1
        if e.key == pygame.K_DOWN and state==PAUSE:
            zone=3

    else:
        if e.key == pygame.K_UP and state==PAUSE:
            zone-=1
            if zone<1:
                zone=3
        if e.key == pygame.K_DOWN and state==PAUSE:
            zone+=1
            if zone>3:
                zone=1

    curseur(e, state, fenetre)


#Gestion du cruseur
def curseur(e, state, fenetre):
    global glow, zone

    if zone!=0 and e.type == pygame.KEYDOWN:
        if zone==1:
           print("Continue en surbrillance") #test
           glow=1
           survol[1]=1
           if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()
        if zone==2:
            print("Retry en surbrillance") #test
            glow=2
            survol[1]=2
            if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()
        if zone==3:
            print("Quit en surbrillance") #test
            glow=3
            survol[1]=3
            if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()


    elif e.type == pygame.MOUSEMOTION and state==PAUSE and zone>=0:
        if e.pos[1]<100:
           print("Continue en surbrillance") #test
           glow, zone=1, 1
           survol[1]=1
           if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()
        if e.pos[1]>=100 and e.pos[1]<200:
            print("Retry en surbrillance") #test
            glow, zone=2, 2
            survol[1]=2
            if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()
        if e.pos[1]>=200:
            print("Quit en surbrillance") #test
            glow, zone=3, 3
            survol[1]=3
            if survol[1]!=survol[0]:
                survol[0]=survol[1]
                musique_survol.play()



#FONCTIONS DES ACTIONS DES BOUTONS
def continuer(state):
    global glow
    glow=0
    musique_continue.play()
    print("continue") #test programme
    return state==RUNNING

def retry():
    global glow
    glow=0
    #Dépend du programme
    musique_retry.play()
    print("retry")  #test programme

def quit():
    #Retour au menu principal + tard
    musique_quit.play()
    print("quit")  #test programme
    sys.exit()



