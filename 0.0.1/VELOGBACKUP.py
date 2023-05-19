import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Tk, ttk, StringVar
import os
import shutil
import subprocess
from datetime import datetime
from glob import glob
import win32com.client
import pickle
import datetime

# 변수
################################################################################################

backup_path = ""
user_name = ""
backup_path2 = ""
delay = ""
cert = ""

# 함수
################################################################################################


def delete_backup():
    folder_path = os.path.dirname(
        [os.path.abspath(file) for file in glob("*exe")][0]) + "\\backup"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

# 데이터 저장 함수


def save_data_to_file(file_path, data):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

# 데이터 불러오기 함수


def load_data_from_file(file_path, default_value=None):
    if not os.path.exists(file_path):
        return default_value
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# 설정 초기화 함수


def delete_txt():
    if os.path.exists('init_setting.txt'):
        os.remove('init_setting.txt')
    startup_folder = get_startup_folder()
    shortcut_path = os.path.join(startup_folder, 'velog_backup.lnk')

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

# 폴더 생성 함수


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def VELOG_BACKUP(VelogBackup, MOVE_PATH, USER_NAME, DELAY, CERT):

    if MOVE_PATH == "":
        MOVE_PATH = VelogBackup

    # ROOT 폴더 경로
    ROOT_PATH = f"backup"

    # 대상 폴더 경로
    CONTENT_PATH = f"{ROOT_PATH}/content"

    # 이동 대상 폴더 경로
    SOURCE_PATH = f"{ROOT_PATH}/images"

    # 이동할 새 경로
    NEW_PATH = MOVE_PATH + f"/{USER_NAME}_velog_backup"

    # 기존 backup 폴더 삭제
    if os.path.exists(ROOT_PATH):
        shutil.rmtree(ROOT_PATH)

    if os.path.exists(NEW_PATH + "/backup"):
        shutil.rmtree(NEW_PATH + "/backup")
    if os.path.exists(NEW_PATH + "/content"):
        shutil.rmtree(NEW_PATH + "/content")
    if os.path.exists(NEW_PATH + "/images"):
        shutil.rmtree(NEW_PATH + "/images")

    if DELAY != "":
        DELAY = f"-d {DELAY}"

    if CERT != "":
        CERT = f"-c {CERT}"

    # cmd 명령어 실행
    subprocess.run(
        ['cmd', '/c', f'node {VelogBackup}/app.js -u {USER_NAME} {DELAY} {CERT}'])

    # 파일 이동
    shutil.move(SOURCE_PATH, CONTENT_PATH)

    # 대상 폴더 내의 모든 파일 경로 탐색

    MD_LIST = glob(f'{CONTENT_PATH}/*.md')

    for file_name in MD_LIST:
        # 파일 열기
        with open(file_name, 'r', encoding='UTF-8') as file:
            content = file.read()

        # 이미지 경로 변경
        new_content = content.replace(f'/images/', 'images/')

        # 변경된 내용 저장
        with open(file_name, 'w', encoding='UTF-8') as file:
            file.write(new_content)

    # backup/content 폴더 이름을 backup-유저명-날짜로 변경

    # 이동할 새 경로
    createFolder(NEW_PATH)

    # 폴더 이동
    shutil.move(CONTENT_PATH, NEW_PATH)

    # 폴더 이름 변경
    os.rename(os.path.join(NEW_PATH, 'content'), os.path.join(
        NEW_PATH, f'velog_backup_{datetime.datetime.today().strftime("%Y%m%d_%H%M%S")}'))

    # backup 폴더 삭제
    shutil.rmtree(ROOT_PATH)

# velog_backup app.js 경로


def select_path():
    path = filedialog.askdirectory()
    path_label.configure(text=path)
    global backup_path
    backup_path = path_label.cget("text")

# 백업 폴더가 저장될 경로


def select_path2():
    path2 = filedialog.askdirectory()
    path_label2.configure(text=path2)
    global backup_path2
    backup_path2 = path_label2.cget("text")

# 유저명 가져오기


def get_username(*args):
    text3 = username_input.get()
    username_label.configure(text=text3)
    global user_name
    user_name = username_label.cget("text")

# 딜레이 가져오기


def get_delay(*args):
    text4 = delay_input.get()
    delay_label.configure(text=text4)
    global delay
    delay = delay_label.cget("text")

# 엑세스 토큰 가져오기


def get_access_token(*args):
    text5 = access_token_input.get()
    access_token_label.configure(text=text5)
    global cert
    cert = access_token_label.cget("text")

# 작업이 끝나면 알림


def execute():
    # 실행할 코드 작성
    messagebox.showinfo(
        "Velog Backup", f"백업이 {backup_path2}/{user_name}_velog_backup에 저장되었습니다.")

# 프로그램 시작시 체크
################################################################################################


# 프로그램 시작 시 특정 파일 유무에 따라 바로가기 생성 또는 삭제
if os.path.exists('init_setting.txt'):
    txt_path = glob("*txt")
    # 상대경로를 절대경로로 변환
    txt_absolute_paths = [os.path.abspath(file) for file in txt_path]
    data_list = load_data_from_file(txt_absolute_paths[0])
    backup_path = data_list[0]
    user_name = data_list[1]
    backup_path2 = data_list[2]
    delay = data_list[3]
    cert = data_list[4]

# twinker GUI 세팅
################################################################################################
root = tk.Tk()

# 창 크기 설정
root.geometry("300x450")

# 창 이름 설정
root.title(f"Velog Backup")

# 경로 선택 창
path_button1 = tk.Button(
    root, text="Select velog-backup Path \n(app.js 파일이 들어있는 폴더를 선택해주세요.)", command=select_path)
path_label = tk.Label(root, text=backup_path)
path_button1.pack()
path_label.pack()

# 텍스트 입력 창 1
username_input = tk.Entry(root)
username_input.pack()
username_button = tk.Button(root, text="유저명 (필수 입력)", command=get_username)
username_label = tk.Label(root, text=user_name)
username_button.pack()
username_label.pack()

# 텍스트 입력 창 2
delay_input = tk.Entry(root)
delay_input.pack()
delay_button = tk.Button(
    root, text="딜레이 (단위 ms, 글이 많은 경우 늘려주세요.\n기본값은 0입니다.)", command=get_delay)
delay_label = tk.Label(root, text=delay)
delay_button.pack()
delay_label.pack()

# 텍스트 입력 창 3
access_token_input = tk.Entry(root)
access_token_input.pack()
access_token_button = tk.Button(
    root, text="velog 유저 엑세스 토큰 \n(필요시 사용, 기본값은 공백입니다.)", command=get_access_token)
access_token_label = tk.Label(root, text=cert)
access_token_button.pack()
access_token_label.pack()

# 경로 선택 창
path_button2 = tk.Button(
    root, text="백업 폴더를 생성할 위치 \n(유저명_velog_backup으로 폴더가 생성됩니다.)", command=select_path2)
path_label2 = tk.Label(root, text=backup_path2)
path_button2.pack()
path_label2.pack()

# 실행 버튼
execute_button = tk.Button(root, text="실행", command=lambda: (delete_backup(), VELOG_BACKUP(backup_path, backup_path2, user_name, delay, cert), save_data_to_file(
    os.path.dirname([os.path.abspath(file) for file in glob("*exe")][0]) + "\\init_setting.txt", [backup_path, user_name, backup_path2, delay, cert]), execute()))
execute_button.pack()

# 설정 초기화
button = ttk.Button(root, text="설정 초기화", command=delete_txt)  # 시작프로그램에 바로가기 생성
button.pack(pady=20)

# GUI 창 실행
root.mainloop()
