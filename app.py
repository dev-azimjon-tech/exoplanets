from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import random

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


def generate_planet_data(weight, surface, atmosphere):
    # Simple logic to generate realistic planet data
    temperature = round(random.uniform(-100, 100), 2)
    gravity = round(weight / (random.uniform(1.5, 2.5)), 2)  # Example of gravity calculation
    
    surface_colors = {
        'ocean': '#0077be',     # Blue
        'desert': '#d2b48c',    # Sandy
        'forest': '#228B22',    # Green
        'ice': '#f0f8ff',       # Light blue
        'volcanic': '#a52a2a'   # Brown
    }
    
    atmosphere_colors = {
        'none': 'transparent',
        'o2': 'rgba(135, 206, 235, 0.5)',  # Blue with transparency
        'co2': 'rgba(255, 99, 71, 0.5)',    # Red with transparency
        'ch4': 'rgba(154, 205, 50, 0.5)'    # Yellow with transparency
    }
    
    return {
        'temperature': temperature,
        'gravity': gravity,
        'surface_color': surface_colors.get(surface, '#ffffff'),
        'atmosphere_color': atmosphere_colors.get(atmosphere, 'transparent')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_planet', methods=['POST'])
def generate_planet():
    data = request.get_json()
    weight = float(data['weight'])
    surface = data['surface']
    atmosphere = data['atmosphere']
    
    planet_data = generate_planet_data(weight, surface, atmosphere)
    
    return jsonify({
        'name': data['name'],
        'temperature': planet_data['temperature'],
        'gravity': planet_data['gravity'],
        'surface_color': planet_data['surface_color'],
        'atmosphere_color': planet_data['atmosphere_color']
    })


if __name__ == '__main__':
    app.run(debug=True)
