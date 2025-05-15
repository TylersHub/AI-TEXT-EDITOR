

from flask import Flask, render_template
#app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')


########################################

@app.route('/<string:page_name>/')
def render_static(page_name):
   return render_template('%s.html' % page_name)

########################################

@app.route('/ahoy')
def ahoy():
   return 'ahoy!'

########################################

@app.route('/galaxy')
def galaxy():
    return app.send_static_file('galaxy.html')

########################################

@app.route('/')
def home():
   return render_template('home.html')


########################################

if __name__ == '__main__':
   app.run(threaded=True, port=5000)
