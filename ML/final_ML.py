import os
import numpy as np
import joblib
import json 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def train_naive_bayes(json_path):
    
    # json 파일 읽어오기 
    with open(json_path,'r',encoding='utf-8') as json_file:
        datas = json.load(json_file)
        
    # 데이터를 특성 벡터로 변환
    ext=[]
    program=[]
    for f_ext, f_prog in datas.items():
        for prog in f_prog:
            ext.append(f_ext)
            program.append(prog)
            
    vectorizer = CountVectorizer()
    X_ext = vectorizer.fit_transform(ext)
    
   # 데이터를 학습 세트와 테스트 세트로 분할 안할거임
    #X_train, X_test, y_train, y_test = train_test_split(X_ext, program, test_size=0.2, random_state=42)
    
    X_train = X_ext
    y_train = program
    
   # 나이브 베이즈 모델 생성 및 학습
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train, y_train)
    
    # 테스트 데이터에 대한 예측
    y_pred = nb_classifier.predict(X_train)
    
    # 정확도 및 분류 보고서 출력
    #accuracy = accuracy_score(y_train, y_pred)
    #report = classification_report(y_train, y_pred)
    
    
    return nb_classifier
    
if __name__ == "__main__":
    
    # 초기 dataset 학습 
    json_path = os.path.join(os.path.expanduser("~"), "Project404", 'data.json')
    trained_nb_classifier = train_naive_bayes(json_path)  # 학습된 모델을 변수에 저장

    # 모델 저장
    model_path = os.path.join(os.path.expanduser("~"),"Project404",'naive_bayes_model.pkl')
    joblib.dump(trained_nb_classifier, model_path)
    