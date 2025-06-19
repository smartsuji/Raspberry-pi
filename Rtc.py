import time
import board
import busio
import adafruit_ds1307
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO

# === GPIO Setup ===
LED_PIN = 17     # You can change this GPIO pin
BUZZER_PIN = 18  # Change as per your circuit

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# === I2C & RTC Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds1307.DS1307(i2c)

# === LCD Setup ===
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A02',
              auto_linebreaks=True, backlight_enabled=True)

# === Optional: Set RTC time ===
# rtc.datetime = time.struct_time((2025, 4, 9, 8, 0, 0, 0, -1, -1))

print("Displaying RTC time and controlling buzzer/LED...")

try:
    while True:
        t = rtc.datetime
        hour = t.tm_hour

        # Format time and date
        date_str = "{:04d}-{:02d}-{:02d}".format(t.tm_year, t.tm_mon, t.tm_mday)
        time_str = "{:02d}:{:02d}:{:02d}".format(hour, t.tm_min, t.tm_sec)

        # Display on LCD
        lcd.clear()
        lcd.write_string(date_str)
        lcd.crlf()
        lcd.write_string(time_str)

        # Check time range and control LED & buzzer
        if (8 <= hour < 9) or (12 <= hour < 13) or (19 <= hour < 20):
            GPIO.output(LED_PIN, GPIO.HIGH)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    lcd.clear()
    GPIO.cleanup()
