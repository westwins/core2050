# CORE 2050

풍기사과에서 예산사과까지, 지역의 고유함을 주민이 직접 소프트웨어와 사업으로 만드는 정책 제안 앱입니다.

**라이브:** https://core2050.soohwalee.com

**2026 지방시대 엑스포 특별세션:** 2026.12.10. 오송 C&V센터 · 이수화

## 화면의 흐름

1. **풍토 지도:** 실제 고도 자료 위에서 풍기·예산·충주 등 7개 권역을 탐색합니다. 땅의 자산과 AI 하방을 각각 네온 히트맵, 입체 막대, 중첩으로 볼 수 있습니다. 선형과 로그 막대는 동일한 수치를 사용합니다.
2. **스카 마케팅:** 풍기와 예산의 이야기를 별도로 구성하고 맛·체험·머무름·여행·산업으로 연결합니다. 현장의 한 문장을 반영한 기획서 템플릿을 내려받을 수 있습니다.
3. **AI 하방:** 주민·시니어 전문가·청년 운영자를 중심으로 조사·기획·번역·제작·운영·검증 AI의 역할을 시각화합니다. 연결 전후와 분야별 분신 수를 조작할 수 있습니다.
4. **100일 실증:** 3개 생활권·주민 300명·프로젝트 30개의 제안 규모와 단계별 검증 기준을 제시합니다.

상단 **3분 발표**로 발언 순서를 띄울 수 있습니다. `P`는 발표, `Q`는 QR, `Esc`는 창 닫기입니다. 휴대폰에서도 모든 핵심 조작을 지원합니다.

## 제출 및 현장 파일

- [A4 두 쪽 DOCX](docs/2026_지방시대엑스포_토론문_이수화_개정본.docx)
- [인쇄용 PDF](docs/2026_지방시대엑스포_토론문_이수화_개정본.pdf)
- [오프라인 단일 HTML](docs/core2050_standalone_singlefile.html) — 내려받아 브라우저로 열면 지도·사진·글꼴·문서가 외부 연결 없이 동작합니다.
- [자료와 방법](docs/SOURCES_AND_METHODS.md)

기존 원고는 이력 보존을 위해 남겨두었으며, 제출에는 **개정본**을 사용합니다.

## 데이터의 의미

지형은 Mapzen Terrain Tiles의 공개 고도 자료입니다. 색과 막대의 수치는 **실증 설계용 예시**이며 실제 농장·소득·당도·전문가 이동 통계가 아닙니다. 원자료 표와 CSV를 앱에서 열 수 있습니다. 로그 변환은 작은 값의 차이를 읽는 방식이며 경제효과의 증명이 아닙니다.

‘AI 기획서’는 지역 선택과 입력 키워드를 반영하는 로컬 템플릿입니다. 외부 생성형 AI 호출이나 실제 예약·결제는 없습니다. 스카 마케팅은 선별·재배의 이력을 다루며 상처나 밀증상의 효능을 주장하지 않습니다.

## 실행

프론트엔드는 빌드 없는 HTML/CSS/JavaScript입니다. 지도·이미지·글꼴은 자체 호스팅하며 외부 CDN에 의존하지 않습니다.

```bash
python -m http.server 8765 --directory frontend
```

기존 Docker 배포를 유지합니다.

```bash
docker compose build core2050-frontend
docker compose up -d --no-deps core2050-frontend
```

Nginx Proxy Manager가 별도 네트워크에 있으면 새 컨테이너를 기존 공유 네트워크에 다시 연결해야 합니다. 현재 운영 구성은 `npm_default`와 `trc-dedicated-net` 연결을 유지합니다. DNS·API·다른 사이트는 변경할 필요가 없습니다.

## 구조와 검수

```text
frontend/index.html             서사와 접근 가능한 HTML
frontend/assets/core.css        반응형 디자인
frontend/assets/core-data.js    지역 원본·사업 제안·예시 데이터
frontend/assets/core.js         지도·AI 조직·기획서·발표 모드
tools/build_terrain.py          공개 고도 타일로 배경 제작
tools/build_manuscript.py       python-docx로 두 쪽 원고 작성
tools/package_offline.py        자산을 포함한 오프라인 HTML 생성
tools/qa-browser.cjs            브라우저 기능·휴대폰 검수
```

문서는 실제 Word 조판으로 2페이지를 확인하고 PDF를 내보내 전체 페이지를 시각 검수했습니다. 브라우저 검수는 1440px 및 390px 화면, 지도 주제·표현·척도, 지역별 사업, 사용자 입력 이스케이프, 다운로드, AI 조직, 실증 단계, QR·발표 모드와 오프라인 조작을 포함합니다. QR은 공개 앱 주소로 디코딩됨을 확인했습니다.

로컬 서버를 켠 뒤 Playwright가 제공된 환경에서 `node tools/qa-browser.cjs`를 실행합니다. `CORE2050_URL`로 검수 대상을 바꿀 수 있습니다. 산출물은 `.qa/`에 저장합니다.

Pretendard의 SIL Open Font License와 지형 출처는 `frontend/assets/Pretendard-LICENSE.txt`, `docs/SOURCES_AND_METHODS.md`를 참고하세요.
