# -*- coding: utf-8 -*-
#!/usr/bin/python
from time import sleep, gmtime, strftime, time
import datetime
import smbus
from threading import Lock

class LCD:
    def __init__(self, i2c_addr=0x27, lcd_width=16):
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
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def clear(self):
        self.lcd_byte(0x01, self.LCD_CMD)
        self.LCD_BACKLIGHT = 0x00

class LCDClock:
    def __init__(self, lcd):
        self.lcd = lcd

    def display_time(self):
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
    def __init__(self, lcd):
        self.lcd = lcd
        self.current_message = ""
        self.lock = Lock()
        
    def display_message(self, message, display_duration=5):
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
        with self.lock:
            self.current_message = new_message
        
            

if __name__ == "__main__":
    try:
        lcd = LCD()
        clock = LCDClock(lcd)
        print('Start:' + str(datetime.datetime.now()))
        clock.display_time()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()
