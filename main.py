import streamlit as st
import random
import time
from datetime import datetime

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(
    page_title="MJ네 MBTI Study Coach ✨",
    page_icon="🧠",
    layout="wide",
)

# ---------------------------
# Custom CSS (fun effects, emoji rain, gradient title)
# ---------------------------
EMOJI_CHOICES = [
    "🎯", "📚", "🧠", "💡", "📝", "📖", "⌛", "🎧", "🧩", "🚀",
    "🌈", "✨", "🔥", "💪", "🍀", "🪄", "🫶", "🥳", "🙌", "💫"
]

def emoji_rain():
    # Sprinkle 20–30 floating emojis
    n = random.randint(20, 30)
    emojis = ''.join(random.choice(EMOJI_CHOICES) for _ in range(n))
    st.markdown(
        f"""
        <div class="emoji-rain">{emojis}</div>
        <style>
        .emoji-rain {{
            position: relative;
            width: 100%;
            height: 50px;
            overflow: hidden;
            filter: drop-shadow(0 2px 1px rgba(0,0,0,0.15));
            font-size: 20px;
            letter-spacing: 8px;
            animation: floaty 4s ease-in-out infinite alternate;
            text-align: center;
        }}
        @keyframes floaty {{
            0% {{ transform: translateY(0px); opacity: 0.9; }}
            100% {{ transform: translateY(-12px); opacity: 1; }}
        }}
        .gradient-title {{
            font-size: clamp(26px, 5vw, 56px);
            font-weight: 800;
            line-height: 1.1;
            background: linear-gradient(90deg, #6EE7F9, #A78BFA, #F472B6, #FBBF24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .pill {{
            display: inline-block; padding: 6px 12px; border-radius: 999px;
            background: rgba(167, 139, 250, .12); color: #6D28D9; font-weight: 600;
            border: 1px solid rgba(109, 40, 217, .2);
        }}
        .card {{
            border-radius: 16px; padding: 16px; border: 1px solid rgba(0,0,0,0.06);
            background: rgba(255,255,255,0.6); box-shadow: 0 6px 24px rgba(0,0,0,.06);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------
# Data: MBTI → study strategies
# ---------------------------
TIP_BANK = {
    "ISTJ": {
        "title": "ISTJ — The Inspector 🗂️",
        "vibe": "명확한 규칙과 체크리스트에 강함!",
        "methods": [
            "📅 주간 계획 → 일일 To‑Do로 세분화 (시간 블록: 50분 집중 / 10분 휴식)",
            "🧱 과목별 체크리스트 + 진행률 바(✅ Done% 표시)",
            "📚 노트는 목차/색인으로 정리 → 나중에 빠른 검색"
        ],
        "pitfalls": "완벽주의로 시작이 늦어질 수 있어요. 80% 완성도에서 출발!",
        "tools": "Google Calendar, Notion Database, Anki"
    },
    "ISFJ": {
        "title": "ISFJ — The Guardian 🫶",
        "vibe": "따뜻한 루틴과 보관 정리에 강점!",
        "methods": [
            "🌿 아침 20분 정리 + 저녁 10분 회고(감사 3가지 적기)",
            "📝 인덱스 카드 요약 → 친구에게 설명하는 듯 써보기",
            "📦 과목별 폴더/바인더 구축 + 포스트잇 색상 규칙"
        ],
        "pitfalls": "타인을 돕느라 나의 공부 시간이 줄어듦 → 학습 ‘약속 시간’ 만들기",
        "tools": "GoodNotes, Forest, Quizlet"
    },
    "INFJ": {
        "title": "INFJ — The Sage 🔮",
        "vibe": "의미/가치 연결 시 폭발적인 집중!",
        "methods": [
            "🧭 ‘왜’ 학습하는지 한줄 미션 작성 → 매 세션 상단에 표시",
            "🧩 개념 간 관계도(마인드맵) 1장에 그리기",
            "🧘 25분 집중 + 5분 호흡/스트레칭 (4세트 후 롱브레이크)"
        ],
        "pitfalls": "과몰입·피로 누적 → 에너지 로그로 조절",
        "tools": "Obsidian, XMind, Headspace"
    },
    "INTJ": {
        "title": "INTJ — The Architect 🧠",
        "vibe": "전략 수립·장기로드맵 천재!",
        "methods": [
            "🗺️ 시험일까지 Gantt 로드맵 → 마일스톤 역산",
            "📈 ‘성장 가설’ 세우고 매주 실험(예: 기억률↑엔 뭘 바꿀까?)",
            "🔁 Feynman 기법으로 개념을 초등학생에게 설명하듯 정리"
        ],
        "pitfalls": "계획만 치밀, 실행은 미룸 → ‘오늘 한 일 3개’ 먼저 시작",
        "tools": "Notion Timeline, Anki, Deep Work Timer"
    },
    "ISTP": {
        "title": "ISTP — The Tinkerer 🛠️",
        "vibe": "손으로 해보면 이해가 훨씬 빨라요!",
        "methods": [
            "🧪 개념 1개 → 바로 미니 실습(코드/문제/사례)",
            "🎯 30분 난이도 믹스(쉬운 3 + 중간 1 + 어려운 1)",
            "📉 오답 노트는 ‘왜 틀렸나’ 원인 라벨링"
        ],
        "pitfalls": "흥미 없으면 중도 이탈 → 미션형 과제 부여",
        "tools": "LeetCode/백준, Desmos, Notion Kanban"
    },
    "ISFP": {
        "title": "ISFP — The Artist 🎨",
        "vibe": "감각·미학 자극 시 몰입!",
        "methods": [
            "🎧 Lo‑fi + 아로마 + 조명 → ‘감각 루틴’ 만들기",
            "🖍️ 색코드 요약/스케치노트로 개념 시각화",
            "🌿 20분마다 마이크로 스트레칭 + 하이드레이션"
        ],
        "pitfalls": "감정 기복으로 흐름 끊김 → 초단위 미션으로 관성 확보",
        "tools": "GoodNotes/Procreate, Tide, Focus To‑Do"
    },
    "INFP": {
        "title": "INFP — The Dreamer 🌈",
        "vibe": "스토리와 가치가 있으면 끝까지 간다!",
        "methods": [
            "📖 개념을 ‘짧은 이야기/비유’로 재창조",
            "🧩 Pomodoro(25/5) + 마지막 5분은 저널링",
            "🤝 스터디메이트와 ‘서로 가르치기’ 페어"
        ],
        "pitfalls": "완벽한 분위기 기다림 → 5분 스타터로 즉시 시작",
        "tools": "Notion Journal, Readwise, Anki"
    },
    "INTP": {
        "title": "INTP — The Analyst 🧪",
        "vibe": "원리 파헤치기 + 구조화 최고!",
        "methods": [
            "🧠 정의→정리→증명→반례 순서로 노트 템플릿",
            "🧵 오류 로그(버그‧오개념) 축적 → 주간 회고",
            "🔬 ‘왜?’를 3번 더 묻기"
        ],
        "pitfalls": "깊게만 파고 마감 놓침 → 타임박스 철저",
        "tools": "Obsidian(Backlinks), Zotero, VS Code + Timer"
    },
    "ESTP": {
        "title": "ESTP — The Dynamo 🏎️",
        "vibe": "즉각적 성과와 경쟁에 불탄다!",
        "methods": [
            "🏁 스톱워치 퀴즈 레이싱(점수판 표시)",
            "📊 일간 랭킹/스코어보드로 게임화",
            "🤼‍♂️ 친구와 ‘스피드 티칭’ 3분 배틀"
        ],
        "pitfalls": "지루하면 탈선 → 작은 승리 계속 제공",
        "tools": "Kahoot/Quizizz, Anki Heatmap, Focus timer"
    },
    "ESFP": {
        "title": "ESFP — The Performer 🪩",
        "vibe": "리듬·사교가 에너지!",
        "methods": [
            "🎶 BGM + 25분 댄스‑브레이크(30초) 보상",
            "📸 공부 Vlog/체크인 셀카로 동기부여",
            "👯 그룹 스터디에서 발표 담당 맡기"
        ],
        "pitfalls": "FOMO → 공부·휴대폰 분리 공간",
        "tools": "Forest, Habitica, Google Meet Timer"
    },
    "ENFP": {
        "title": "ENFP — The Spark ✨",
        "vibe": "아이디어 폭주 → 프로젝트형이 딱!",
        "methods": [
            "🧨 7일 미니 프로젝트(결과물 1개) 설계",
            "🔗 흥미 연결(관심사 ↔ 학습 주제 매핑 보드)",
            "🍀 랜덤 보상 뽑기(캡슐/룰렛)"
        ],
        "pitfalls": "시작 多, 마무리 少 → ‘끝내기 스프린트’ 예약",
        "tools": "Notion Kanban, Wheel of Names, Trello"
    },
    "ENTP": {
        "title": "ENTP — The Debater 🗣️",
        "vibe": "논쟁·실험이 동력!",
        "methods": [
            "🎤 주장‑반박‑재반박 카드 만들기",
            "🧪 학습 가설 세우고 A/B 공부법 실험",
            "🧩 브레인라이팅(제한시간 3분 아이디어 폭발)"
        ],
        "pitfalls": "지루함에 쉽게 이탈 → 타이머와 데드라인",
        "tools": "Miro/Mural, Notion DB, Focus Keeper"
    },
    "ESTJ": {
        "title": "ESTJ — The Director 📊",
        "vibe": "표준 운영 절차(SOP) 좋아함!",
        "methods": [
            "📋 학습 SOP(준비→실행→검토) 체크리스트",
            "🔁 매주 KPI: 시간/정확도/속도 측정",
            "🧭 주간 회의(셀프 스탠드업) 10분"
        ],
        "pitfalls": "유연성 부족 → ‘실험의 날’ 1회 추가",
        "tools": "Google Sheets Dashboard, Toggl, Anki"
    },
    "ESFJ": {
        "title": "ESFJ — The Host 🤝",
        "vibe": "사람과 함께할 때 최고 성과!",
        "methods": [
            "👥 페어 스터디(서로 칭찬·리뷰 카드)",
            "🍪 스터디 간식 보상 시스템",
            "📅 주중 2회 ‘가르치기 세션’ 예약"
        ],
        "pitfalls": "남 챙기다 본인 놓침 → ‘내 공부 타임’ 고정",
        "tools": "Google Calendar, Notion Template, Quizlet"
    },
    "ENFJ": {
        "title": "ENFJ — The Mentor 🧑‍🏫",
        "vibe": "목표 공유·리더십 있을 때 몰입!",
        "methods": [
            "📣 스터디 리더 맡아 커리큘럼 설계",
            "📝 주간 리플렉션 폼 공유",
            "🎯 주간 OKR(목표/핵심결과) 설정"
        ],
        "pitfalls": "과부하 → 위임·자동화 도구 활용",
        "tools": "Typeform/Google Forms, Notion OKR, Slack"
    },
    "ENTJ": {
        "title": "ENTJ — The Commander 🦾",
        "vibe": "목표 지향 + 시스템 드라이브",
        "methods": [
            "🏆 역산형 로드맵 + 버퍼 관리",
            "📈 대시보드로 지표 실시간 추적",
            "🧠 고난도 과제 ‘황금 시간대’에 배치"
        ],
        "pitfalls": "과도한 압박 → 회복 루틴 예약",
        "tools": "Airtable/Sheets, Pomofocus, Notion Template"
    },
    "ISTJ2": {},  # placeholder (kept for structure; not used)
}

# Add remaining types succinctly to keep file size reasonable while covering all 16
TIP_BANK.update({
    "ENTP": TIP_BANK["ENTP"],
})

# Fill missing types compactly to ensure all 16 exist
for t in ["ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP","ESTP","ESFP","ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ"]:
    assert t in TIP_BANK, f"Missing tips for {t}"

ALL_TYPES = list(TIP_BANK.keys())

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.caption("아이폰 이모지 감성 듬뿍✨ 공부 코치")
    selected = st.selectbox(
        "MBTI 유형을 골라주세요",
        options=ALL_TYPES,
        index=ALL_TYPES.index("ENFP") if "ENFP" in ALL_TYPES else 0,
        help="16가지 유형 중 하나를 선택하면 맞춤 공부법을 제안해요."
    )
    focus_mode = st.toggle("🧘 Focus Mode (잡것 숨기기)", value=False)
    if st.button("🎁 랜덤 응원 받기"):
        st.toast(random.choice([
            "작게라도 시작하면 이미 승리! 🏁",
            "오늘의 1%가 내일의 100%가 돼요 💫",
            "물 한잔 + 25분 집중 가자! 💧⌛",
            "어제의 나를 이기는 중…🔥",
        ]), icon="🎉")

# ---------------------------
# Header
# ---------------------------
st.markdown("<div class='gradient-title'>MBTI Study Coach</div>", unsafe_allow_html=True)
emoji_rain()
st.write("")

card_col1, card_col2, card_col3 = st.columns([1.2,1,1])
with card_col1:
    st.markdown("<span class='pill'>📚 Personalized Study Tips</span>", unsafe_allow_html=True)
    st.caption("선택한 MBTI에 맞는 방법을 자동 추천해요.")
with card_col2:
    st.markdown("<span class='pill'>⌛ Pomodoro Timer</span>", unsafe_allow_html=True)
    st.caption("25/5 또는 커스텀 타이머.")
with card_col3:
    st.markdown("<span class='pill'>📥 Download Plan</span>", unsafe_allow_html=True)
    st.caption("나만의 플랜 텍스트 내려받기.")

# ---------------------------
# Main content
# ---------------------------
data = TIP_BANK[selected]

left, right = st.columns([1.2, 1])
with left:
    st.subheader(f"{data['title']}")
    st.write(f"**Vibe**: {data['vibe']} 🫶")

    with st.container(border=True):
        st.markdown("**✅ Best Methods**")
        for m in data["methods"]:
            st.markdown(f"- {m}")
        st.markdown(f"**⚠️ Watch‑outs**: {data['pitfalls']}")
        st.markdown(f"**🛠️ Tools**: {data['tools']}")

    # Create a quick, printable daily plan text
    plan_text = f"""
    📅 Daily Plan for {selected} ({datetime.now().date()})\n
    1) Focus Block 1 — 25min (Goal): ____________________\n       5min Break — Stretch + Water\n    2) Focus Block 2 — 25min (Goal): ____________________\n       5min Break — Breathe\n    3) Focus Block 3 — 25min (Goal): ____________________\n       15min Big Break — Walk\n
    Checklists:\n    [ ] 핵심 개념 3개 요약\n    [ ] 오늘의 1문장 회고\n    [ ] 내일 시작점 1개 적기\n    """

    st.download_button(
        label="📥 나만의 데일리 플랜 다운로드",
        data=plan_text,
        file_name=f"study_plan_{selected}_{datetime.now().date()}.txt",
        mime="text/plain",
        help="텍스트 파일로 저장됩니다."
    )

    # Fun status meters
    with st.container(border=True):
        st.markdown("**📈 오늘의 집중 게이지**")
        pg = st.progress(0, text="부팅 중… 🚀")
        for i in range(0, 101, 5):
            time.sleep(0.01)
            pg.progress(i, text=f"집중력 충전 {i}% ✨")
        st.success("집중력 충전 완료!🔥")

with right:
    st.subheader("⌛ Pomodoro Timer")
    st.caption("기본 25/5. ‘Start’ 누르면 화면 업데이트됩니다.")
    colA, colB = st.columns(2)
    with colA:
        focus_min = st.number_input("Focus (min)", min_value=5, max_value=90, value=25, step=5)
    with colB:
        break_min = st.number_input("Break (min)", min_value=1, max_value=30, value=5, step=1)

    timer_spot = st.empty()
    if st.button("▶️ Start Pomodoro"):
        st.balloons()
        # Focus phase
        total = focus_min * 60
        for remaining in range(total, -1, -1):
            mm, ss = divmod(remaining, 60)
            timer_spot.metric("Focus Time", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        st.toast("Break time! 🎉", icon="🍵")
        st.snow()
        # Break phase
        total_b = break_min * 60
        for remaining in range(total_b, -1, -1):
            mm, ss = divmod(remaining, 60)
            timer_spot.metric("Break Time", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        st.success("세트 완료! 다음 라운드도 가볼까요? 🏁")

# ---------------------------
# Focus mode CSS tweak
# ---------------------------
if focus_mode:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        footer, header { opacity: .2; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------
# Chat‑style encouragement
# ---------------------------
st.divider()
st.subheader("💬 Quick Coach")
msg = st.text_input("질문이나 현재 상태를 적어보세요 (예: ‘집중이 안 돼요’ ‘어떤 과목부터 할까요?’)", value="")
if msg:
    with st.chat_message("user"):
        st.write(msg)
    with st.chat_message("assistant"):
        reply_bank = [
            "작게 시작해요. 5분만 타이머 스타트! ⏱️",
            "오늘의 장애물 하나만 정의하고 치워봅시다 🧹",
            "지금 에너지 70%라면, 난이도 중간 과제부터! ⚖️",
            "목표를 ‘행동’으로: 동사로 시작하는 한 줄! ✍️",
        ]
        st.write(random.choice(reply_bank))
        st.markdown("_응원 이모지 팡팡!_ 🥳🙌✨💪")
