import json, datetime

file_name = 'templates/data.json'

var = {}

class templates:
    def searcher(self, lista: list, look_for):
        '''Sprwdza, czy jest zmienna przeznaczona na ten dzień'''
        for a in lista:  #przeszukaj liste postów
            if look_for in a:
                #zwróc index danej daty
                return True 
        return False #jeśli nie ma takiej

    def add_post(self, title,content):
        '''Dodaje post do pliku json i zwraca w tupli link z tytułem wpisu'''
        with open(file_name, 'r+', encoding='utf-8') as f:
            data = json.loads(f.read())
            posts = data['posts']

            today = datetime.datetime.now().strftime('%d-%m-%Y')
            founded = self.searcher(posts, today)

            if not founded:
                posts[today] = []   #jak nie znalazłeś, dodaj słownik do danego dnia
        
            #przypisz liste dzisiejszych postów tej zmiennej
            today_posts = posts[today]  
            #stwórz nowy słownik z tymi danymi
            var['title'] = title
            now_time = datetime.datetime.now().strftime('%H:%M')
            var['time'] = now_time
            var['saved'] = "False"
            var['content'] = content
            #dodaj ten słownik do listy dzisiejszych postów
            today_posts.append(var)
            #przejdź na sam początek i wyczyść plik
            f.seek(0) 
            f.truncate()
            #ensure_ascii -> kodowanie znaków do utf-8
            #indent -> ilość spacji przy wcięciach
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()   
            
            
            amount = len(today_posts)
            link = "{}/{}".format(today, amount-1)
            return link

    def send_to_wordpress(self, title, content):
        '''zapisuje tekst do dict wordpress'''
        with open(file_name, 'r+', encoding='utf-8') as f:
            data = json.loads(f.read())
            posts = data['posts']['wordpress']

            today = datetime.datetime.now().strftime('%d-%m-%Y')
            founded = self.searcher(posts, today)

            if not founded:
                posts[today] = [] #jak nie znalazłeś, dodaj słownik do danego dnia 

            #przypisz liste dzisiejszych postów tej zmiennej
            today_posts = posts[today]
            #stwórz nowy słownik z tymi danymi
            var['title'] = title
            now_time = datetime.datetime.now().strftime('%H:%M')
            var['time'] = now_time
            var['content'] = content
            #dodaj ten słownik do listy dzisiejszych postów
            today_posts.append(var)
            #przejdź na sam początek i wyczyść plik
            f.seek(0) 
            f.truncate()

            #ensure_ascii -> kodowanie znaków do utf-8
            #indent -> ilość spacji przy wcięciach
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()    

            amount = len(today_posts)
            path = "{}/{}".format(today, amount-1)
            return path

    def give_dict(self):
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def change_source(self, date=None, idx = None):
        '''Tworzy listę z odnośnikami lub stronę z historią'''
        with open(file_name, 'r', encoding='utf-8') as js:
            data = json.loads(js.read())
            js.close()

        #Tworzy listę hiperłączy z historiami podzielonymi według dnia
        posts = data['posts'] 
        if date is None:
            hrefs = [a for a in posts]
            title = 'Wszystkie możliwe dni do wyboru'
            content = []

            with open('templates/hrefs_template.html', 'r', encoding='utf-8') as f:
                source = f.read()
                f.close()

            for a in reversed(hrefs):
                line = f'<li><a class="link" href="{a}">{a}</a></li>'
                content.append(line)
            translate = {'^title^' : str(title), "^content^":'\n'.join(content)}
            
            for a,b in translate.items():
                source = source.replace(a,b)

            return source


        #Zwraca wszystkie wpisy ze wskazanego dnia
        posts = data['posts'][date]

        if idx is None:
            
            titles = []
            hrefs = []

            #w razie gdyby się powtarzały dodaje im numerek, np '#2'
            for a in posts:
                title = a['title']
                if title in titles:
                    title += f' #{titles.count(title)+1}'
                hrefs.append(title)
                titles.append(title)

            title = date
            content = []
            
            #numeruje linki i łączy je w tuple
            to_reverse = [(a,b) for a,b in enumerate(hrefs)] 

            #tworzy linki segregując je od najstarszych do najnowszych 
            for a, b in reversed(to_reverse):
                line = f'<li><a class="story-link" href="{a}">{b}</a></li>'
                content.append(line)
            translate = {'^title^' : str(title), "^content^":'\n'.join(content)}
            
            with open('templates/hrefs_template.html', 'r', encoding='utf-8') as f:
                source = f.read()
                for a,b in translate.items():
                    source = source.replace(a,b)
                f.close()

            return source

        #zwraca wskazany post
        post = posts[idx]
        title = post['title']
        content = post['content']
        translate = {'^title^' : str(title), "^content^":content, "\r\n":'<br>&nbsp;&nbsp; ', "<<":"&lt;&lt", ">>":"&gt;&gt"}

        with open('templates/clear_template.html', 'r', encoding='utf-8') as html:
            source = str(html.read())
            for a, b in translate.items():
                source = source.replace(a,b)
            html.close()

        return source

    def create_template(self, date=None, idx=None):
        with open('templates/output_index.html', 'w', encoding='utf-8') as f:
            string = self.change_source(date, idx)
            f.write(string)
            f.close()

    def post_template(self, title, content):
        with open('templates/post.html', 'r', encoding='utf-8') as html:
            source = html.read()
            html.close()
            link = self.add_post(title, content)

        translate = {'^title^' : str(title), "^link^":link}
            
        for a,b in translate.items():
            source = source.replace(a,b)
    
        with open('templates/output_index.html', "w", encoding="utf-8") as f:
            f.write(source)
            f.close()