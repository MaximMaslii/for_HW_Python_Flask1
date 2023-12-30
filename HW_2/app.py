from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'JohnDoe' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        response = make_response(render_template('welcome.html', username=username))
        response.set_cookie('username', username)
        response.set_cookie('email', email)

        return response

@app.route('/logout', methods=['POST'])
def logout():

    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    response.delete_cookie('email')

    return response

if __name__ == '__main__':
    app.run(debug=True)
