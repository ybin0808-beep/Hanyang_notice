"""
한양대 공지 → 텔레그램 알림 봇
RSS 피드를 읽어서, 새로 올라온 공지만 텔레그램으로 보냅니다.
(코드를 직접 고칠 필요는 거의 없어요. 아래 FEEDS 의 주소만 확인하면 됩니다.)
"""
import os
import sys
import json
import html
import feedparser
import requests

# ============================================================
# 여기 RSS 주소만 확인하세요.
# README 의 "5단계: RSS 주소 채우기" 를 보고 정확한 주소로 바꾸면 됩니다.
# 알림 이름은 자유롭게 바꿔도 됩니다. (예: "경영대" -> "경영대학부")
# 게시판을 더 추가하고 싶으면 같은 형식으로 한 줄 더 넣으면 됩니다.
# ============================================================
FEEDS = {
    "한양대 전체공지": "https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=kr_ac_hanyang_noticeBoard_web_portlet_NoticeBoardPortlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&_kr_ac_hanyang_noticeBoard_web_portlet_NoticeBoardPortlet_cmd=rss",
    "경영대 공지": "https://bizug.hanyang.ac.kr/-3?p_p_id=kr_ac_hanyang_bbs_web_portlet_BbsPortlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&_kr_ac_hanyang_bbs_web_portlet_BbsPortlet_cmd=rss",
}
# ============================================================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
SEEN_FILE = "seen.json"     # 이미 보낸 공지를 기억해 두는 파일 (자동 관리됨)
MAX_KEEP = 300              # 게시판별로 기억해 둘 공지 개수


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=20,
        )
        if resp.status_code != 200:
            print("텔레그램 전송 실패:", resp.text)
    except Exception as e:
        print("텔레그램 전송 중 오류:", e)


def main():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("오류: TELEGRAM_TOKEN 또는 CHAT_ID 가 설정되지 않았습니다.")
        print("GitHub 저장소의 Settings > Secrets 에 등록했는지 확인하세요.")
        sys.exit(1)

    seen = load_seen()
    first_run = len(seen) == 0   # seen.json 이 비어 있으면 '첫 실행'

    for name, feed_url in FEEDS.items():
        feed = feedparser.parse(feed_url)
        entries = feed.entries
        print(f"[{name}] 공지 {len(entries)}개 읽음")

        # RSS 주소가 틀렸거나 사이트 점검 중이면 글이 0개로 읽힙니다.
        if len(entries) == 0:
            if first_run:
                send_telegram(
                    f"⚠️ '{name}' 의 RSS 주소를 확인해 주세요.\n"
                    f"공지를 하나도 읽지 못했습니다. (주소가 틀렸을 수 있어요)"
                )
            continue

        old_ids = seen.get(name, [])
        old_set = set(old_ids)

        current_ids = []
        new_entries = []
        for e in entries:
            eid = e.get("id") or e.get("link") or e.get("title")
            current_ids.append(eid)
            if eid not in old_set:
                new_entries.append(e)

        # 첫 실행: 기존 공지를 한꺼번에 폭탄처럼 보내지 않고 '읽음'으로만 기록
        if first_run:
            seen[name] = current_ids[:MAX_KEEP]
            continue

        # 새 공지를 오래된 것부터 순서대로 전송
        for e in reversed(new_entries):
            title = html.unescape(e.get("title", "(제목 없음)"))
            link = e.get("link", "")
            msg = f"📢 <b>{html.escape(name)}</b>\n{html.escape(title)}"
            if link:
                msg += f"\n{link}"
            send_telegram(msg)
            print(f"  → 전송: {title}")

        # 기억 목록 갱신 (새 글 + 기존 글 중 최신 MAX_KEEP개만 유지)
        merged = current_ids + [i for i in old_ids if i not in current_ids]
        seen[name] = merged[:MAX_KEEP]

    save_seen(seen)

    if first_run:
        print("첫 실행 완료: 기존 공지를 모두 '읽음'으로 기록했습니다.")
        print("다음 실행부터 새로 올라온 공지만 알림이 갑니다.")


if __name__ == "__main__":
    main()
