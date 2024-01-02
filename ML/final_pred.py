import os
import json 
import final_serach 
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

json_path = os.path.join(os.path.expanduser("~"), "Project404", 'data.json')
whitelist_path = os.path.join(os.path.expanduser("~"), "Project404", 'List.json')
model_path = os.path.join(os.path.expanduser("~"), "Project404", 'naive_bayes_model.pkl')

# CountVectorizer를 초기화
vectorizer = CountVectorizer()

# 2주간 열었던 파일 데이터 읽어오기 
with open (json_path,'r',encoding='utf-8') as f_json:
    u_list = json.load(f_json)

# 화이트리스트 가져오기
with open(whitelist_path,'r',encoding= 'utf-8') as f_json:
    w_list = json.load(f_json)

def predict_program():
    
    # w_ext에 ext가 없는 경우 추가.
    new_keys_add = []

    for key in u_list.keys():
        if key not in w_list:
            new_keys_add.append(key)
    
    for key in new_keys_add:
        w_list[key] = []

    
    # 저장 되어 있는 모델 불러오기 
    loaded_model = joblib.load(model_path)

    # 모델에 전달할 확장자. (확장자만)
    ext_list = []
    for key in w_list.keys():
        if '.' in key:
            ext_list.append(key)

    # 입력 확장자 벡터화 
    X_ext = vectorizer.fit_transform(ext_list)

    # 기존 모델을 사용하여 예측
    predicted = loaded_model.predict(X_ext)

    # 예측 결과 리스트로 저장 (확장자 + 예측한 prog)
    predic_list={}
    for ext, prog in zip(X_ext,predicted):
        ext_list = vectorizer.inverse_transform(ext)[0].tolist()
        ext_str = '.'+' '.join(vectorizer.inverse_transform(ext)[0])
        predic_list[ext_str]=str(prog)
        #print(f"Extension: {x}, Predicted Program: {prog}")

    # 기존 화이트리스트와 예측 결과 리스트를 비교하여 시작함수를 추가 
    for p_ext, p_prog in predic_list.items():
        if p_ext in w_list:
            w_list[p_ext].append(p_prog)

    # 내 파일에서 긁어온 시작 함수도 화이트리스트에 추가
    for p_ext, p_prog in u_list.items():
        if p_ext in w_list:
            # 확장자에 대한 프로그램 리스트를 set으로 변환하여 중복 제거
            w_list[p_ext] = list(set(w_list[p_ext] + p_prog))
        else:
            w_list[p_ext] = p_prog

    # 화이트리스트 저장
    with open(whitelist_path, 'w', encoding='utf-8') as json_file:
        json.dump(w_list, json_file, indent=4, ensure_ascii=False)

    return w_list

    
def ML_whitelist_update(update_w_list):

    # 데이터를 특성 벡터로 변환
    ext=[]
    program=[]
    for f_ext, f_prog in update_w_list.items():
        for prog in f_prog:
            ext.append(f_ext)
            program.append(prog)
         
    # 벡터화 
    vectorizer = CountVectorizer()
    X_ext = vectorizer.fit_transform(ext)

    # 나이브 베이즈 모델 생성 및 학습
    update_model = MultinomialNB()
    update_model.fit(X_ext, program)

    # 모델 저장
    joblib.dump(update_model, model_path)
    
if __name__ == "__main__":
    final_serach.sort_two_weeks()
    update_w_list = predict_program()
    ML_whitelist_update(update_w_list)

