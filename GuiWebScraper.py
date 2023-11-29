import pyautogui as pag
from time import sleep

print("Give window focus to any browser, starting automation in: ")
for i in range(10, 0, -1):
    print(f'{i}')
    sleep(1)

class GuiWebScraper:


    def start():
        pag.PAUSE = 2
        pag.press('tab')
        pag.write('Florida')
        pag.press('tab', presses=2, interval=0.25)
        pag.write('Jackson')
        pag.press('down', presses=2, interval=0.25)
        pag.press('enter')  

        # Move mouse and click on 
        #pag.moveTo(900, 560)  # Property Search
        pag.moveTo(900, 620)  # View Map
        pag.click()

        print("Moving to Search Box")
        pag.moveTo(1615, 100) # Search Box 
        pag.click()
        pag.write('2924 Green')
        pag.press('down', interval=1)
        pag.press('enter', interval=1)
     
        print("Moving to Report Tab")
        pag.moveTo(309, 160) # Report Tab
        pag.click()

        print("Moving to 1st item in Result Tab search")
        pag.moveTo(420, 313)
        pag.click()

        #pag.press('tab', presses=3, interval=0.25)
        #pag.press('enter') 
        
if __name__ == "__main__":
    GuiWebScraper.start()