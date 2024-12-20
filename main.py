from flask import Flask, render_template

app = Flask(__name__)

# 딕셔너리에 저장된 스크립트
scripts = {
    "script": [
        "첫번째줄",
        "두번째줄.",
        "스크립트입니다."
    ]
}

# 플레이 요약 정보
play_summary = {
    "title": "모험의 시작",
    "description": "당신은 용사가 되어 세상을 구하기 위한 여정을 떠납니다.",
    "progress": "현재 진행률: 50%"
}

# 플레이 로그
play_log = {
    "log": [
        "몬스터를 물리쳤습니다.",
        "새로운 동료를 얻었습니다.",
        "보물을 발견했습니다."
    ]
}

# 엔딩 스크립트
ending_scripts = {
    "script": [
        "이것이 당신의 여정의 끝입니다.",
        "모험을 함께 해주셔서 감사합니다.",
        "당신은 영웅입니다!"
    ]
}

@app.route("/")
def home():
    return render_template("main/ending.html", scripts=scripts["script"])

@app.route("/ending")
def ending():
    return render_template(
        "main/ending.html", 
        ending_scripts=ending_scripts["script"], 
        play_summary=play_summary, 
        play_log=play_log["log"]
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)