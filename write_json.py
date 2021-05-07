import json, datetime

file_json = 'templates/data.json'

var = {}

class templates:
    def __init__(self, categories:list):
        self.categories = categories  #lisa tupli
        self.translated = {a:b for a,b in self.categories} #lista słownkiów zrobionych z tupli

    def searcher(self, lista: list, look_for):
        '''Sprwdza, czy jest zmienna przeznaczona na ten dzień'''
        for a in lista:  #przeszukaj liste postów
            if look_for in a:
                #zwróc index danej daty
                return True 
        return False #jeśli nie ma takiej

    def add_post(self, title, category, content):
        '''Dodaje post do pliku json i zwraca w tupli link z tytułem wpisu'''
        with open(file_json, 'r+', encoding='utf-8') as f:
            data = json.loads(f.read())
            posts = data['posts']

            today = datetime.datetime.now().strftime('%m-%Y')
            founded = self.searcher(posts, today)

            if not founded:
                posts[today] = []   #jak nie znalazłeś, dodaj słownik do danego dnia
        
            #przypisz liste dzisiejszych postów tej zmiennej
            today_posts = posts[today]  
            #stwórz nowy słownik z tymi danymi
            var['title'] = title
            now_time = datetime.datetime.now().strftime('%H:%M')
            var['time'] = now_time
            var['category'] = category
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
            link = "date/{}/{}".format(today, amount-1)
            return link

    def send_to_wordpress(self, title, content):
        '''zapisuje tekst do dict wordpress'''
        with open(file_json, 'r+', encoding='utf-8') as f:
            data = json.loads(f.read())
            posts = data['posts']['wordpress']

            today = datetime.datetime.now().strftime('%m-%Y')
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
        with open(file_json, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def give_links(self, tuple_list):
        output = []
        for a, b in reversed(tuple_list):
            line = f'\n<li><a class="story-link" href="{a}">{b}</a></li>'
            output.append(line)
        return output

    def give_filtered(self, filter_name):
        filtered_posts = []
        with open(file_json, 'r', encoding='utf-8') as js:
            data = json.loads(js.read())
            js.close()
        posts = data['posts']    
        
        #posts -> wszystkie posty
        #date -> string, którym przeszukuje posty
        #index -> numer postu w liście postów z danego dnia
        #post -> konkretny post
        
        for date in posts:  #dla daty w postach   
            for index in range(len(posts[date])): #dla postów wg indeksów
                post = posts[date][index]
                if post['category'] == filter_name:  #jeśli tytuł posta
                    link = f'/stories/date/{date}/{index}'
                    filtered_posts.append((link, post['title']))
        print('\n', filtered_posts)
        return filtered_posts

    def change_source(self, show_by=None, first_place=None, idx=None):
        '''Tworzy listę z odnośnikami lub stronę z historią'''

        with open(file_json, 'r', encoding='utf-8') as js:
            data = json.loads(js.read())
            js.close()

        def edit_source(file: str, translate: dict):  
            '''edytuje wskazany plik według danego słownika'''
            with open(f'templates/{file}', 'r', encoding='utf-8') as html:
                source = str(html.read())
                for a, b in translate.items():
                    source = source.replace(a,b)
                html.close()
                return source

        if show_by == None:
            title = "Wybierz sortowanie"
            links = [('date', "Według daty"), ('filtr', "Według kategorii")]
            content = self.give_links(links)
            translate = {'^title^' : str(title), "^content^":''.join(content)}
            return edit_source('hrefs_template.html', translate)

        if show_by == 'filtr': #Jeżeli filtrujemy
            if first_place is not None:  #wyświetlanie postów z daną kategorią
                print('category')
                posts = self.give_filtered(first_place)
                title = f"Posty z kategorii: {self.translated[first_place]}"
                content = self.give_links(posts)
                translate = {'^title^' : str(title), "^content^":''.join(content)}
                return edit_source("hrefs_template.html", translate)
            print("Filtered")
            posts = self.categories     #Wyświetlanie możliwych Kategorii
            title = "Filtry do wyboru"
            content = self.give_links(posts)
            translate = {'^title^' : str(title), "^content^":''.join(content)}
            return edit_source("hrefs_template.html", translate)

        if show_by == "date":
            
            #Tworzy listę hiperłączy z historiami podzielonymi według dnia
            posts = data['posts'] 
            if first_place is None:
                print("Date None")
                hrefs = [a for a in posts]
                title = 'Wszystkie możliwe dni do wyboru'
                content = []

                #łączy daty w pary w pary  <a href=date>date</a>
                tuple_list = [(a,a) for a in hrefs]
                content = self.give_links(tuple_list)
                translate = {'^title^' : str(title), "^content^":''.join(content)}
                
                return edit_source('hrefs_template.html', translate)

            #Zwraca wszystkie wpisy ze wskazanego dnia
            posts = data['posts'][first_place]

            if idx is None:
                print("IDX none")
                
                titles = []
                hrefs = []

                #w razie gdyby się powtarzały dodaje im numerek, np '#2'
                for a in posts:
                    title = a['title']
                    if title in titles:
                        title += f' #{titles.count(title)+1}'
                    hrefs.append(title)
                    titles.append(title)

                title = first_place
                content = []
                
                #numeruje linki i łączy je w tuple
                links = [(a,b) for a,b in enumerate(hrefs)] 

                #tworzy linki segregując je od najstarszych do najnowszych 
                content = self.give_links(links)
                translate = {'^title^' : str(title), "^content^":''.join(content)}
                
                return edit_source('hrefs_template.html', translate)

            #zwraca wskazany post
            print("post")
            post = posts[idx]
            title = post['title']
            content = post['content']
            translate = {'^title^' : str(title), "^content^":"<p>{}</p>".format(content), "\r\n":'</p><p>', "<<":"&lt;&lt", ">>":"&gt;&gt"}

            return edit_source('clear_template.html', translate)

    def create_template(self, **args):                
        '''Tworzy plik html do wyświetlenia'''
        print(args)
        show_by = args.get('show_by')
        first_place = args.get('first_place')
        idx = args.get('idx')

        with open('templates/output_index.html', 'w', encoding='utf-8') as f:
            string = self.change_source(show_by, first_place, idx)
            f.write(string)
            f.close()

    def post_template(self, title, category, content):
        with open('templates/post.html', 'r', encoding='utf-8') as html:
            source = html.read()
            html.close()
            link = self.add_post(title, category, content)

        translate = {'^title^' : str(title), "^link^":link}
            
        for a,b in translate.items():
            source = source.replace(a,b)
    
        with open('templates/output_index.html', "w", encoding="utf-8") as f:
            f.write(source)
            f.close()


categories = [
    ("swiadectwo", "Świadectwo"),
    ("modlitwa", "Modlitwa"),
    ("historia", "Historia"),
    ("inne", "Inne")
    ]