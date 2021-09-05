from graphics import *
from keyboard import *
def create_win():
    win = GraphWin("Game Window", 700, 700, autoflush=False)
    return win
class Basics:
    def __init__(self, win):
        self.win = win
    def get_centro(self):
        return Point(self.win.getWidth() / 2, self.win.getHeight() / 2)
    def create_room(self, wall, peaks_off_on, p1, fire_sala2):
        fire_sala2.draw(self.win)
        wall.draw(self.win)
        peaks_off_on[1].draw(self.win)
        p1.draw(self.win)
        """back_ground = Image(self.get_centro(), "src/bg_image chao rio.png")
        back_ground.draw(self.win)"""
    def frequency_traps(self, traps, freq):
        if freq%2 == 0:
            traps[1].draw(self.win)
            traps[0].undraw()
            return True
        traps[1].undraw()
        traps[0].draw(self.win)
        return False


    def get_char_points(self, p1):
        x = p1.getAnchor().getX()
        y = p1.getAnchor().getY() + p1.getHeight()/2
        ponto_left, ponto_right = Point(x - p1.getWidth()//2,y), Point(x + p1.getWidth()//2, y)
        return ponto_left, ponto_right

    def movimento(self, p1, wall, estrutura, peaks_off_on, onOff, nivel, fire_1, fire_1_estrut, movi_fogo, dialog, porta_sala_2, test_porta):
        color_wall = [255, 0, 118] # Rosa
        color_dead = [255,0,0] # Vermelho
        color_next_level = [0, 255, 11] # Verde
        passos = 3 # Velocidade
        ponto_left, ponto_right = self.get_char_points(p1)
        x1, y1 = int(ponto_left.getX()) + 700*nivel, int(ponto_left.getY())         # Pego dois pontos, a esquerda e a direita
        x2, y2 = int(ponto_right.getX()) + 700*nivel, int(ponto_right.getY())       # do personagem, esses são os pés
        if p1.getAnchor().getX() >=524 and p1.getAnchor().getX() <= 542 and p1.getAnchor().getY() <= 142 and test_porta and nivel == 1: # Portao abre
            print(p1.getAnchor().getY())
            porta_sala_2[0].undraw()
            porta_sala_2[1].undraw()
            test_porta = False
        if p1.getAnchor().getX() >=602 and p1.getAnchor().getY() >= 640: # Inseri uma caixa de dialogo
            dialog = self.dialog_box(nivel, dialog)
        else: # Remove a caixa de dialogo quando o personagem sai
            if dialog[0] == 0:
                dialog = (2, dialog[1], dialog[2])
                dialog = self.dialog_box(nivel, dialog)
        if  wall.getPixel(x2, y2) == color_next_level or wall.getPixel(x1, y1) == color_next_level: # Passando de nível
                wall.move(-700,0)
                peaks_off_on[0].move(-700,0 )
                peaks_off_on[1].move(-700,0 )
                p1.undraw()
                p1 = Image(Point(20,640), 'src/char_d.png')
                p1.draw(self.win)
                nivel += 1
                fire_1.move(-700,0)
                estrutura.move(-700,0)
                fire_1_estrut.move(-700,0)
                porta_sala_2[0].move(-700,0)
                porta_sala_2[1].move(-700,0)
                test_porta = True
        if wall.getPixel(x2, y2) == color_dead or  wall.getPixel(x1, y1) == color_dead or ((peaks_off_on[1].getPixel(x2,y2) != [0, 0, 0] or peaks_off_on[1].getPixel(x1, y1) != [0,0,0]) and onOff) or (fire_1.getPixel(x2 - movi_fogo*5,y2)== color_dead or fire_1.getPixel(x1 - movi_fogo*5, y1) == color_dead):
            p1, test_porta = self.dead(nivel, p1, porta_sala_2, test_porta) # se pisar no vermelho, Morre
        if is_pressed('c'): # Alguns testes para desenvolvimento
            print(wall.getPixel(x2, y2))
            print(p1.getAnchor())
        # O resto do código é para se mver quando é pressionado w, a, s ou d
        if is_pressed('d'):
            if not wall.getPixel(x2+3, y2) == color_wall and not ( porta_sala_2[0].getPixel(x2+3, y2) == color_wall and test_porta):
                loc = p1.getAnchor()
                p1.undraw()
                p1 = Image(loc, 'src/char_d.png')
                p1.draw(self.win)
                p1.move(passos, 0)
        if is_pressed('a') and not wall.getPixel(x1-3, y1) == color_wall and not ( porta_sala_2[0].getPixel(x1-3, y2) == color_wall and test_porta):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_a.png')
            p1.draw(self.win)
            p1.move(-passos, 0)
        if is_pressed('w') and not wall.getPixel(x2, y2-5) == color_wall and not wall.getPixel(x1, y1-3) == color_wall and not ( porta_sala_2[0].getPixel(x2, y2 - 5) == color_wall and test_porta):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_w.png')
            p1.draw(self.win)
            p1.move(0, -passos)
        if is_pressed('s') and not wall.getPixel(x2, y2+4) == color_wall and not wall.getPixel(x1, y1+3) == color_wall and not ( porta_sala_2[0].getPixel(x2, y2 + 3) == color_wall and test_porta):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_s.png')
            p1.draw(self.win)
            p1.move(0, passos)
        return p1, wall,peaks_off_on, nivel, dialog, test_porta

    def dead(self, nivel, p1, porta_sala_2, test_sala_2): # nivel: interações futuras
        if nivel == 1 and not test_sala_2:
            porta_sala_2[0].draw(self.win)
            porta_sala_2[1].draw(self.win)
        p1.undraw()
        p1 = Image(Point(20,640), 'src/char_d.png')
        p1.draw(self.win)
        return p1, True
    def dialog_box(self, nivel, test):
        nivel += 1
        if test[0] == 1:
            test[nivel].draw(self.win)
            return (0, test[1], test[2])
        if test[0] == 0:
            return (0, test[1], test[2])
        else:
            test[nivel].undraw()
            return (1, test[1], test[2])