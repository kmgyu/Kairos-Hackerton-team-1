from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    playrecord = {
        '2024-07-21':"이거이거함"
    }
    
    return render_template('/index.html')

@app.route('/start')
def start():
    playrecord = {
        '2024-07-21':"이거이거함"
    }
    
    return render_template('start.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# 기능 기준으로 템플릿 이름 