import hid
import time
import sys
import math

# --- Wiiリモコンの標準的なVID/PID ---
# 多くのシステムでWiiリモコンは以下のIDで認識されます。
# Nintendo Vendor ID: 0x057e
# Wii Remote (Standard): 0x0306 (多くのシステムでのPID)
TARGET_VID = 0x057e
TARGET_PID = 0x0306

# Wiiリモコン固有の定数
REPORT_MODE_ACCEL = 0x31 # ボタン + 加速度センサー (6バイトレポート)
HID_OUTPUT_REPORT_ID = 0x12 # データレポート形式設定のためのコントロールレポートID

# ----------------------------------------------------
# ⚠️ 注意: このコードを実行する前に、以下の手順が必要です
# 1. PC (Windows/Mac/Linux) のBluetooth設定でWiiリモコンをペアリングする。
#    - SYNCボタンを押す (WindowsではPINコードを求められたら「何も入力せず」次へ)。
# 2. 接続が確立され、OSがデバイスをHIDデバイスとして認識した状態にする。
# ----------------------------------------------------

count = 0

def calculate_accelerometer(report):
    """
    Wiiリモコンのレポート0x31から加速度値を抽出・計算する (簡略版)。
    
    レポート形式 0x31: [Report ID (0x31), Button_L, Button_H, Accel_X_Low, Accel_Y_Low, Accel_Z_Low]
    加速度データは10ビットで、ボタンバイトの上位ビットに分散している。
    
    Args:
        report (list): hidapiから読み取ったバイトデータのリスト。
        
    Returns:
        tuple or None: (raw_x, raw_y, raw_z) または None。
    """
    # レポートが短い、またはレポートIDが一致しない場合は処理しない
    # 実際には、レポートID 0x31 のレポートの長さは 6 バイトですが、
    # OSやBluetoothスタックによっては、より長いレポートとして送られてくることがあるため、len(report)のチェックを緩めます。
    if not report or report[0] != REPORT_MODE_ACCEL or len(report) < 6:
        return None

    # ボタンデータ (上位2ビットが加速度の上位ビットを含む)
    button_L = report[1]
    button_H = report[2]
    
    # 加速度データの抽出 (下位8ビット)
    # hidapiのread()はレポートIDを含めて返すため、インデックスは0から始まります。
    accel_x_low = report[3]
    accel_y_low = report[4]
    accel_z_low = report[5]

    # 加速度データの上位2ビットを取得し、10ビットデータに結合
    # X軸の上位2ビットは Button_L (report[1]) のビット6と7
    accel_x_high = (button_L & 0x60) >> 5 # bit 6, 5 
    # Y軸の上位2ビットは Button_H (report[2]) のビット6と7
    accel_y_high = (button_H & 0x60) >> 5 # bit 6, 5
    # Z軸の上位2ビットは Button_L (report[1]) のビット4と3
    accel_z_high = (button_L & 0x18) >> 3 # bit 4, 3

    # 10ビットデータの復元 (Wiiリモコンの非公式プロトコルに基づく)
    # 実際には、(下位8ビット << 2) | 上位2ビット の組み合わせで10ビットを構成します。
    raw_x = (accel_x_low << 2) | accel_x_high
    raw_y = (accel_y_low << 2) | accel_y_high
    raw_z = (accel_z_low << 2) | accel_z_high

    # 生データ (0-1023) を返す
    return raw_x, raw_y, raw_z

def calculate_jump_magnitude(raw_x, raw_y, raw_z, zero_g=(512, 512, 512), one_g_sensitivity=140):
    """
    生データから加速度の合計の大きさ (Magnitude) を計算します。
    
    Args:
        raw_x, raw_y, raw_z (int): 10ビットの生加速度データ。
        zero_g (tuple): ゼロg (無重力状態) での各軸のバイアス値 (キャリブレーション値)。
        one_g_sensitivity (int): 1gあたりの生データの変化量。
        
    Returns:
        float: g単位での加速度の合計の大きさ (Magnitude)。
    """
    # 1. ゼロgからの差分 (g単位への変換)
    ax_g = (raw_x - zero_g[0]) / one_g_sensitivity
    ay_g = (raw_y - zero_g[1]) / one_g_sensitivity
    az_g = (raw_z - zero_g[2]) / one_g_sensitivity
    
    # 2. ベクトルのノルム (合計の大きさ) を計算
    # Magnitude = sqrt(ax^2 + ay^2 + az^2)
    magnitude = math.sqrt(ax_g**2 + ay_g**2 + az_g**2)
    
    return magnitude

def communicate_with_wiimote(vid, pid):
    """
    Wiiリモコンに接続し、加速度センサーデータを読み取る。
    """
    device = None
    
    # 接続確認のため、デバイスを列挙します
    devices = hid.enumerate(vid, pid)
    if not devices:
        print(f"エラー: 指定されたVID/PID (0x{vid:04x}/0x{pid:04x}) のWiiリモコンが見つかりません。")
        print(" -> OSのBluetooth設定でリモコンが接続済みか確認してください。")
        return

    try:
        # 1. デバイスのオープン
        path = devices[0]['path']
        device = hid.device()
        device.open_path(path)
        
        print("接続成功！")
        print(f" 製品名: {device.get_product_string()}")
        print(f" メーカー名: {device.get_manufacturer_string()}")
        
        # 2. ノンブロッキングモードに設定 (ポーリングループを可能にするため)
        device.set_nonblocking(True)
        
        # 3. コントロールレポートの送信 (加速度センサーレポート0x31を有効化)
        # 🚨 hidapiのwrite()は先頭にレポートIDを要求するため、0x00を追加します。
        # コマンド: [0x00, 0xA2, 0x12, 0x00, 0x31]
        # command_data = [0x00, 0xA2, HID_OUTPUT_REPORT_ID, 0x00, REPORT_MODE_ACCEL]
        
        bytes_written = device.write([0x12, 0x00, 0x31])  # 例：LED1点灯
        print(f"\nデバイスに {bytes_written} バイトのレポート形式設定コマンドを送信しました。")
        
        # 4. データ読み取りループ
        # ⚠️ 注意: 正確なジャンプ判定には、キャリブレーション (ゼロg値の測定) が必要です。
        # ここでは、簡略化のためゼロgを (512, 512, 512) と仮定しています。
        ZERO_G_CALIBRATION = (512, 512, 512) 
        ONE_G_SENSITIVITY = 250 # 1gあたりの生データ変化量 (約512±250が目安)
        JUMP_THRESHOLD_HIGH = 1.0 # 踏み切り判定用のしきい値 (g)
        JUMP_THRESHOLD_LOW = 0.5  # 空中判定用のしきい値 (g)
        
        print("\nデータ読み取りを開始します... (Ctrl+Cで停止)")
        print(f"ジャンプ判定基準: 踏み切り > {JUMP_THRESHOLD_HIGH}g, 空中 < {JUMP_THRESHOLD_LOW}g")
        print("-" * 50)
        
        jump_state = "IDLE" # 状態: IDLE, TAKEOFF, AIRBORNE
        
        while True:
            # read() は最大レポートサイズ (Wiiリモコンの標準レポートは21バイトなど) を指定します。
            # レポートID 0x31 は 6 バイトですが、常に最大長で読み込みます。
            report = device.read(22) 
            
            if report:
                report_id = report[0]
                
                # ユーザーが求めている0x31レポート（加速度センサーデータ）かどうかをチェック
                if report_id == REPORT_MODE_ACCEL:
                    accel_data = calculate_accelerometer(report)
                    
                    if accel_data:
                        raw_x, raw_y, raw_z = accel_data
                        print(raw_x, raw_y, raw_z)
                        
                        # 加速度の合計の大きさを計算
                        magnitude = calculate_jump_magnitude(
                            raw_x, raw_y, raw_z, 
                            zero_g=ZERO_G_CALIBRATION, 
                            one_g_sensitivity=ONE_G_SENSITIVITY
                        )
                        
                        # 状態遷移によるジャンプ判定 (誤判定防止のため)
                        new_state = jump_state
                        if jump_state == "IDLE" and raw_y >= 680:
                            # 待機中 -> 高いピークを検出 -> 踏み切り状態へ
                            new_state = "TAKEOFF"
                            jump_g = raw_y

                        # elif jump_state == "TAKEOFF" and raw_y <= jump_g - raw_y <= 480:
                        #     # 空中状態 -> 大きな衝撃を検出 -> 着地 -> 待機状態へ
                        #     new_state = "IDLE"
                        #     print("--- [LANDED] --- 着地を検出しました。")
                        
                        jump_state = new_state
                        
                        # コンソール出力
                        # if count > 0:
                        #     print(
                        #         f"X:{raw_x:4d} | Y:{raw_y:4d} | Z:{raw_z:4d} | "
                        #         f"Mag:{magnitude:.2f}g | State: {jump_state}"
                        #     )
                    
                # 別のレポート（例: 0x20, 0x21, 0x30 など）を受信した場合は無視し、コンソールを汚さない
                else:
                    # print(f"他のレポートを受信 (ID: 0x{report_id:02x}) - 無視します。")
                    pass

            
            # ノンブロッキングモードのため、CPUを占有しないよう短いウェイトを入れます。
            time.sleep(0.02)
            
    except KeyboardInterrupt:
        print("\nユーザーによって停止されました。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}", file=sys.stderr)
    finally:
        # 5. デバイスのクローズ
        if device:
            device.close()
            print("\n接続をクローズしました。")

if __name__ == "__main__":
    communicate_with_wiimote(TARGET_VID, TARGET_PID)