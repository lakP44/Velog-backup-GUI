# Velog-backup-GUI

- HEY_CJAEWON님의 [velog-backup](https://github.com/cjaewon/velog-backup)에 GUI를 추가했습니다.

</br>

> ### [1.2.1 (실행파일 + readme)](https://github.com/lakP44/Velog-backup-GUI/tree/main/1.2.1)

>> ### [1.1.0](https://github.com/lakP44/Velog-backup-GUI/tree/main/1.1.0)

>> ### [1.0.0 exe 파일](https://github.com/lakP44/Velog-backup-GUI/tree/main/1.0.0/dist)

</br>

## v 1.2.1

- 자세한 설명은 아래의 v 1.1.0, v 1.0.0, 사용법을 참고바랍니다. 

- 엑세스 거부 버그, 인덱스 버그를 수정하였습니다.

- 한 폴더의 최대 백업 저장 개수가 10개로 조정됩니다. (11개 이상부터는 선입선출됩니다.)

  - 제대로 백업되지 못한 경우를 대비해 빈폴더가 하나라도 있으면 선입선출이 이뤄지지 않습니다.
  
  - 백업폴더 이외의 빈폴더도 마찬가지니 백업폴더내에 빈폴더를 없애주기실 권장드립니다. (선입선출을 원하지 않으시면 빈폴더를 일부러 추가하셔도 괜찮습니다.)

- 설치파일에 init_setting을 업데이트 하지 못하는 문제가 발생하여, portable 버전을 이용해주시면 감사하겠습니다.

  - 동일한 문제, 또는 이외의 문제 발생시 issues에 남겨주시면 감사하겠습니다.

<details>
  <summary><h2>v 1.1.0</h2></summary>

  ![image](https://github.com/lakP44/Velog-backup-GUI/assets/110088655/7c188eb9-cbb0-4ecf-85fc-b2411a7ac4be)

  </br>

  - portable 버전과 install버전이 나눠졌습니다. portable 버전은 폴더째로 다운받으시면 됩니다.

  - 이전 설정값을 저장할 수 있는 기능이 추가되었습니다.
  - 설정값이 존재할 시 15초안에 자동저장을 취소하거나, 자동저장 후 종료를 하는 것 중에 선택할 수 있습니다.
    - 즉 세팅값이 존재하면 프로그램을 실행시키기만 해도 15초 뒤 자동저장이 됩니다.
  - 설정 저장 버튼은 현재 입력한 값들을 저장합니다.
  - 설정 초기화는 설정 파일을 삭제합니다.

  > 사용시 문제가 발생하면 app.js 경로, 백업할 폴더의 경로내에 backp, content, images 폴더가 있는지 확인 후 있다면 삭제하고 재시작해주세요.
  문제가 해결되지 않을 시 issues에 남겨주시면 확인하겠습니다.
  
</details>

<details>
  <summary><h2>v 1.0.0</h2></summary>

<img src=https://github.com/lakP44/Velog-backup-GUI/assets/110088655/dd4a87f4-950d-412e-9e33-a88e6dd9c213>

</br>
</br>

- 날짜순으로 폴더를 생성하는 기능이 추가되었습니다.

</details>

</br>

# 사용법

- 본 설명은 [이 링크](https://github.com/cjaewon/velog-backup)의 과정이 전부 끝났다는 가정하에 진행됩니다.

- Select velog-backup Path에는 app.js가 존재하는 (git clone한) 폴더를 선택해주시면 됩니다.

- 유저명은 필수입력이며 딜레이와 엑세스 토큰은 선택입니다. (꼭 버튼을 눌러서 입력해주셔야 합니다.) [참고](https://github.com/cjaewon/velog-backup)

- 백업 폴더를 생성할 위치는 기본적으로 app.js가 존재하는 위치이며

- 폴더를 선택시 아래와 같이 저장됩니다.

> `선택한 폴더 (default : app.js의 위치)`
> > `ㄴ 유저명_velog_backup`
> > > `ㄴ velog_backup_저장시각`
