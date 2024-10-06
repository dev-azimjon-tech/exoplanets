from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample quizzes data
quizzes = {
    "Exoplanet Quiz": {
        "questions": [
            {"question": "What is an exoplanet?", "options": ["A planet in our solar system", "A planet outside our solar system", "A moon of a planet", "None of the above"], "answer": 1},
            {"question": "How many exoplanets have been discovered?", "options": ["Over 4,000", "About 1,000", "Over 10,000", "Less than 500"], "answer": 0},
            {"question": "What method is commonly used to detect exoplanets?", "options": ["Direct imaging", "Transit method", "Astrometry", "All of the above"], "answer": 3}
        ]
    }
}

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Library page
@app.route('/library')
def library():
    quizzes = {
        'quiz1': 'Quiz 1 Title',
        'quiz2': 'Quiz 2 Title',
        # Add more quizzes here
    }

    books = [
        {'title': 'Book 1', 'author': 'Author 1'},
        {'title': 'Book 2', 'author': 'Author 2'},
        # Add more books here
    ]

    videos = [
        {'title': 'Video 1', 'url': 'http://video1.com'},
        {'title': 'Video 2', 'url': 'http://video2.com'},
        # Add more videos here
    ]

    return render_template(
            'library.html',
            quizzes=quizzes.keys(),  # Pass quiz titles or IDs
            books=books,             # Pass book list
            videos=videos            # Pass video list
        )

@app.route('/quiz/<quiz_id>')
def quiz_detail(quiz_id):
    quiz = quizzes.get(quiz_id)
    if quiz:
        return render_template('quiz_detail.html', quiz=quiz)
    else:
        return "Quiz not found", 404

# Quiz page
@app.route('/quiz/<quiz_name>', methods=['GET', 'POST'])
def quiz(quiz_name):
    if request.method == 'POST':
        score = 0
        total_questions = len(quizzes[quiz_name]['questions'])
        for i, question in enumerate(quizzes[quiz_name]['questions']):
            user_answer = request.form.get(f'question-{i}')
            if user_answer and int(user_answer) == question['answer']:
                score += 1
        flash(f'You scored {score} out of {total_questions}!', 'success')
        return redirect(url_for('library'))
    return render_template('quiz.html', quiz_name=quiz_name, questions=quizzes[quiz_name]['questions'])

# Registration system
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            flash(f'Successfully registered as {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please fill out all fields.', 'error')
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form
        return redirect(url_for('library'), data)

if __name__ == '__main__':
    app.run(debug=True)