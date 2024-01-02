import os
import json
import final_serach

whitelist_path = os.path.join(os.path.expanduser("~"), "Project404", 'List.json')
json_path = os.path.join(os.path.expanduser("~"), "Project404", 'data.json')
    
# 2주간 열었던 파일 데이터 읽어오기 
with open (json_path,'r',encoding='utf-8') as u_json:
    u_list = json.load(u_json)

# 화이트리스트 가져오기
with open(whitelist_path,'r',encoding= 'utf-8') as w_json:
    w_list = json.load(w_json)
    
def whitelist_update():
    
    for u_ext, u_prog in u_list.items():
        if u_ext not in w_list:
            w_list[u_ext] = u_prog
        else:
            # 이미 있는 키의 경우 중복된 값을 제외하고 추가
            w_list[u_ext] = list(set(w_list[u_ext] + u_prog))



    # 화이트리스트 저장
    with open(whitelist_path, 'w', encoding='utf-8') as json_file:
        json.dump(w_list, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    final_serach.sort_two_weeks()
    whitelist_update()

    