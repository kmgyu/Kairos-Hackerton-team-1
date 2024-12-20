from openai import OpenAI

dotenv.load_dotenv()
API_KEY=os.environ.get('API_KEY')


class Player():

    def __init__(self):
        self.CharID = 'bla'
        self.Username = 'einhilde'
        self.PCName = 'foxthroat1'
        self.ATK = 4
        self.DEF = 6
        self.AGI = 10
        self.INV1 = '램프'
        self.INV2 = '낡은직검'
        self.INV3 = '양초폭탄'
        self.INV4 = '포도탄'
        self.INV5 = '냄새나는두건'
        self.AM1 = '양날단검'
        self.AM2 = '로브'
        self.AM3 = '가죽장화'
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

user_data = dict(Player())

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