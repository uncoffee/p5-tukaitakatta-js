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
screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN  | pygame.SCALED | pygame.HWSURFACE)


#変更可

fps = 100#一秒間に画面更新をする回数

split_varue = 20 #円が出てくるマス目の細かさ

use_aruco = False #True:設定したarucoマーカを追尾　False:マウスカードルを追尾

comment_size = 200 #コメントのサイズを指定する
comment_file_list = ["good.png"] #コメントのバリエーション　追加可能
comment_list = []

edge_range = 3 #外周と生成円の距離HTMLのpaddingのノリ

count_down_time = 2 #画面が切り替わった後の待機時間

circle_size = 180#表示される円の大きさ

level_frame_size = 1800#レベルを囲んでいる枠の大きさ

level_size = 600#難易度boxの大きさ

button_size = 1000#スタートボタンの大きさ


#変更不可
count_down_time *= fps

level_file_list = ["easy.png" , "normal.png" , "hard.png"] #難易度のバリエーション
level_list = []

start_button_file_list = ["start_button.png" , "start_button_frame.png"]
start_button_list = []


design_file_list = [
    ("level_frame.png",1800)
]
design_list = [] 

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

comment_x = 0
comment_y = 0
comment_text = ""
comment_q = []

#surfaceの設定
pygame.display.set_caption("デジタル体育")

front_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

middle_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

back_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)



# comment_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

# check_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

# cursor_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

# move_entity_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
# back_entity_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

left_top = (0,0)
right_top = (0,0)
right_bottom = (0,0)
left_bottom = (0,0)
red_feet = (0,0,0)
red_hand = (0,0,0)
blue_feet = (0,0,0)
blue_hand = (0,0,0)

circle_time = 0

check_count = 0

if mode == "play":
    if difficulty_level == "easy":
        circle_time = 10

    if difficulty_level == "normal":
        circle_time = 7

    if difficulty_level == "hard":
        circle_time = 5



def spotlight(point):
    x , y = point
    pygame.draw.circle(front_surface,(255,255,255,200),(x,y),25)

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def set_color(color,change_value):
    for i in range(len(color)):
        color[i] -= change_value
        if color[i] < 0:
            color[i] = 0

    return color

team = 4

def backcolor(h,s,v):

    h/=100
    s/=100
    v/=100

    r,g,b = colorsys.hsv_to_rgb(h,s,v)

    return r*255,g*255,b*255

    #cps　「1秒間に～」の間隔 後で単位を調整したい　下のコメントチェック
default_size = 50#最終円のサイズ指定
class play_screen:
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
            if self.circle_id + 5 == red_feet[2]:
                mouse_x , mouse_y , id = red_feet

            if self.circle_id + 5 == red_hand[2]:
                mouse_x , mouse_y , id = red_hand
        
            if self.circle_id + 5 == blue_feet[2]:
                mouse_x , mouse_y , id = blue_feet

            if self.circle_id + 5 == blue_hand[2]:
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

def random_position(length):
    return random.randint(0 + length / split_varue, 0 - length / split_varue)

def make_circle():
    if len(play_circle_list) <= 0:
        x = (random_position(screen_width))
        y = (random_position(screen_height))

    else:
        while abs(new_circle_x - last_circle_x) <= split_screen_x * 5 and abs(new_circle_y - last_circle_y) <= split_screen_y * 5:
            new_circle_x = random.randint(edge_range,split_varue - edge_range) * split_screen_x
            new_circle_y = random.randint(edge_range,split_varue - edge_range) * split_screen_y
        new_circle = make_circle(new_circle_x,new_circle_y,circle_time,random.randint(0,len(circle_list) - 1))

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

def player_chege_point(player):
    mouse_y = 0
    mouse_x = 0
    
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

def image_changer(img_name,size):
    img = pygame.image.load(img_name)
    scale = size / img.get_width()
    img_data = pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))
    return img_data


effect_circle_list = []

class effect_circle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 5
        self.clear = 200
        self.alive = True
        self.r,self.g,self.b = random_color()
    
    def draw(self):
        pygame.draw.circle(back_surface,(self.r,self.g,self.b,self.clear),(self.x,self.y),self.size)
        pygame.draw.circle(back_surface,(0,0,0,0),(self.x,self.y),self.size - 4)

        self.size += screen_width / 200
        self.clear -= 1
        if self.clear <= 0:
            self.clear = 0
            self.alive = False

clock = pygame.time.Clock()



class aruco_entity:
    def __init__(self,marker_id,set_point,img,task):
        self.count = 0
        self.task = task
        self.marker_id = marker_id
        self.set_point = set_point
        self.draw_point = set_point
        self.now_point = (0,0) #プレイヤーの位置を特定するのに必要な値（初期値）
        self.img = img


    def set_mode(self):
        self.count += 1
        if self.marker_id <= 4:
            pygame.draw.circle(back_surface, (255,0,0),(self.draw_point), 30)

        else:
            back_surface.blit(self.img,self.draw_point)



class edge_marker(aruco_entity):
    def __init__(self,marker_id,name,draw_point):
        goal = 5 #0.2秒間に読み取る目標を設定する。

        super().__init__(marker_id,draw_point,None,goal)

        self.name = name


class player_marker(aruco_entity):
    def __init__(self,marker_id,img_name,size,draw_point):
        img = image_changer(img_name,size)
        goal = 5 #0.2秒間に読み取る目標を設定する。

        super().__init__(marker_id,draw_point,img,goal)
        super(play_entity).__init(marker_id,img,size)


def count_checker():
    for i in set_entity_list:
        if i.count >= i.task:
            continue
        else:
            for j in set_entity_list:
                j.count = 0
            return False
    return True



class menu_entity:
    def __init__(self,img_name,img,draw_point,defa_clear,move):
        self.img_name = img_name
        self.img = img
        self.draw_point = draw_point
        self.defa_clear = defa_clear#初めの透明度をメモしておく
        self.now_clear = defa_clear#今の透明度を表す値
        self.move = move#動くエンティティーかどうか(surfaceを区別する為)



class level_entitys(menu_entity):
    def __init__(self,img_name,size,draw_point,push_range,level_seter):
        defa_clear = 50 #エンティティーの初期透明度の指定　min:0 max:255
        move = True
        img = image_changer(img_name,size)

        super().__init__(img_name,img,draw_point,defa_clear,move)

        self.push_range = push_range
        self.level_seter = level_seter
        self.now_chews = False#今選択されているクラスであるかどうか。


    def action(self):
        self.now_clear += 5 #この値でどれくらい長押し？すればアクションが起きるかを設定できる。
        if self.now_clear > 255:
            self.now_clear = 255

            for i in level_entity_list:
                i.now_chews = False
            self.now_chews = True

            global difficulty_level
            difficulty_level = self.level_seter


    def back_action(self):
        if not self.now_chews:
            self.now_clear -= 5
            if self.now_clear < self.defa_clear:
                self.now_clear = self.defa_clear
        



class back_entity(menu_entity):
    def __init__(self,img_name,size,draw_point):
        defa_clear = 255
        move = False
        img = image_changer(img_name,size)
        super().__init__(img_name,img,draw_point,defa_clear,move)


class start_button_entity(menu_entity):
    def __init__(self,img_name,size,draw_point,push_range,mode_seter):
        if img_name == "start_button.png":
            defa_clear = 255 #エンティティーの初期透明度の指定　min:0 max:255
            move = False

        else:
            defa_clear = 0 #エンティティーの初期透明度の指定　min:0 max:255
            move = True

        img = image_changer(img_name,size)
        super().__init__(img_name,img,draw_point,defa_clear,move)

        self.mode_seter = mode_seter
        self.push_range = push_range

        self.count = 0

        
    def action(self):
        self.now_clear += 3
        if self.now_clear > 255:
            self.now_clear = 255
            global mode
            global circle_time
            mode = self.mode_seter

            if difficulty_level == "easy":
                circle_time = 10

            if difficulty_level == "normal":
                circle_time = 7

            if difficulty_level == "hard":
                circle_time = 5


    def back_action(self):
        self.now_clear -= 3
        if self.now_clear < self.defa_clear:
            self.now_clear = self.defa_clear




class play_entity:
    def __init__(self,marker_id,img,size):
        self.marker_id = marker_id
        self.img = img
        self.size = size
        self.spawn_point = (0,0)#初期位置の設定（画面サイズをオーバーしていなければ問題なし）

class



def push_checker(cursor,entity):
     #aから始まるものはアンダー（底辺）に当たる座標。tから始まるものはトップ（上底）に当たる座標。
        a_x , t_x , a_y , t_y = entity.push_range
        c_x , c_y = cursor

        if a_x <= c_x <= t_x and a_y <= c_y <= t_y:
            entity.action()

        else:
            entity.back_action()

def p(text,time):
    if time == "n":
        print(text)
        return

    if time % 50 == 0:
        print(text)

def position_manager(mode):

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        if mode == "set":

            pygame.draw.circle(back_surface, (255,255,255),(int(screen_width * 0.1),int(screen_height *0.1)), 30)
            pygame.draw.circle(back_surface, (255,255,255),(int(screen_width * 0.9),int(screen_height * 0.1)), 30)
            pygame.draw.circle(back_surface, (255,255,255),(int(screen_width * 0.9),int(screen_height * 0.9)), 30)
            pygame.draw.circle(back_surface, (255,255,255),(int(screen_width * 0.1),int(screen_height * 0.9)), 30)
            
            opencv_cap_surface = pygame.surfarray.make_surface(frame)
            screen.blit(opencv_cap_surface,(screen_width / 2 - 340,screen_height * 2 / 3 - 204))

        markers, ids, rejected = aruco_detector.detectMarkers(frame)
        if ids is not None:
            for i in range(len(markers)):
                ID = ids[i]
                C1 = markers[i][0][0]
                C2 = markers[i][0][1]
                C3 = markers[i][0][2]
                C4 = markers[i][0][3]
                ave = int((C1[0] + C2[0] + C3[0] + C4[0]) / 4) , int((C1[1] + C2 [1] + C3[1] + C4[1]) / 4)

                for j in set_entity_list:
                    if j.marker_id == int(ID):
                        if mode == "set":
                            j.set_mode()


                        if int(ID) <= 4:#1~4までのIDは隅の四点に設置しているマーカー
                            j.now_point = ave

                        else:#5~8までのIDはプレイヤーの四肢に装着しているマーカー
                            j.now_point = player_chege_point(ave)




def menu_manager(cursor):
    for i in menu_entity_list:
        draw_x , draw_y = i.draw_point
        i.img.set_alpha(i.now_clear)

        if i.move:
            push_checker(cursor,i)
            middle_surface.blit(i.img, (draw_x , draw_y))

        else:
            back_surface.blit(i.img, (draw_x , draw_y))



edge_marker_list = [
    edge_marker(1,"left_top",[int(screen_width * 0.1),int(screen_height * 0.1)]),
    edge_marker(2,"right_top",[int(screen_width * 0.9),int(screen_height * 0.1)]),
    edge_marker(3,"right_buttom",[int(screen_width * 0.9),int(screen_height * 0.9)]),
    edge_marker(4,"left_buttom",[int(screen_width * 0.1),int(screen_height * 0.9)])
]

player_marker_list = [
    player_marker(5,"青足.png",circle_size,[(screen_width * 5 // 9) - 90,(screen_height * 1 // 9) - 50]),
    player_marker(6,"赤足.png",circle_size,[(screen_width * 5 // 9) - 90,(screen_height * 2 // 9) - 50]),
    player_marker(7,"青手.png",circle_size,[(screen_width * 4 // 9) - 90,(screen_height * 1 // 9) - 50]),
    player_marker(8,"赤手.png",circle_size,[(screen_width * 4 // 9) - 90,(screen_height * 2 // 9) - 50])
]

set_entity_list = edge_marker_list + player_marker_list #セットモードで使うリスト

level_entity_list = [
    level_entitys("easy.png",level_size,((screen_width * 3 / 12) -300,(screen_height / 3) - 167),(277,679,242,485),"easy"),
    level_entitys("normal.png",level_size,((screen_width * 6 / 12) -300,(screen_height / 3) - 167),(757,1159,242,485),"normal"),
    level_entitys("hard.png",level_size,((screen_width * 9 / 12) -300,(screen_height / 3) - 167),(1237,1639,242,485),"hard")

]

start_button_list = [
    start_button_entity("start_button.png",button_size,((screen_width / 2) -500,(screen_height * 4 / 5) -278),None,None),
    start_button_entity("start_button_frame.png",button_size,((screen_width / 2) -500,(screen_height * 4 / 5) -278),(524,1398,734,1006),"play")
]

back_entity_list = [
    back_entity("level_frame.png",level_frame_size,((screen_width / 2) - 900,(screen_height / 2) - 500))
]

menu_entity_list = level_entity_list + start_button_list + back_entity_list #メニューモードで使うリスト



aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

cap = cv2.VideoCapture(0)

if use_aruco:
    ret, frame = cap.read()
    while ret != True:
        print("カメラが接続されていません。")
        ret, frame = cap.read()

    print("カメラの接続が確認されました。")
else:
    print("現在の設定ではuse_arucoはFalseです。")
    print("カメラを使用せずに開始します。")

    #ウィンドウの状況

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
    front_surface.fill((0,0,0,0))
    middle_surface.fill((0,0,0,0))
    back_surface.fill((0,0,0,0))

    if mode == "set":
        if use_aruco:
            count += 1




            if count % 3 == 0:
                position_manager("set")#この関数からクラスの関数をたたいているため、描画もこれに含まれる。

            if count % 100 == 0:
                if count_checker():
                    mode = "menu"

        else:
            mode = "menu"

    if mode == "menu":
        if use_aruco:
            for i in player_marker_list:
                if i.marker_id == 6:#marker_idの6は"赤足.png"
                    player_cursor = i.now_point

        else:
            player_cursor = pygame.mouse.get_pos()

        count += 1
 
        spotlight(player_cursor)

        menu_manager(player_cursor)#描画+エンティティーの動きを担当。

    if mode == "play":
        count += 1
        if not count <= count_down_time:
            if count % 600 == 0:
                make_circle(random.randint(0,3))




        # level_list[0].set_alpha(easy_count)
        # level_list[1].set_alpha(normal_count)
        # level_list[2].set_alpha(hard_count)
        # start_button_list[1].set_alpha(start_count)

        # menu_surface.blit(game_level_frame, ((screen_width / 2) - 900,(screen_height / 2) - 500))
        # menu_surface.blit(level_list[0], ((screen_width * 3 / 12) -300,(screen_height / 3) - 167))
        # menu_surface.blit(level_list[1], ((screen_width * 6 / 12) -300,(screen_height / 3) - 167))
        # menu_surface.blit(level_list[2], ((screen_width * 9 / 12) -300,(screen_height / 3) - 167))
        # menu_surface.blit(start_button_list[0], ((screen_width / 2) -500,(screen_height * 4 / 5) -278))
        # menu_surface.blit(start_button_list[1], ((screen_width / 2) -500,(screen_height * 4 / 5) -278))

        # screen.blit(menu_surface,(0,0))
        # screen.blit(cursor_surface,(0,0))
        # if count % 5 == 0:

    # if mode =="play":
    #     #総フレーム数（カウント
    #     count += 1

    #     if count % 150 == 0:
    #         for i in [red_feet,blue_feet]:
    #             new_effect_circle = effect_circle(i[0],i[1])
    #             effect_circle_list.append(new_effect_circle)

    #     effect_surface.fill((0,0,0,255 // 20))
    #     alive_effect_circle_list = []
    #     for i in effect_circle_list:
    #         if i.alive:
    #             alive_effect_circle_list.append(i)

    #     effect_circle_list = alive_effect_circle_list
    #     for i in effect_circle_list:
    #         i.draw()
            
    #     #円の座標を設定する
    #     if  count % (circle_time * 125) == 0:
    #         while abs(new_circle_x - last_circle_x) <= split_screen_x * 5 and abs(new_circle_y - last_circle_y) <= split_screen_y * 5:
    #             new_circle_x = random.randint(edge_range,split_varue - edge_range) * split_screen_x
    #             new_circle_y = random.randint(edge_range,split_varue - edge_range) * split_screen_y
    #         new_circle = make_circle(new_circle_x,new_circle_y,circle_time,random.randint(0,len(circle_list) - 1))
    #         circles.append(new_circle)
    #         last_circle_x = new_circle_x
    #         last_circle_y = new_circle_y

    #     #surfaceの描画
    #     alive_circles = []
    #     for i in circles:
    #         if i.alive:
    #             alive_circles.append(i)
                
    #     for i in alive_circles:
    #         i.update()
    #         i.draw()

    # #     for i in comment_q:
    # #         i.update()
    # #         i.draw()
        
    #     screen.blit(comment_surface,(0,0))

    screen.blit(back_surface,(0,0))

    screen.blit(middle_surface,(0,0))

    screen.blit(front_surface,(0,0))

    pygame.display.update() 

# 7. Pygame の終了処理
pygame.quit()
print("ウィンドウを閉じました。")
