import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
kk_imgs = {
    (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
    (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
    (0, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),
    (+5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 0.9),
    (+5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 180, 0.9),
    (+5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 0.9),
    (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 0.9),
    (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんor爆弾rct
    戻り値：横縦タプル
    rectオブジェクトの値から画面内/外(True/False)を判断する
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return (yoko, tate)


def en1_gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面の実装
    ブラックアウト、こうかとん画像2枚、gameoverの文字を表示する
    """
    # ブラックアウト
    go_bg = pg.Surface((1100,650))
    pg.draw.rect(go_bg, (0, 0, 0), pg.Rect(0, 0, 1100, 650))
    go_bg.set_alpha(200)
    # 悲しむこうかとん
    kk_go = pg.image.load("fig/8.png")
    # gameoverの文字
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    screen.blit(go_bg, [0, 0])
    screen.blit(kk_go, [330, 250])
    screen.blit(kk_go, [760, 250])
    screen.blit(txt, [380, 250])


def en2_init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    戻り値：加速度と拡大爆弾のリスト
    時間経過で爆弾が拡大、加速する
    """
    bb_accs = [a for a in range(1, 11)]
    bb_val = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  
        bb_val.append(bb_img)
    return bb_val, bb_accs


def en3_get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    """
    return kk_imgs[sum_mv]

    


def main():

    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5


    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = en2_init_bb_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            en1_gameover(screen)
            pg.display.update()
            time.sleep(5)
            return

        bb_img = bb_imgs[min(tmr//500, 9)]
        # 加速度の計算
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # こうかとん画像切替
        kk_img = en3_get_kk_img((0, 0))
        kk_img = en3_get_kk_img(tuple(sum_mv))

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
