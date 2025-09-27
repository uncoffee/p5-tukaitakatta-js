import numpy
def change_x(A, B, now):
    x1, y1 = A
    x2, y2 = B
    now_X, now_y = now

    return ((x1 - x2) / (y1 - y2)) * (now_y-y1) + x1
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

    return (y1 - y2) / (now_y - y1)

def keisan(A,B,now):
    x1, y1 = A
    x2, y2 = B
    now_x, now_y = now


    return (x1 - x2) / (y1 - y2) * now_y




#left_top:(np.float32(71.0), np.float32(108.0))
#right_top:(np.float32(365.25), np.float32(73.25))
#right_bottom:(np.float32(396.75), np.float32(263.5))
#left_bottom:(np.float32(42.0), np.float32(123.75))
#player:(np.float32(189.25), np.float32(243.0))


left_top = 38,213
right_top = 262,214
right_bottom = 337,402
left_bottom = 46,441
player = 150,336
#numpy.abs(int((left_top[0] - right_top[0])))},{int(player[0])}",{numpy.abs(int((left_top[0] - right_top[0]))) - int(player[0])
print(f"個人計算:{(keisan(left_bottom,left_top,player) - keisan(right_bottom,right_top,player)) / player[0]}")

実験 = ()
print(f"実験:{実験}")

print(f"チェンジx左{int(change_x(left_top,left_bottom,player))},右{int(change_x(right_top,right_bottom,player))}")
print



mouse_x = 1280 / ((int(change_x(left_top,left_bottom,player)) - int(change_x(right_top,right_bottom,player))) / (player[0] - int(change_x(left_top,left_bottom,player))))
print(mouse_x)

mouse_y = 720 / change_y(left_bottom,left_top,player)
print(mouse_y)

