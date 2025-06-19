import time
import board
import busio
import adafruit_ds1307
from RPLCD.i2c import CharLCD

# Initialize I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# RTC setup
rtc = adafruit_ds1307.DS1307(i2c)

# LCD setup (change 0x27 if your LCD has a different I2C address)
lcd = CharLCD('PCF8574', 0x27)

# ✅ Set RTC time (run once, then comment this line out)
# rtc.datetime = time.struct_time((2025, 4, 9, 10, 42, 0, 0, -1, -1))

print("Time written to RTC. Displaying on LCD...")

# ✅ Display time loop
while True:
    t = rtc.datetime
    date_str = "{:04d}-{:02d}-{:02d}".format(t.tm_year, t.tm_mon, t.tm_mday)
    time_str = "{:02d}:{:02d}:{:02d}".format(t.tm_hour, t.tm_min, t.tm_sec)
    
    lcd.clear()
    lcd.write_string(date_str)
    lcd.crlf()
    lcd.write_string(time_str)
    
    time.sleep(1)
