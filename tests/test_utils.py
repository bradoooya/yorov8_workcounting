import pytest
from unittest.mock import MagicMock
from time import sleep

from src.utils.utils import LCD, LCDMessage

# from your_module import LCD, LCDMessage

@pytest.fixture
def lcd():
    lcd = LCD()
    lcd.lcd_init = MagicMock()
    lcd.lcd_byte = MagicMock()
    lcd.lcd_string = MagicMock()
    lcd.clear = MagicMock()
    return lcd

@pytest.fixture
def lcd_message(lcd):
    return LCDMessage(lcd)

def test_initialization(lcd):
    lcd.lcd_init.assert_called_once()

def test_display_message(lcd_message, lcd):
    message = "Test Message"
    lcd_message.display_message(message, display_duration=1)

    expected_line_1 = message[:lcd.LCD_WIDTH]
    expected_line_2 = message[lcd.LCD_WIDTH:lcd.LCD_WIDTH * 2]

    lcd.lcd_string.assert_any_call(expected_line_1, lcd.LCD_LINE_1)
    lcd.lcd_string.assert_any_call(expected_line_2, lcd.LCD_LINE_2)

def test_update_message(lcd_message, lcd):
    initial_message = "Initial Message"
    new_message = "New Message"

    lcd_message.display_message(initial_message, display_duration=2)
    sleep(1)  # 1秒待機して途中でメッセージを更新
    lcd_message.update_message(new_message)

    expected_line_1 = new_message[:lcd.LCD_WIDTH]
    expected_line_2 = new_message[lcd.LCD_WIDTH:lcd.LCD_WIDTH * 2]

    lcd.lcd_string.assert_any_call(expected_line_1, lcd.LCD_LINE_1)
    lcd.lcd_string.assert_any_call(expected_line_2, lcd.LCD_LINE_2)

def test_clear(lcd_message, lcd):
    lcd_message.lcd.clear()
    lcd.clear.assert_called_once()
