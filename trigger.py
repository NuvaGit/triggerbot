import keyboard
import time
import ctypes
import PIL.ImageGrab
import winsound 
 
S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 70
TRIGGER_KEY = "ctrl + alt"
 
class triggerBot():
    def __init__(self):
        self.toggled = False
 
    def toggle(self):
        self.toggled = not self.toggled
 
    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
 
    def validate(self, r_list, g_list, b_list):
        found = False
        for pixel in  range(0, len(r_list)):
            if self.approx(r_list[pixel], g_list[pixel], b_list[pixel]):
                found = True
        return found
 
    def approx(self, r, g ,b):
        valid = 0
        if PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE:
            valid += 1
            if PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE:
                valid += 1
                if PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE:
                    valid += 1
        return valid == 3
 
    def scan(self):
        start_time = time.time()
        r_list = []
        g_list = []
        b_list = []
        grabzone = 15
        pmap = PIL.ImageGrab.grab(bbox=(S_HEIGHT/2-grabzone, S_WIDTH/2-grabzone, S_HEIGHT/2+grabzone, S_WIDTH/2+grabzone))
        for x in range(0, grabzone*2):
            for y in range(0, grabzone*2):
                r, g, b = pmap.getpixel((x,y))
                r_list.append(r)
                g_list.append(g)
                b_list.append(b)
        if self.validate(r_list, g_list, b_list):
            self.click()
            print("Bot's reaction time : {} ms".format(int((time.time() - start_time)*1000)))
            time.sleep(0.1)
 
if __name__ == "__main__":
    print("MACRAV alpha Build v0.2")
    print("Features :\n -- ",TRIGGER_KEY," : Activate Trigger Bot")
 
    bot = triggerBot()
    while True:
        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            if bot.toggled:
                print("Activated")
                winsound.Beep(440, 75)
                winsound.Beep(700, 100)
            else:
                print("Deactivated")
                winsound.Beep(440, 75)
                winsound.Beep(200, 100)
            while keyboard.is_pressed(TRIGGER_KEY):
                pass
        if bot.toggled:
            bot.scan()