import flask, os
from write_json import templates
import datetime

app = flask.Flask(__name__, static_url_path='')
#static folder -> style.css
#templates -> html files
html = templates()

@app.route('/', methods=['GET'])
def index():   
    return flask.render_template('index.html')

@app.route('/uploads/<path:filename>')
def download_files(filename):
    print('file', filename)
    return  flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['POST'])
def index_post():
    title = flask.request.form['story-title'],
    title = ''.join(map(str, title))
    content = flask.request.form['story-content']

    if '#word' in str(title):
        title = title[6:]
        amount = html.send_to_wordpress(title, content)
        return flask.redirect(flask.url_for('post_wordpress', amount=amount))
    
    html.post_template(title, content)       
    return flask.redirect(flask.url_for('post_normal'))
    

@app.route('/thanks/<amount>')
def post_wordpress(amount):
    return flask.render_template('output_index.html', dane=amount)


@app.route('/thanks')
def post_normal():
    return flask.render_template('output_index.html')

@app.route('/stories/json')
def stories_json():
    file_string = html.give_dict()
    return flask.jsonify(file_string)

@app.route('/stories')
def stories_slash():
    return flask.redirect('/stories/')


@app.route('/stories/')
def stories_():
    html.create_template()
    return flask.render_template('output_index.html')

@app.route('/stories/<date>/')
def stories_date(date):
    html.create_template(date, None)
    return flask.render_template('output_index.html')

@app.route('/stories/<date>/<int:idx>/')
def stories_idx(date, idx):
    html.create_template(date, idx)
    return flask.render_template('output_index.html')

app.run(host='0.0.0.0', debug=True, port=5000)