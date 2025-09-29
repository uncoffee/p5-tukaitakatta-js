img_size = int(input("画像の大きさを半角で入力 : "))

magnification = img_size / 180
print(f"xのズレ:{-90 * magnification} , yのズレ{-50 * magnification}")
