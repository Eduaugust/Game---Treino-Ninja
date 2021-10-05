#   Execute esse arquivo para jogar
import os
try:
    import keyboard
except:
    os.system('pip install keyboard')
from funcoesBasicas import *
from graphics import *
import random
def main(nivel, count_mortes, moedas_count):
    win = GraphWin("", 256, 256, autoflush= False)
    basics = Basics(win)
    p1, chao, enfeites, fogo, paredes, peaks_off, peaks_on, portas, moedas_chaves = basics.create_all_room()
    if nivel > 2:
        pode_atirar = True
    else:
        pode_atirar = False
    peaks_test = True
    moeda_chave_test = True
    tempo = 0
    qtd_teletransporte = 0
    inimigo_draw = False
    inimigo_vivo = True
    controlador_fogo = 0
    boss_draw = False
    boss_hit_count = 0
    boss_animacao = True
    boss_ataque = False
    boss_radius_ataque = 0
    boss_rectangle_angle =  1 * pi
    bullet = (Point(0,0), Point(0,0), False, Point(0,0))
    mortes = Text(Point(16, 16), "")
    mortes.draw(win)
    moeda_draw_count = Text(Point(256 - 16, 16), "")
    moeda_draw_count.draw(win)
    basics.texto_nivel0(nivel)
    for i in range(nivel):
        x, p1, x = basics.next_level(moedas_count,nivel, p1, moedas_chaves, moeda_chave_test, portas, chao, enfeites, fogo, paredes, peaks_off, peaks_on, portas, moedas_chaves)
    while not (win.isClosed()):
        pode_atirar = basics.text_nivel_2(nivel, p1.getAnchor(), pode_atirar)
        tempo += 1
        esquerda_baixo, esquerda_cima, direita_baixo, direita_cima = basics.get_sensores(p1, nivel)
        if direita_cima[0] > 210 + 256*nivel and direita_cima[1] <65 and nivel != 4 and (nivel != 2 or pode_atirar):
            nivel, p1, moeda_chave_test = basics.next_level(moedas_count, nivel, p1, moedas_chaves, moeda_chave_test, portas, chao, enfeites, fogo, paredes, peaks_off, peaks_on, portas, moedas_chaves)
        p1 = basics.move(p1, paredes, portas, moeda_chave_test, nivel, esquerda_baixo, esquerda_cima, direita_baixo, direita_cima)
        fogo, controlador_fogo = basics.move_fire(fogo, nivel, controlador_fogo)
        peaks_test = basics.peaks_on(peaks_test, peaks_off, tempo)
        moeda_chave_test, moedas_count = basics.moeda_chave_gotcha(moedas_chaves, moeda_chave_test, portas, p1, nivel, moedas_count)
        count_mortes ,p1, moedas_chaves, moeda_chave_test, moedas_count = basics.trap_check_dead(moedas_count, count_mortes, p1, tempo, peaks_off, peaks_on, peaks_test, fogo, controlador_fogo, moedas_chaves, moeda_chave_test, portas, esquerda_baixo, esquerda_cima, direita_baixo, direita_cima)
        p1, qtd_teletransporte = basics.teletransporte(nivel, 3, p1, (208, 192), (224, 224), Point(16*3 ,128), qtd_teletransporte)
        p1, qtd_teletransporte = basics.teletransporte(nivel, 3, p1, (208, 192 - 80), (224, 224 - 80), Point(16*3 ,128 - 80), qtd_teletransporte)
        if pode_atirar:
            bullet = basics.tiro(p1.getAnchor(), bullet)        
        # Inimigo no nivel 3
        if not inimigo_draw and nivel == 3 and inimigo_vivo:
            inimigo = Image(Point(64 + 256/2,256/2), 'src/inimigos.png')
            inimigo.draw(win)
            inimigo_draw = True
        elif qtd_teletransporte == 1 and nivel == 3:
            p1, qtd_teletransporte, inimigo, count_mortes = basics.move_inimigo(inimigo, p1, qtd_teletransporte, inimigo_vivo, count_mortes)
            inimigo_vivo = basics.inimigo_morte(inimigo, ponto_bala, inimigo_vivo)

        # Atira bala
        if bullet[2]: 
            bullet[0].move(bullet[1][0], bullet[1][1])
            sensor_bullet = bullet[0].getAnchor()
            tamanho, nada = basics.modulo( Point( int(sensor_bullet.getX()), int(sensor_bullet.getY()) ), bullet[3] )
            if int(tamanho) > 256 and bullet:
                bullet =(bullet[0], bullet[1], basics.bullet_undraw(bullet[0]), bullet[3])
        # Bala 
        try:
            ponto_bala = bullet[0].getAnchor()
        except:
            ponto_bala = Point(0,0)
        
        # Boss Final!
        if nivel == 4:
            # Desenhar boss
            if not boss_draw:
                boss = Image(Point(256/2, 256/2), 'src/boss.png')
                boss.draw(win)
                boss_draw = True
            # Animação do boss 
            
            if tempo%10 == 0:
                if tempo%20 == 0:
                    boss_animacao = True
                else:
                    boss_animacao = False
            if boss_animacao:
                boss.move(0, -1)
            else:
                boss.move(0, +1)
        # boss morte
            boss_centro = boss.getAnchor()
            if abs( ponto_bala.getX() - boss_centro.getX() ) < 19 and abs( ponto_bala.getY() - boss_centro.getY() ) < 21 and bullet[2]:
                if p1_x > 16*3 + 10 or p1_y < 256-16*3-10:
                    boss_hit_count += 1
                    bullet =(bullet[0], bullet[1], basics.bullet_undraw(bullet[0]), bullet[3])
            
                if boss_hit_count == 50:
                    ganhou = Text(Point(256/2, 256/2), "Parabéns, você venceu\nAperte enter para fechar")
                    ganhou.setSize(18)
                    ganhou.setOutline('white')
                    ganhou.setFill('purple')
                    ganhou.draw(win)
                    x = 'a'
                    while x != 'Return':
                        x = win.checkKey()
                    nivel, count_mortes, moedas_count = 0, 0, 0
                    break
        # boss ataque
            if not boss_ataque:
                ataque = Circle(Point(256/2, 256/2), boss_radius_ataque)
                ataque.setOutline('red')
                ataque.draw(win)  
                safe_zone = Rectangle(Point(256/2 - 10, 256/2 - 10 ), Point(256/2+ 10 , 256/2 + 10))
                safe_zone.setFill('green')
                safe_zone.setOutline(color_rgb(0, 0, 0))
                safe_zone.draw(win)
                boss_ataque = True
            else:
                boss_radius_ataque, ataque, safe_zone = basics.boss_ataque(ataque, safe_zone, boss_radius_ataque, boss_rectangle_angle)
            # Reset ataque
            if boss_radius_ataque > 270/2:
                ataque.undraw()
                safe_zone.undraw()
                boss_radius_ataque = 0
                boss_ataque = False
                boss_rectangle_angle = random.uniform(0, 2) * pi
            # P1 morre pelo boss
            distancia_p1_centro = int(basics.modulo(p1.getAnchor(), Point(256/2,256/2) )[0] )
            # -------- angulo = arccos ( x . y / |x| . |y| ) ------------
            safe_zone_centro = safe_zone.getCenter()
            p1_centro = p1.getAnchor()
            p1_x, p1_y = p1_centro.getX(), p1_centro.getY()
            safe_zone_x, safe_zone_y =  safe_zone_centro.getX(), safe_zone_centro.getY()
            if distancia_p1_centro > boss_radius_ataque - 2 and distancia_p1_centro < boss_radius_ataque + 2 and not (safe_zone_x + 10 > p1_x and safe_zone_x - 10 < p1_x and safe_zone_y + 10 > p1_y and safe_zone_y - 10 < p1_y) and p1_centro or (p1_x > 256/2 - 20 and p1_x < 256/2 + 20 and p1_y > 256/2 - 20 and p1_y < 256/2 + 20) :
                if p1_x > 16*3 + 10 or p1_y < 256-16*3-10:
                    p1 = basics.morreu_para_boss(p1)
                    count_mortes += 1
                boss_hit_count = 0
        mortes.undraw()
        mortes = Text(Point(48, 8), "Mortes: " + str(count_mortes))
        mortes.setFill('white')
        mortes.draw(win)
        moeda_draw_count.undraw()
        moeda_draw_count = Text(Point(256 - 48, 8), "Moedas: " + str(moedas_count))
        moeda_draw_count.setFill('white')
        moeda_draw_count.draw(win)
        
        update(30)
    win.close()
    return nivel, count_mortes, moedas_count
nivel, count_mortes, moedas_count = inicio()
nivel, count_mortes, moedas_count = main(nivel, count_mortes, moedas_count)
save(nivel, count_mortes, moedas_count)