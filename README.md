한양대 공지 → 텔레그램 알림 봇 (설치 가이드)
이 가이드만 천천히 따라 하면, 한양대 전체공지와 경영대 공지에 새 글이 올라올 때마다 텔레그램으로 자동 알림을 받을 수 있습니다. 코딩 지식은 필요 없어요. "복사 → 붙여넣기 → 버튼 누르기"만 하면 됩니다.

준비물: 텔레그램 앱, 그리고 PC(노트북). 일부 단계는 PC가 편합니다. 전체 소요 시간: 약 20~30분.

큰 그림 (먼저 이해하고 가기)
텔레그램에서 알림을 보내줄 봇을 하나 만듭니다. → 비밀번호 같은 '토큰'을 받습니다.
그 봇이 누구에게(나에게) 보낼지 알려주는 'CHAT_ID'를 알아냅니다.
GitHub라는 무료 사이트에 파일 4개를 올립니다.
GitHub가 30분마다 자동으로 공지를 확인해서, 새 글만 텔레그램으로 보냅니다.
이 4개 파일이 준비되어 있습니다:

check_notices.py (실제로 일하는 코드)
requirements.txt
notices.yml (자동 실행 설정)
README.md (이 안내문)
1단계. 텔레그램 봇 만들기 (토큰 받기)
텔레그램 앱에서 검색창에 @BotFather 를 검색해 들어갑니다. (파란 체크 표시가 있는 공식 계정)
START 또는 /start 를 누릅니다.
/newbot 이라고 보냅니다.
봇 이름을 물어보면 아무거나 적습니다. 예: 한양공지알림
봇 아이디(username)를 물어보면 반드시 bot 으로 끝나야 합니다. 예: hyu_notice_bot (이미 있는 이름이면 다른 걸로 다시 시도)
성공하면 BotFather가 긴 문자열을 줍니다. 예:
8123456789:AAE1aBcD...길고복잡한문자열
이게 TELEGRAM_TOKEN 입니다. 메모장에 복사해 두세요. (절대 남에게 공유 금지)
2단계. 내 CHAT_ID 알아내기
방금 만든 내 봇을 검색해서 들어간 뒤 아무 메시지나 하나 보냅니다. (예: 안녕)
이 단계를 꼭 먼저 해야 합니다. 안 하면 봇이 나에게 메시지를 못 보냅니다.
텔레그램에서 @userinfobot 을 검색해 들어가 /start 를 누릅니다.
숫자로 된 Id를 알려줍니다. 예: 1234567890 이게 CHAT_ID 입니다. 역시 메모장에 복사해 두세요.
3단계. GitHub 가입하고 저장소(repository) 만들기
https://github.com 에 들어가 무료 가입 / 로그인 합니다.
오른쪽 위 + 버튼 → New repository 클릭.
Repository name 에 아무 이름이나 적습니다. 예: hyu-notice
Private (비공개)를 선택하는 걸 추천합니다.
아래 Create repository 클릭.
4단계. 파일 4개 올리기
GitHub 저장소 화면에서 Add file → Upload files 를 누른 뒤, 받은 파일 3개를 올립니다:

check_notices.py
requirements.txt
README.md
그 다음, 자동 실행 설정 파일(notices.yml)은 특정 폴더 안에 들어가야 합니다. 가장 쉬운 방법:

저장소 화면에서 Add file → Create new file 클릭.
파일 이름 칸에 정확히 이렇게 입력합니다 (슬래시 / 포함):
.github/workflows/notices.yml
(/ 를 입력하면 자동으로 폴더가 만들어집니다)
받은 notices.yml 파일의 내용을 전부 복사해서 그 안에 붙여넣습니다.
맨 아래 Commit changes (초록 버튼) 클릭.
정리하면 최종 구조는 이렇게 됩니다:

hyu-notice/
├─ check_notices.py
├─ requirements.txt
├─ README.md
└─ .github/
   └─ workflows/
      └─ notices.yml
5단계. RSS 주소 채우기 (가장 중요)
check_notices.py 안의 두 줄을 진짜 RSS 주소로 바꿔야 합니다.

RSS 주소 찾는 법 (PC 권장):

크롬 같은 브라우저에서 공지 페이지를 엽니다.
한양대 전체공지: https://www.hanyang.ac.kr/notice_all
경영대 공지: https://bizug.hanyang.ac.kr/-3
페이지에서 검색창 근처에 있는 RSS 라는 글자(또는 주황색 아이콘)를 찾습니다.
그 RSS 글자 위에서 마우스 오른쪽 클릭 → "링크 주소 복사" 를 누릅니다. (모바일이라면 RSS 글자를 길게 눌러 "링크 복사")
복사한 주소를 check_notices.py 의 해당 자리에 붙여넣습니다.
GitHub에서 파일을 고치는 법:

저장소에서 check_notices.py 를 클릭합니다.
오른쪽 위 연필 아이콘(Edit) 을 누릅니다.
아래 두 줄을 찾아서 따옴표 안의 안내문을 복사한 RSS 주소로 교체합니다.
"한양대 전체공지": "여기에_한양대_공지_RSS_주소를_붙여넣으세요",
"경영대 공지": "여기에_경영대_공지_RSS_주소를_붙여넣으세요",
바꾼 뒤 예시:
"한양대 전체공지": "https://www.hanyang.ac.kr/.../rss",
"경영대 공지": "https://bizug.hanyang.ac.kr/.../rss",
Commit changes 클릭.
RSS 주소를 못 찾겠으면, 우선 이 단계를 건너뛰고 7단계에서 직접 실행해 보세요. 코드가 "RSS를 못 읽었어요"라고 텔레그램으로 알려주거나, 실행 기록(로그)에 공지 0개 읽음 이라고 표시됩니다. 그때 다시 주소를 확인하면 됩니다.

6단계. 비밀값(토큰) 등록하기
토큰을 코드에 직접 적지 않고 안전한 곳에 보관합니다.

GitHub 저장소에서 위쪽 Settings 탭 클릭.
왼쪽 메뉴에서 Secrets and variables → Actions 클릭.
New repository secret 클릭.
Name 에 TELEGRAM_TOKEN, Secret 에 1단계에서 받은 토큰을 붙여넣고 Add secret.
다시 New repository secret 클릭.
Name 에 CHAT_ID, Secret 에 2단계에서 받은 숫자를 붙여넣고 Add secret.
이름(TELEGRAM_TOKEN, CHAT_ID)은 철자 그대로 적어야 합니다. 대소문자도 동일하게.

7단계. 직접 한번 실행해서 확인하기
GitHub 저장소에서 위쪽 Actions 탭 클릭.
(처음이면 "I understand my workflows..." 초록 버튼이 나오면 눌러 허용)
왼쪽에서 한양대 공지 알림 을 클릭.
오른쪽 Run workflow 버튼 → 다시 Run workflow 클릭.
잠시 뒤 실행 항목을 클릭하면 진행 상황을 볼 수 있습니다. 초록 체크(✓)가 뜨면 성공입니다.
실행 기록(로그)을 열어 공지 N개 읽음 처럼 숫자가 0보다 크면 정상입니다.
첫 실행에서는 기존 공지가 한꺼번에 오지 않도록 '읽음'으로만 기록하고 알림은 안 보냅니다. 이게 정상이에요. 이후 새 공지가 올라오면 그때부터 텔레그램으로 알림이 옵니다.

이제 끝입니다. 앞으로 30분마다 자동으로 확인합니다.

문제 해결
알림이 안 와요 (빨간 X 표시) → Actions의 실행 기록을 열어 빨간 글씨를 봅니다. → TELEGRAM_TOKEN / CHAT_ID 가 설정되지 않았습니다 → 6단계 Secret 이름 철자 확인. → 공지 0개 읽음 → 5단계 RSS 주소가 틀렸습니다. 다시 복사해서 넣으세요.

2단계에서 봇이 메시지를 못 보내요 → 내 봇에게 먼저 아무 메시지나 보냈는지 확인하세요. (봇이 말을 먼저 걸 수 없어요)

알림이 너무 자주/늦게 와요 → notices.yml 의 */30 숫자를 바꾸면 됩니다. */60 = 1시간마다. (GitHub 무료 계정은 정시보다 몇 분 늦을 수 있는데 정상입니다.)

공지 게시판을 더 추가하고 싶어요 → check_notices.py 의 FEEDS 목록에 같은 형식으로 한 줄 더 추가하면 됩니다.

막히는 단계가 있으면 그 화면을 캡처해서 물어보면, 그 지점부터 다시 짚어드릴게요.
