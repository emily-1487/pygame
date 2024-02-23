###################匯入模組###################
import imaplib
import pygame
import sys
import math
###################定義函式###################
def check_click(pos,x_min,y_min,x_max,y_max):
    """判斷滑鼠是否典籍在指定的區域內"""
    x_match=x_min<pos[0]<x_max
    y_match=y_min<pos[1]<y_max
    if x_match and y_match:
        return True
    else:
        return False
###################初始化###################
pygame.init()#啟動pygame
width=800#設定視窗寬度
height=780#設定視窗高度
###################建立視窗及物件###################
#設定視窗大小
screen=pygame.display.set_mode((width,height))
#設定視窗標題
pygame.display.set_caption("我差一題啊!!!!")
#建立畫布
bg=pygame.Surface((width,height))
#畫布為白色(R,G,B)
bg.fill((255,255,255))
#######################建立文字######################
#取得系統字體
typeface=pygame.font.get_default_font()
#設定字體和大小
font=pygame.font.Font(typeface,24)
#設定文字參數:文字內容,是否開啟反鋸齒,文字顏色,背景顏色
title=font.render("Start",True,(0,0,0))
#取得文字寬度
tit_w=title.get_width()
#取得文字高度
tit_h=title.get_height()
#將文字畫在視窗的(0,0)
screen.blit(title,(0,0))
###################循環偵測###################
paint=False

while True:
    screen.blit(bg,(0,0))#在繪圖視窗繪製畫布
    mouse_pos=pygame.mouse.get_pos()
    # print(mouse_pos)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:#如果按下[x]就退出
            sys.exit()#離開遊戲
        if event.type==pygame.MOUSEBUTTONDOWN:
            if check_click(mouse_pos,0,0,tit_w,tit_h):
                paint=not paint#當點擊時,切換畫布狀態
            print("clickll")
            print(pygame.mouse.get_pos())
    # if paint:
    #     pygame.draw.circle(bg,(0,0,255),(200,100),30,0)
            
    #繪製畫布於視窗左上角
    screen.blit(bg,(0,0))
    screen.blit(title,(0,0))#將標題圖像繪製在螢幕的(0,0)位置
    #更新視窗
    pygame.display.update()
    # #畫圓形(畫布,顏色,圓心,半徑,線寬)
    # pygame.draw.circle(bg,(255,255,0),(200,100),30,0)
    # #畫矩形(畫布,顏色,圓心,半徑,線寬)
    # pygame.draw.rect(bg,(125,50,100),[270,130,60,40],5)
    # # 畫橢圓, (畫布, 顏色, [x, y, 寬, 高], 線寬)
    # pygame.draw.ellipse(bg,(255,0,0),[130,160,60,35],5)
    # # 畫線, (畫布, 顏色, 起點, 終點, 線寬)
    # #pygame.draw.line(bg, (255, 0, 255), (280, 220), (220, 220), 3)
    # # 畫多邊形, (畫布, 顏色, [[x1, y1], [x2, y2], [x3, y3]], 線寬)
    # pygame.draw.polygon(bg,(125,50,100),[[100,100],[0,200],[200,200]],5)
    # # 畫圓弧, (畫布, 顏色, [x, y, 寬, 高], 起始角度, 結束角度, 線寬)
    # pygame.draw.arc(bg,(125,50,100),[100,100,100,50],math.radians(180),math.radians(0),2)




    
    if paint:
        bg.fill((255,255,255))
        pygame.draw.line(bg,(100,50,100),(300,300),(500,300),3)
        pygame.draw.line(bg,(125,50,100),(600,300),(650,300),3)
        pygame.draw.rect(bg,(125,50,100),[470,350,60,40],5)
        pygame.draw.ellipse(bg,(255,0,0),[650,400,60,35],5)
        pygame.draw.ellipse(bg,(255,0,0),[300,400,60,35],5)
        pygame.draw.circle(bg,(255,255,0),(498,475),30,0)
    else:
        bg.fill((255,255,255))
        
        pygame.draw.circle(bg,(255,255,0),(400,300),30,0)
        pygame.draw.circle(bg,(255,255,0),(600,300),30,0)
        pygame.draw.rect(bg,(125,50,100),[470,350,60,40],5)
        pygame.draw.ellipse(bg,(255,0,0),[650,400,60,35],5)
        pygame.draw.ellipse(bg,(255,0,0),[300,400,60,35],5)
        pygame.draw.line(bg,(125,50,100),(580,475),(417,475),3)
        screen.blit(title,(0,0))#將標題圖像繪製在螢幕的(0,0)位置
        pygame.display.update()

    pygame.mouse.get_pos()
    x,y=pygame.mouse.get_pos()#存取座標