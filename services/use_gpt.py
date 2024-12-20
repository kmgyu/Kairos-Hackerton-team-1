from openai import OpenAI

dotenv.load_dotenv()
API_KEY=os.environ.get('API_KEY')


class PlayerCh(db.Model):
    __tablename__ = 'PlayerCh'

    CharID = db.Column(db.String(156), primary_key=True, nullable=False)
    Username = db.Column(db.String(150), db.ForeignKey('userlist.username'), nullable=False)
    PCName = db.Column(db.String(10), nullable=False)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)
    
    INV1 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV2 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV3 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV4 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV5 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM1 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM2 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM3 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)

user_data = {

}

def get_farming_recommendation(data):
    # 모델에 전달할 프롬프트 생성
    prompt = generate_prompt(data)
    
    client = OpenAI(
        api_key=API_KEY
    )
    
    # ChatCompletion 형식으로 요청을 전송합니다.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 "gpt-4" 모델을 사용할 수 있습니다.
        messages=[
            {"role": "system", "content": "You are an agricultural assistant."},
            {"role":"system", "content": "다음과 같은 형식으로 대응작업을 제시합니다. todo_name:todo name,todo_content:todo content,cycle:(if need it then input number. unit is day),startdate:YYYY-MM-DD,period:unit is day"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        
    )
    
    recommendation_text = response.choices[0].message.content.strip()
    result = recommendation_text
    
    return result