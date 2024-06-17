from machine import Pin, I2C
from gpio_lcd import GpioLcd
from time import sleep

i2c = I2C(0, scl = Pin(1), sda = Pin(0), freq = 400000)

lcd = GpioLcd(rs_pin = Pin(2),
              enable_pin = Pin(3),
              d4_pin = Pin(4),
              d5_pin = Pin(5),
              d6_pin = Pin(6),
              d7_pin = Pin(7),
              num_lines = 2, num_columns = 16)

button1 = Pin(14, Pin.IN, Pin.PULL_UP)
button2 = Pin(15, Pin.IN, Pin.PULL_UP)

frequency = 87.0
tolerance = 0.001

def setFrequency(freq):
    if((freq < 87) or (freq > 108)):
        return false
    return setChannel(round(freq * 20))

def setChannel(channel):
    if((channel < 1740) or (channel > 2160)):
        return false
    buf1 = bytearray(1)
    buf1[0] = ((int(channel) & 0x1FE) >> 1)
    buf2 = bytearray(1)
    buf2[0] = ((int(channel) >> 9) | 0x68)
    buf3 = bytearray(1)
    buf3[0] = (((int(channel) & 0x001) << 7) | 0x01)
    buf4 = bytearray(1)
    buf4[0] = 0x34
    i2c.writeto_mem(0x3E, 0x00, buf1)
    i2c.writeto_mem(0x3E, 0x01, buf2)
    i2c.writeto_mem(0x3E, 0x02, buf3)
    i2c.writeto_mem(0x3E, 0x04, buf4)

lcd.move_to(2, 0)
lcd.putstr('<---FM-TR--->')
lcd.move_to(3, 1)
setFrequency(frequency)
lcd.putstr(str(frequency))
lcd.move_to(9, 1)
lcd.putstr('MHz')

while True:
    if(button1.value() == 0 and frequency > 87.0):
        sleep(0.15)
        frequency = frequency - 0.1
        setFrequency(frequency);
        if(frequency < 100.0):
            lcd.move_to(3, 1)
            lcd.putstr(str(round(frequency, 2)))
        if((frequency - 100.0) >= -tolerance): 
            lcd.move_to(3, 1)
            lcd.putstr(str(round(frequency, 2)))
    if(button2.value() == 0 and frequency < 108.0): 
        sleep(0.15);
        frequency = frequency + 0.1
        setFrequency(frequency)
        if(frequency < 100.0):
            lcd.move_to(3, 1)
            lcd.putstr(str(round(frequency, 2)))
    
        if((frequency - 100.0) >= -tolerance):
            lcd.move_to(3, 1)
            lcd.putstr(str(round(frequency, 2)))
     