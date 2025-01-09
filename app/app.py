# app.py
import os

from flask import Flask, request, render_template, redirect, url_for, session, send_file, flash
from db import init_db, create_user, verify_user, get_user_by_username, set_vote, get_vote, get_all_users_votes, get_vote_counts, get_all_usernames
from captcha.image import ImageCaptcha
import random
import string

app = Flask(__name__, template_folder='/app/templates/', static_folder='/app/static/')

app.config['SECRET_KEY'] = os.urandom(32)

init_db()

flag_1 = os.getenv("FLAG_1", "CTFkom{fake_flag_1}")
flag_2 = os.getenv("FLAG_2", "CTFkom{fake_flag_2}")


def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@app.route('/captcha')
def serve_captcha():
    captcha_text = generate_captcha_text(length=5)
    session['captcha_text'] = captcha_text
    image = ImageCaptcha()
    data = image.generate(captcha_text)

    return send_file(data, mimetype='image/png')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha_input = request.form.get('captcha')

        if not all([username, password, captcha_input]):
            error = 'Please fill out all fields.'
            return render_template('register.html', error=error)

        if 'captcha_text' not in session or captcha_input.upper() != session['captcha_text']:
            error = 'Invalid CAPTCHA.'
            return render_template('register.html', error=error)

        session.pop('captcha_text', None)

        success = create_user(username, password)
        if not success:
            error = 'Username or email already exists.'
            return render_template('register.html', error=error)

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            error = 'Please fill out all fields.'
            return render_template('login.html', error=error)
        try:
            if verify_user(username, password):
                user = get_user_by_username(username)
                session['user_id'] = user['id']
                session['username'] = username
                return redirect(url_for('dashboard'))

            error = 'Invalid username or password.'
            return render_template('login.html', error=error)
        except Exception as e:
            return render_template('login.html', error=e)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))
    username = session.get('username')
    current_vote = get_vote(username)
    all_users_votes = get_all_users_votes()
    vote_counts = get_vote_counts()

    # Calculate total votes
    total_votes = sum(vote_counts.values()) if vote_counts else 0

    # Calculate percentages
    vote_percentages = {}
    for candidate, count in vote_counts.items():
        percentage = (count / total_votes) * 100 if total_votes > 0 else 0
        vote_percentages[candidate.capitalize()] = round(percentage, 2)

    return render_template('dashboard.html',
                           username=username,
                           current_vote=current_vote,
                           users=all_users_votes,
                           vote_counts=vote_percentages,
                           flag_1=flag_1 if username == "admin" else None,
                           flag_2=flag_2 if vote_percentages["Borat"] == 100 else None

                           )


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        flash('Please log in to vote.')
        return redirect(url_for('login'))

    username = session.get('username')

    if request.method == 'POST':
        candidate = request.form.get('candidate')

        if candidate not in ['trump', 'harris', 'borat']:
            error = 'Invalid candidate selected.'
            return render_template('vote.html', error=error)

        success = set_vote(username, candidate)
        if success:
            flash(f'Your vote for {candidate.capitalize()} has been recorded.')
            return redirect(url_for('dashboard'))
        error = 'There was an error recording your vote.'
        return render_template('vote.html', error=error)

    current_vote = get_vote(username)
    return render_template('vote.html', current_vote=current_vote)


@app.route('/users')
def users():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    if session.get('username') == "admin":
        return get_all_usernames()


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(*a, **k):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
