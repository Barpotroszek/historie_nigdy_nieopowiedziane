# %%
from logging import captureWarnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import math
import time
import glob
import subprocess as sub
from dotenv import load_dotenv

load_dotenv()

os.chdir(os.path.dirname(__file__))

class insta_bot():
    def __init__(self, link):
        self.link = link
        self.size = 800
        options = Options()
        mobile_emulation = {
            "deviceMetrics": { "width": self.size, "height": self.size, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
            }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument(f"--window-size={self.size}{self.size}")
        self.bot = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.variabeles_to_template = {}


    def check_posts(self):
        '''Opening page you've given'''
        #self.bot.get(input('Podaj link do strony: '))
        self.bot.get(self.link)
        time.sleep(3)
        self.bot.execute_script('document.styleSheets[0].cssRules[23].style.removeProperty("padding")')
        
        get_text = lambda id: self.bot.execute_script(f'return document.getElementById("{id}").innerHTML')
        
        title = get_text('story-title')[7:]
        category = get_text('story-category')
        self.variabeles_to_template['date'] = get_text('story-date')
        self.variabeles_to_template['title'] = title
        self.variabeles_to_template['category'] = category
        self.variabeles_to_template['link'] = self.link
        self.variabeles_to_template['tag_title'] = title.lower().replace(' ', '_')
        self.variabeles_to_template['lower_category'] = category.lower().replace(' ', '_')

        to_print = [f"{a} -> {b}" for a,b in self.variabeles_to_template.items()]
        print('\n'.join(to_print))

 
 
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
        print("Screen saved!")

    def upload_photo_by_autoit(self, path: str):
        '''Uploading photo'''
        import autoit as ai
        print("Uploading by autoit")
        #print(path)
        self.bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/div[3]/div[2]/a[2]').click()
        time.sleep(3)
        while True:
            try:
                ai.win_activate('Otwieranie')
                ai.control_send('Otwieranie', 'Edit1', os.path.join(os.path.dirname(__file__), path))
                ai.control_click('Otwieranie', 'Button1')
                time.sleep(2)
                print('Powinno być wgrane')
                break
            except:
                print("By AutoIt: Nie wiem co się stało")
                break

    def upload_photos_by_input(self, files: list):
        bot = self.bot
        sended = False
        if len(files) ==  1:
            input_field = bot.find_element_by_xpath('//input[@value="photo"]')
        elif len(files) > 1:
            input_field = bot.find_element_by_xpath('//input[@value="carousel"]')
        for file in files:
            def upload_it():
                global sended
                for a in range(3):
                    try:
                        input_field.send_keys(file)
                        print('Sended by input')
                        sended = True
                        break
                    except:
                        print('By input: something gone wrong')
                        time.sleep(5)
            upload_it()
            if not sended:
                self.upload_photo_by_autoit(file)
            
            while not bot.execute_script("return getComputedStyle(document.getElementById('loading-overplay')).display") == 'none':
                time.sleep(3)

    def publish_post(self, username, password):
        '''Publishing photos with caption'''
        bot = self.bot
        #login to site latelysocial
        bot.get('https://latelysocial.com/auth/login')
        login = bot.find_element_by_name('email')
        passwd = bot.find_element_by_name('password')
        login.clear()
        passwd.clear()
        login.send_keys(username)
        passwd.send_keys(password)
        bot.find_element_by_xpath('//button[text()="Login"]').click()
        
        while not bot.current_url == 'https://latelysocial.com/dashboard':
            time.sleep(5)

        #go to site intended for instagram publishing 
        bot.get('https://latelysocial.com/instagram/post')
        time.sleep(4)
        try:
            bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[2]/ul/li/a').click()
        except:
            #bot.find_element_by_xpath('//div[text()="historie.nigdy.nieopowiedziane"]')
            print('By div')
        try:
            bot.execute_script('document.getElementById("root").remove()')
        except:
            pass

        time.sleep(5)

        #load photos
        dirname = lambda path: os.path.dirname(path)
        path = os.path.join(dirname(__file__), 'photos')
        files = glob.glob(f'{path}\*.jpg')

        if len(files) ==  1:
            bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/div[1]/div/a[1]').click()
            #input_field = bot.find_element_by_xpath('//input[@value="photo"]')
        elif len(files) > 1:
            bot.find_element_by_xpath("//a[@href='#carousel']").click()
            #input_field = bot.find_element_by_xpath('//input[@value="carousel"]')
        
        time.sleep(2)
        self.upload_photos_by_input(files)

        #add a caption           
        caption_place = bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/div[7]/div[2]/div[1]')
        caption_place.click()
        print("Dodawanie opisu")
        with open('opis.txt', 'r', encoding='utf-8') as f:
            caption_text = f.read()
            f.close()

        caption_place.send_keys(caption_text)
        os.system('pause')

        #Post Now
        try:
            bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/button[1]').click()
        except:
            print("Nie mogę kliknąć...")
            input()
        time.sleep(30)
        os.system('pause')
        return

        #close prompts
        bot.find_element_by_xpath('//a[text()="x"]').click()
    
    def create_caption(self):
        '''Tworzenie opisu'''
        print('Tworzenie opisu')
        with open('template_opis.txt', 'r', encoding='utf-8') as f:
            template = f.read()
            f.close()

        formated_text = template.format(**self.variabeles_to_template)
        
        with open('opis.txt', 'w', encoding='utf-8') as f:
            f.write(formated_text)
            f.close()

    def clean_file_manager(self):
        '''Usuwanie starych plików'''
        bot = self.bot
        print('Clean files')
        bot.get('https://latelysocial.com/file_manager')
        time.sleep(3)
        bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/div/div/div/form/div/div[2]/div[1]/button').click()
        bot.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/div/div/div/form/div/div[2]/div[1]/div/button[4]').click()
        time.sleep(2)
        bot.find_element_by_xpath('//*[@id="show_del"]/button[1]').click()

path = os.path.join('photos', 'photo 0.jpg')

bot = insta_bot(input("Podaj link do wpisu: "))
'''bot.check_posts()
sub.run('pause', shell=True)
bot.create_caption()

bot.make_shot()
'''
bot.publish_post('tester_bot@int.pl', os.getenv('PASSWORD'))
bot.clean_file_manager()

sub.run('pause', shell=True)

"""
try:
    raise KeyboardInterrupt()
except:
    pass"""
# %%
