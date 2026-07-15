# -*- coding: utf-8 -*-
"""
시민체감형 사회안전 스마트시티 교육연구단 (BK21) 정적 사이트 생성기
------------------------------------------------------------------
편집 방법:
  - 아래 CONFIG 값(제목/링크/교수 명단/과목 등)만 고치면 됩니다.
  - 링크가 아직 없는 항목은 "#" 으로 두었습니다. 실제 URL로 교체하세요.
  - 저장 후:  python3 generate.py   실행 → 루트에 html, assets/style.css 생성
"""
import os, html, datetime

OUT = os.path.dirname(os.path.abspath(__file__))

# ======================================================================
# 1) 편집 영역 (CONFIG)  ------------------------------------------------
# ======================================================================
SITE = {
    "name_ko": "시민체감형 사회안전 스마트시티 교육연구단",
    "name_en": "Education and Research Group for Citizen-Centered Public Safety in Smart Cities",
    "short": "BK21 스마트시티 교육연구단",
    "program": "지역대학 연합형 교육연구단 지원 시범사업 · 4단계 BK21",
    "period": "2026 – 2027 (1년 6개월)",
    "vision_ko": "사회안전과 인프라 문제를 지능적으로 해결하고,\n시민이 체감할 수 있는 성과를 창출하는 융합형 전문인력 양성",
    "email": "byang@cbnu.ac.kr",   # 대표 연락 이메일 (교체 가능)
}

# 4개 축(핵심 기조)
PILLARS = [
    ("사회안전", "Public Safety", "복합재난 및 사회위험 대응 역량 강화"),
    ("인프라",   "Infrastructure", "기반시설 유지관리 및 회복력 향상"),
    ("지능화",   "Intelligence", "데이터·AI 기반 분석 및 의사결정 고도화"),
    ("시민체감", "Citizen-Centered", "현장적용과 지역사회 체감성과 확산"),
]

# 참여 대학 (주관/참여 구분, 학과, 역할, 대표색, 홈페이지)
UNIVERSITIES = [
    {"tag": "주관", "name": "충북대학교", "dept": "토목공학부", "logo": "cbnu",
     "role": "인프라 진단 · 유지관리", "url": "https://www.cbnu.ac.kr", "dept_url": "#"},
    {"tag": "참여", "name": "대전대학교", "dept": "재난안전공학과", "logo": "dju",
     "role": "재난안전 대응", "url": "https://www.dju.ac.kr", "dept_url": "#"},
    {"tag": "참여", "name": "청주대학교", "dept": "인공지능소프트웨어학과", "logo": "cju",
     "role": "AI · 데이터 분석", "url": "https://www.cju.ac.kr", "dept_url": "#"},
    {"tag": "참여", "name": "국립한밭대학교", "dept": "건설환경공학과", "logo": "hanbat",
     "role": "기술확산 · 실용화", "url": "https://www.hanbat.ac.kr", "dept_url": "#"},
]

# 참여교수 (대학 → 명단). lead=True 는 교육연구단장 표시.
MEMBERS = {
    "충북대학교 토목공학부": [
        {"name": "정종원", "photo": "jung", "lead": True, "field": "지반공학",
         "courses": ["스마트기반시설설계프로젝트", "스마트건설공학특론"]},
        {"name": "양범주", "photo": "yang", "field": "콘크리트공학 · 기능성 건설재료",
         "courses": ["스마트건설재료", "토목구조물설계"]},
        {"name": "윤형철", "photo": "yoonhc", "field": "품질/안전 · 스마트 구조",
         "courses": ["스마트구조공학", "스마트구조물모니터링"]},
        {"name": "이의훈", "photo": "lee", "field": "수공학 · 스마트 워터 시스템",
         "courses": ["도시급배수망 스마트설계", "수자원시스템을 위한 인공지능"]},
        {"name": "송헌수", "photo": "song", "field": "원격탐사 · 공간정보 (신진연구원)",
         "courses": ["데이터융합 및 인공신경망", "사진측량학 특론"]},
    ],
    "대전대학교 재난안전공학과": [
        {"name": "김규범", "photo": "kim", "field": "수공학 · Data 기반 수자원 안정공학",
         "courses": ["수자원개발 최신 기술", "지반정보통계분석론"]},
        {"name": "윤형구", "photo": "yoonhg", "field": "지반공학 · 스마트건설안전공학",
         "courses": ["구조물방재특론", "고급방재조사"]},
    ],
    "청주대학교 인공지능소프트웨어학과": [
        {"name": "고혜경", "photo": "ko", "field": "데이터베이스 · 데이터공학",
         "courses": ["데이터아키텍처", "데이터베이스보안"]},
        {"name": "최형욱", "photo": "choi", "field": "인공지능 · 컴퓨터비전 (신진연구원)",
         "courses": ["인공지능이해", "인공신경망"]},
    ],
    "국립한밭대학교 건설환경공학과": [
        {"name": "곽신영", "photo": "kwak", "field": "동력학 · 구조해석",
         "courses": ["최적설계", "전산구조"]},
        {"name": "전해민", "photo": "jeon", "field": "품질/안전 · 건설IT",
         "courses": ["건설IT 특론: 프로그래밍", "건설자동화를 위한 컴퓨터비전"]},
    ],
}

# 공동교과목 / 온라인 강의 (2학기 운영). link=강의실 URL, submit=과제제출 URL
COURSES = [
    {"title": "스마트건설재료", "univ": "충북대", "prof": "양범주",
     "mode": "블렌디드(실시간 온라인 병행)", "link": "#", "submit": "#"},
    {"title": "스마트구조물모니터링", "univ": "충북대", "prof": "윤형철",
     "mode": "블렌디드(실시간 온라인 병행)", "link": "#", "submit": "#"},
    {"title": "수자원시스템을 위한 인공지능", "univ": "충북대", "prof": "이의훈",
     "mode": "블렌디드(실시간 온라인 병행)", "link": "#", "submit": "#"},
    {"title": "구조물방재특론", "univ": "대전대", "prof": "윤형구",
     "mode": "실시간 온라인", "link": "#", "submit": "#"},
    {"title": "인공지능이해", "univ": "청주대", "prof": "최형욱",
     "mode": "실시간 온라인", "link": "#", "submit": "#"},
    {"title": "최적설계", "univ": "한밭대", "prof": "곽신영",
     "mode": "실시간 온라인", "link": "#", "submit": "#"},
]

# 빠른 링크 (홈 상단 포털)
QUICK_LINKS = [
    ("과제 제출", "제출 기한과 파일 업로드", "courses.html#submit", "▲"),
    ("온라인 강의", "실시간·녹화 강의실 입장", "courses.html#online", "▶"),
    ("공동교과목 안내", "학점교류 · 수강 절차", "courses.html", "◆"),
    ("참여교수", "4개 대학 11인", "members.html", "●"),
]

# 바로가기 (portal.html)
PORTAL = {
    "대학 · 학과": [
        ("충북대학교 토목공학부", "#"),
        ("대전대학교 재난안전공학과", "#"),
        ("청주대학교 인공지능소프트웨어학과", "#"),
        ("국립한밭대학교 건설환경공학과", "#"),
    ],
    "사업 · 기관": [
        ("한국연구재단 BK21 FOUR", "https://bk21four.nrf.re.kr/"),
        ("교육부", "https://www.moe.go.kr"),
        ("한국연구재단(NRF)", "https://www.nrf.re.kr"),
    ],
    "자료 · 서식": [
        ("사업계획서 / 자체평가", "#"),
        ("참여대학원생 서식", "#"),
        ("연구윤리 · 규정", "#"),
    ],
}

# 공지 (홈 최근소식). 최신순.
NOTICES = [
    ("2026-07", "2학기 공동교과목(블렌디드) 운영 및 타대학 수강 신청 안내"),
    ("2026-07", "4개 대학 대학원 학점교류 절차 안내 (석사 3–6학점)"),
    ("2026-06", "시민체감형 사회안전 스마트시티 교육연구단 최종 선정"),
]

NAV = [
    ("home",     "홈",        "index.html"),
    ("about",    "사업 소개",  "about.html"),
    ("members",  "참여교수",   "members.html"),
    ("courses",  "공동교과목", "courses.html"),
    ("portal",   "바로가기",   "portal.html"),
]

# ======================================================================
# 2) 템플릿 / 렌더링  ---------------------------------------------------
# ======================================================================
def esc(s): return html.escape(str(s))

def head(title, active):
    nav_items = "".join(
        f'<a class="nav-link{" is-active" if key==active else ""}" href="{href}">{esc(label)}</a>'
        for key, label, href in NAV
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(SITE['short'])}</title>
<meta name="description" content="{esc(SITE['name_ko'])} — {esc(SITE['name_en'])}">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 40 40" width="34" height="34">
          <circle cx="8" cy="8" r="3.4"/><circle cx="32" cy="8" r="3.4"/>
          <circle cx="8" cy="32" r="3.4"/><circle cx="32" cy="32" r="3.4"/>
          <circle cx="20" cy="20" r="4.2" class="node-c"/>
          <path d="M8 8 L20 20 L32 8 M8 32 L20 20 L32 32" class="node-link"/>
        </svg>
      </span>
      <span class="brand-text">
        <b>BK21</b><i>스마트시티 사회안전 교육연구단</i>
      </span>
    </a>
    <nav class="nav" aria-label="주요 메뉴">{nav_items}</nav>
    <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="nav-mobile">{nav_items}</div>
</header>
<main id="main">
"""

def foot():
    year = datetime.date.today().year
    unis = " · ".join(f'{u["name"]} {u["dept"]}' for u in UNIVERSITIES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <div class="foot-title">{esc(SITE['name_ko'])}</div>
      <div class="foot-en">{esc(SITE['name_en'])}</div>
      <div class="foot-unis">{esc(unis)}</div>
    </div>
    <div class="foot-links">
      <a href="about.html">사업 소개</a>
      <a href="members.html">참여교수</a>
      <a href="courses.html">공동교과목</a>
      <a href="portal.html">바로가기</a>
      <a href="mailto:{esc(SITE['email'])}">문의</a>
    </div>
  </div>
  <div class="wrap foot-logos">
    <img src="assets/logo_cbnu.png" alt="충북대학교">
    <img src="assets/logo_dju.png" alt="대전대학교">
    <img src="assets/logo_cju.png" alt="청주대학교">
    <img src="assets/logo_hanbat.png" alt="국립한밭대학교">
    <img src="assets/logo_brainkorea.png" alt="BrainKorea">
  </div>
  <div class="wrap foot-base">
    <span>© {year} {esc(SITE['short'])}</span>
    <span>{esc(SITE['program'])}</span>
  </div>
</footer>
<script>
(function(){{
  var t=document.querySelector('.nav-toggle'), m=document.querySelector('.nav-mobile');
  if(t&&m){{t.addEventListener('click',function(){{
    var open=m.classList.toggle('open');
    t.setAttribute('aria-expanded',open); t.classList.toggle('x',open);
  }});}}
}})();
</script>
</body></html>"""

def page(name, title, active, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(head(title, active) + body + foot())

# ---- 홈 -------------------------------------------------------------
def render_home():
    stat_items = [
        ("04", "참여 대학"),
        ("11", "참여교수"),
        ("04", "핵심 기조"),
        ("18", "사업 개월"),
    ]
    stats = "".join(
        f'<div class="stat"><span class="stat-num">{n}</span><span class="stat-label">{esc(l)}</span></div>'
        for n, l in stat_items
    )
    quick = "".join(
        f'''<a class="qcard" href="{href}">
              <span class="qsym" aria-hidden="true">{sym}</span>
              <span class="qtitle">{esc(t)}</span>
              <span class="qdesc">{esc(d)}</span>
              <span class="qarrow" aria-hidden="true">→</span>
            </a>'''
        for t, d, href, sym in QUICK_LINKS
    )
    pillars = "".join(
        f'''<div class="pillar">
              <span class="pillar-en">{esc(en)}</span>
              <h3>{esc(ko)}</h3>
              <p>{esc(desc)}</p>
            </div>'''
        for ko, en, desc in PILLARS
    )
    uni_cards = "".join(
        f'''<a class="uni" href="{u["url"]}" target="_blank" rel="noopener">
              <span class="uni-logo"><img src="assets/logo_{u['logo']}.png" alt="{esc(u['name'])} 로고" loading="lazy"></span>
              <span class="uni-tag {'is-lead' if u['tag']=='주관' else ''}">{esc(u['tag'])}</span>
              <span class="uni-name">{esc(u['name'])}</span>
              <span class="uni-dept">{esc(u['dept'])}</span>
              <span class="uni-role">{esc(u['role'])}</span>
            </a>'''
        for u in UNIVERSITIES
    )
    notices = "".join(
        f'<li><time>{esc(d)}</time><span>{esc(txt)}</span></li>'
        for d, txt in NOTICES
    )
    vis = esc(SITE['vision_ko']).replace("\n", "<br>")
    body = f"""
<section class="hero">
  <div class="hero-net" aria-hidden="true">
    <svg viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice">
      <defs>
        <radialGradient id="glow" cx="50%" cy="40%" r="70%">
          <stop offset="0%" stop-color="#123a7a" stop-opacity="0.55"/>
          <stop offset="100%" stop-color="#071634" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1200" height="520" fill="url(#glow)"/>
      <g class="net-links">
        <path d="M180 120 L600 260 M1020 120 L600 260 M180 400 L600 260 M1020 400 L600 260 M180 120 L1020 120 M180 400 L1020 400"/>
      </g>
      <g class="net-nodes">
        <circle cx="180" cy="120" r="6"/><circle cx="1020" cy="120" r="6"/>
        <circle cx="180" cy="400" r="6"/><circle cx="1020" cy="400" r="6"/>
        <circle cx="600" cy="260" r="10" class="hub"/>
        <circle cx="390" cy="190" r="3"/><circle cx="810" cy="190" r="3"/>
        <circle cx="390" cy="330" r="3"/><circle cx="810" cy="330" r="3"/>
      </g>
    </svg>
  </div>
  <div class="wrap hero-inner">
    <p class="eyebrow">{esc(SITE['program'])}</p>
    <h1 class="hero-title">{vis}</h1>
    <p class="hero-en">{esc(SITE['name_en'])}</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="courses.html">공동교과목 · 온라인 강의</a>
      <a class="btn btn-ghost" href="about.html">사업 소개</a>
    </div>
    <div class="hero-stats">{stats}</div>
  </div>
</section>

<section class="band band-quick">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">QUICK ACCESS</span>
      <h2>바로 사용하기</h2>
    </div>
    <div class="qgrid">{quick}</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">CORE PILLARS</span>
      <h2>4대 핵심 기조</h2>
      <p class="section-sub">인프라 유지관리에 AI·데이터 지능화를 접목해, 시민이 체감하는 사회안전으로 잇습니다.</p>
    </div>
    <div class="pillar-grid">{pillars}</div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">CONSORTIUM</span>
      <h2>4개 대학 연합</h2>
    </div>
    <div class="uni-grid">{uni_cards}</div>
  </div>
</section>

<section class="band">
  <div class="wrap notice-wrap">
    <div class="section-head left">
      <span class="eyebrow">NOTICE</span>
      <h2>최근 소식</h2>
    </div>
    <ul class="notice-list">{notices}</ul>
  </div>
</section>
"""
    page("index.html", "홈", "home", body)

# ---- 사업 소개 -------------------------------------------------------
def render_about():
    goals = [
        ("교육혁신", "스마트시티 사회안전을 위한 융합 교육"),
        ("연구혁신", "실무형 전문가 양성을 위한 공동연구"),
        ("지역사회혁신", "지역 문제 해결과 시민체감 성과 확산"),
    ]
    goal_html = "".join(
        f'<div class="goal"><span class="goal-idx">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(goals, 1)
    )
    roles = "".join(
        f'''<tr><td class="rt">{esc(u['tag'])}</td>
              <th>{esc(u['name'])}<span>{esc(u['dept'])}</span></th>
              <td>{esc(u['role'])}</td></tr>'''
        for u in UNIVERSITIES
    )
    expects = [
        ("학문적", "융합형 스마트시티 교육·연구 모델 제시",
         ["융합형 교육·연구모델", "사회안전·인프라 지능화", "공동교과·캡스톤 교육", "4개 대학 연합형 교육체계"]),
        ("사회적", "시민체감형 사회안전 수준 향상",
         ["생활안전·복합재난 대응", "인프라 관리 및 도시 회복력", "지역·산업 연계 실증", "시민체감형 안전서비스"]),
        ("경제적", "전문인력 양성과 지역산업 경쟁력 강화",
         ["전문인력 양성 및 일자리", "스마트 안전기술 실용화", "지역산업 경쟁력 강화", "지역혁신 지속성장 기반"]),
    ]
    exp_html = "".join(
        f'''<div class="expect">
              <span class="expect-kind">{esc(kind)}</span>
              <h3>{esc(title)}</h3>
              <ul>{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul>
            </div>'''
        for kind, title, items in expects
    )
    vis = esc(SITE['vision_ko']).replace("\n", "<br>")
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">ABOUT</span>
    <h1>사업 소개</h1>
    <p class="lead">자연적·인위적 복합재난을 사전에 예측·진단·대응하기 위해, 인프라 유지관리 기술에 AI·데이터 기반 지능화 기술을 접목하여
       시민이 체감할 수 있는 사회안전 향상에 기여하는 통합형 안전관리 시스템을 지향합니다.</p>
  </div>
</section>

<section class="band">
  <div class="wrap vision-block">
    <span class="eyebrow center">VISION</span>
    <p class="vision-text">{vis}</p>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">3 GOALS</span><h2>3대 혁신 목표</h2></div>
    <div class="goal-grid">{goal_html}</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">ROLES</span><h2>대학별 역할</h2></div>
    <table class="role-table"><tbody>{roles}</tbody></table>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">EXPECTED OUTCOMES</span><h2>기대효과</h2></div>
    <div class="expect-grid">{exp_html}</div>
  </div>
</section>
"""
    page("about.html", "사업 소개", "about", body)

# ---- 참여교수 -------------------------------------------------------
def render_members():
    groups = ""
    for uni, people in MEMBERS.items():
        cards = ""
        for p in people:
            lead = '<span class="m-lead">교육연구단장</span>' if p.get("lead") else ""
            courses = "".join(f"<li>{esc(c)}</li>" for c in p["courses"])
            if p.get("photo"):
                avatar = f'<span class="m-avatar has-photo"><img src="assets/photo_{p["photo"]}.jpg" alt="{esc(p["name"])} 사진" loading="lazy"></span>'
            else:
                avatar = f'<span class="m-avatar" aria-hidden="true">{esc(p["name"][0])}</span>'
            cards += f'''<div class="mcard{' is-lead' if p.get('lead') else ''}">
                  <div class="mcard-top">
                    {avatar}
                    <div>
                      <div class="m-name">{esc(p['name'])} {lead}</div>
                      <div class="m-field">{esc(p['field'])}</div>
                    </div>
                  </div>
                  <ul class="m-courses">{courses}</ul>
                </div>'''
        groups += f'''<div class="mgroup">
              <h2 class="mgroup-title">{esc(uni)}</h2>
              <div class="mgrid">{cards}</div>
            </div>'''
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">MEMBERS</span>
    <h1>참여교수</h1>
    <p class="lead">4개 대학 11인의 참여교수가 인프라 · 지능화 · 사회안전 · 시민체감을 아우르는 융합 교육·연구를 수행합니다.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">{groups}</div>
</section>
"""
    page("members.html", "참여교수", "members", body)

# ---- 공동교과목 / 온라인 강의 --------------------------------------
def render_courses():
    rows = ""
    for c in COURSES:
        link = c["link"]; submit = c["submit"]
        link_btn = (f'<a class="mini-btn" href="{link}" target="_blank" rel="noopener">입장</a>'
                    if link and link != "#" else '<span class="mini-btn disabled">준비중</span>')
        sub_btn = (f'<a class="mini-btn alt" href="{submit}" target="_blank" rel="noopener">제출</a>'
                   if submit and submit != "#" else '<span class="mini-btn alt disabled">준비중</span>')
        rows += f'''<tr>
              <td class="c-title">{esc(c['title'])}</td>
              <td>{esc(c['univ'])}</td>
              <td>{esc(c['prof'])}</td>
              <td><span class="mode">{esc(c['mode'])}</span></td>
              <td class="c-act">{link_btn}</td>
              <td class="c-act">{sub_btn}</td>
            </tr>'''
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">COURSES</span>
    <h1>공동교과목 · 온라인 강의</h1>
    <p class="lead">2학기에는 각 대학 기존 대학원 과목 중 일부를 <b>BK21 공동교과목</b>으로 지정하고,
       실시간 온라인을 병행하여 타대학 학생이 이동 부담 없이 수강할 수 있도록 운영합니다.</p>
  </div>
</section>

<section class="band" id="online">
  <div class="wrap">
    <div class="section-head left"><span class="eyebrow">ONLINE / SUBMIT</span><h2>강의 · 과제</h2>
      <p class="section-sub">강의실 입장과 과제 제출을 한 표에서 처리합니다. 링크가 준비되면 버튼이 활성화됩니다.</p>
    </div>
    <div class="table-scroll" id="submit">
      <table class="course-table">
        <thead><tr>
          <th>교과목</th><th>대학</th><th>담당</th><th>운영</th><th>강의실</th><th>과제</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">HOW IT WORKS</span><h2>타대학 수강 절차</h2></div>
    <div class="steps">
      <div class="step"><span class="step-n">1</span><h3>학점교류 확인</h3>
        <p>소속 대학원 교학팀에서 4개 대학 간 학점교류 협정과 신청 기간을 확인합니다. (석사 3–6학점 인정)</p></div>
      <div class="step"><span class="step-n">2</span><h3>수강 신청</h3>
        <p>학점교류 신청서를 제출하고, 원하는 공동교과목을 선택합니다. 방학 중 수강신청 기간을 확인하세요.</p></div>
      <div class="step"><span class="step-n">3</span><h3>온라인 입장</h3>
        <p>확정 후 위 표의 <b>강의실 입장</b> 버튼으로 실시간 강의에 참여합니다.</p></div>
      <div class="step"><span class="step-n">4</span><h3>과제 제출</h3>
        <p>과제는 <b>제출</b> 버튼을 통해 기한 내 업로드합니다. 성적은 소속 대학 학점으로 인정됩니다.</p></div>
    </div>
    <p class="note">※ 학점교류 협정·수강신청 마감일은 대학마다 다릅니다. 자세한 사항은 소속 대학원 교학팀 또는
       <a href="mailto:{esc(SITE['email'])}">교육연구단</a>으로 문의하세요.</p>
  </div>
</section>
"""
    page("courses.html", "공동교과목", "courses", body)

# ---- 바로가기 -------------------------------------------------------
def render_portal():
    blocks = ""
    for title, links in PORTAL.items():
        items = "".join(
            (f'<a href="{url}" target="_blank" rel="noopener">{esc(name)}<span aria-hidden="true">↗</span></a>'
             if url and url != "#"
             else f'<a class="pending" href="#">{esc(name)}<span aria-hidden="true">준비중</span></a>')
            for name, url in links
        )
        blocks += f'<div class="portal-block"><h2>{esc(title)}</h2><div class="portal-links">{items}</div></div>'
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">LINKS</span>
    <h1>바로가기</h1>
    <p class="lead">참여 대학·학과, 사업 기관, 자료실로 이동합니다.</p>
  </div>
</section>
<section class="band">
  <div class="wrap portal-grid">{blocks}</div>
</section>
"""
    page("portal.html", "바로가기", "portal", body)

# ======================================================================
# 3) CSS  --------------------------------------------------------------
# ======================================================================
CSS = r"""
:root{
  --ink:#0a1e3f; --navy:#071634; --blue:#2456d6; --blue-2:#1b46b8;
  --cyan:#37c6f4; --sky:#cfe0ff;
  --paper:#f4f7fc; --paper-2:#eaf0fa; --line:#dbe4f2; --card:#ffffff;
  --text:#132846; --muted:#5a6b88; --faint:#8a97ad;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --sans:'Pretendard Variable',Pretendard,system-ui,'Apple SD Gothic Neo',sans-serif;
  --w:1160px; --r:14px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sans);color:var(--text);background:var(--paper);
  line-height:1.65;-webkit-font-smoothing:antialiased;letter-spacing:-.01em}
a{color:inherit;text-decoration:none}
h1,h2,h3{line-height:1.25;letter-spacing:-.02em;margin:0}
.wrap{width:min(var(--w),92vw);margin-inline:auto}
.skip{position:absolute;left:-999px}
.skip:focus{left:12px;top:12px;z-index:100;background:#fff;padding:8px 14px;border-radius:8px}
.eyebrow{font-family:var(--mono);font-size:.72rem;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;color:var(--blue)}
.eyebrow.center{display:block;text-align:center}

/* header */
.site-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.9);
  backdrop-filter:saturate(160%) blur(10px);border-bottom:1px solid var(--line)}
.header-inner{display:flex;align-items:center;gap:20px;height:66px}
.brand{display:flex;align-items:center;gap:11px;margin-right:auto}
.brand-mark svg{display:block}
.brand-mark circle{fill:var(--blue)}
.brand-mark .node-c{fill:var(--cyan)}
.brand-mark .node-link{stroke:var(--blue);stroke-width:1.4;fill:none;opacity:.55}
.brand-text{display:flex;flex-direction:column;line-height:1.1}
.brand-text b{font-family:var(--mono);font-size:.82rem;letter-spacing:.14em;color:var(--blue)}
.brand-text i{font-style:normal;font-weight:700;font-size:.92rem;color:var(--ink)}
.nav{display:flex;gap:4px}
.nav-link{padding:9px 14px;border-radius:9px;font-weight:600;font-size:.94rem;color:#33456a}
.nav-link:hover{background:var(--paper-2);color:var(--ink)}
.nav-link.is-active{color:var(--blue);background:var(--paper-2)}
.nav-toggle{display:none;flex-direction:column;gap:5px;width:42px;height:42px;
  border:1px solid var(--line);border-radius:10px;background:#fff;cursor:pointer;align-items:center;justify-content:center}
.nav-toggle span{width:20px;height:2px;background:var(--ink);transition:.25s}
.nav-toggle.x span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-toggle.x span:nth-child(2){opacity:0}
.nav-toggle.x span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.nav-mobile{display:none;flex-direction:column;padding:8px 4vw 14px;gap:2px;
  background:#fff;border-bottom:1px solid var(--line)}
.nav-mobile.open{display:flex}
.nav-mobile .nav-link{padding:12px 12px}

/* hero */
.hero{position:relative;overflow:hidden;background:
  linear-gradient(160deg,#071634 0%,#0c2a5e 55%,#123a7a 100%);color:#fff}
.hero-net{position:absolute;inset:0;opacity:.9}
.hero-net svg{width:100%;height:100%}
.net-links path{stroke:var(--cyan);stroke-width:1;fill:none;opacity:.28}
.net-nodes circle{fill:var(--cyan);opacity:.75}
.net-nodes .hub{fill:#fff;opacity:.95}
.hero-inner{position:relative;padding:88px 0 76px}
.hero .eyebrow{color:var(--cyan)}
.hero-title{font-size:clamp(1.7rem,3.6vw,2.9rem);font-weight:800;margin:18px 0 16px;
  text-wrap:balance;text-shadow:0 2px 30px rgba(0,0,0,.25)}
.hero-en{color:var(--sky);font-size:.98rem;max-width:640px}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0 44px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:11px;
  font-weight:700;font-size:.96rem;transition:.2s;border:1px solid transparent}
.btn-primary{background:var(--cyan);color:#04233a}
.btn-primary:hover{background:#5fd6fb;transform:translateY(-2px)}
.btn-ghost{border-color:rgba(255,255,255,.4);color:#fff}
.btn-ghost:hover{background:rgba(255,255,255,.12)}
.hero-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;max-width:620px}
.stat{border-top:2px solid rgba(255,255,255,.25);padding-top:12px}
.stat-num{display:block;font-family:var(--mono);font-size:2rem;font-weight:700;color:#fff}
.stat-label{font-size:.82rem;color:var(--sky)}

/* bands */
.band{padding:76px 0}
.band-alt{background:var(--paper-2)}
.band-quick{padding-top:56px;padding-bottom:56px}
.section-head{max-width:720px;margin:0 auto 40px;text-align:center}
.section-head.left{text-align:left;margin-left:0}
.section-head h2{font-size:clamp(1.5rem,2.6vw,2.05rem);font-weight:800;margin-top:8px;color:var(--ink)}
.section-sub{color:var(--muted);margin-top:12px}

/* quick cards */
.qgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.qcard{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--r);
  padding:24px 22px;display:flex;flex-direction:column;gap:6px;transition:.22s;overflow:hidden}
.qcard::before{content:"";position:absolute;left:0;top:0;height:100%;width:4px;background:var(--blue);
  transform:scaleY(0);transform-origin:top;transition:.22s}
.qcard:hover{transform:translateY(-4px);box-shadow:0 18px 40px -22px rgba(12,42,94,.5);border-color:#c3d3ec}
.qcard:hover::before{transform:scaleY(1)}
.qsym{font-family:var(--mono);color:var(--cyan);font-size:1.1rem}
.qtitle{font-weight:800;font-size:1.08rem;color:var(--ink)}
.qdesc{color:var(--muted);font-size:.9rem}
.qarrow{position:absolute;right:20px;bottom:18px;color:var(--blue);font-weight:700;
  opacity:0;transform:translateX(-6px);transition:.22s}
.qcard:hover .qarrow{opacity:1;transform:translateX(0)}

/* pillars */
.pillar-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.pillar{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:26px 22px;
  border-top:3px solid var(--blue)}
.pillar-en{font-family:var(--mono);font-size:.72rem;letter-spacing:.12em;color:var(--faint);text-transform:uppercase}
.pillar h3{font-size:1.25rem;margin:6px 0 10px;color:var(--ink)}
.pillar p{color:var(--muted);font-size:.92rem;margin:0}

/* universities */
.uni-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.uni{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px 22px;
  display:flex;flex-direction:column;gap:5px;transition:.22s}
.uni:hover{transform:translateY(-4px);box-shadow:0 18px 40px -24px rgba(12,42,94,.55)}
.uni-logo{display:flex;align-items:center;justify-content:flex-start;height:40px;margin-bottom:10px}
.uni-logo img{max-height:34px;max-width:150px;object-fit:contain}
.uni-tag{align-self:flex-start;font-family:var(--mono);font-size:.68rem;font-weight:700;letter-spacing:.1em;
  padding:3px 9px;border-radius:20px;background:var(--paper-2);color:var(--muted)}
.uni-tag.is-lead{background:var(--ink);color:#fff}
.uni-name{font-weight:800;font-size:1.15rem;color:var(--ink);margin-top:6px}
.uni-dept{color:var(--blue);font-weight:600;font-size:.92rem}
.uni-role{color:var(--muted);font-size:.88rem;margin-top:4px}

/* notices */
.notice-wrap{display:grid;grid-template-columns:220px 1fr;gap:40px;align-items:start}
.notice-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.notice-list li{display:flex;gap:20px;align-items:baseline;padding:18px 4px;border-bottom:1px solid var(--line)}
.notice-list time{font-family:var(--mono);font-size:.82rem;color:var(--blue);flex:none;width:70px}
.notice-list span{color:#28374f}

/* page hero */
.page-hero{background:linear-gradient(160deg,#0c2a5e,#123a7a);color:#fff;padding:70px 0 56px}
.page-hero h1{font-size:clamp(1.8rem,3.4vw,2.6rem);font-weight:800;margin:14px 0 16px}
.page-hero .eyebrow{color:var(--cyan)}
.lead{color:var(--sky);max-width:760px;font-size:1.02rem}
.lead b{color:#fff}

/* vision block */
.vision-block{text-align:center;max-width:840px;margin-inline:auto}
.vision-text{font-size:clamp(1.3rem,2.6vw,1.9rem);font-weight:800;color:var(--ink);
  line-height:1.5;margin-top:18px;text-wrap:balance}

/* goals */
.goal-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.goal{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:30px 26px}
.goal-idx{font-family:var(--mono);font-size:1.4rem;font-weight:700;color:var(--cyan)}
.goal h3{font-size:1.3rem;margin:10px 0 8px;color:var(--ink)}
.goal p{color:var(--muted);margin:0}

/* role table */
.role-table{width:100%;border-collapse:collapse;background:var(--card);
  border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.role-table tr{border-bottom:1px solid var(--line)}
.role-table tr:last-child{border-bottom:0}
.role-table td,.role-table th{padding:18px 20px;text-align:left;vertical-align:middle}
.role-table .rt{font-family:var(--mono);font-size:.72rem;font-weight:700;color:var(--muted);width:70px}
.role-table th{font-weight:800;color:var(--ink);font-size:1.05rem;width:260px}
.role-table th span{display:block;font-weight:600;font-size:.86rem;color:var(--blue)}
.role-table td:last-child{color:var(--muted)}

/* expects */
.expect-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.expect{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:28px 24px;
  border-top:3px solid var(--cyan)}
.expect-kind{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;color:var(--blue);font-weight:700}
.expect h3{font-size:1.15rem;margin:8px 0 14px;color:var(--ink)}
.expect ul{margin:0;padding-left:0;list-style:none}
.expect li{padding:7px 0 7px 20px;position:relative;color:#33455f;font-size:.92rem;border-top:1px solid var(--paper-2)}
.expect li::before{content:"›";position:absolute;left:4px;color:var(--cyan);font-weight:700}

/* members */
.mgroup{margin-bottom:52px}
.mgroup:last-child{margin-bottom:0}
.mgroup-title{font-size:1.15rem;color:var(--ink);padding-bottom:12px;margin-bottom:22px;
  border-bottom:2px solid var(--ink);font-weight:800}
.mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:22px 20px;transition:.2s}
.mcard:hover{box-shadow:0 16px 36px -24px rgba(12,42,94,.5);transform:translateY(-3px)}
.mcard.is-lead{border-color:var(--blue);box-shadow:0 0 0 1px var(--blue) inset}
.mcard-top{display:flex;gap:14px;align-items:center;margin-bottom:14px}
.m-avatar{width:52px;height:52px;border-radius:12px;flex:none;display:grid;place-items:center;
  background:linear-gradient(150deg,var(--blue),var(--cyan));color:#fff;font-weight:800;font-size:1.15rem;overflow:hidden}
.m-avatar.has-photo{background:var(--paper-2)}
.m-avatar img{width:100%;height:100%;object-fit:cover}
.m-name{font-weight:800;font-size:1.1rem;color:var(--ink);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.m-lead{font-family:var(--mono);font-size:.62rem;font-weight:700;background:var(--blue);color:#fff;
  padding:3px 8px;border-radius:20px;letter-spacing:.04em}
.m-field{color:var(--blue);font-size:.86rem;font-weight:600}
.m-courses{list-style:none;margin:0;padding:0;border-top:1px solid var(--paper-2)}
.m-courses li{padding:8px 0 8px 18px;position:relative;font-size:.9rem;color:#3a4b64;border-bottom:1px solid var(--paper-2)}
.m-courses li:last-child{border-bottom:0}
.m-courses li::before{content:"—";position:absolute;left:0;color:var(--faint)}

/* courses table */
.table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--card)}
.course-table{width:100%;border-collapse:collapse;min-width:680px}
.course-table thead th{background:var(--ink);color:#fff;font-size:.82rem;font-weight:700;
  padding:14px 16px;text-align:left;letter-spacing:.02em}
.course-table td{padding:16px;border-bottom:1px solid var(--line);vertical-align:middle;font-size:.94rem}
.course-table tr:last-child td{border-bottom:0}
.c-title{font-weight:800;color:var(--ink)}
.mode{font-size:.78rem;color:var(--muted);background:var(--paper-2);padding:4px 10px;border-radius:20px;white-space:nowrap}
.c-act{width:78px}
.mini-btn{display:inline-block;padding:7px 15px;border-radius:9px;font-size:.82rem;font-weight:700;
  background:var(--blue);color:#fff;transition:.18s;white-space:nowrap}
.mini-btn:hover{background:var(--blue-2)}
.mini-btn.alt{background:var(--cyan);color:#04233a}
.mini-btn.alt:hover{background:#5fd6fb}
.mini-btn.disabled{background:var(--paper-2);color:var(--faint);pointer-events:none}

/* steps */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.step{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px 20px;position:relative}
.step-n{font-family:var(--mono);font-size:1.5rem;font-weight:700;color:var(--cyan)}
.step h3{font-size:1.08rem;margin:8px 0 8px;color:var(--ink)}
.step p{color:var(--muted);font-size:.9rem;margin:0}
.note{margin-top:22px;color:var(--muted);font-size:.9rem;background:var(--card);
  border:1px dashed var(--line);border-radius:12px;padding:16px 18px}
.note a{color:var(--blue);font-weight:600;border-bottom:1px solid var(--blue)}

/* portal */
.portal-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.portal-block h2{font-size:1.05rem;color:var(--ink);border-bottom:2px solid var(--ink);
  padding-bottom:10px;margin-bottom:14px;font-weight:800}
.portal-links{display:flex;flex-direction:column;gap:8px}
.portal-links a{display:flex;justify-content:space-between;align-items:center;
  background:var(--card);border:1px solid var(--line);border-radius:11px;padding:14px 16px;
  font-weight:600;color:#28374f;transition:.18s}
.portal-links a:hover{border-color:var(--blue);color:var(--blue);transform:translateX(3px)}
.portal-links a span{color:var(--faint);font-size:.85rem}
.portal-links a:hover span{color:var(--blue)}
.portal-links a.pending{opacity:.7}
.portal-links a.pending span{font-family:var(--mono);font-size:.7rem}

/* footer */
.site-footer{background:var(--navy);color:#c7d5ee;padding:52px 0 26px;margin-top:0}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:30px;padding-bottom:30px;
  border-bottom:1px solid rgba(255,255,255,.12)}
.foot-title{color:#fff;font-weight:800;font-size:1.1rem}
.foot-en{font-size:.86rem;color:#8fa6cc;margin:6px 0 12px}
.foot-unis{font-size:.85rem;color:#9db2d6}
.foot-links{display:flex;flex-wrap:wrap;gap:8px 22px;align-content:flex-start}
.foot-links a{color:#c7d5ee;font-weight:600;font-size:.92rem}
.foot-links a:hover{color:var(--cyan)}
.foot-logos{display:flex;align-items:center;gap:26px;flex-wrap:wrap;padding:24px 0 4px}
.foot-logos img{height:30px;max-width:130px;object-fit:contain;
  background:#fff;padding:6px 10px;border-radius:8px}
.foot-base{display:flex;justify-content:space-between;gap:16px;padding-top:20px;
  font-size:.8rem;color:#7f95bb;flex-wrap:wrap}

/* responsive */
@media(max-width:960px){
  .nav{display:none}.nav-toggle{display:flex}
  .qgrid,.pillar-grid,.uni-grid,.steps{grid-template-columns:repeat(2,1fr)}
  .goal-grid,.expect-grid,.portal-grid,.mgrid{grid-template-columns:repeat(2,1fr)}
  .notice-wrap{grid-template-columns:1fr;gap:20px}
  .hero-stats{max-width:none}
}
@media(max-width:600px){
  .qgrid,.pillar-grid,.uni-grid,.steps,.goal-grid,.expect-grid,.portal-grid,.mgrid{grid-template-columns:1fr}
  .hero-stats{grid-template-columns:repeat(2,1fr);gap:14px 20px}
  .band{padding:52px 0}.hero-inner{padding:60px 0 52px}
  .role-table th{width:auto}.foot-grid{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto}}
"""

# ======================================================================
# 4) 빌드  -------------------------------------------------------------
# ======================================================================
def build():
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    render_home(); render_about(); render_members(); render_courses(); render_portal()
    print("빌드 완료:", ", ".join(n for _,_,n in NAV), "+ assets/style.css")

if __name__ == "__main__":
    build()
