import flask, os
os.environ['TZ'] = 'Europe/Warsaw'
from write_json import templates
from kill import kill_process

app = flask.Flask(__name__, static_url_path='')

#static folder -> style.css
#templates -> html files

try:
    os.chdir(os.path.dirname(__file__))
except:
    pass

categories = [
    ("swiadectwo", "Świadectwo"),
    ("modlitwa", "Modlitwa"),
    ("historia", "Historia"),
    ("cytat", "Cytat"),
    ('changes', 'Możliwe poprawki'),
    ("inne", "Inne")
    ]

html = templates(categories)

with open("pid.txt", "w+") as pid_file:
    pid_file.write(str(os.getpid()))
    pid_file.close()

@app.after_request
def check_status(response):
    status = response.status_code
    if status == 500:
        kill_process()
    return response

@app.route('/uploads/<path:filename>')
def download_files(filename):
    print('file', filename)
    return  flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
def index():   
    global categories
    return flask.render_template('index.html', head=html.return_head(), categories = categories)

@app.route('/', methods=['POST'])
def index_post():
    title = flask.request.form['story-title'],
    title = ''.join(map(str, title))
    category = flask.request.form['category']
    content = flask.request.form['story-content']
    print("Selected:", category)

    if '#word' in str(title):
        title = title[6:]
        amount = html.send_to_wordpress(title, content)
        return flask.redirect(flask.url_for('post_wordpress', amount=amount))
    
    html.post_template(title, category, content)       
    return flask.redirect(flask.url_for('post_normal'))
    
@app.route('/thanks/<amount>')
def post_wordpress(amount):
    return flask.render_template('output_index.html', dane=amount, head=html.return_head())

@app.route('/thanks')
def post_normal():
    return flask.render_template('output_index.html', head=html.return_head())

@app.route('/about')
def about():
    return flask.render_template("about.html", head=html.return_head())


@app.route('/stories/json')
def stories_json():
    file_string = html.give_dict()
    return flask.jsonify(file_string)

@app.route('/published_post')
def last_post():
    link = flask.globals.request.args.get('link')
    pieces = link.split('/')

    stories_idx = pieces.index('stories') #check on which place is "stories" keyword.
    href = '/'+'/'.join(pieces[stories_idx:stories_idx+4])+'/'
    html.change_link(href)
    return "Coś mam"

@app.route('/stories')
@app.route('/stories/')
def choose_sorting():
    html.create_template(sorting_style = True)
    return flask.render_template('output_index.html', head=html.return_head())

@app.route('/stories/<show_by>/')
@app.route('/stories/<show_by>/<first_place>/')
@app.route('/stories/<show_by>/<first_place>/<int:idx>/')
def stories_date(show_by=None, first_place=None, idx=None):
    html.create_template(show_by=show_by, first_place=first_place, idx=idx)
    return flask.render_template('output_index.html', head=html.return_head())

@app.route('/welcome')
def welcome():
    return flask.render_template("welcome_post.html", head = html.return_head())


@app.route('/data')
def data():
  with open('data.json', 'r', encoding='utf-8') as f:
    data = f.read()
    f.close()
  return data

@app.route('/update')
def update():
    from os import system
    system('~/historie/update.sh')
    return "<h1>OK</h1>"
    
app.run(host='0.0.0.0', debug=True, port=5000)