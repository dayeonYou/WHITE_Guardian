import os
import subprocess
import winreg
import win32com.client
import json
import re
from datetime import date, datetime, timedelta

# 바로가기 파일경로를 사용하여 대상 파일의 실제 경로 찾아 반환
def get_target_path(lnk_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnk_path)
    target_path = shortcut.Targetpath
    return target_path
    
# 해당 파일 타입에 대한 기본 프로그램 경로 반환
def get_associated_program_path(ext):
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ext, 0, winreg.KEY_READ) as key:
            prog_id = winreg.QueryValueEx(key, None)[0]
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'{prog_id}\\shell\\open\\command', 0, winreg.KEY_READ) as key:
            command = winreg.QueryValueEx(key, None)[0]
       
        # 필요한 명령 부분만 추출
        match = re.search(r'"(.+?\.exe)"', command)
        if match:
            program_path = match.group(1)
        else:
            program_path = command.split()[0]

        return program_path
    except FileNotFoundError:
        return get_default_notepad(ext)

#노트패드 찾는용...
def get_default_notepad(ext):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\{ext}\\UserChoice") as key:
            prog_id = winreg.QueryValueEx(key, "ProgId")[0]

        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command") as key:
            command = winreg.QueryValueEx(key, None)[0]           
        
        # 큰따옴표 안의 텍스트를 추출하는 정규표현식 패턴
        pattern = r'"([^"]+)"'
        match = re.search(pattern, command)            
    
        return match.group(1)
    
    except FileNotFoundError:
        pass


# 2주내로 사용한 파일의 정보 정렬, JSON 파일로 저장
def sort_two_weeks():
    folder_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Recent')
    file_list = os.listdir(folder_path)
    today = datetime.today()
    two_weeks_ago = today - timedelta(days=14)
    
    # 2주 이전에 열린 파일들을 저장할 리스트
    recent_files = []

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
       # 파일의 수정 시간이 현재 시간에서 2주 이내인 경우에만 리스트에 추가
        if today - modified_time <= timedelta(days=14):
            recent_files.append(file_path)
    
    # recent_files 리스트를 파일 수정 시간 기준으로 정렬 (내림차순)
    sorted_files = sorted(recent_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    
    # 폴더를 제외한 프로그램만 저장.
    sorted_recent_file=[] 
    
    for f_path in sorted_files:
        parts = f_path.split('\\')[-1]
        f_name = parts.split('.')
        if len(f_name) == 3:
            sorted_recent_file.append(f_path)
    
    # 파일 정보 저장 딕셔너리 
    file_info ={}

    for f_path in sorted_recent_file:
        f_ext = os.path.splitext(f_path)[1]
        if f_ext == '.lnk':  # 바로가기 파일인 경우 처리
            origin_path = get_target_path(f_path)
            file_ext = os.path.splitext(origin_path)[1]
            origin_prog = get_associated_program_path(file_ext)
            print(file_ext) 
            print(origin_prog) 
            ''' 
            if origin_prog is not None and origin_prog != "None":
                f_name = origin_path.split("\\")[-1]
                ext = "."+f_name.split(".")[-1]
                file_info[ext] = [origin_prog]
            '''    
                
    # 사용자의 홈 디렉토리 경로 얻고, 전체 경로 얻기
    json_path = os.path.join(os.path.expanduser("~"), "Project404")
    
    # 해당 경로에 폴더가 존재하지 않는 경우, 폴더 생성
    if not os.path.exists(json_path):
        os.mkdir(json_path)
        
    # 데이터를 JSON 파일로 저장
    file_path = os.path.join(json_path, 'data.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(file_info, json_file, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    sort_two_weeks() 
