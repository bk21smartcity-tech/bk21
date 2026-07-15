# 시민체감형 사회안전 스마트시티 교육연구단 (BK21) 홈페이지

충북대·대전대·청주대·국립한밭대 4개 대학 연합 BK21 교육연구단 정적 웹사이트.
`generate.py` 로 HTML을 생성하고, GitHub → Netlify 로 배포합니다.

## 구성
```
index.html      홈 (히어로 · 빠른링크 · 4대 기조 · 4개 대학 · 소식)
about.html      사업 소개 (비전 · 3대 혁신목표 · 대학별 역할 · 기대효과)
members.html    참여교수 (4개 대학 11인)
courses.html    공동교과목 · 온라인 강의 · 과제 제출 · 학점교류 절차
portal.html     바로가기 (대학/학과 · 사업기관 · 자료)
assets/style.css   스타일 (생성됨)
generate.py     ← 모든 내용/링크를 여기서 편집
```

## 내용 수정 방법
1. `generate.py` 상단의 **CONFIG 영역**만 편집합니다.
   - `SITE` : 사업명, 기간, 비전, 대표 이메일
   - `UNIVERSITIES` / `MEMBERS` : 대학 · 참여교수
   - `COURSES` : 과목명, 담당, 운영방식, **강의실 링크(link)**, **과제제출 링크(submit)**
   - `QUICK_LINKS`, `PORTAL`, `NOTICES` : 링크 · 공지
   - 링크가 아직 없으면 `"#"` 로 두세요. → 버튼이 "준비중"으로 표시됩니다.
2. 저장 후 실행:
   ```bash
   python3 generate.py
   ```
   → html 파일과 `assets/style.css` 가 다시 생성됩니다.

## 배포 (GitHub → Netlify)
1. 이 폴더를 GitHub 저장소에 push
   ```bash
   git init
   git add .
   git commit -m "BK21 교육연구단 홈페이지"
   git branch -M main
   git remote add origin https://github.com/<계정>/<저장소>.git
   git push -u origin main
   ```
2. [Netlify](https://app.netlify.com) → **Add new site → Import from Git** → 저장소 선택
3. 빌드 설정은 `netlify.toml` 이 자동 적용 (Publish directory = `.`)
4. Deploy 완료 후 `Site settings → Domain` 에서 원하는 서브도메인(예: `cbnu-bk21.netlify.app`) 지정

> 내용을 고칠 때는 `generate.py` 수정 → `python3 generate.py` → 생성된 html을 커밋/푸시하면
> Netlify가 자동 재배포합니다.

## 채워야 할 항목 (TODO)
- [ ] 각 대학/학과 실제 홈페이지 URL (`UNIVERSITIES[].dept_url`, `PORTAL`)
- [ ] 공동교과목 강의실 · 과제제출 URL (`COURSES[].link`, `COURSES[].submit`)
- [ ] 자료실/서식 링크 (`PORTAL['자료 · 서식']`)
- [ ] 대표 연락 이메일 확인 (`SITE['email']`)
