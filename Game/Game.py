from graphics import *
from basics import *
# assets from 
# https://pixel-boy.itch.io/
# https://twitter.com/pixel_poem
# Meta do dia 28/08 - Colocar armadilhas spikes
# Meta 29/08 - Foguinho
# Meta 30/08 - Colocar caixa de diálogo
def main():
    nivel = 0    #Qual sala está
    win = create_win() # Cria a janela
    basics = Basics(win) # Chama as funções básicas
    centroY = basics.get_centro().getY()
    fogo_sala2 = Image(Point(700, centroY ), 'src/fogo_sala2.png')
    dialogos = (1, Image(Point(700,350), 'src/Caixa_dialogo_sala1.png'), Image(Point(700,350), 'src/Caixa_dialogo_sala2.png'))
    fogo_sala2_estrutura = Image(Point(700, centroY ), 'src/fogo_sala2_estrutura.png')
    wall = Image(Point(700, centroY), 'src/paredes.png') # Cria as paredes e armadilhas estáticas
    peaks_off_on = (Image(Point(700, centroY), 'src/peaks_off.png'), Image(Point(700, centroY), 'src/peaks_on.png')) # Cria e desenha as armadilhas dinamicas

    p1 = Image(Point(620, 40), 'src/char_s.png') # Cria o player 1

    basics.create_room(wall, peaks_off_on, p1, fogo_sala2) # Desenha as salas
    fogo_sala2_estrutura.draw(win)
    estrutura = Image(Point(700, centroY), 'src/estrutura.png') # Desenhos bonitinhos
    estrutura.draw(win)
    porta_sala_2 = (Image(Point(700,centroY), 'src/porta_sala_2.png'), Image(Point(700,centroY), 'src/porta_sala_2_estrut.png'))
    porta_sala_2[0].draw(win)
    porta_sala_2[1].draw(win)
    test_porta = True
    temporizador = 0
    text_tempo = Text(Point(10,10), temporizador)
    text_tempo.draw(win)
    count = 0 # Controlador do tempo e frequencia das armadilhas dinamicas
    onOff = True
    i = 0
    while not (win.isClosed()):
        p1, wall, peaks_off_on, nivel, dialogos, test_porta= basics.movimento(p1, wall, estrutura, peaks_off_on, onOff, nivel, fogo_sala2, fogo_sala2_estrutura, i, dialogos, porta_sala_2, test_porta) # Se move e interagem com varias coisas ( morre, aparec dialogos )
        count +=1
        if count%30 == 0: # Mostra o tempo e controla a frequencia das armadilhas dinamicas
            temporizador += 1
            onOff = basics.frequency_traps(peaks_off_on, temporizador)
            text_tempo.undraw()
            text_tempo = Text(Point(10,10), temporizador)
            text_tempo.draw(win)
        if nivel == 1:
            i += 1 # Controla o movimento do fogo
            fogo_sala2.move(5,0)
            fogo_sala2_estrutura.move(5,0)
            if fogo_sala2.getAnchor().getX() == 175:
                i = 0
                fogo_sala2.move(-175,0)
                fogo_sala2_estrutura.move(-175,0)        
        update(30)
    win.close()
main()