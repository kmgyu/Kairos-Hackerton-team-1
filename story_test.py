from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    branch = int(request.args.get('branch', 0))  # branch 값이 없으면 기본값 0
    scripts = ['first',
               'second',
               'third',
               '4',
               '5']
    return render_template('main/play.html', script=scripts[branch])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)