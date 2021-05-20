# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import os
import math
import time
import glob
import subprocess as sub
from dotenv import load_dotenv

load_dotenv()

os.chdir(os.path.dirname(__file__))

class insta_bot():
    def __init__(self):
        self.size = 800
        options = Options()
        mobile_emulation = {
            "deviceMetrics": { "width": self.size, "height": self.size, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
            }

        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        options.add_argument(f"--window-size={self.size}{self.size}")
        self.bot = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    def check_posts(self):
        '''Opening page you've given'''
        self.bot.get(input('Podaj link do strony: '))
        self.bot.execute_script('document.styleSheets[0].cssRules[23].style.removeProperty("padding")')

    def make_shot(self):
        '''Making screenshot of the page'''
        bot = self.bot

        #opróżnij ten folder -> usuń wcześniejsze zdjęcia
        for f in glob.glob("photos/*.jpg", recursive=False):
            os.system(f"del \"{f}\"")

        bot.execute_script("to_share()")
        height = bot.execute_script("return document.body.scrollHeight")
        move_by = self.size-50
        os.system('pause')

        for a in range(math.ceil(height / move_by)):
            bot.save_screenshot(f"photos/photo {a}.jpg")
            time.sleep(0.7)
            bot.execute_script(f"window.scrollBy(0,{move_by})")
        time.sleep(3)
        print("Done")

    def login(self, login, passwd):
        '''Opening Instagram and loging on it'''
        bot = self.bot
        bot.get("https://instagram.com/")
        bot.find_element_by_xpath('//button[text()="Akceptuję wszystko"]').click()
        time.sleep(1)
        try:
            bot.find_element_by_xpath('//button[text()="Zaloguj się"]').click()
        except:
            pass
        def complete_it():
            global username, password
            try:
                username = bot.find_element_by_name('username')
                password = bot.find_element_by_name('password')
            except:
                complete_it()
        complete_it()
        username.clear()
        password.clear()
        username.send_keys(login)
        password.send_keys(passwd+'\n')
        time.sleep(3)
        bot.find_element_by_xpath('//*[text()="Nie teraz"]').click()
        try:
            time.sleep(3)
            bot.find_element_by_xpath('//*[text()="Anuluj"]').click()
        except:
            pass

    def upload_photo(self, path: str):
        '''Uploading photo'''
        import autoit as ai
        print(path)
        time.sleep(3)
        while True:
            try:
                ai.win_activate('Otwieranie')
                ai.control_send('Otwieranie', 'Edit1', os.path.join(os.path.dirname(__file__), path))
                ai.control_click('Otwieranie', 'Button1')
                time.sleep(2)
                print("here")
                ai.control_click('Otwieranie', 'Button1')

            except:
                print("break")
                break
        
    def send(self, path):
        '''Publishing photo on Instagram'''
        bot = self.bot
        time.sleep(2)
        bot.find_element_by_xpath('//*[@data-testid="new-post-button"]').click()

        self.upload_photo(path)

        time.sleep(4)
        bot.find_element_by_xpath('//*[text()="Dalej"]').click()
        time.sleep(3)
        describe = bot.find_element_by_xpath('//textarea[@placeholder="Dodaj opis..."]')

        with open("photos/opis.txt", "r", encoding='utf-8') as f:
            describe.send_keys(f.read())
            f.close()
        bot.find_element_by_xpath('//button[text()="Udostępnij"]').click()

    def __del__(self):
        #self.bot.quit()
        pass

path = os.path.join('photos', 'photo 0.jpg')

bot = insta_bot()
bot.check_posts()
bot.make_shot()

bot.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))
bot.send(path)

sub.run('pause', shell=True)

"""
try:
    raise KeyboardInterrupt()
except:
    pass"""
# %%
