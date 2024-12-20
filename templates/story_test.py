from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    branch = int(request.args.get('branch', 0))  # branch 값이 없으면 기본값 0
    return render_template('main/play.html', branch=branch)

if __name__ == '__main__':
    app.run(debug=True)
