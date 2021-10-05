'''
Não mexa nesse arquivo, apenas execute o arquivo jogo.py
Obrigado!
'''
from math import *
from graphics import *
from keyboard import *
class Basics:
    def __init__(self, win):
        self.win = win
    def create_p1(self):
        return Image(Point(16*3,256-16*3), 'src/char_d.png')
    def redraw_p1(self, p1, point):
        p1.undraw()
        p1 = Image(point, 'src/char_d.png')
        p1.draw(self.win)
        return p1
    def redraw_inimigo(self, inimigo):
        try:
            inimigo.undraw()
            inimigo = Image(Point(32 + 256/2,256/2), 'src/inimigos.png')
            inimigo.draw(self.win)
            return inimigo
        except:
            return inimigo
    def create_all_room(self):
        p1 = self.create_p1()
        chao = Image(Point(256*5/2,256/2), 'src/chao.png')
        enfeites = Image(Point(256*5/2,256/2), 'src/enfeites.png')
        fogo = Image(Point(256*5/2,256/2), 'src/fogo.png')
        paredes = Image(Point(256*5/2,256/2), 'src/paredes.png')
        peaks_off = Image(Point(256*5/2,256/2), 'src/peaks_off.png')
        peaks_on = Image(Point(256*5/2,256/2), 'src/peaks_on.png')
        portas = Image(Point(256*5/2,256/2), 'src/portas.png')
        moedas_chaves = Image(Point(256*5/2,256/2), 'src/moedas_chaves.png')
        chao.draw(self.win)
        paredes.draw(self.win)
        peaks_on.draw(self.win)
        peaks_off.draw(self.win)
        portas.draw(self.win)
        fogo.draw(self.win)
        enfeites.draw(self.win)
        p1.draw(self.win)
        moedas_chaves.draw(self.win)
        return p1, chao, enfeites, fogo, paredes, peaks_off, peaks_on, portas, moedas_chaves
    def texto_nivel0(self, nivel):
        
        if nivel == 0:
            texto = Image(Point(256/2,256/2), 'src/nivel0_text.png')
            texto.draw(self.win)
            self.win.getMouse()
            texto.undraw()
    def text_nivel_2(self, nivel, p1_center, bala):
        if not bala:
            x, y, centro = p1_center.getX(), p1_center.getY(), 256/2
            if nivel == 2 and (x > centro - 10 and x < centro + 10 and y > centro - 10 and y < centro + 10) and not bala:
                texto = Image(Point(256/2,256/2), 'src/nivel2_text.png')
                texto.draw(self.win)
                self.win.getMouse()
                texto.undraw()
                return True
            return bala
        return bala
    def get_sensores(self, p1, nivel):
        x = int(p1.getAnchor().getX() + 256*nivel)
        y = int(p1.getAnchor().getY() + p1.getHeight()/2)
        esquerda_baixo = (x - p1.getWidth()//2 + 4, y)
        esquerda_cima = (x - p1.getWidth()//2 + 4,y - 7)
        direita_baixo = (x + p1.getWidth()//2 - 4, y)
        direita_cima = (x + p1.getWidth()//2 - 4, y- 7)
        return esquerda_baixo, esquerda_cima, direita_baixo, direita_cima
    def next_level(self, moedas_count, nivel, p1, moeda_chave, moeda_chave_test, portas,*elements):
        nivel +=1
        for item in elements:
            item.move(-256,0)
        p1 = self.redraw_p1(p1, Point(16*3,256-16*3))
        x = self.redraw_moeda_key(moedas_count, moeda_chave, moeda_chave_test, portas)
        return nivel, p1, True
    def peaks_on(self, peak_test, peaks, tempo):
        if tempo%30==0:
            if tempo%60 == 0:
                peaks.draw(self.win)
                return not peak_test
            else:
                peaks.undraw()
                return not peak_test
        return peak_test
    def move_fire(self, fogo, nivel, control):
        if nivel == 0:
            if fogo.getAnchor().getX() == 814:
                fogo.move(640 - 814, 0)
                return fogo, 0
            fogo.move(3, 0)
            return fogo, control + 1
        return fogo, 0
    def moeda_chave_gotcha(self, moedas_chaves, moedas_chaves_test, portas, p1, nivel, moedas_count):
        if moedas_chaves_test:
            x = p1.getAnchor().getX()
            y = p1.getAnchor().getY()
            if nivel == 0:
                if x > 110 and x < 130 and y < 100 and y > 75:
                    moedas_chaves.undraw()
                    return False, moedas_count + 1
            if nivel == 1:
                if x > 87 and x < 114 and y <= 136 and y >= 130:
                    moedas_chaves.undraw()
                    portas.undraw()
                    return False, moedas_count + 1
        return moedas_chaves_test,moedas_count
    def redraw_moeda_key(self, moedas_count, moeda_chave, moeda_chave_test, portas):
        if not moeda_chave_test:
                moeda_chave.draw(self.win)  
                try:
                    portas.draw(self.win)
                    return moedas_count - 1
                except:
                    return moedas_count - 1
        return moedas_count
    def teletransporte(self, nivel, nivel_desejado, p1, pontoi, pontof, point, qtd_teletransporte):
        if nivel == nivel_desejado:
            if p1.getAnchor().getX() > pontoi[0] and p1.getAnchor().getY() > pontoi[1] and p1.getAnchor().getX() < pontof[0] and p1.getAnchor().getY() < pontof[1]:
                return self.redraw_p1(p1, point), qtd_teletransporte + 1
        return p1, qtd_teletransporte
    def trap_check_dead(self, moedas_count, count_mortes, p1, tempo, peak_off, peak_on, peaks_test, fogo, controlador_fogo, moeda_chave, moeda_chave_test, portas, esquerda_baixo, esquerda_cima, direita_baixo, direita_cima):
        peak_on = peak_on.getPixel(esquerda_baixo[0], esquerda_baixo[1]) != [0,0,0] or peak_on.getPixel(esquerda_cima[0], esquerda_cima[1]) != [0,0,0] or peak_on.getPixel(direita_baixo[0], direita_baixo[1]) != [0,0,0] or peak_on.getPixel(direita_cima[0], direita_cima[1]) != [0,0,0]
        peak_off = peak_off.getPixel(esquerda_baixo[0], esquerda_baixo[1]) != [0,0,0] or peak_off.getPixel(esquerda_cima[0], esquerda_cima[1]) != [0,0,0] or peak_off.getPixel(direita_baixo[0], direita_baixo[1]) != [0,0,0] or peak_off.getPixel(direita_cima[0], direita_cima[1])!= [0,0,0]
        deslocamento_fogo = int(controlador_fogo*3)
        try:
            fogo = fogo.getPixel(esquerda_baixo[0] - deslocamento_fogo, esquerda_baixo[1]) != [0,0,0] or fogo.getPixel(esquerda_cima[0] - deslocamento_fogo, esquerda_cima[1]) != [0,0,0] or fogo.getPixel(direita_baixo[0] - deslocamento_fogo, direita_baixo[1]) != [0,0,0] or fogo.getPixel(direita_cima[0] - deslocamento_fogo, direita_cima[1])!= [0,0,0]
        except:
            fogo = False
        if (peak_on and peak_off and not peaks_test) or (peak_on and not peak_off) or fogo:
            moedas_count = self.redraw_moeda_key(moedas_count, moeda_chave, moeda_chave_test, portas)
            p1 = self.redraw_p1(p1, Point(16*3,256-16*3))
            return count_mortes + 1, p1, moeda_chave, True, moedas_count

        return count_mortes, p1, moeda_chave, moeda_chave_test, moedas_count
    def move_inimigo(self, inimigo, p1, qtd_teletransporte, inimigo_vivo, count_mortes):
        inimigo_centro = inimigo.getAnchor()
        p1_centro = p1.getAnchor()
        vetor_passo = self.vetor_distancia(inimigo_centro, p1_centro, 1)
        inimigo.move(vetor_passo[0], vetor_passo[1])
        if - p1_centro.getX() + inimigo_centro.getX() < 5 and - p1_centro.getY() + inimigo_centro.getY() < 5 and inimigo_vivo:
            p1 = self.redraw_p1(p1, Point(16*3,256-16*3))
            inimigo = self.redraw_inimigo(inimigo)
            return p1, qtd_teletransporte - 1, inimigo, count_mortes + 1
        return p1, qtd_teletransporte, inimigo, count_mortes
    def inimigo_morte(self, inimigo, ponto_bala, inimigo_vivo):
        inimigo_centro = inimigo.getAnchor()
        if abs(ponto_bala.getX() - inimigo_centro.getX()) < 10 and abs(ponto_bala.getY() - inimigo_centro.getY()) < 10 and (inimigo_vivo):
            inimigo.undraw()
            return False
        return inimigo_vivo
    def tiro(self, p1_centro, bullet):
        clickPoint = self.win.checkMouse()
        if clickPoint != None and not bullet[2]:
            direcao = self.vetor_distancia(p1_centro , clickPoint, 10)
            bullet = self.draw_bullet(direcao, p1_centro)
            return (bullet, direcao, True, p1_centro)
        return bullet
    def draw_bullet(self, bullet, p1):
        x, y = p1.getX(), p1.getY()
        '''bullet = Polygon(Point(x, y), Point(x + int(bullet[0]), y + int(bullet[1])))
        bullet.setOutline('red')'''
        bullet = Image(Point(x, y), 'src/shuriken.png')
        bullet.draw(self.win)
        return bullet
    def bullet_undraw(self, desenho_bullet):
        desenho_bullet.undraw()
        return False
    def boss_ataque(self, ataque, safe_zone, raio, angulo_retangulo):
        ataque.undraw()
        ataque = Circle(Point(256/2, 256/2), raio + 1)
        ataque.setOutline('red')
        ataque.draw(self.win)  
        x, y = cos(angulo_retangulo), sin(angulo_retangulo)
        safe_zone.move(x, y)
        return raio + 1, ataque, safe_zone
    def morreu_para_boss(self, p1):
        return self.redraw_p1(p1, Point(16*3,256-16*3))
    def modulo(self, ponto1, ponto2):
        vetor_diretor = (ponto1.getX() - ponto2.getX(), ponto1.getY() - ponto2.getY())  #xp - xi
        modulo = abs( (vetor_diretor[0]**2 + vetor_diretor[1]**2)**0.5 ) # 
        return modulo, vetor_diretor
    def vetor_distancia(self, p1_centro, mouse, tamanho_bala):
        try:
            modulo, vetor_diretor = self.modulo(mouse, p1_centro)
            vetor_resultante = (vetor_diretor[0]*tamanho_bala/modulo, vetor_diretor[1]*tamanho_bala/modulo )
            return vetor_resultante
        except:
            return (0,0)
        '''
            M = (x²+y²)**1/2
            M.(3/M) = (3/M) . (x²+y²)**1/2
            3 = (3²/M²)^0.5 . (x²+y²)**1/2
            3 = (3²/M² . (x²+y²) )^0.5
            3 = ((x² . 3²/M² + y² . 3²/M²) )^0.5
            3 = (( (x . 3/M)² + (y . 3/M)² ) )^0.5 
        '''
    def is_empty_pixel(self, item, x, y):
        return item.getPixel(x,y) == [0,0,0]
    def move(self, p1, wall, portas, key_test, nivel, esquerda_baixo, esquerda_cima, direita_baixo, direita_cima):
        passos = 3
        if is_pressed('d') and self.is_empty_pixel(wall, direita_baixo[0] + passos + 1, direita_baixo[1]) and self.is_empty_pixel(wall, direita_cima[0] + passos + 1, direita_cima[1]):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_d.png')
            p1.draw(self.win)
            p1.move(passos, 0)
        if is_pressed('a') and self.is_empty_pixel(wall,esquerda_baixo[0] - passos - 1, esquerda_baixo[1]) and self.is_empty_pixel(wall, esquerda_cima[0] - passos - 1, esquerda_cima[1]):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_a.png')
            p1.draw(self.win)
            p1.move(-passos, 0)
        if is_pressed('w') and self.is_empty_pixel(wall,esquerda_cima[0], esquerda_cima[1] - passos - 1) and self.is_empty_pixel(wall, direita_cima[0], direita_cima[1] - passos - 1):
            if key_test:
                if self.is_empty_pixel(portas, esquerda_cima[0], esquerda_cima[1] - passos - 1) and self.is_empty_pixel(portas, direita_cima[0], direita_cima[1] - passos - 1):
                    loc = p1.getAnchor()
                    p1.undraw()
                    p1 = Image(loc, 'src/char_w.png')
                    p1.draw(self.win)
                    p1.move(0, -passos)
            else:
                loc = p1.getAnchor()
                p1.undraw()
                p1 = Image(loc, 'src/char_w.png')
                p1.draw(self.win)
                p1.move(0, -passos)
        if is_pressed('s') and self.is_empty_pixel(wall, esquerda_baixo[0], esquerda_baixo[1]+passos + 1) and self.is_empty_pixel(wall, direita_baixo[0], direita_baixo[1] + passos + 1):
            loc = p1.getAnchor()
            p1.undraw()
            p1 = Image(loc, 'src/char_s.png')
            p1.draw(self.win)
            p1.move(0, passos)
        return p1
def inicio():
    fileName = "save.txt"
    existe = bool()
    try:
        file = open(fileName)
        file.close()
        existe = True
    except:
        existe = False
    if  not existe:
        f = open(fileName, 'w')
        f.write('0 0 0 ')
        f.close()
    f = open(fileName, 'r')
    text = f.read()
    f.close()
    text = text.split()
    nivel = int(text[0])
    count_mortes = int(text[1])
    moedas_count = int(text[2])
    return nivel, count_mortes, moedas_count
def save(nivel, count_mortes, moedas_count):
    fileName = "save.txt"
    f = open(fileName, 'w')
    f.write(str(nivel) +  ' ' + str(count_mortes) + ' ' + str(moedas_count))
    f.close()
