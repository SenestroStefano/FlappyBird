# sudo pip install pygame
import oggetti # importo il file oggetti.py che riporta 2 classi
import pygame, random
from pygame import mixer

pygame.init()

# Valori di proporzionalità
MULT = 2 # rapporto di proporzione allo schermo NON INFERIORE AD 1
DELTA_TIME = 1 # Delta_Time (Congliabile 1/2 MAX 3) serve per avere una proporzione di frame pari a quella ideata inizialmente, usata sopratutto nelle animazioni
FPS = 60 * DELTA_TIME # Frame per second
VEL_AVANZ = 3 * MULT / DELTA_TIME # Velocità dello sfondo

#SCREEN
TITLE = "Flappy Bird"
SCREEN_width, SCREEN_height = 288 * MULT, 512 * MULT
SCREEN = pygame.display.set_mode((SCREEN_width,SCREEN_height))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)	# indica se il cursore è visibile a schermo

#immagini
uccello = pygame.image.load('immagini/uccello.png').convert_alpha()
gameover = pygame.image.load('immagini/gameover.png').convert_alpha()

pygame.display.set_icon(uccello) # imposta come icona di finestra flappy

sfondo = pygame.image.load('immagini/sfondo.png').convert()
base = pygame.image.load('immagini/base.png').convert()
tubo_giu = pygame.image.load('immagini/tubo.png').convert()
tubo_su = pygame.transform.flip(tubo_giu, False, True)

#Scale
# ottengo la largezza e altezza effetiva dell'immagine e la moltiplico in proporzione allo schermo
sfondo = pygame.transform.scale(sfondo, (sfondo.get_width() * MULT, sfondo.get_height() * MULT))
uccello = pygame.transform.scale(uccello, (uccello.get_width() * MULT, uccello.get_height() * MULT))
base = pygame.transform.scale(base, (base.get_width() * MULT, base.get_height() * MULT))
gameover = pygame.transform.scale(gameover, (gameover.get_width() * MULT, gameover.get_height() * MULT))
tubo_giu = pygame.transform.scale(tubo_giu, (tubo_giu.get_width() * MULT, tubo_giu.get_height() * MULT))
tubo_su = pygame.transform.scale(tubo_su, (tubo_su.get_width() * MULT, tubo_su.get_height() * MULT))

#Grandezze
uccello_width = uccello.get_width()
uccello_height = uccello.get_height()

tubo_height = tubo_giu.get_height()
tubo_width = tubo_giu.get_width()

tubo_width = tubo_giu.get_width()
tubo_height = tubo_giu.get_height()

#SUONI
gameover_sound = mixer.Sound("suoni/ulose.wav")
jump_sound = mixer.Sound("suoni/jump.wav")
record_sound = mixer.Sound("suoni/newRecord.wav")

#Funzioni

# Variabili di default
def inizializza():
	global uccellox, uccelloy, uccello_vely, uccelloy_default
	global inizia, run, contatore_flip
	global basex, basey, pavimento
	global tubo1, tubo2, tubo3, tubo4
	global contatore, r_contatore
	global distanza

	contatore = 0
	distanza = 100	# dIstanza trai i due tubi
	uccellox, uccelloy = 60 * MULT, 150 * MULT
	uccello_vely = 0 * MULT
	uccelloy_default = uccelloy
	basex = 0 * MULT
	basey = 400 * MULT
	inizia = False
	run = True
	contatore_flip = True

	pavimento = oggetti.Base((basex, basey),VEL_AVANZ, MULT)

	tubo1 = oggetti.Tubo(uccello,1,distanza,(uccellox,uccelloy),tubo_width,tubo_height,VEL_AVANZ, (SCREEN_width,SCREEN_height),MULT)
	tubo2 = oggetti.Tubo(uccello,1.5,distanza,(uccellox,uccelloy),tubo_width,tubo_height,VEL_AVANZ,(SCREEN_width,SCREEN_height),MULT)
	tubo3 = oggetti.Tubo(uccello,2,distanza,(uccellox,uccelloy),tubo_width,tubo_height,VEL_AVANZ, (SCREEN_width,SCREEN_height),MULT)
	tubo4 = oggetti.Tubo(uccello,2.5,distanza,(uccellox,uccelloy),tubo_width,tubo_height,VEL_AVANZ, (SCREEN_width,SCREEN_height),MULT)

	# Imposto una musica di background
	mixer.music.load("suoni/background_music.wav")
	mixer.music.play(-1)	# La setto a -1 che indica un loop quindi a infinito

	# Apre il file score.txt in modalità lettura
	with open('score.txt', 'r') as f:
		f_contest = f.readlines()	# legge le linee del file di testo e ti riporta una lista
		r_contatore = f_contest[1]	# imposto il valore della riga 2 a r_contantore
	f.close()	# chiudo il file per evitare problemi di lag


# Disegna a schermo
def disegna_oggetti():
    
	SCREEN.blit(sfondo, (0,0))	# prima disegno lo sfondo
	SCREEN.blit(uccello, (uccellox,uccelloy))	# poi il giocatore

	# e poi i vari tubi
	SCREEN.blit(tubo_su, (tubo1.x,tubo1.y))
	SCREEN.blit(tubo_giu, (tubo1.x,tubo1.height+tubo1.y+distanza * MULT))

	SCREEN.blit(tubo_su, (tubo2.x,tubo2.y))
	SCREEN.blit(tubo_giu, (tubo2.x,tubo2.height+tubo2.y+distanza * MULT))

	SCREEN.blit(tubo_su, (tubo3.x,tubo3.y))
	SCREEN.blit(tubo_giu, (tubo3.x,tubo3.height+tubo3.y+distanza * MULT))

	SCREEN.blit(tubo_su, (tubo4.x,tubo4.y))
	SCREEN.blit(tubo_giu, (tubo4.x,tubo4.height+tubo4.y+distanza * MULT))

	# e infine la base
	SCREEN.blit(base, (pavimento.x,pavimento.y))

# Aggiorna lo schermo
def aggiorna():
	pygame.display.flip()
	pygame.display.update()	# SERVE PER AGGIORNARE IL DISPLAY
	pygame.time.Clock().tick(FPS)	# INDICA A QUANTE VOLTE DEVE ESSERE AGGIORNATO
	
# Funzione che imposta una text
def set_text(string, coordx, coordy, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)  # serve per indicare il tipo di font e la grandezza
    text = font.render(string, True, (255, 255, 255)) 	# imposta il testo, la visibilità e il colore
    textRect = (coordx, coordy)	# imposto le cordinate
    return (text, textRect) # ritorna il testo e la posizione

# Funzione di game over
def haiperso():
    	
	mixer.music.stop()	# per fermare la musica di background
	gameover_sound.play()	# avvia il suono di game_over
	
	SCREEN.blit(gameover,(SCREEN_width/2-gameover.get_width()/2, 180 * MULT))

	ricominciamo = False
	
	while not ricominciamo:
		
		for event_pausa in pygame.event.get():
			
			keys_pressed = pygame.key.get_pressed()

			if keys_pressed[pygame.K_SPACE]:
				inizializza()	# mi riapplica le variabili di default quindi è come se riavviassi il gioco
				ricominciamo = True

			if event_pausa.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
				pygame.quit()

		aggiorna()


inizializza()

# MAIN PRINCIPALE
while run:
	
	uccello_vely += 1 * MULT / DELTA_TIME	# setto la velcità del flappy
	uccelloy += uccello_vely	# imposto le cordinate di y del flappy alla velocità indicata in precendeza

	# passo la posizione del giocatore al metodo della classe per fare poi gli eventuali confronti
	tubo1.setPlayerPosition(uccellox,uccelloy)
	tubo2.setPlayerPosition(uccellox,uccelloy)
	tubo3.setPlayerPosition(uccellox,uccelloy)
	tubo4.setPlayerPosition(uccellox,uccelloy)
	pavimento.update()

	# Funzionalità che serve ad aspettare che l'utente clicchi un pulsante prima di avviare il gioco
	if  not inizia:
		
		# Se la corrente posizione di flappy rimane minore o uguale a quella originaria allora:
		if uccelloy >=uccelloy_default+random.randint(10, 90):			
			uccello_vely = -(random.randint(10, 15) * MULT / DELTA_TIME)	# faccio alzare flappy
	
	else:
		
		# Metodo che va ad aggiornare la posizione dei vari tubi
		tubo1.update()
		tubo2.update()
		tubo3.update()
		tubo4.update()

	for event in pygame.event.get():
		
		keys_pressed = pygame.key.get_pressed()	# imposto una variabile key, in modo da non indicarla ogni volta

		if keys_pressed[pygame.K_UP]:
			
			if not inizia:
				inizia = True

			uccello_vely = -10  * MULT / DELTA_TIME	# faccio alzare flappy

		if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
			run = False	# se clicco il pulsante di uscita oppure clicco ESC setta run come False e pertanto mi fa uscire

	# se la posizione del flappy è uguale a quella del tubo, allora incrementa il contatore (score)
		
	if uccellox == tubo1.x or uccellox == tubo2.x or uccellox == tubo3.x or uccellox == tubo4.x:
		contatore += 1

		#RECORD
		# Controllo se il secondo valore della riga 2 di 'score.txt' è minore di contatore
		if int(r_contatore) < contatore:
				
			# Questa if mi permette di produrre un suono solo e unicamente quando viene superato il record 1 volta
			if contatore_flip:
				record_sound.play()
				contatore_flip = False
			
			# Apri il file in modalita scrittura
			with open('score.txt', 'w') as f:
				f.write("Record:\n")
				f.write(str(contatore))
			f.close()

			# Apri il file in modalita lettura
			with open('score.txt', 'r') as f:
				f_contest = f.readlines()
				r_contatore = f_contest[1]
			f.close()
	
	#COLLISIONI
	# controllo le varie collisioni col giocatore e i tubi e controllo anche la sua altezza (pertanto se è troppo basso o è troppo alto)
	if tubo1.checkCollision() or tubo2.checkCollision() or tubo3.checkCollision() or tubo4.checkCollision() or (uccelloy >= (SCREEN_height - base.get_height() - uccello_height) or uccelloy <= 0):
		haiperso()

	disegna_oggetti()	# disegno i vari elementi a schermo

	if inizia:
		# imposto una text visibile a schermo tramite la funzione di set_text()
		score = set_text(str(contatore), SCREEN_width/2, 40*MULT, 30*MULT) # parametri: (stringa, posX, posY, GrandezzaFont)
		record = set_text(("Record: "+str(r_contatore)), 20*MULT, 10*MULT, 10*MULT) # parametri: (stringa, posX, posY, GrandezzaFont)

		# stampo a schermo le text
		SCREEN.blit(score[0], score[1])	# (Testo, (posX, posY)) 
		SCREEN.blit(record[0], record[1])	# (Testo, (posX, posY)) 

	aggiorna()	# aggiorno lo schermo

# ESCI DA PYGAME
pygame.quit()