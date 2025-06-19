import time
import board
import busio
import adafruit_ds1307

# Initialize I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the RTC
rtc = adafruit_ds1307.DS1307(i2c)

# ========================
# ✅ Set the RTC time here
# ========================
# Format: (year, month, day, hour, minute, second, weekday, yearday, isdst)
rtc.datetime = time.struct_time((2025, 4, 9, 10, 44, 0, 0, -1, -1))  # Set this to your current time

print("Time has been written to RTC.")

# ========================
# ✅ Read back the time
# ========================
while True:
    t = rtc.datetime
    print("RTC Time: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t.tm_year, t.tm_mon, t.tm_mday,
        t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1)
