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

# AUDIT Questions
audit_questions = [
    "How often do you have a drink containing alcohol?",
    "How many drinks containing alcohol do you have on a typical day when you are drinking?",
    "How often do you have six or more drinks on one occasion?",
    "How often during the last year have you found that you were not able to stop drinking once you had started?",
    "How often during the last year have you failed to do what was normally expected from you because of drinking?",
    "How often during the last year have you needed a first drink in the morning to get yourself going after a heavy drinking session?",
    "How often during the last year have you had a feeling of guilt or remorse after drinking?",
    "How often during the last year have you been unable to remember what happened the night before because you had been drinking?",
    "Have you or someone else been injured as a result of your drinking?",
    "Has a relative or friend or a doctor or another health worker been concerned about your drinking or suggested you cut down?"
]

# audit options
audit_options = [
    ["Never", "Monthly or less", "2-4 times a month", "2-3 times a week", "4 or more times a week"], 
    ["1 or 2", "3 or 4", "5 or 6", "7 to 9", "10 or more"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"], 
    ["No", "Yes, but not in the last year", "Yes, during the last year"], 
    ["No", "Yes, but not in the last year", "Yes, during the last year"],
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
    elif issue == 'alcohol':
        return redirect(url_for('audit'))
    else:
        return f"<h1>Thank you, {name}. Your issue ({issue}) has been noted.</h1>"


@app.route('/dudit', methods=['GET', 'POST'])
def dudit():
    if request.method == 'POST':
        answers = request.form
        return f"Thank you for completing the DUDIT questionnaire. Your answers: {dict(answers)}"
    return render_template('dudit.html',
                           questions=dudit_questions,
                           options=dudit_options,
                           enumerate=enumerate)


@app.route('/audit', methods=['GET', 'POST'])
def audit():
    if request.method == 'POST':
        answers = request.form
        return f"Thank you for completing the AUDIT questionnaire. Your answers: {dict(answers)}"
    return render_template('audit.html',
                           questions=audit_questions,
                           options=audit_options,
                           enumerate=enumerate)


if __name__ == '__main__':
    app.run(debug=True)
