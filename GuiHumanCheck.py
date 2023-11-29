import pyautogui as pag
from time import sleep
import random

print("Give window focus to the Automated Safari browser, starting automation in: ")
for i in range(10, 0, -1):
    print(f'{i}')
    sleep(1)

while(True):
    pag.PAUSE = random.uniform(0.10, 0.5)
    # Move mouse and click on 
    pag.moveTo(1855, 610, duration=random.uniform(0.25, 0.75))
    sleep(random.uniform(0, 1))
    pag.click()
    pag.moveTo(random.uniform(900, 3000), random.uniform(300, 900))