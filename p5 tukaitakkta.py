#"C:/Program Files/Python311/python.exe" pythonのインストール先
#pip install 打ち込むの忘れずにね！

#歩いたら　オノマトペだそうね！

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
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))


#pygameの中で使う変数の宣言


#変更可

fps = 100#一秒間に起きる画面更新の回数

split_varue = 20 #円が出てくるマス目の細かさ

comment_file_list = ["good.png"] #コメントのバリエーション
comment_list = []

comment_size = 200#コメントのサイズを指定する



edge_range = 3 #外周と生成円の距離HTMLのpaddingのノリ

#変更不可

for filename in comment_file_list:
    image = pygame.image.load(filename)
    scale = comment_size / image.get_width()
    newimage = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    comment_list.append(newimage)

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

del_target_comment = "nan"

# 3. ウィンドウのタイトルを設定
pygame.display.set_caption("初めてのPygameウィンドウ")


backcolor_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)
circle_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
comment_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

cursor_surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
cursor_list = []

class cursor:
    def __init__(self,cursor_point):
        self.x,self.y = cursor_point
        self.clear = 200

    def draw(self):
        cursor_surface.fill((0,0,0,0))
        pygame.draw.circle(cursor_surface,(255,255,255,self.clear),(self.x,self.y),25)
        self.clear -= 100
        if self.clear <= 0:
            self.clear = 0
            


x_list = []


team = 4

def backcolor(h,s,v):

    h/=100
    s/=100
    v/=100

    r,g,b = colorsys.hsv_to_rgb(h,s,v)

    return r*255,g*255,b*255

    #bpsh　「100秒間に～」の間隔 後で単位を調整したい　下のコメントチェック
default_size = 50#最終円のサイズ指定
class make_circle:
    def __init__ (self,x,y,bps):
        self.alive = True
        self.age = 0
        self.size = default_size * 4
        self.main_size = self.size
        self.clear = 0
        self.x = x
        self.y = y
        self.bps = bps
        self.color = [255,255,255] #円の色の初期値
        self.move = True
        #self.lo = lo

        #print(f"self.bps  {self.bps}")

    
    def update(self):
        temp = self.bps * fps

        if self.move:#デフォルトサイズどうする?仮にsize 25とする
            sa = self.main_size - default_size
            #temp = self.bps * fps
            #print(f"temp  {temp}")
            if self.size >= default_size:
                self.size -= sa / temp
            else:
                self.size = default_size


            if self.clear <= 200:
                self.clear += 200 / temp 
            else:
                self.clear = 200

            self.age += 1
            if self.age / temp >= 1:
                self.move = False
                self.age = 0
        else:
            global game_point
            global del_target

            self.age += 1
            if self.age / (fps * 0.1) >= 1:
                if self.clear >= 10:
                    self.clear -= 200 / (fps * 0.1)
                else:
                    self.clear = 0

            if self.alive:
                if abs(self.x - mouse_x) <= default_size and abs(self.y - mouse_y ) <= default_size:
                    game_point += 1
                    print(game_point)
                    #self.clear = 255
                    self.alive = False
                    new_comment = tap_comment(self.x,self.y,comment_list[random.randint(0,len(comment_list)-1)])
                    comment_q.append(new_comment)

            if self.clear == 0:
                for i in range(len(circles)):
                    if circles[i] == self:
                        del_target_circle = i
                

    def draw(self):

        #print(f"self_clear  {self.clear}")
        r,g,b = self.color
        
        circle_surface.fill((0,0,0,0))
        #外周円
        pygame.draw.circle(circle_surface,(r,g,b,self.clear),(self.x,self.y),self.size)
        pygame.draw.circle(circle_surface,(r,g,b,0),(self.x,self.y),self.size - 4)
        #内周円
        pygame.draw.circle(circle_surface,(max(0,r-9),max(0,g-64),max(0,b-67),self.clear),(self.x,self.y),default_size)
        #pygame.draw.circle(circle_surface,(0,0,0),(self.x,self.y),default_size)

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



clock = pygame.time.Clock()

def change_x(A, B, now):
    x1, y1 = A
    x2, y2 = B
    now_X, now_y = now

    result = x1 + ((x1 - x2) / (y1 - y2)) * (now_y-y1) + x1
    return result
    #try:
    #     result = x1 + (now_y - y1) * (x1 - x2) / now_y
    #     return result
    # except ZeroDivisionError:
    #     # A と B が水平線上にある場合のフォールバック
    #     return (x1 + x2) / 2

def change_y(A, B, now):
    x1, y1 = A
    x2, y2 = B
    now_x, now_y = now

    result = (y1 - y2) / now_y
    return result

    # try:
    #     result = y1 + now_x * ((y1 - y2) * (x1 - x2)) - ((y1 - y2) / (x1 , x2) * x1)
    #     return result
    # except ZeroDivisionError:
    #     # A と B が垂直線上にある場合のフォールバック
    #     return (y1 + y2) / 2

#ここ4x4だよ！画像4x4にしたんでしょ？って言われるかもね。　　　　　　↓
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

cap = cv2.VideoCapture(0)


left_top = (1,1)
right_top = (2,2)
right_bottom = (3,3)
left_bottom = (4,4)
player = (1,1)

ret, frame = cap.read()
while ret != True:
    print("カメラつながってない")


# 4. ゲームループ
running = True
while running:

    ret, frame = cap.read()
    if ret:
        markers, ids, rejected = aruco_detector.detectMarkers(frame)
        #print(markers)

        for i in range(len(markers)):
            ID = ids[i]
            C1 = markers[i][0][0]
            C2 = markers[i][0][1]
            C3 = markers[i][0][2]
            C4 = markers[i][0][3]
            #ave[x,y]
            ave = (C1[0] + C2[0] + C3[0] + C4[0]) / 4 , (C1[1] + C2 [1] + C3[1] + C4[1]) / 4

            print(ID)

            if ID == 1:
                left_top = ave
                #print(left_top)

            if ID == 2:
                right_top = ave
                #print(right_top)

            if ID == 3:
                right_bottom = ave
                #print(right_bottom)

            if ID == 4:
                left_bottom = ave
                #print(left_bottom)

            if ID == 5:
                player = ave
                #print(player)

    # 5. イベント処理
    
    for event in pygame.event.get():

        #まうすの動きを感知
        #if event.type == pygame.MOUSEMOTION:
            #mouse_x, mouse_y = event.pos
            #print(mouse_x,mouse_y)

        #AI
        if event.type == pygame.QUIT:
            running = False

            

    #fpsフレーム数の取得 clock.get_fps()

    #総フレーム数（カウント
    count += 1
    #print(f"count  {count}")


    #マウスの位置を人がいる位置に置き換えるプログラム（日本語はもともとおかしいわ！
    if count % 100 == 0:
        print(f"left_top:{left_top}")

        print(f"right_top:{right_top}")

        print(f"right_bottom:{right_bottom}")

        print(f"left_bottom:{left_bottom}")

        print(f"player:{player}")
    
    try:
        mouse_x = ((screen.get_width()) / int(change_x(left_top,left_bottom,player) - change_x(right_top,right_bottom,player) / (player[0])))
        mouse_x = int(numpy.abs(mouse_x))
    except ZeroDivisionError:
        mouse_x = 1
    try:
        mouse_y = (screen.get_height() / left_bottom[1] - left_top[1] / player[1])
        mouse_y = int(numpy.abs(mouse_y))
    except ZeroDivisionError:
        mouse_y = 1

    #print(mouse_x)
    #print(mouse_y)




    #背景がゲーミングになる設定 今は使ってない。
    if count % 4 == 0:
        color_count += 1
        if color_count >= 100:
            color_count = 0


    #実験用のマウス追従円
    new_cursor = cursor((mouse_x,mouse_y))
    cursor_list.append(new_cursor)
    for i in cursor_list:
        i.draw()
    if len(cursor_list) > 10:
        cursor_list = cursor_list[-4:]






    #円の座標を設定する
    if  count % 400 == 0 :
        while abs(new_circle_x - last_circle_x) <= split_screen_x * 5 and abs(new_circle_y - last_circle_y) <= split_screen_y * 5:
            new_circle_x = random.randint(edge_range,split_varue - edge_range) * split_screen_x
            new_circle_y = random.randint(edge_range,split_varue - edge_range) * split_screen_y
        new_circle = make_circle(new_circle_x,new_circle_y,3)
        circles.append(new_circle)
        last_circle_x = new_circle_x
        last_circle_y = new_circle_y
        #print(new_circle_x)
        #print(new_circle_y)

        count = 0

    #geming背景にしたい 曲のリズムに合わせて変えたい
    if count % 2 == 0:
        colors = backcolor(color_count % 100,50,50)
        backcolor_surface.fill((0,0,0,150))
        #backcolor_surface.fill((colors[0],colors[1],colors[2],200))
        

    #丸を描画する
    

    # 6. 画面の更新
    for i in circles:
        i.update()
        i.draw()

    #print(len(comment_q))
    for i in comment_q:
        i.update()
        i.draw()

    if del_target_circle != "nan":
        del circles[del_target]
        del_target = "nan"

    if del_target_comment != "nan":
        #print()
        del comment_q[del_target_comment]
        del_target_comment = "nan"
    
    screen.blit(backcolor_surface,(0,0))
    screen.blit(comment_surface,(0,0))
    screen.blit(circle_surface,(0,0))
    screen.blit(cursor_surface,(0,0))

    pygame.display.flip() # または pygame.display.update

    #fpsの値を設定
    clock.tick(fps)

# 7. Pygame の終了処理
pygame.quit()
print("ウィンドウを閉じました。")
