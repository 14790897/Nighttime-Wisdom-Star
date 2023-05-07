from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# 存储用户数据的简单内存结构
users = {}

@app.route('/')
def home():
    return render_template_string('''
<!doctype html>
<html>
  <head>
    <title>Registration System</title>
  </head>
  <body>
    <h1>Welcome to the Registration System</h1>
    <p><a href="{{ url_for('register') }}">Register</a></p>
  </body>
</html>
''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        users[username] = {}
        return redirect(url_for('user_page', username=username))
    return render_template_string('''
<!doctype html>
<html>
  <head>
    <title>Register</title>
  </head>
  <body>
    <h1>Register</h1>
    <form method="post">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>
      <button type="submit">Register</button>
    </form>
  </body>
</html>
''')

@app.route('/user/<username>')
def user_page(username):
    return render_template_string('''
<!doctype html>
<html>
  <head>
    <title>{{ username }}'s Page</title>
  </head>
  <body>
    <h1>Welcome, {{ username }}!</h1>
    <p>Your personalized message will be displayed here.</p>
  </body>
</html>
''', username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
