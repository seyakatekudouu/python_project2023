from flask import Flask, render_template
import random

app = Flask(__name__)

# レイアウトサンプル
@app.route('/')
def sample_top():
    return render_template('index.html')

@app.route('/list')
def sample_list():
    book_list = [
        ('よく分かるPython', '佐々木 磨生', 'MCL出版', 200),
        ('LinuC 詳解', '細川 潤哉', 'MCL出版', 400),
        ('Servlet 入門', '高橋 洋平', 'ジョビ出版', 250),
        ('Flask 入門', '高橋 洋平', 'ジョビ出版', 150),
        ('よく分かるUML', '細川 潤哉', 'MCL出版', 220),
        ('Django 入門', '佐々木 磨生', '龍澤出版', 350),
    ]
    return render_template('list.html', books=book_list)

@app.route('/register')
def sample_register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)