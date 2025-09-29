#"C:/Program Files/Python311/python.exe" pythonのインストール先
#pip install 打ち込むの忘れずにね！

#pip要る
import numpy
import pygame
import cv2 #pip install opencv-python モジュ:pip install opencv-contrib-python


#pipいらない
import random
import colorsys

# 1. Pygame の初期化
pygame.init()

# 2. ウィンドウのサイズを設定  あとでプロジェクターのサイズに要調整。

# mode_check = True
# while mode_check:
#     screen_mode = int(input("画面モードを選択してください (0: 1280x720, 1: 1920x1080 フルスクリーン): "))
    
#     if screen_mode == 0:
#         screen_width = 1280
#         screen_height = 720
#         screen = pygame.display.set_mode((screen_width, screen_height))
#         mode_check = False

#     if screen_mode == 1:
#         screen_width = 1920
#         screen_height = 1080
#         screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.HWSURFACE)
#         mode_check = False

#pygameの中で使う画像の比率


#pygameの中で使う変数の宣言

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height),pygame.HWSURFACE)


#変更可

fps = 100#一秒間に起きる画面更新の回数

split_varue = 20 #円が出てくるマス目の細かさ

use_aruco = False #True:設定したarucoマーカを追尾　False:マウスカードルを追尾

comment_size = 200 #コメントのサイズを指定する
comment_file_list = ["good.png"] #コメントのバリエーション　追加可能
comment_list = []

circle_size = 180 #円のサイズを指定する

level_size = 600#難易度boxの大きさを変える

edge_range = 3 #外周と生成円の距離HTMLのpaddingのノリ


#変更不可
circle_file_list =["青足.png","赤足.png","青手.png","赤手.png"] #円のバリエーション
circle_list = []

level_file_list = ["easy.png" , "normal.png" , "hard.png"] #難易度のバリエーション
level_list = []

start_button_file_list = ["start_button.png" , "start_button_frame.png"]
start_button_list = []

for filename in comment_file_list:
    image = pygame.image.load(filename)
    scale = comment_size / image.get_width()
    newimage = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    comment_list.append(newimage)

for filename in circle_file_list:
    image = pygame.image.load(filename)
    scale = circle_size / image.get_width()
    newimage = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    circle_list.append(newimage)

for filename in level_file_list:
    image = pygame.image.load(filename)
    scale = level_size / image.get_width()
    newimage = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    level_list.append(newimage)

for filename in start_button_file_list:
    image = pygame.image.load(filename)
    scale = 1000 / image.get_width()
    newimage = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    start_button_list.append(newimage)

image = pygame.image.load("level_frame.png")
scale = 1800 / image.get_width()
game_level_frame = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

mode = "set"

difficulty_level = "easy"

game_point = 0

count = 0

color_count = 0

half_circle = 20

circles = []

last_circle_x = 0
last_circle_y = 0

new_circle_x = 0
new_circle_y = 0

split_screen_x = screen_width / split_varue
split_screen_y = screen_height / split_varue

mouse_x = 0
mouse_y = 0

del_target_circle = "nan"

font = pygame.font.SysFont('Arial', 72)
comment_x = 0
comment_y = 0
comment_text = ""
comment_q = []

coo = (0,0),0
coo_x = 0
coo_y = 0

easy_count = 255
normal_count = 55
hard_count = 55

start_count = 0

del_target_comment = "nan"

#surfaceの設定
pygame.display.set_caption("デジタル体育")

menu_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

backcolor_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

circle_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

comment_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

check_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

cursor_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

left_top = (0,0)
right_top = (0,0)
right_bottom = (0,0)
left_bottom = (0,0)
red_feet = (0,0,0)
red_hand = (0,0,0)
blue_feet = (0,0,0)
blue_hand = (0,0,0)

circle_time = 0

if mode == "play":
    if difficulty_level == "easy":
        circle_time = 10

    if difficulty_level == "normal":
        circle_time = 7

    if difficulty_level == "hard":
        circle_time = 5



def spotlight(point):
    x , y = point
    pygame.draw.circle(cursor_surface,(255,255,255,200),(x,y),25)

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


x_list = []


team = 4

def backcolor(h,s,v):

    h/=100
    s/=100
    v/=100

    r,g,b = colorsys.hsv_to_rgb(h,s,v)

    return r*255,g*255,b*255

    #cps　「1秒間に～」の間隔 後で単位を調整したい　下のコメントチェック
default_size = 50#最終円のサイズ指定
class make_circle:
    def __init__ (self,x,y,cps,circle_id):
        self.alive = True
        self.age = 0
        self.size = default_size * 8
        self.main_size = self.size
        self.clear = 0
        self.x = x
        self.y = y
        self.cps = cps
        self.color = [255,255,255] #円の色の初期値
        self.move = True
        self.circle_id = circle_id
        #self.lo = lo

        #print(f"self.bps  {self.bps}")

    
    def update(self):
        mouse_x = 0
        mouse_y = 0
        if use_aruco:
            if self.circle_id == red_feet[2]:
                mouse_x , mouse_y , id = red_feet

            if self.circle_id == red_hand[2]:
                mouse_x , mouse_y , id = red_hand
        
            if self.circle_id == blue_feet[2]:
                mouse_x , mouse_y , id = blue_feet

            if self.circle_id == blue_hand[2]:
                mouse_x , mouse_y , id = blue_hand
        else:
            mouse_x , mouse_y = pygame.mouse.get_pos()

        if self.move:#デフォルトサイズどうする?仮にsize 25とする
            sa = self.main_size - default_size

            temp = self.cps * fps

            if self.size >= default_size:
                self.size -= sa / temp
            else:
                self.size = default_size

            self.clear += 200 / temp 
            if self.clear >= 200:
                self.clear = 200

            self.age += 1
            if self.age / temp >= 1:
                self.move = False
                self.age = 0
        else:
            global game_point

            self.age += 1
            if self.age / (fps * 0.1) >= 1:
                self.clear -= 200 / (fps * 0.1)
                if self.clear <= 0:
                    self.alive = False

            if self.alive:
                if abs(self.x - mouse_x) <= default_size and abs(self.y - mouse_y) <= default_size:
                    game_point += 1
                    print(game_point)
                    self.alive = False
                    new_comment = tap_comment(self.x,self.y,comment_list[random.randint(0,len(comment_list)-1)])
                    comment_q.append(new_comment)
                

    def draw(self):
        r,g,b = self.color
        
        #外周円
        pygame.draw.circle(circle_surface,(r,g,b,self.clear),(self.x,self.y),self.size)
        pygame.draw.circle(circle_surface,(r,g,b,0),(self.x,self.y),self.size - 4)

        #内周円
        circle_list[self.circle_id].set_alpha(self.clear)
        screen.blit(circle_list[self.circle_id], (self.x - 90, self.y - 50))

class tap_comment:

    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text.copy()
        self.text_time = 0
        self.text_set = 0
        self.clear = 255

    def update(self):
        self.clear -= 255 / (fps * 1)
        if self.clear <= 0:
            self.clear = 0
        self.text.set_alpha(self.clear)


    def draw(self):
        if self.clear != 0:
            screen.blit(self.text, (self.x, self.y))
        else:
            if self.clear == 0:
                if self in comment_q:
                    comment_q.remove(self)

def coordinate():
    if use_aruco:
        ret, frame = cap.read()
        if ret:
            markers, ids, rejected = aruco_detector.detectMarkers(frame)
            
            for i in range(len(markers)):
                ID = ids[i]
                C1 = markers[i][0][0]
                C2 = markers[i][0][1]
                C3 = markers[i][0][2]
                C4 = markers[i][0][3]

                #ave[x,y]
                ave = (C1[0] + C2[0] + C3[0] + C4[0]) / 4 , (C1[1] + C2 [1] + C3[1] + C4[1]) / 4
                
                if ID == 5:
                    red_feet = player_chege_point(ave),5
                if ID == 6:
                    red_hand = player_chege_point(ave),6
                if ID == 7:
                    blue_feet = player_chege_point(ave),7
                if ID == 8:
                    blue_hand = player_chege_point(ave),8
        return red_feet,red_hand,blue_feet,blue_hand
    else:
        return pygame.mouse.get_pos(),0,1,2,3,4

def player_chege_point(player):
    if use_aruco:

        try:
            left_x = change_x(left_top,left_bottom,player)
            right_x = change_x(right_top,right_bottom,player)

            mouse_x = int(screen_width * 0.8 * (player[0] - left_x) / (right_x - left_x) + screen_width * 0.1)

            #print(f"横 :{left_x,player[0],right_x, mouse_x}")
        except:
            if count % 50 == 0:
                print("eroDivisionError")
            
        try:
            top_y = change_y(left_top,right_top,player)
            bottom_y = change_y(left_bottom,right_bottom,player)

            mouse_y = int(screen_height * 0.8 * (player[1] -  top_y) / (bottom_y - top_y) + screen_height * 0.1)

            #print(f"縦 :{top_y,player[1],bottom_y, mouse_y}")
        except:
            if count % 50 == 0:
                print("eroDivisionError")

        return mouse_x , mouse_y



clock = pygame.time.Clock()

def change_x(A, B, now):
    x1, y1 = A
    x2, y2 = B
    now_X, now_y = now

    return ((x1 - x2) / (y1 - y2)) * (now_y-y1) + x1

def change_y(A, B, now):
    x1, y1 = A
    x2, y2 = B
    now_x, now_y = now

    return ((y1 - y2) / (x1 - x2)) * (now_x - x1) + y1
    

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

cap = cv2.VideoCapture(0)


left_top = ()
right_top = ()
right_bottom = ()
left_bottom = ()
player = ()

if use_aruco:
    ret, frame = cap.read()
    while ret != True:
        print("カメラが接続されていません。")
        ret, frame = cap.read()

    print("カメラの接続が確認されました。")
else:
    print("現在の設定ではuse_arucoはFalseです。")
    print("カメラを使用せずに開始します。")


# 4. ゲームループ
running = True
while running:

    #ウィンドウの状況をチェック
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    #fpsの値を設定
    clock.tick(fps)

    #描写のリセット
    screen.fill((50,50,50))
    backcolor_surface.fill((0,0,0,0))
    circle_surface.fill((0,0,0,0))
    comment_surface.fill((0,0,0,0))
    cursor_surface.fill((0,0,0,0))
    menu_surface.fill((0,0,0,0))

    if mode == "set":
        if use_aruco:
            count += 1

            pygame.draw.circle(check_surface, (255,255,255),(int(screen_width * 0.1),int(screen_height *0.1)), 30)

            pygame.draw.circle(check_surface, (255,255,255),(int(screen_width * 0.9),int(screen_height * 0.1)), 30)

            pygame.draw.circle(check_surface, (255,255,255),(int(screen_width * 0.9),int(screen_height * 0.9)), 30)

            pygame.draw.circle(check_surface, (255,255,255),(int(screen_width * 0.1),int(screen_height * 0.9)), 30)

            if count % 5 == 0:

                ret, frame = cap.read()

                cv2.imshow('check_window', frame)


                
                if ret:
                    markers, ids, rejected = aruco_detector.detectMarkers(frame)
                    
                    for i in range(len(markers)):
                        ID = ids[i]
                        C1 = markers[i][0][0]
                        C2 = markers[i][0][1]
                        C3 = markers[i][0][2]
                        C4 = markers[i][0][3]
                        #ave[x,y]
                        ave = (C1[0] + C2[0] + C3[0] + C4[0]) / 4 , (C1[1] + C2 [1] + C3[1] + C4[1]) / 4

                        #print(ID)

                        if ID == 1:
                            left_top = ave
                            pygame.draw.circle(check_surface, (255,0,0),(int(screen_width * 0.1),int(screen_height *0.1)), 30)
                            #print(left_top)

                        if ID == 2:
                            right_top = ave
                            pygame.draw.circle(check_surface, (255,0,0),(int(screen_width * 0.9),int(screen_height * 0.1)), 30)
                            #print(right_top)

                        if ID == 3:
                            right_bottom = ave
                            pygame.draw.circle(check_surface, (255,0,0),(int(screen_width * 0.9),int(screen_height * 0.9)), 30)
                            #print(right_bottom)

                        if ID == 4:
                            left_bottom = ave
                            pygame.draw.circle(check_surface, (255,0,0),(int(screen_width * 0.1),int(screen_height * 0.9)), 30)
                            #print(left_bottom)

                        if ID == 5:
                            red_feet = player_chege_point(ave),5
                            check_surface.blit(circle_list[0], ((screen_width * 4 // 9) - 90,(screen_height * 1 // 9) - 50))

                        if ID == 6:
                            red_hand = player_chege_point(ave),6
                            check_surface.blit(circle_list[1], ((screen_width * 4 // 9) - 90,(screen_height * 2 // 9) - 50))

                        if ID == 7:
                            blue_feet = player_chege_point(ave),7
                            check_surface.blit(circle_list[2], ((screen_width * 5 // 9) - 90,(screen_height * 1 // 9) - 50))

                        if ID == 8:
                            blue_hand = player_chege_point(ave),8
                            check_surface.blit(circle_list[3], ((screen_width * 5 // 9) - 90,(screen_height * 2 // 9) - 50))

                        if ids in 1 and ids in 2 and ids in 3 and ids in 4 and (ids in 5 or ids in 6 or ids in 7 or ids in 8):
                            check_count += 1
                            if check_count >= 300:
                                if ids in 1 and ids in 2 and ids in 3 and ids in 4 and (ids in 5 or ids in 6 or ids in 7 or ids in 8):
                                    mode = "menu"
                                    cv2.destroyAllWindows()
                                else:
                                    check_count = 0

            screen.blit(check_surface,(0,0))

        else:
            mode = "menu"

    if mode == "menu":
                
        count += 1
        if count % 5 == 0:
            coo = coordinate()
            print(coo)
            coo_x,coo_y = coo[0] #red_feet or mouse
        spotlight(coo[0])

        level_list[0].set_alpha(easy_count)
        level_list[1].set_alpha(normal_count)
        level_list[2].set_alpha(hard_count)
        start_button_list[1].set_alpha(start_count)

        menu_surface.blit(game_level_frame, ((screen_width / 2) - 900,(screen_height / 2) - 500))
        menu_surface.blit(level_list[0], ((screen_width * 3 / 12) -300,(screen_height / 3) - 167))
        menu_surface.blit(level_list[1], ((screen_width * 6 / 12) -300,(screen_height / 3) - 167))
        menu_surface.blit(level_list[2], ((screen_width * 9 / 12) -300,(screen_height / 3) - 167))
        menu_surface.blit(start_button_list[0], ((screen_width / 2) -500,(screen_height * 4 / 5) -278))
        menu_surface.blit(start_button_list[1], ((screen_width / 2) -500,(screen_height * 4 / 5) -278))

        if 277 <= coo_x <= 679 and 242 <= coo_y <= 485:
            easy_count += 4
            if easy_count >= 255:
                if 277 <= coo_x <= 679 and 242 <= coo_y <= 485:
                    easy_count = 255
                    difficulty_level = "easy"
        else:
            if difficulty_level != "easy":
                easy_count = 55


        if 757 <= coo_x <= 1159 and 242 <= coo_y <= 485:
            normal_count += 4
            if normal_count >= 255:
                if 757 <= coo_x <= 1159 and 242 <= coo_y <= 485:
                    normal_count = 255
                    difficulty_level = "normal"
        else:
            if difficulty_level != "normal":
                normal_count = 55



        if 1237 <= coo_x <= 1639 and 242 <= coo_y <= 485:
            hard_count += 4
            if hard_count >= 255:
                if 1237 <= coo_x <= 1639 and 242 <= coo_y <= 485:
                    hard_count = 255
                    difficulty_level = "hard"
        else:
            if difficulty_level != "hard":
                hard_count = 55

        if 524 <= coo_x <= 1398 and 734 <= coo_y <= 1006:
            start_count += 2
            if start_count >= 200:
                if 524 <= coo_x <= 1398 and 734 <= coo_y <= 1006:
                    start_count = 255
                    mode = "play"
                    if mode == "play":
                        if difficulty_level == "easy":
                            circle_time = 10

                        if difficulty_level == "normal":
                            circle_time = 7

                        if difficulty_level == "hard":
                            circle_time = 5

        else:
            start_count -=8
            if start_count <= 0:
                start_count = 0



        screen.blit(menu_surface,(0,0))
        screen.blit(cursor_surface,(0,0))


            
            
    if mode =="play":
        #fpsフレーム数の取得 clock.get_fps()

        #総フレーム数（カウント
        count += 1

        #マウスの位置を人がいる位置に置き換えるプログラム（日本語はもともとおかしいわ！



        #円の座標を設定する
        if  count % (circle_time * 125) == 0:
            while abs(new_circle_x - last_circle_x) <= split_screen_x * 5 and abs(new_circle_y - last_circle_y) <= split_screen_y * 5:
                new_circle_x = random.randint(edge_range,split_varue - edge_range) * split_screen_x
                new_circle_y = random.randint(edge_range,split_varue - edge_range) * split_screen_y
            new_circle = make_circle(new_circle_x,new_circle_y,circle_time,len(circle_list) - 1)
            circles.append(new_circle)
            last_circle_x = new_circle_x
            last_circle_y = new_circle_y
            

        #surface の描画
        
        screen.blit(backcolor_surface,(0,0))

        alive_circles = []
        for i in circles:
            if i.alive:
                alive_circles.append(i)
                
        for i in alive_circles:
            i.update()
            i.draw()

        for i in comment_q:
            i.update()
            i.draw()
        
        screen.blit(circle_surface,(0,0))
        
        screen.blit(comment_surface,(0,0))

        screen.blit(cursor_surface,(0,0))

    pygame.display.update() 

# 7. Pygame の終了処理
pygame.quit()
print("ウィンドウを閉じました。")
