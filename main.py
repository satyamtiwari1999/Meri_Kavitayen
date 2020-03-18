from flask import Flask, render_template
from flask import request
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/kya_chahta_hu')
def chahta_hu():
    return render_template('kya_chahta_hu.html')


@app.route('/bachpan')
def bachpan():
    return render_template('bachpan.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/public', methods=["POST", "GET"])
def public():
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
            txt.write(str(name) + '\n@@\n' + str(poem_title) + '\n@@\n' + str(poem) + '\n@@\n')
            txt.close()
    # f = open('public_content.txt', 'a')
    # f.write("\n@@")
    # f.close()
    file = open('public_content.txt', 'r')
    count = 0
    current = []
    for line in file:
        if line == '\n':
            continue
        if line.split() == ['@@']:
            count += 1
            rem = count % 3
            if rem == 1:
                names.append(current[0])
                current = []
            elif rem == 2:
                headings.append(current[0])
                current = []
            elif rem == 0:
                poems.append(current)
                current = []
        else:
            current.append(line)
    file.close()
    return render_template('public_post.html', title=title, names=names, poems=poems,
                           titles=headings, length=len(names))


@app.route('/author')
def author():
    return render_template('author.html')


app.run(debug=True)
