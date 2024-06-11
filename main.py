from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for using sessions

# DUDIT Questions
dudit_questions = [
    "How often do you use drugs other than alcohol?",
    "Do you use more than one type of drug on the same occasion?",
    "How many times do you take drugs on a typical day when you use drugs?",
    "How often are you influenced heavily by drugs?",
    "Over the past year, have you felt that your longing for drugs was so strong that you could not resist it?",
    "Has it happened, over the past year, that you have not been able to stop taking drugs once you started?",
    "How often over the past year have you taken drugs and then neglected to do something you should have done?",
    "How often over the past year have you needed to take a drug the morning after heavy drug use the day before?",
    "How often over the past year have you had guilt feelings or a bad conscience because you used drugs?",
    "Have you or anyone else been hurt (mentally or physically) because you used drugs?",
    "Has a relative or a friend, a doctor or a nurse, or anyone else, been worried about your drug use or said to you that you should stop using drugs?"
]

dudit_options = [
    "Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    issue = request.form['issue']
    session['issue'] = issue
    return redirect(url_for('greetings', issue=issue))


@app.route('/greetings')
def greetings():
    issue = request.args.get('issue')
    return render_template('greetings.html', issue=issue)


@app.route('/store', methods=['POST'])
def store():
    issue = request.form['issue']
    name = request.form['name']
    session['name'] = name
    if issue == 'drugs':
        return redirect(url_for('dudit'))
    else:
        return f"<h1>Thank you, {name}. Your issue ({issue}) has been recorded.</h1>"


@app.route('/dudit', methods=['GET', 'POST'])
def dudit():
    if request.method == 'POST':
        answers = request.form
        return f"Thank you for completing the DUDIT questionnaire. Your answers: {dict(answers)}"
    return render_template('dudit.html',
                           questions=dudit_questions,
                           options=dudit_options,
                           enumerate=enumerate)


if __name__ == '__main__':
    app.run(debug=True)
