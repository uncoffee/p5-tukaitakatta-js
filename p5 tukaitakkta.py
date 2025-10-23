#"C:/Program Files/Python311/python.exe" pythonのインストール先
#pip install 打ち込むの忘れずにね！

#pip要る
import numpy
import pygame
import cv2 #pip install opencv-python モジュ:pip install opencv-contrib-python


#pipいらない
import random
import sys

pygame.init()

w = 1920
h = 1080
screen = pygame.display.set_mode((w, h),pygame.FULLSCREEN  | pygame.SCALED | pygame.HWSURFACE)

#変更可

fps = 100#一秒間に画面更新をする回数

split_varue = 20 #円が出てくるマス目の細かさ

# use_aruco = True #True:設定したarucoマーカを追尾　False:マウスカードルを追尾

comment_size = 200 #コメントのサイズを指定する

circle_size = 180#表示される円の大きさ

level_frame_size = 1800#レベルを囲んでいる枠の大きさ

level_size = 600#難易度boxの大きさ

button_size = 1000#スタートボタンの大きさ

play_time = 60

#変更不可
game_point = 0

scan_count = 0


#surfaceの設定
difficulty_level = None

pygame.display.set_caption("デジタル体育")

front_surface = pygame.Surface((w,h), pygame.SRCALPHA)

middle_surface = pygame.Surface((w,h), pygame.SRCALPHA)

back_surface = pygame.Surface((w,h),pygame.SRCALPHA)


circle_time = 0

check_count = 0

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def random_position(length):
    circle_spot = length / split_varue
    return random.randint(circle_spot , length-circle_spot)

def make_circle():
    m = random.choice(player_marker_list)
    m.draw_point = (random_position(w),random_position(h))
    m.clear = 255
    
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
    if use_aruco:
        for i in edge_marker_list:
            if i.name == "left_top":
                left_top = i.now_point
            if i.name == "right_top":
                right_top = i.now_point
            if i.name == "right_buttom":
                right_bottom = i.now_point
            if i.name == "left_buttom":
                left_bottom = i.now_point
        # print(f"四隅の座標 :{left_top,right_top,right_bottom,left_bottom}")

    else:
        # mouse_y = 0
        # mouse_x = 0
        # left_top = (0,0)
        # right_top = (0,0)
        # right_bottom = (0,0)
        # left_bottom = (0,0)
        return pygame.mouse.get_pos()
        

    left_x = change_x(left_top,left_bottom,player)
    right_x = change_x(right_top,right_bottom,player)

    mouse_x = int(w * 0.8 * (player[0] - left_x) / (right_x - left_x) + w * 0.1)

    #print(f"横 :{left_x,player[0],right_x, mouse_x}")

    top_y = change_y(left_top,right_top,player)
    bottom_y = change_y(left_bottom,right_bottom,player)

    mouse_y = int(h * 0.8 * (player[1] -  top_y) / (bottom_y - top_y) + h * 0.1)

    #print(f"縦 :{top_y,player[1],bottom_y, mouse_y}")

    return mouse_x , mouse_y


def image_maker(img_name,size):
    img = pygame.image.load(img_name)
    scale = size / img.get_width()
    img_data = pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))
    return img_data


clock = pygame.time.Clock()

class aruco_entity:
    def __init__(self,marker_id,set_point):
        self.count = 1000
        self.marker_id = marker_id
        self.set_point = set_point
        self.draw_point = set_point
        self.now_point = (0,0) #プレイヤーの位置を特定するのに必要な値（初期値）
        self.clear = 0

    def count_plus1(self):
        self.count += 1
        self.clear -= 1
    
    def set_now_point(self, now_point):
        self.now_point = now_point
        self.count = 0

    def set_mode(self):
        self.count += 1
        if self.marker_id <= 4:
            pygame.draw.circle(back_surface, (255,0,0),(self.set_point), 30)

        else:
            back_surface.blit(self.img,self.set_point)
    

class edge_marker(aruco_entity):
    def __init__(self,marker_id,name,draw_point):
        super().__init__(marker_id,draw_point)

        self.name = name

    def draw(self, mode):
        if mode == "set":
            if not self.count < 5:
                pygame.draw.circle(back_surface, (255,255,255),(self.set_point), 30)
            else:
                pygame.draw.circle(back_surface, (255,0,0),(self.set_point), 30)


class player_marker(aruco_entity):
    def __init__(self,marker_id,img_name,size,draw_point):
        self.img_size = 180
        self.img = image_maker(img_name,size)
        draw_point = set_img_point(draw_point,size)
        self.push_range = 0,0,0,0

        super().__init__(marker_id,draw_point)

    def draw(self, mode):
        img_point = set_img_point(self.draw_point,self.img_size)
        clear = 255 - self.clear
        self.img.set_alpha(clear)

        if mode == "set":
            if self.count < 5:
                back_surface.blit(self.img,self.set_point)
        if mode == "menu":
            if self.marker_id == 6:#id6は赤足
                pygame.draw.circle(front_surface, (255,255,255),player_chege_point(self.now_point), 30)

        if mode == "play":
            if self.clear > 1:
                front_surface.blit(self.img,img_point)
                pygame.draw.circle(middle_surface,(255,255,255,clear),self.draw_point,self.clear + 50, 5)

                if self.count < 5:
                    pygame.draw.circle(middle_surface, (255,255,255), player_chege_point(self.now_point), 30)

            elif self.clear == 1:
                x , y = self.draw_point
                self.push_range = x-45, x+45,y-45, y+45#ここの値を後で変える。
                push_checker(player_chege_point(self.now_point),self)#この50は赤青手足マークの大体の直径である。

    def action(self):
        random.choice(comment_list).make(self.draw_point)
        count_result.touch()
        #音を出す。

    def back_action(self):
        count_result.miss()


class coment_text:
    def __init__(self,img_name):
        self.img = image_maker(img_name,400)
        self.draw_point = (0,0)
        self.clear = 0

    def make(self,draw_point):
        p("叩いてるよ","n")
        self.draw_point = draw_point
        self.clear = 255

    def draw(self):
        self.img.set_alpha(self.clear)
        front_surface.blit(self.img,self.draw_point)

        self.clear -= 1
        if self.clear < 0:
            self.clear = 0

        p("叩いてる","n")

                

def count_checker():
    for i in set_entity_list:
        if i.count > 5:
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

    def draw(self):
        if self.move == True:
            self.img.set_alpha(self.now_clear)
            middle_surface.blit(self.img, self.draw_point)

        else:
            back_surface.blit(self.img, self.draw_point)
        


class level_entitys(menu_entity):
    def __init__(self,img_name,size,draw_point,push_range,level_seter,move):
        if move == True:
            defa_clear = 0 #エンティティーの初期透明度の指定　min:0 max:255
            img = image_maker(img_name,size)

        else:
            defa_clear = 255
            img = image_maker(img_name,size)

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
        img = image_maker(img_name,size)
        super().__init__(img_name,img,draw_point,defa_clear,move)


class start_button_entity(menu_entity):
    def __init__(self,img_name,size,draw_point,push_range,mode_seter):
        if img_name == "start_button.png":
            defa_clear = 255 #エンティティーの初期透明度の指定　min:0 max:255
            move = False

        else:
            defa_clear = 0 #エンティティーの初期透明度の指定　min:0 max:255
            move = True

        img = image_maker(img_name,size)
        super().__init__(img_name,img,draw_point,defa_clear,move)

        self.mode_seter = mode_seter
        self.push_range = push_range

        self.count = 0

    
    def action(self):
        global difficulty_level
        if difficulty_level != None:
            self.now_clear += 5
            if self.now_clear > 255:
                self.now_clear = 0#またメニューに戻ってきても押せるようにリセットする。
                global mode
                global circle_time
                mode = self.mode_seter

                if difficulty_level == "easy":
                    circle_time = 7

                if difficulty_level == "normal":
                    circle_time = 6

                if difficulty_level == "hard":
                    circle_time = 5

                count_timer.reset(60)
        


    def back_action(self):
        self.now_clear -= 3
        if self.now_clear < self.defa_clear:
            self.now_clear = self.defa_clear

        
def text_draw(text,font,draw_point,get_color = None):
    if not get_color == None:
        color = get_color
    
    else:
        color = 255,255,255

    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (draw_point)
    
    screen.blit(text_surface, text_rect)


class counter:
    def __init__(self):
        self.count_time = -1#マイナスの状態であれば表示されない。

    def count(self):
        if self.count_time <= 0:
            return True

        else:
            self.count_time -= 1
            return False
        
    def draw(self):
        if self.count_time > 0:
            text_draw(self.count_time,pygame.font.Font(None, 100),(w / 20 * 18,h / 20 * 1))

    def reset(self,time):
        self.count_time = time

        
class play_result:
    def __init__(self):
        self.combo = 0
        self.get_touch = 0
        self.miss_touch = 0
        self.score = 0

    def touch(self):
        self.get_touch += 1
        self.combo += 1
        self.score += int(self.combo / 10 + 1) * 100

    def miss(self):
        self.combo = 0
        self.miss_touch += 1

    def draw(self):
        text_draw(f"score:{self.score}",pygame.font.Font(None,500),(w/2,h/4))#,64,224,208
        text_draw(f"combo:{self.combo}",pygame.font.Font(None,200),(w/20*15,h/3*2))
        text_draw(f"good:{self.get_touch}",pygame.font.Font(None,200),(w/20*3,h/5*3))
        text_draw(f"miss:{self.miss_touch}",pygame.font.Font(None,200),(w/20*3,h/5*4))


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

    elif time % 50 == 0:
        print(text)

def set_img_point(draw_point,img_size):
    d_x , d_y = draw_point
    magnification = img_size / 180
    return (int(-90 * magnification + d_x),int(-50 * magnification + d_y))



def scan_manager(scan_count,mode):
    for j in set_entity_list:
        j.count_plus1()

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        if mode == "set":
            opencv_cap_surface = pygame.surfarray.make_surface(frame)
            screen.blit(opencv_cap_surface,(w / 2 - 340,h * 2 / 3 - 204))

        if scan_count % 5 == 0:#この5は、5フレームのことを指す。
                
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
                                j.set_now_point(ave)




def menu_manager(cursor):
    for i in menu_entity_list:
        draw_x , draw_y = i.draw_point
        i.img.set_alpha(i.now_clear)

        if i.move:
            push_checker(cursor,i)
            middle_surface.blit(i.img, (draw_x , draw_y))

        else:
            back_surface.blit(i.img, (draw_x , draw_y))


comment_list = [
    coment_text("good.png"),
]



edge_marker_list = [
    edge_marker(1,"left_top",[int(w * 0.1),int(h * 0.1)]),
    edge_marker(2,"right_top",[int(w * 0.9),int(h * 0.1)]),
    edge_marker(3,"right_buttom",[int(w * 0.9),int(h * 0.9)]),
    edge_marker(4,"left_buttom",[int(w * 0.1),int(h * 0.9)])
]

player_marker_list = [
    player_marker(5,"青足.png",circle_size,[(w * 5 // 9) - 90,(h * 1 // 9) - 50]),
    player_marker(6,"赤足.png",circle_size,[(w * 5 // 9) - 90,(h * 2 // 9) - 50]),
    player_marker(7,"青手.png",circle_size,[(w * 4 // 9) - 90,(h * 1 // 9) - 50]),
    player_marker(8,"赤手.png",circle_size,[(w * 4 // 9) - 90,(h * 2 // 9) - 50])
]

set_entity_list = edge_marker_list + player_marker_list #セットモードで使うリスト+座標設定にも使ってる。



level_entity_list = [
    level_entitys("moveeasy.png",level_size,((w * 3 / 12) -300,(h / 3) - 167),(277,679,242,485),"easy",True),
    level_entitys("easy.png",level_size,((w * 3 / 12) -300,(h / 3) - 167),None,None,False),
    level_entitys("movenormal.png",level_size,((w * 6 / 12) -300,(h / 3) - 167),(757,1159,242,485),"normal",True),
    level_entitys("normal.png",level_size,((w * 6 / 12) -300,(h / 3) - 167),None,None,False),
    level_entitys("movehard.png",level_size,((w * 9 / 12) -300,(h / 3) - 167),(1237,1639,242,485),"hard",True),
    level_entitys("hard.png",level_size,((w * 9 / 12) -300,(h / 3) - 167),None,None,False)
]

start_button_list = [
    start_button_entity("start_button.png",button_size,((w / 2) -500,(h * 4 / 5) -278),None,None),
    start_button_entity("start_button_frame.png",button_size,((w / 2) -500,(h * 4 / 5) -278),(524,1398,734,1006),"play")
]

back_entity_list = [
    back_entity("level_frame.png",level_frame_size,((w / 2) - 900,(h / 2) - 500))
]

menu_entity_list = back_entity_list + level_entity_list + start_button_list #メニューモードで使うリスト


count_timer = counter()


count_result = play_result()


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if ret != True: #while文からif文に変えた。
    use_aruco = False
    mode = "menu" #スキャンするカメラがないためメニューから。
    print("カメラが接続されていません。")
    print("現在の設定ではuse_arucoはFalseです。")
    print("カメラを使用せずに開始します。")

else:
    use_aruco = True
    print("カメラの接続が確認されました。")

scan_count = 0
count = 0


running = True
while running:
    
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

    scan_count += 1
    scan_manager(scan_count, mode)#setmodeの時だけ妥協でカメラの画像を出力する。

    #タイマーを使いまわすためにここに配置。
    count_timer.draw()


    if mode == "set":
        if count_checker():
            mode = "menu"

    elif mode == "menu":
        player = (0, 0)
        for i in player_marker_list:
            if i.marker_id == 6:#marker_idの6は"赤足.png"
                player = i
                player.draw(mode)

        p(player.now_point,"n")
        
        for i in menu_entity_list:
            i.draw()

            if i.move:
                push_checker(player_chege_point(player.now_point),i)

    elif mode == "play":
        if scan_count % int(fps*circle_time) == 0:
            make_circle()

        if scan_count % fps == 0:
            if count_timer.count():
                mode = "end"
                count_timer.reset(10)

        for i in comment_list:
            i.draw()
        

    elif mode == "end":
        count_result.draw()

        if count_timer.count():
            mode = "menu" 


    for e in set_entity_list:
        e.draw(mode)



    screen.blit(back_surface,(0,0))

    screen.blit(middle_surface,(0,0))

    screen.blit(front_surface,(0,0))

    pygame.display.update() 

pygame.quit()
print("ウィンドウを閉じました。")

sys.exit()#ごり押し処理　修正