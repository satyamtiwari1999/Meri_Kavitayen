from flask import Flask, render_template
from flask import request, redirect, url_for
app = Flask(__name__)
# redirect and url for are useful
# now defing the usersids and passwords
user_name = []
pass_word = []
login = [False, 'not_done']


def print_from_file(names, headings, poems):
    file = open('public_content.txt', 'r')
    current = []
    for line in file.readlines():
        line = line.strip()
        if len(line) > 0:
            line_list = line.split()
            if line_list[0] == 'name':
                if len(current) != 0:
                    poems.append(current)
                    current = []
                line = ' '.join(line.split()[1:])
                names.append(line)
            elif line_list[0] == 'title':
                line = ' '.join(line.split()[1:])
                headings.append(line)
            else:
                current.append(line.upper())
        else:
            current.append('\n')
    if len(current) != 0:
        poems.append(current)
        current = []
    file.close()
    return


def fill_from_file():
    ''' fills the user_name and pass_word '''
    f = open('user.txt')
    count = 0
    for line in f.readlines():
        line = line.strip().split()
        print(line, len(line))
        if line[0] == 'U' and line[1] not in user_name:
            user_name.append(line[1])
            count = 1
        elif line[0] == 'P' and count == 1:
            pass_word.append(line[1])
            count = 0


@app.route('/signup', methods=["POST", "GET"])
def signup():
    ''' will help user to sign up '''
    username, password = '', ''
    if request.method == "POST":
        username = str(request.form['id'])
        # print(username)
        password = str(request.form['password'])
        confirm_password = str(request.form['confirm_password'])
        if username in user_name:
            return render_template('signup.html', error="User Already Exists")
        else:
            if (password == confirm_password and len(username) > 0 and
                    len(username.split()) == 1):
                if len(password) <= 4:
                    error = "Password must have atleast 5 characters"
                    return render_template('signup.html', error=error)
                # feed the username and pass_word in user.txt
                f = open('user.txt', 'a')
                f.write('U ' + username + '\n')
                f.write('P ' + password + '\n')
                f.close()
                print('done')
                login[1] = 'signed_up'
                return redirect(url_for('login_page'))
            else:
                error = "Username can't be empty or have spaces"
                return render_template('signup.html', error=error)
    return render_template('signup.html', error="")


@app.route('/')
@app.route('/login', methods=['GET', "POST"])
def login_page():
    fill_from_file()
    print(user_name)
    print(pass_word)
    login[0] = False
    if login[1] == 'signed_up':
        error = 'Sign up successful'
        action = ''
    else:
        error = ''
        action = 'Please Try Again'
    count = 0  # to check if user found or not
    checked = False  # see if user has tried to login once or not
    if request.method == 'POST':
        login[1] = 'not_done'
        if request.form['button'] == 'login':
            checked = True
            username = str(request.form['id'])
            password = str(request.form['password'])
            for ind, user in enumerate(user_name):
                print(ind)
                if user == username:
                    count += 1
                    if pass_word[ind] == password:
                        login[0] = True
                        break
                    else:
                        error = 'Wrong Username or(and) Password'
                        break
        else:
            login[1] = 'not_done'
            return redirect(url_for('signup'))
    if count == 0 and checked:
        action = 'You need to Sign Up First'
        return render_template('login.html', error='Username Not Found!',
                               action=action)
    elif login[0]:
        return render_template('index.html', error='', action='')
    else:
        return render_template("login.html", error=error, action=action)


@app.route('/home')
def home():
    if login[0]:
        return render_template('index.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/kya_chahta_hu')
def chahta_hu():
    if login[0]:
        return render_template('kya_chahta_hu.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/bachpan')
def bachpan():
    if login[0]:
        return render_template('bachpan.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/upload')
def upload():
    if login[0]:
        return render_template('upload.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/public', methods=["POST", "GET"])
def public():
    if login[0]:
        names = []
        headings = []
        poems = []
        title = "Public Post"
        if request.method == "POST":
            name = str(request.form['poet']).upper()
            poem_title = str(request.form['head']).upper()
            poem = request.form['poem']
            # now saving the contents in a file.
            if len(name) > 0 and len(poem) > 0 and len(poem_title) > 0:
                txt = open('public_content.txt', 'a')
                txt.write('name ' + str(name) + '\n' + 'title ' +
                          str(poem_title) + '\n' + str(poem).upper() + '\n')
                txt.close()
        # f = open('public_content.txt', 'a')
        # f.write("\n@@")
        # f.close()
        print_from_file(names, headings, poems)

        return render_template('public_post.html', title=title, names=names,
                               poems=poems, titles=headings, length=len(names))
        return render_template('login.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/author')
def author():
    if login[0]:
        return render_template('author.html')
    else:
        return redirect(url_for('login_page'))


app.run(debug=True)
