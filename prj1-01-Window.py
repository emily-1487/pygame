###################匯入模組###################
import imaplib
import pygame
import sys
import math
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
###################循環偵測###################
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:#如果按下[x]就退出
            sys.exit()#離開遊戲
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("clickll")
            print(pygame.mouse.get_pos())
            
    #繪製畫布於視窗左上角
    screen.blit(bg,(0,0))
    #更新視窗
    pygame.display.update()
    #畫圓形(畫布,顏色,圓心,半徑,線寬)
    pygame.draw.circle(bg,(255,255,0),(200,100),30,0)
    #畫矩形(畫布,顏色,圓心,半徑,線寬)
    pygame.draw.rect(bg,(125,50,100),[270,130,60,40],5)
    # 畫橢圓, (畫布, 顏色, [x, y, 寬, 高], 線寬)
    pygame.draw.ellipse(bg,(255,0,0),[130,160,60,35],5)
    # 畫線, (畫布, 顏色, 起點, 終點, 線寬)
    pygame.draw.line(bg,(125,50,100),(100,100),(320,220),3)
    # 畫多邊形, (畫布, 顏色, [[x1, y1], [x2, y2], [x3, y3]], 線寬)
    pygame.draw.polygon(bg,(125,50,100),[[100,100],[0,200],[200,200]],5)
    # 畫圓弧, (畫布, 顏色, [x, y, 寬, 高], 起始角度, 結束角度, 線寬)
    pygame.draw.arc(bg,(125,50,100),[100,100,100,50],math.radians(180),math.radians(0),2)

    pygame.draw.circle(bg,(255,255,0),(400,300),30,0)
    pygame.draw.circle(bg,(255,255,0),(600,300),30,0)
    pygame.draw.rect(bg,(125,50,100),[470,350,60,40],5)
    pygame.draw.ellipse(bg,(255,0,0),[650,400,60,35],5)
    pygame.draw.ellipse(bg,(255,0,0),[300,400,60,35],5)
    pygame.draw.line(bg,(125,50,100),(469,464),(320,220),3)



    pygame.mouse.get_pos()
    x,y=pygame.mouse.get_pos()#存取座標