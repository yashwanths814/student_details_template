from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://karthik:admin@data.kv0kadm.mongodb.net/')
db = client['students_db']
collection = db['students']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        birth_date = request.form['birth_date']
        email = request.form['email']
        github = request.form['github']
        linkedin = request.form['linkedin']

        if '@' not in email or '.' not in email:
            return render_template('index.html', error='Invalid email format')

        existing_student = collection.find_one({'usn': usn})
        if existing_student:
            collection.update_one(
                {'usn': usn},
                {'$set': {'name': name, 'birth_date': birth_date, 'email': email, 'github': github, 'linkedin': linkedin}}
            )
        else:
            collection.insert_one({
                'usn': usn,
                'name': name,
                'birth_date': birth_date,
                'email': email,
                'github': github,
                'linkedin': linkedin
            })

    return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        usn = request.form['usn']
        student = collection.find_one({'usn': usn})
        if student:
            return render_template('output.html', student=student)
        else:
            return render_template('output.html', not_found=True)

    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True)
