# -*- coding: utf-8 -*-
#!/usr/bin/python
from time import sleep
import traceback

from src.utils import utils


if __name__ == "__main__":
    try:
        lcd =  utils.LCD()
        # message = "Hello, World! This is a test message."
        message = "Hello, World!"
        lcd_pred = utils.LCDMessage(lcd)
        print('Start')
        lcd_pred.display_message(message, display_duration=10)
        sleep(5)
        lcd_pred.display_message("New!", display_duration=10)
        
    except KeyboardInterrupt:
        traceback.print_exc()
        pass
    except Exception as e:
        traceback.print_exc()
        print(e)
    except ValueError as e:
        print(e)
    finally:
        lcd.clear()
   