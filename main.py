from flask import Flask, request, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for using sessions
UPSTAGE_API_KEY = os.environ['UPSTAGE_API_KEY']

os.makedirs('data/client', exist_ok=True)

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

# AUDIT Questions
audit_questions = [
    "How often do you have a drink containing alcohol?",
    "How many drinks containing alcohol do you have on a typical day when you are drinking?",
    "How often do you have six or more drinks on one occasion?",
    "How often during the last year have you found that you were not able to stop drinking once you had started?",
    "How often during the last year have you failed to do what was normally expected of you because of drinking?",
    "How often during the last year have you needed a first drink in the morning to get yourself going after a heavy drinking session?",
    "How often during the last year have you had a feeling of guilt or remorse after drinking?",
    "How often during the last year have you been unable to remember what happened the night before because of your drinking?",
    "Have you or someone else been injured because of your drinking?",
    "Has a relative, friend, doctor, or other health care worker been concerned about your drinking or suggested you cut down?"
]


def save_responses(filename, data):
    filepath = os.path.join('data/client', filename)
    with open(filepath, 'a') as file:
        json.dump(data, file)
        file.write('\n')


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
        answers = request.form.to_dict()
        pairs = [(dudit_questions[int(k[1:])], v) for k, v in answers.items()]
        response_data = {
            'name': session.get('name'),
            'issue': session.get('issue'),
            'responses': pairs
        }
        save_responses('dudit_responses.json', response_data)
        return f"<h1>Thank you for completing the DUDIT questionnaire. Your responses have been noted.</h1>"
    return render_template('dudit.html',
                           questions=dudit_questions,
                           enumerate=enumerate)


@app.route('/audit', methods=['GET', 'POST'])
def audit():
    if request.method == 'POST':
        answers = request.form.to_dict()
        pairs = [(audit_questions[int(k[1:])], v) for k, v in answers.items()]
        response_data = {
            'name': session.get('name'),
            'issue': session.get('issue'),
            'responses': pairs
        }
        save_responses('audit_responses.json', response_data)
        return f"<h1>Thank you for completing the AUDIT questionnaire. Your responses have been noted.</h1>"
    return render_template('audit.html',
                           questions=audit_questions,
                           enumerate=enumerate)


if __name__ == '__main__':
    app.run(debug=True)
