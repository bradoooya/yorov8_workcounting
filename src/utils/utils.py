# -*- coding: utf-8 -*-
#!/usr/bin/python
from time import sleep, gmtime, strftime, time
import datetime
import smbus
from threading import Lock

class LCD:
    """
    I2C接続のLCDディスプレイを制御するクラス。
    
    Attributes:
        I2C_ADDR (int): I2Cアドレス。デフォルトは0x27。
        LCD_WIDTH (int): LCDの表示幅。デフォルトは16文字。
        LCD_CHR (int): 文字モードのフラグ。
        LCD_CMD (int): コマンドモードのフラグ。
        LCD_LINE_1 (int): 1行目のアドレス。
        LCD_LINE_2 (int): 2行目のアドレス。
        LCD_BACKLIGHT (int): バックライト制御のフラグ。
        ENABLE (int): Enableピンのフラグ。
        E_PULSE (float): Enableピンのパルス時間。
        E_DELAY (float): パルス間の遅延時間。
        bus (SMBus): I2C通信のためのSMBusインスタンス。
    """
    def __init__(self, i2c_addr=0x27, lcd_width=16):
        # 初期設定
        self.I2C_ADDR = i2c_addr
        self.LCD_WIDTH = lcd_width

        self.LCD_CHR = 1
        self.LCD_CMD = 0

        self.LCD_LINE_1 = 0x80
        self.LCD_LINE_2 = 0xC0

        self.LCD_BACKLIGHT = 0x08

        self.ENABLE = 0b00000100

        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        self.bus = smbus.SMBus(1)

        self.lcd_init()

    def lcd_init(self):
        """LCDの初期化を行うメソッド"""
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        """
        LCDにデータを送信するためのメソッド。
        
        Args:
            bits (int): 送信するデータ。
            mode (int): コマンドモードか文字モードを指定。
        """
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        """
        Enableピンを制御してLCDにデータを送信するメソッド。
        
        Args:
            bits (int): 送信するデータ。
        """
        sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        """
        指定された行に文字列を表示するメソッド。
        
        Args:
            message (str): 表示する文字列。
            line (int): 表示する行を指定。
        """
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def clear(self):
        """LCDの画面をクリアし、バックライトをオフにするメソッド。"""
        self.lcd_byte(0x01, self.LCD_CMD)
        self.LCD_BACKLIGHT = 0x00

class LCDClock:
    """
    LCDに現在の時刻を表示するクラス。
    
    Attributes:
        lcd (LCD): LCDインスタンス。
    """
    def __init__(self, lcd):
        self.lcd = lcd

    def display_time(self):
        """時刻をLCDに表示するメソッド。"""
        while True:
            local_time = datetime.datetime.now()
            self.lcd.lcd_string(strftime("%Y.%m.%d (%a)", gmtime()), self.lcd.LCD_LINE_1)
            self.lcd.lcd_string(local_time.strftime("%H:%M"), self.lcd.LCD_LINE_2)
            sleep(1)

            local_time = datetime.datetime.now()
            self.lcd.lcd_string(strftime("%Y.%m.%d (%a)", gmtime()), self.lcd.LCD_LINE_1)
            self.lcd.lcd_string(local_time.strftime("%H %M"), self.lcd.LCD_LINE_2)
            sleep(1)
            
class LCDMessage():
    """
    メッセージをLCDに表示するクラス。
    
    Attributes:
        lcd (LCD): LCDインスタンス。
        current_message (str): 現在表示されているメッセージ。
        lock (Lock): メッセージ更新のための排他制御。
    """
    def __init__(self, lcd):
        self.lcd = lcd
        self.current_message = ""
        self.lock = Lock()
        
    def display_message(self, message, display_duration=5):
        """
        指定されたメッセージを一定期間LCDに表示するメソッド。
        
        Args:
            message (str): 表示するメッセージ。
            display_duration (int): メッセージを表示する秒数。
        """
        with self.lock:
            self.current_message = message
            end_time = time() + display_duration

            while time() < end_time:
                # 分割して表示
                line_1 = self.current_message[:self.lcd.LCD_WIDTH]
                line_2 = self.current_message[self.lcd.LCD_WIDTH:self.lcd.LCD_WIDTH*2]

                self.lcd.lcd_string(line_1, self.lcd.LCD_LINE_1)
                self.lcd.lcd_string(line_2, self.lcd.LCD_LINE_2)
                
                sleep(0.1)  # 短い間隔で更新をチェック

    def update_message(self, new_message):
        """
        現在のメッセージを更新するメソッド。
        
        Args:
            new_message (str): 新しいメッセージ。
        """
        with self.lock:
            self.current_message = new_message
        
            

if __name__ == "__main__":
    # メイン処理
    try:
        lcd = LCD() # LCDのインスタンス作成
        clock = LCDClock(lcd) # LCDClockのインスタンス作成
        print('Start:' + str(datetime.datetime.now()))
        clock.display_time()  # 時刻表示の開始
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear() # 終了時にLCDをクリア
