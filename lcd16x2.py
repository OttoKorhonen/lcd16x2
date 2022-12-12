import RPi.GPIO as GPIO
from time import sleep

'''
https://datasheetspdf.com/pdf-file/519148/CA/LCD-1602A/1
https://datasheetspdf.com/pdf-file/1110199/TINSHARP/TC1602A-21T/1
'''


class Lcd16x2:

    def __init__(self, data_pin_7: int, data_pin_6: int, data_pin_5: int, data_pin_4: int, e_pin: int, rs_pin: int):
        self.data_pin_7 = data_pin_7  # data pins are used to write on the display
        self.data_pin_6 = data_pin_6
        self.data_pin_5 = data_pin_5
        self.data_pin_4 = data_pin_4
        self.e_pin = e_pin  # chip enable signal, pin is called everytime pin value is changed
        # register selector, DDRAM (display data ram) or CGRAM (character generator ram)
        self.first_line = 0x80
        self.second_line = 0xC0
        self.rs_pin = rs_pin
        self.display_width = 16
        self.display_height = 2
        self.pulse = 0.0005
        self.delay = 0.0005

    def setup(self):
        '''
        setup pins and board
        '''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin_7, GPIO.OUT)
        GPIO.setup(self.data_pin_6, GPIO.OUT)
        GPIO.setup(self.data_pin_5, GPIO.OUT)
        GPIO.setup(self.data_pin_4, GPIO.OUT)
        GPIO.setup(self.e_pin, GPIO.OUT)
        GPIO.setup(self.rs_pin, GPIO.OUT)
        self.set_data_for_display(0x28, 0)
        self.set_data_for_display(0x0c, 0)
        self.set_data_for_display(0x01, 0)

        sleep(self.delay)

    def enable_chip(self):
        '''
        function enables chip signal
        '''
        sleep(self.delay)
        GPIO.output(self.e_pin, 1)
        sleep(self.pulse)
        GPIO.output(self.e_pin, 0)
        sleep(self.delay)

    def set_high_bits(self, bit: int):

        GPIO.output(self.data_pin_4, 0)
        GPIO.output(self.data_pin_5, 0)
        GPIO.output(self.data_pin_6, 0)
        GPIO.output(self.data_pin_7, 0)
        if bit & 0x10 == 0x10:
            GPIO.output(self.data_pin_4, 1)
        if bit & 0x20 == 0x20:
            GPIO.output(self.data_pin_5, 1)
        if bit & 0x40 == 0x40:
            GPIO.output(self.data_pin_6, 1)
        if bit & 0x80 == 0x80:
            GPIO.output(self.data_pin_7, 1)

        self.enable_chip()

    def set_low_bits(self, bit: int):

        GPIO.output(self.data_pin_4, 0)
        GPIO.output(self.data_pin_5, 0)
        GPIO.output(self.data_pin_6, 0)
        GPIO.output(self.data_pin_7, 0)
        if bit & 0x01 == 0x01:
            GPIO.output(self.data_pin_4, 1)
        if bit & 0x02 == 0x02:
            GPIO.output(self.data_pin_5, 1)
        if bit & 0x04 == 0x04:
            GPIO.output(self.data_pin_6, 1)
        if bit & 0x08 == 0x08:
            GPIO.output(self.data_pin_7, 1)

        self.enable_chip()


    def set_data_for_display(self, bit: int, value: int):
        '''this function sets data in registers'''
        GPIO.output(self.rs_pin, value)
        self.set_high_bits(bit)
        self.set_low_bits(bit)

    def set_cursor_to_right(self):
        '''function sets cursor one step to the right'''
        self.set_data_for_display(0x14, 0)

    def set_cursor_to_left(self):
        '''function sets cursor on step to the left'''
        self.set_data_for_display(0x10, 0)

    def scroll_message_to_right(self):
        '''function scrolls the entire message to the right'''
        self.set_data_for_display(0x1c, 0)

    def scroll_message_to_left(self):
        '''function scrolls the entire message to the left'''
        self.set_data_for_display(0x18, 0)

    def clear_screen(self):
        '''function clears screen'''
        self.set_data_for_display(0x01, 0)

    def write_on_display(self, message: str, line: int):
        '''function writes message on the display'''

        self.set_data_for_display(line, 0)

        '''Python ord() function returns the Unicode code from a given character. '''
        for character in message:
            self.set_data_for_display(ord(character), 1)


# if __name__ == '__main__':
#     l = Lcd16x2(12, 16, 18, 22, 24, 26)
#     l.setup()
#     print('on')
#     try:

#         while True:
#             l.write_on_display('Hello World!', l.first_line)
#             sleep(1)

#     except KeyboardInterrupt:
#         pass

#     finally:
#         l.clear_screen()
#         GPIO.cleanup()
