import json, datetime

file_name = 'templates/data.json'

var = {}

class json_files:
    def searcher(self, lista: list, look_for):
        '''Sprwdza, czy jest zmienna przeznaczona na ten dzień'''
        for a in lista:  #przeszukaj liste postów
            if look_for in a:
                #zwróc index danej daty
                return True 
        return False #jeśli nie ma takiej

    def add_post(self, title,content):
        '''Dodaje post do pliku json'''
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
            counter = 0 
            for a in posts:
                counter += len(posts[a])
            return counter


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

            #do policzenia postów
            counter = 0 
            for a in posts:
                counter += len(posts[a])
            return counter

    def give_dict(self):
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    
    def change_source(self, date, idx = None):
        '''Tworzy listę z odnośnikami lub stronę z historią'''
        with open(file_name, 'r', encoding='utf-8') as js:
            data = json.loads(js.read())
            js.close()

        posts = data['posts'][date]
        if idx is None:
            hrefs = [a['title'] for a in posts]
            title = date
            content = []

            for a, b in enumerate(hrefs):
                line = f'<li><a href="./{a}">{b}</a></li>'
                content.append(line)
            translate = {'^title^' : str(title), "^content^":'\n'.join(content)}
            
            with open('templates/hrefs_template.html', 'r', encoding='utf-8') as f:
                source = f.read()
                for a,b in translate.items():
                    source = source.replace(a,b)
                f.close()

            return source


        post = posts[idx]
        title = post['title']
        content = post['content']
        translate = {'^title^' : str(title), "^content^":content}

        with open('templates/clear_template.html', 'r', encoding='utf-8') as html:
            source = str(html.read())
            for a, b in translate.items():
                source = source.replace(a,b)
            html.close()

        return source

with open('templates/output_index.html', 'w', encoding='utf-8') as f:
    string = json_files().change_source('05-04-2021')
    f.write(string)