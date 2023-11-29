import json

from flask import render_template, request, flash, redirect, url_for, session

from core import app


def read_data():
    with open('core/static/articles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_data(data):
    with open('core/static/articles.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def read_users():
    with open('core/static/users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_users(data):
    with open('core/static/users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


@app.route('/')
def index():
    with open('core/static/articles.json', 'r', encoding='utf-8') as file:
        articles = json.load(file)
    return render_template('index.html', articles=articles)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        new_post = {
            "title": request.form['title'],
            "content": request.form['content'],
        }
        data = read_data()
        data.append(new_post)
        write_data(data)
        flash('Пост создан', 'success')
        return redirect(url_for('index'))
    return render_template('post.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = read_users()

        for user in data:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                flash('Успешный вход в профиль', 'success')
                return redirect(url_for('index'))
        flash('Не правильное имя или пароль', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        data = read_users()
        for user in data:
            if user['username'] == username:
                flash('Имя пользователя уже используется!.', 'danger')
                return redirect(url_for('register'))

        
        new_user = {
            "username": username,
            "password": password  
        }
        data.append(new_user)
        write_users(data)

        flash('Регистрация прошла успешно!.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/post_update/<int:post_id>', methods=['GET', 'POST'])
def post_update(post_id):
    articles = read_data()

    if 0 <= post_id < len(articles):
        post = articles[post_id]

        if request.method == 'POST':
            
            post["title"] = request.form['title']
            post["content"] = request.form['content']

            
            write_data(articles)

            flash('Пост обновлен', 'success')
            return redirect(url_for('index', post_id=post_id))

        return render_template('post_update.html', post=post, post_id=post_id)
    
    flash('Пост не найден', 'danger')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>')
def delete(post_id):
    data = read_data()
    del data[post_id]
    write_data(data)
    flash('Пост удален', 'success')
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    articles = read_data()

    if 0 <= post_id < len(articles):
        post = articles[post_id]
        return render_template('post_detail.html',  post=post, post_id=post_id)
    
    flash('Пост не найден', 'danger')
    return redirect(url_for('index'))
