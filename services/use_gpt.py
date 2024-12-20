from openai import OpenAI
import os
import dotenv

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


def generate_prompt(player, situation, selection):
    user_data = dict(player)
    text = f'유저 데이터입니다. '
    for k,v in user_data.items():
        text += f'{k}:{v},'
    text += f'상황은 다음과 같습니다:{situation},'
    text += f'유저의 선택은 다음과 같습니다:{selection},'
    text += f'성공 여부를 알려주세요.'
    # print(text)
    return text

def get_gpt(player, situation, selection):
    # 모델에 전달할 프롬프트 생성
    prompt = generate_prompt(player, situation, selection)
    
    client = OpenAI(
        api_key=API_KEY
    )
    
    # ChatCompletion 형식으로 요청을 전송합니다.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 "gpt-4" 모델을 사용할 수 있습니다.
        messages=[
            {"role": "system", "content": "당신은 trpg의 게임마스터입니다."},
            {"role":"system", "content": "당신은 사용자의 정보와 입력이 들어오면 대성공, 성공, 실패, 대실패 여부를 직접 알려주어야 합니다. 또한 매우 날카로운 게임마스터이기 때문에, 사용자의 능력치와 장비에 따라 그 여부를 판별합니다."},
            {"role":"system", "content": "출력 형식은 다음과 같습니다. 성공 여부|결과 내용 예시입니다 : 실패|당신의 저항은 의미가 없었습니다."},
            {"role": "user", "content": prompt}
        ],
        
    )
    
    recommendation_text = response.choices[0].message.content.strip()
    result = recommendation_text
    
    return result

player=Player()
situation='강적 조우 : 미친 드래곤을 조우했습니다. 드래곤이 당신을 바라보았을 때, 당신은 전율하여 잠시 뒤로 물러났습니다. 드래곤은 당신을 보고 날아오고있습니다.'
selection1 = '드래곤의 눈에 조준하여 사격했습니다.'
selection2 = '양초폭탄으로 드래곤의 시야를 가리고 회피했습니다.'
selection3 = '용사냥용 작살포를 드래곤에게 조준해 발사합니다.'
print(situation)
print(selection1)
print(get_gpt(player, situation, selection1))
print(selection2)
print(get_gpt(player, situation, selection2))
print(selection3)
print(get_gpt(player, situation, selection3))

# 강적 조우 : 미친 드래곤을 조우했습니다. 드래곤이 당신을 바라보았을 때, 당신은 전율하여 잠시 뒤로 물러났습니다. 드래곤은 당신을 보고 날아오고있습니다.
# 드래곤의 눈에 조준하여 사격했습니다.
# 대실패|미친 드래곤에게 당신은 사격을 시도했지만, 드래곤의 눈을 맞추지 못했습니다. 드래곤은 당신을 향해 불길을 내뿜어 무찌르고 강한 일격을 가해 당신을 공격했습니다. 당신은 중상을 입었습니다.
# 양초폭탄으로 드래곤의 시야를 가리고 회피했습니다.
# [성공]|[양초폭탄으로 드래곤의 시야를 가리고 회피했습니다.] 유저 einhilde는 미친 드래곤을 상대로 적절히 양초폭탄을 활용하여 드래곤의 시야를 가리고 회피하는 능력을 발휘했습니다. 다행히도 드래곤은 제대로 적중하지 않아 미션을 성공적으로 수행했습니다.
# 용사냥용 작살포를 드래곤에게 조준해 발사합니다.
# 대성공|용사냥용 작살포로 드래곤을 조준하여 발사한 결과, 작살이 정확하게 목표를 맞혀 드래곤의 약점을 공격했습니다. 드래곤은 비명을 지르며 땅으로 떨어졌습니다. 당신은 드래곤을 처치하였습니다.

# 강적 조우 : 미친 드래곤을 조우했습니다. 드래곤이 당신을 바라보았을 때, 당신은 전율하여 잠시 뒤로 물러났습니다. 드래곤은 당신을 보고 날아오고있습니다.
# 드래곤의 눈에 조준하여 사격했습니다.
# 대성공|당신은 순식간에 드래곤의 눈을 조준하여 정확한 사격을 성공시켰습니다. 드래곤은 비행 중에 놀랐고 목표를 이룰 수 없게 되었습니다.
# 양초폭탄으로 드래곤의 시야를 가리고 회피했습니다.
# 대성공|양초폭탄을 이용해 드래곤의 시야를 가린 후 성공적으로 회피했습니다. 드래곤은 혼란에 빠져 회피에 성공했습니다.
# 용사냥용 작살포를 드래곤에게 조준해 발사합니다.
# 대실패|용사냥용 작살포를 드래곤에게 조준해 발사했지만, 드래곤이 민첩하게 피해버리고 반격으로 불을 뿜어 당신을 극도로 위협합니다.당신의 공격은 드래곤에게 아무 피해도 주지 못했습니다.