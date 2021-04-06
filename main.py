import flask, os
import write_json as json_file
import datetime

app = flask.Flask(__name__, static_folder='static')
#static folder -> style.css
#templates -> html files

@app.route('/', methods=['GET'])
def index():   
    return flask.render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    title = flask.request.form['story-title'],
    title = ''.join(map(str, title))
    content = flask.request.form['story-content']

    if '#word' in str(title):
        title = title[6:]
        amount = json_file.send_to_wordpress(title, content)
        return flask.redirect(flask.url_for('post_wordpress', amount=amount))
    
    json_file.add_post(title, content)       
    return flask.redirect(flask.url_for('post_normal'))
    

@app.route('/thanks/<amount>')
def post_wordpress(amount):
    return flask.render_template('post_wordpress.html', dane=amount)


@app.route('/thanks')
def post_normal():
    return flask.render_template('post.html')

@app.route('/stories/json')
def stories_json():
    file_string = json_file.give_dict()
    return flask.jsonify(file_string)

app.run(host='0.0.0.0', debug=True, port=5000)