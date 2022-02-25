# QUESTO E' IL PRIMO FILE VISTO IN CLASSE (NON VENGONO UTILIZZATE LE ClASSI)

# sudo pip install pygame

import pygame, random
from pygame import mixer

pygame.init()

# Valori di proporzionalità
MULT = 2 # rapporto di proporzione allo schermo NON INFERIORE AD 1
DELTA_TIME = 2 # Delta_Time (Congliabile 1/o numero un massimo che moltiplicato per i frame dia 120) serve per avere una proporzione di frame pari a quella ideata inizialmente, usata sopratutto nelle animazioni
FPS = 60 * DELTA_TIME # Frame per second
VEL_AVANZ = 3 * MULT / DELTA_TIME # Velocità dello sfondo

#immagini
sfondo = pygame.image.load('immagini/sfondo.png')
uccello = pygame.image.load('immagini/uccello.png')
base = pygame.image.load('immagini/base.png')
gameover = pygame.image.load('immagini/gameover.png')
tubo_giu = pygame.image.load('immagini/tubo.png')
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

contatore = 0

#SUONI
gameover_sound = mixer.Sound("suoni/ulose.wav")
jump_sound = mixer.Sound("suoni/jump.wav")
record_sound = mixer.Sound("suoni/newRecord.wav")

#SCREEN
TITLE = "Flappy Bird"
SCREEN_width, SCREEN_height = 288 * MULT, 512 * MULT
SCREEN = pygame.display.set_mode((SCREEN_width,SCREEN_height))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)	# indica se il cursore è visibile a schermo
pygame.display.set_icon(uccello) # imposta come icona di finestra flappy

#Funzioni

# Variabili di default
def inizializza():
	global uccellox, uccelloy, uccello_vely, uccelloy_default
	global inizia, run, contatore_flip
	global basex, basey
	global tuboX
	global tuboX1
	global tuboX2
	global tuboX3
	global contatore
	global distanza

	contatore = 0
	distanza = 100	# dIstanza trai i due tubi
	tuboX = SCREEN_width
	tuboX1 = SCREEN_width*1.5
	tuboX2 = SCREEN_width*2
	tuboX3 = SCREEN_width*2.5
	uccellox, uccelloy = 60 * MULT, 150 * MULT
	uccello_vely = 0 * MULT
	uccelloy_default = uccelloy
	basex = 0 * MULT
	basey = 400 * MULT
	inizia = False
	run = True
	contatore_flip = True

# Disegna a schermo
def disegna_oggetti():
	SCREEN.blit(sfondo, (0,0))
	SCREEN.blit(base, (basex,basey))
	SCREEN.blit(uccello, (uccellox,uccelloy))

# Aggiorna lo schermo
def aggiorna():
	pygame.display.update()
	pygame.time.Clock().tick(FPS)
	
# Funzione di game over
def haiperso():
    	
	mixer.music.stop()
	gameover_sound.play()
	
	SCREEN.blit(gameover,(SCREEN_width/2-gameover.get_width()/2, 180 * MULT))
	aggiorna()

	ricominciamo = False
	
	while not ricominciamo:
		
		for event_pausa in pygame.event.get():
			
			keys_pressed = pygame.key.get_pressed()

			if keys_pressed[pygame.K_SPACE]:
				inizializza()
				ricominciamo = True
				mixer.music.play(-1)
				f.close()

			if event_pausa.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
				pygame.quit()

# Funzione che imposta una text
def set_text(string, coordx, coordy, fontSize):

    font = pygame.font.Font('freesansbold.ttf', fontSize)  # serve per indicare il tipo di font e la grandezza
    text = font.render(string, True, (255, 255, 255)) 	# imposta il testo, la visibilità e il colore
    textRect = (coordx, coordy)	# imposto le cordinate
    return (text, textRect) # ritorna il testo e la posizione


inizializza()

# Apre il file score.txt in modalità lettura
with open('score.txt', 'r') as f:
	f_contest = f.readlines()	# legge le linee del file di testo e ti riporta una lista
	r_contatore = f_contest[1]	# imposto il valore della riga 2 a r_contantore
f.close()	# chiudo il file per evitare problemi di lag

# Imposto una musica di background
mixer.music.load("suoni/background_music.wav")
mixer.music.play(-1)	# La setto a -1 che indica un loop quindi a infinito

while run:
	
	uccello_vely += 1 * MULT / DELTA_TIME	# setto la velcità del flappy
	uccelloy += uccello_vely	# imposto le cordinate di y del flappy alla velocità indicata in precendeza

	# Funzionalità che serve ad aspettare che l'utente clicchi un pulsante prima di avviare il gioco
	if  not inizia:
		
		# SETTO LA POSIZIONE DI NASCITA DEGLI OGGETTI
		tuboX = SCREEN_width
		tuboX1 = tuboX * 1.5
		tuboX2 = tuboX * 2
		tuboX3 = tuboX * 2.5

		# Se la corrente posizione di flappy rimane minore o uguale a quella originaria allora:
		if uccelloy >=uccelloy_default+random.randint(10, 90):			
			uccello_vely = -(random.randint(10, 15) * MULT / DELTA_TIME)	# faccio alzare flappy

	for event in pygame.event.get():
		
		keys_pressed = pygame.key.get_pressed()	# imposto una variabile key, in modo da non indicarla ogni volta

		if keys_pressed[pygame.K_UP]:
			
			if not inizia:
    				
				inizia = True
				once1 = True
				once2 = True
				once3 = True
				once4 = True

			uccello_vely = -10  * MULT / DELTA_TIME	# faccio alzare flappy

		if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
			run = False	# se clicco il pulsante di uscita oppure clicco ESC setta run come False e pertanto mi fa uscire

	#VELOCITA' DEL BACKGROUND
	basex -= VEL_AVANZ

	tuboX -= VEL_AVANZ
	tuboX1 -= VEL_AVANZ
	tuboX2 -= VEL_AVANZ
	tuboX3 -= VEL_AVANZ


	#CONTROLLI DELLA POSIZIONE DEGLI OGGETTI
	if basex < -48 * MULT:
		basex = 0

	if tuboX < -SCREEN_width:
		tuboX = SCREEN_width
		once1 = True
	
	if tuboX1 < -SCREEN_width:
		tuboX1 = SCREEN_width
		once2 = True

	if tuboX2 < -SCREEN_width:
		tuboX2 = SCREEN_width
		once3 = True

	if tuboX3 < -SCREEN_width:
		tuboX3 = SCREEN_width
		once4 = True

	disegna_oggetti()

	# SETTO L'ALTEZZA RANDOMICA CHE DEVE AVERE OGNI TUBO
	if inizia:
			
		if once1:
			valore1 = random.randint(-200, -80) * MULT
			once1 = False
		
		if once2:
			valore2 = random.randint(-200, -80) * MULT
			once2 = False

		if once3:
			valore3 = random.randint(-200, -80) * MULT
			once3 = False

		if once4:
			valore4 = random.randint(-200, -80) * MULT
			once4 = False

		# TRAMITE QUESTO "once" MI PERMETTE DI FARLO UNA VOLTA A GENERAZIONE


		SCREEN.blit(tubo_su, (tuboX,valore1))	# IL TUBO SOPRA
		SCREEN.blit(tubo_giu, (tuboX,tubo_height+valore1+distanza * MULT)) # IL TUBO IN BASSO CHE CORRISPONDE ALLA SUA CORRENTE X (tuboX,tubo_height) + ALTEZZA + LA DISTANZA IMPOSTATA PRIMA

		SCREEN.blit(tubo_su, (tuboX1,valore2))	# IL TUBO SOPRA
		SCREEN.blit(tubo_giu, (tuboX1,tubo_height+valore2+distanza * MULT)) # IL TUBO IN BASSO CHE CORRISPONDE ALLA SUA CORRENTE X (tuboX,tubo_height) + ALTEZZA + LA DISTANZA IMPOSTATA PRIMA

		SCREEN.blit(tubo_su, (tuboX2,valore3))	# IL TUBO SOPRA
		SCREEN.blit(tubo_giu, (tuboX2,tubo_height+valore3+distanza * MULT)) # IL TUBO IN BASSO CHE CORRISPONDE ALLA SUA CORRENTE X (tuboX,tubo_height) + ALTEZZA + LA DISTANZA IMPOSTATA PRIMA

		SCREEN.blit(tubo_su, (tuboX3,valore4))	# IL TUBO SOPRA
		SCREEN.blit(tubo_giu, (tuboX3,tubo_height+valore4+distanza * MULT)) # IL TUBO IN BASSO CHE CORRISPONDE ALLA SUA CORRENTE X (tuboX,tubo_height) + ALTEZZA + LA DISTANZA IMPOSTATA PRIMA

		SCREEN.blit(base, (basex,basey)) # La base che mi serve per coprire i tubi inferiori
		
		
		#print("Pos y:"+str(uccelloy)+"| Pos Tubo alto: " +str(valore1+t)+"| Pos Tubo basso: "+str(t+valore1+120)+"| Zona safe: "+str((t+valore1+120)-(valore1+t)))
	
	#SCORE

	# se la posizione del flappy è uguale a quella del tubo, allora incrementa il contatore (score)
	if uccellox == tuboX or uccellox == tuboX1 or uccellox == tuboX2 or uccellox == tuboX3:
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

			with open('score.txt', 'r') as f:
				f_contest = f.readlines()
				r_contatore = f_contest[1]

			f.close()	# Chiude il file

		#print("Punteggio: "+str(contatore))

	if inizia:
		
		# imposto una text visibile a schermo tramite la funzione di set_text()
		score = set_text(str(contatore), SCREEN_width/2, 40*MULT, 30*MULT) # parametri: (stringa, posX, posY, GrandezzaFont)
		record = set_text(("Record: "+str(r_contatore)), 20*MULT, 10*MULT, 10*MULT) # parametri: (stringa, posX, posY, GrandezzaFont)

		SCREEN.blit(score[0], score[1])	# (Testo, (posX, posY)) 
		SCREEN.blit(record[0], record[1])	# (Testo, (posX, posY)) 

	#COLLISIONI
	d = distanza * MULT

	#controllo se flappy è sulla base o se è troppo alto
	if uccelloy >= (SCREEN_height - base.get_height() - uccello_height) or uccelloy <= 0:
		haiperso()

	# Se la posX di flappy <= punto destro della base del tubo e  la posX di flappy => punto sinistro della base del tubo e non (posY di flappy <= posY bassa della distanza e posY di flappy <= posY alta della distanza)
	if uccellox <= (tubo_width+tuboX) and uccellox >= tuboX-uccello_width and not (uccelloy <= (tubo_height+valore1+d-uccello_height) and uccelloy >= (valore1+tubo_height)):
		haiperso()

	# Se la posX di flappy <= punto destro della base del tubo e  la posX di flappy => punto sinistro della base del tubo e non (posY di flappy <= posY bassa della distanza e posY di flappy <= posY alta della distanza)	
	if uccellox <= (tubo_width+tuboX1) and uccellox >= tuboX1-uccello_width and not (uccelloy <= (tubo_height+valore2+d-uccello_height) and uccelloy >= (valore2+tubo_height)):
		haiperso()

	# Se la posX di flappy <= punto destro della base del tubo e  la posX di flappy => punto sinistro della base del tubo e non (posY di flappy <= posY bassa della distanza e posY di flappy <= posY alta della distanza)
	if uccellox <= (tubo_width+tuboX2) and uccellox >= tuboX2-uccello_width and not (uccelloy <= (tubo_height+valore3+d-uccello_height) and uccelloy >= (valore3+tubo_height)):
		haiperso()

	# Se la posX di flappy <= punto destro della base del tubo e  la posX di flappy => punto sinistro della base del tubo e non (posY di flappy <= posY bassa della distanza e posY di flappy <= posY alta della distanza)
	if uccellox <= (tubo_width+tuboX3) and uccellox >= tuboX3-uccello_width and not (uccelloy <= (tubo_height+valore4+d-uccello_height) and uccelloy >= (valore4+tubo_height)):
		haiperso()

		#print("| Valore 1: "+str(valore1)+"| Valore 2: "+str(valore2)+"| Valore 3: "+str(valore3)+"| Valore 4: "+str(valore4))

	aggiorna()

# ESCI DA PYGAME
pygame.quit()