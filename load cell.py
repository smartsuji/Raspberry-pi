import RPi.GPIO as GPIO
import time
from hx711 import HX711
from RPLCD.i2c import CharLCD

# -------------------------
# GPIO & HX711 Setup
# -------------------------
DT = 5    # HX711 Data pin
SCK = 6   # HX711 Clock pin

hx = HX711(DT, SCK)
GPIO.setwarnings(False)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)

hx.reset()
hx.tare()  # Tare to zero with empty scale
print("Tared. Place a known weight.")

# -------------------------
# LCD Setup (16x2, I2C Address 0x27)
# -------------------------
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A02',
              auto_linebreaks=True, backlight_enabled=True)

lcd.clear()
lcd.write_string("Taring... Done")
time.sleep(2)

# -------------------------
# Calibration
# -------------------------
input("Place known weight & press Enter...")
reading = hx.get_weight(5)
print(f"Reading: {reading}")
known_weight = float(input("Enter known weight in grams: "))

ref_unit = reading / known_weight
hx.set_reference_unit(ref_unit)
print(f"Reference unit set: {ref_unit:.2f}")

lcd.clear()
lcd.write_string("Calibrated!")
time.sleep(2)

# -------------------------
# Display weight
# -------------------------
try:
    while True:
        weight = max(0, hx.get_weight(5))
        print(f"Weight: {weight:.2f} g")

        lcd.clear()
        lcd.write_string("Weight:")
        lcd.crlf()
        lcd.write_string("{:.2f} g".format(weight))

        hx.power_down()
        hx.power_up()
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
    lcd.clear()
    lcd.write_string("Goodbye!")
