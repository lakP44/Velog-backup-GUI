import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
import subprocess
from datetime import datetime
from glob import glob
import pickle
import stat

# 폴더 권한 변경


def removeReadOnly(func, path, excinfo):
    # Using os.chmod with stat.S_IWRITE to allow write permissions
    os.chmod(path, stat.S_IWRITE)
    func(path)


horizontal = 330
vertical = 600

# 폴더 크기 확인 함수


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

# glob 폴더 삭제 함수


def delete_folder(path, parameter):
    while True:
        cd_path = glob(path)
        cd_path.sort()
        if cd_path:
            if (len(cd_path) - parameter) <= 0:
                break
            shutil.rmtree(cd_path[0], onerror=removeReadOnly)
        else:
            break

# 자동저장 기능 활성화 함수


def toggle_value():
    global exit_code
    global temp_code
    if exit_code == 0:
        exit_code = 1
        temp_code = 0
        auto_save_label.config(text="자동저장이 활성화 되었습니다.")
    else:
        auto_save_label.config(text="자동저장이 꺼졌습니다.")
        exit_code = 0
    print("exit_code:", exit_code)

# readme.txt를 여는 함수


def open_readme():
    if os.path.exists("readme.txt"):
        with open("readme.txt", "r", encoding="utf-8") as file:
            # 파일 내용을 읽어서 처리하는 로직을 여기에 작성
            # 예시로 파일 내용을 출력하는 코드를 작성
            content = file.read()
            messagebox.showinfo("readme", content)

# 타이머 표시


def update_timer(seconds):
    if (seconds > 0) and (exit_code == 1) and (os.path.exists('init_setting.txt')):
        # 1초 후에 update_timer 함수를 호출하여 1초씩 감소
        root.after(1000, update_timer, seconds - 1)
        cancel_label.config(text=f"{seconds}초 뒤 자동저장 후 \n프로그램이 종료됩니다...")

# 프로그램 자동 종료


def exit_program():
    if (exit_code == 1) and (os.path.exists('init_setting.txt')) and (temp_code == 1):
        VELOG_BACKUP(backup_path, backup_path2, user_name, delay, cert)
        root.destroy()

# 자동 종료 취소


def cancel_exit():
    global exit_code
    global cancel_label
    exit_code = 0
    cancel_label.configure(text="자동저장이 취소되었습니다")
    # 취소된 경우 추가 동작 수행 가능

# 자동 저장, 종료 타이머


def start_exit_timer():
    global exit_timer
    # 30분(1800000밀리초) 후에 exit_program 실행
    exit_timer = root.after(15000, exit_program)

# 폴더 생성 함수


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

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

# 자동 저장 취소, 설정 변경


def cancel_exit():
    global exit_code
    global cancel_label
    exit_code = 0
    cancel_label.configure(text="자동저장 & 종료가 취소되었습니다.")

# 설정 초기화 함수


def delete_txt():
    if os.path.exists('init_setting.txt'):
        os.remove('init_setting.txt')
        global init_delete
        init_delete.configure(text="설정파일이 삭제되었습니다.")
    else:
        init_delete.configure(text="설정이 존재하지 않습니다.")

# 설정 저장 함수


def save_txt():
    if (backup_path != "") and (user_name != ""):
        save_data_to_file("init_setting.txt", [
                          backup_path, user_name, backup_path2, delay, cert, exit_code])
        global init_save
        init_save.configure(text="설정파일이 저장되었습니다.")
    else:
        init_save.configure(text="app.js의 경로와 유저명을 입력해주세요.")


def VELOG_BACKUP(VelogBackup, MOVE_PATH, USER_NAME, DELAY, CERT):

    if MOVE_PATH == "":
        MOVE_PATH = VelogBackup

    # ROOT 폴더 경로
    ROOT_PATH = f"backup"

    # 대상 폴더 경로
    CONTENT_PATH = f"{ROOT_PATH}/content"

    # 이동 대상 폴더 경로
    SOURCE_PATH = f"{ROOT_PATH}/images"

    # 기존 backup 폴더 삭제
    if os.path.exists(ROOT_PATH):
        shutil.rmtree(ROOT_PATH, onerror=removeReadOnly)

    if DELAY != "":
        DELAY = f"-d {DELAY}"

    if CERT != "":
        CERT = f"-c {CERT}"

    # cmd 명령어 실행
    subprocess.run(
        ['cmd', '/c', f'node {VelogBackup}/app.js -u {USER_NAME} {DELAY} {CERT}'])

    # 파일 이동
    shutil.move(SOURCE_PATH, CONTENT_PATH)

    # markdown파일 전부 탐색
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
    NEW_PATH = MOVE_PATH + f"/{USER_NAME}_velog_backup"
    createFolder(NEW_PATH)

    # 폴더 이동
    shutil.move(CONTENT_PATH, NEW_PATH)

    folder_name = f'velog_backup_{datetime.today().strftime("%Y%m%d_%H%M%S")}'

    # 폴더 이름 변경
    os.rename(os.path.join(NEW_PATH, 'content'),
              os.path.join(NEW_PATH, folder_name))

    cd_path = glob(NEW_PATH + "/*")

    i = 0
    # glob 자동삭제
    for path_name in cd_path:
        if get_dir_size(path_name) > 0:
            i += 1
    if i == len(cd_path):
        delete_folder(NEW_PATH + "/*", 10)

    # backup 폴더 삭제
    shutil.rmtree(ROOT_PATH, onerror=removeReadOnly)


backup_path = ""
user_name = ""
backup_path2 = ""
delay = ""
cert = ""
exit_code = 0
temp_code = 1

# 시작하자마자 세팅
if os.path.exists('init_setting.txt'):
    data_list = load_data_from_file('init_setting.txt')
    backup_path = data_list[0]
    user_name = data_list[1]
    backup_path2 = data_list[2]
    delay = data_list[3]
    cert = data_list[4]
    exit_code = data_list[5]


def select_path():
    path = filedialog.askdirectory()
    path_label.configure(text=path)
    global backup_path
    backup_path = path_label.cget("text")


def select_path2():
    path2 = filedialog.askdirectory()
    path_label2.configure(text=path2)
    global backup_path2
    backup_path2 = path_label2.cget("text")


def get_username(*args):
    text3 = username_input.get()
    username_label.configure(text=text3)
    global user_name
    user_name = username_label.cget("text")


def get_delay(*args):
    text4 = delay_input.get()
    delay_label.configure(text=text4)
    global delay
    delay = delay_label.cget("text")


def get_access_token(*args):
    text5 = access_token_input.get()
    access_token_label.configure(text=text5)
    global cert
    cert = access_token_label.cget("text")


def execute():
    # 실행할 코드 작성
    messagebox.showinfo(
        "Velog Backup", f"백업이 {backup_path2}/{user_name}_velog_backup에 저장되었습니다.")


root = tk.Tk()

start_exit_timer()

# 창 크기 설정
root.geometry(f"{horizontal}x{vertical}")

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
execute_button = tk.Button(root, text="실행", command=lambda: (save_txt(
), VELOG_BACKUP(backup_path, backup_path2, user_name, delay, cert), execute()))
execute_button.pack()

# 자동저장 취소
cancel_button = tk.Button(root, text=f"자동저장 & 종료 취소", command=cancel_exit)
cancel_button.pack()
if os.path.exists('init_setting.txt'):
    cancel_label = tk.Label(root, text="설정 파일이 존재합니다.")
else:
    cancel_label = tk.Label(root, text="설정 파일이 존재하지 않습니다.")
cancel_label.pack()

# 설정 초기화
button = ttk.Button(root, text="설정 초기화", command=delete_txt)  # 시작프로그램에 바로가기 생성
button.pack()
init_delete = tk.Label(root, text="")
init_delete.pack()

# 설정만 저장
button = ttk.Button(root, text="설정 저장", command=save_txt)  # 시작프로그램에 바로가기 생성
button.pack()
init_save = tk.Label(root, text="")
init_save.pack()

# 설정만 저장
button = ttk.Button(root, text="자동저장 활성화",
                    command=toggle_value)  # 시작프로그램에 바로가기 생성
button.pack()
auto_save_label = tk.Label(root, text="")
auto_save_label.pack()

# readme 열기
button = tk.Button(root, text="Open Readme (도움말)", command=open_readme)
button.pack()

update_timer(15)

# GUI 창 실행
root.mainloop()
