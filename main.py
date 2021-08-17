import pygame as py
import random as rd
import time

py.init()
width = 1000
height = 600
enemy_speed = 50
score = 0
y1, y2 = 0, 0

player_size = 60, 60
enemy_size = 70, 70
background_size = width, height
out_image_size = 100, 100

display = py.display.set_mode((width, height))

font_style = py.font.SysFont("Segoe UI", 50)
font_style2 = py.font.SysFont("Segoe UI", 100)
font_style3 = py.font.SysFont("Segoe UI", 25)

clock = py.time.Clock()

enemy_pos = [rd.randint(0, width-enemy_size[0]), 0]
player_pos = [500, 500]
out_image_pos = [400, 320]
background_pos = [0, 0]

enemy_list = [enemy_pos]

out = py.image.load('out.png')
out = py.transform.scale(out, (out_image_size[0], out_image_size[1]))

background = py.image.load('sky.jpg')
background = py.transform.scale(background, (background_size[0], background_size[1]))

player = py.image.load('player.png')
player = py.transform.scale(player, (player_size[0], player_size[1]))


enemy = py.image.load('enemy.png')
enemy = py.transform.scale(enemy, (enemy_size[0], enemy_size[1]))


def my_out():
    display.blit(out, (out_image_pos[0], out_image_pos[1]))


def my_player():
    display.blit(player, (player_pos[0], player_pos[1]))


def final_words(msg, the_score):
    msgs = font_style2.render(msg, 1, 'red')
    sr = font_style2.render(the_score, 'bold', 'white')
    display.blit(msgs, (300, 200))
    display.blit(sr, (270, 400))


def help(move_right,move_left):
    movement1 = font_style3.render(move_right, 1, 'white')
    movement2 = font_style3.render(move_left, 1, 'white')
    display.blit(movement1, (110, 40))
    display.blit(movement2, (0, 10))


def my_background():
    display.blit(background, [background_pos[0], background_pos[1]])


def level(score, enemy_speed):
    if score < 10:
        enemy_speed = 5
    elif score < 25:
        enemy_speed = 10
    elif score < 50:
        enemy_speed = 15
    elif score <70:
        enemy_speed = 20
    elif score < 100:
        enemy_speed = 25
    else:
        enemy_speed = (score/5) + 5
    return enemy_speed


def my_score(score):
    sr = 'score :' + str(score)
    scores = font_style.render(sr, 1, 'yellow')
    display.blit(scores, (width-200, height-60))


def enemy_drop(enemy_list):
    delay = rd.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = rd.randint(0, width-enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemy(enemy_list):
    for enemy_pos in enemy_list:
        display.blit(enemy, (enemy_pos[0], enemy_pos[1]))


def update_enemy(enemy_list,score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if collision(player_pos, enemy_pos):
            return True
    return False


def collision(player_pos, enemy_pos):
    p_x, p_y = player_pos[0], player_pos[1]
    e_x, e_y = enemy_pos[0], enemy_pos[1]
    if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x < (e_x + enemy_size[0])):
        if (e_y >= p_y and e_y < (p_y + player_size[0])) or (p_y >= e_y and p_y < (e_y + enemy_size[0])):
            return True
    return False

def high_score_file():
    high_score = open('score.txt','r')
    high_score = int(high_score.read())
    return high_score


def my_high_score(high_score, score):
    if high_score < score:
        high_score = open('score.txt', 'w')
        high_score.write(str(score))
        high_score.close()
        high_score = open('score.txt', 'r')
        high_score = int(high_score.read())
        return high_score
    elif high_score >= score:
        high_score = open('score.txt','r')
        high_score = int(high_score.read())
        return high_score

def display_high_score(high_score):
    hs = "High Score :" + str(high_score)
    dhs = font_style.render(hs,True,'yellow')
    display.blit(dhs,(650,10))

try:
    high_score = high_score_file()
except:
    high_score = 0


game_over =False

while not game_over:

    if player_pos[0] >= (width - player_size[0]) or player_pos[0] <= 0:
        game_over = True

    for event in py.event.get():
        if event.type == py.QUIT:
            game_over = True

        if event.type == py.KEYDOWN:
            if event.key == py.K_d:
                y1 = +15
                player_pos[0] += y1
            elif event.key == py.K_a:
                y1 = -15
                player_pos[0] += y1

    display.fill('green')
    my_background()
    help(move_left="Press Key: 'a' - to move left", move_right="'d' - to move right")
    my_player()
    enemy_drop(enemy_list)
    score = update_enemy(enemy_list, score)
    if collision_check(enemy_list, player_pos):
        game_over = True
    my_score(score)
    high_score = my_high_score(high_score,score)
    display_high_score(high_score)
    draw_enemy(enemy_list)
    enemy_speed = level(score, enemy_speed)
    clock.tick(10)
    py.display.update()

display.fill('black')
my_out()
final_words(msg='You lost', the_score=f'Your score : {score}')
py.display.update()
time.sleep(2)
py.quit()
quit()
