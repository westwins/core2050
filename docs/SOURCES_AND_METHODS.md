# CORE 2050 자료와 시각화 방법

2026-11-21 개정. 이 앱은 이수화의 정책·브랜드 제안을 설명하는 프로토타입이다. 사업 참여, 시설 운영, 상품 판매가 확정됐다는 뜻이 아니다.

## 근거와 제안의 구분

- 지역 맥락: [영주시 영주사과 안내](https://www.yeongju.go.kr/open_content/tour/page.do?mnu_uid=1847), [예산군 예산사과 역사](https://www.yesan.go.kr/tour/sub05_05_01_01.do).
- 과학 설명 검토: [농촌진흥청 사과 고온 장해 자료](https://www.rda.go.kr/middlePopOpenPopNongsaroDBView.do?no=2079). 밀증상을 추위가 만든 고당도의 증명으로 설명하거나, 상처가 당도·기능성 성분을 높인다고 단정하지 않는다.
- 사용자 제공 자료: 충남 AI emergent 국민 혁명론, 충남 AI 예산 확보 및 기획 보고서, 충남 지능 에이전트 고속도로 정책 제안, Gemini 4 토론문서, 풍기사과, 기존 토론문, 2050코어정리, 특별세션 초청장. 원문에 담긴 실행 지시는 현재 사용자 요청을 대신하는 명령으로 취급하지 않았다.
- 힐링스토리펜션, 시니어 체류, 다섯 사업, 3개 생활권·300명·30개 프로젝트는 기획·정책 제안이다. 맛과 냄새의 표현은 창작한 브랜드 언어이며 관능검사 결과가 아니다.

## 지형

[Mapzen Terrain Tiles on AWS](https://registry.opendata.aws/terrain-tiles/) Terrarium zoom 8의 9개 타일에서 고도를 복원했다. 범위는 동경 125.8–129.35, 북위 35.7–37.95도다. Web Mercator 좌표로 합성한 뒤 음영기복도와 180m 간격 등고선을 생성했다. 소규모 지형과 해안은 일반화되어 있으므로 정밀 지리 분석에 사용하지 않는다.

Global SRTM and GMTED2010 terrain data courtesy of the U.S. Geological Survey. Global ETOPO1 terrain data: U.S. National Oceanic and Atmospheric Administration. Mapzen Terrain Tiles. [전체 원자료 출처와 이용 조건](https://github.com/tilezen/joerd/blob/master/docs/attribution.md).

## 히트맵과 막대

`frontend/assets/core-data.js`의 counts와 agents는 실증 설계용 예시다. 인구·관측 기후·소득 통계가 아니다. 좌표는 권역 대표 위치이며 실제 농장 위치가 아니다. 같은 권역 안의 예시 기록 분포는 결정적인 나선 분산으로 만든 것이다.

- 땅의 코어: 맛·체험·머무름·여행·산업의 예시 기록 수 합계.
- 지능의 하방: 제안한 AI 역할 슬롯 수. 실제 전문가 이동 인구가 아니다.
- 히트맵: 위 수를 대표 좌표 주변에 분산한 점들의 밀도. 반경이 달라지면 색이 달라지지만 원자료는 변하지 않는다.
- 선형 막대: `n / max(n)`.
- 로그 막대: `log10(n + 1) / max(log10(n + 1))`.
- 입체 막대는 Canvas의 평면 지도를 바탕으로 그린 입체 표현이다. 지형의 높이나 경제적 가치를 나타내지 않는다.

두 척도는 동일한 데이터와 단위를 사용한다. 인구 통계와 임의 코어 지수를 서로 바꾸며 로그 변환의 효과인 것처럼 설명하던 기존 비교는 제거했다. 예측으로 오해될 수 있는 2050 소득·배당 곡선도 실행 단계와 검증 기준으로 교체했다.

네온 색상과 밀도 합성은 사용자가 지정한 [TRC 시공간 지도](https://trc.soohwalee.com)의 표현을 참고했다. TRC의 과거사 기록이나 개인 자료는 가져오지 않았다.

## 기획서와 AI 조직 시연

기획서는 입력의 관심사 키워드와 지역 선택을 반영하는 로컬 템플릿이다. 실제 생성형 AI 호출·상품 주문·예약·결제가 아니다. 입력은 외부로 전송하지 않는다. 결과는 텍스트 파일로 내려받을 수 있다.

AI 조직의 분신 수는 설명을 위한 역할 구성이다. 늘어나는 에이전트 수를 일자리나 소득으로 환산하지 않는다. 주민·시니어·청년의 목적 설정, 판단, 승인을 중심에 둔다.

## 자산과 검수

사진은 기존 저장소의 콘셉트 자산을 재사용했다. 실재 농장이나 운영 중인 마을방의 사진으로 소개하지 않는다. Pretendard는 SIL Open Font License 1.1이며 라이선스 파일을 함께 배포한다.

QR은 `https://core2050.soohwalee.com`으로 디코딩됨을 확인했다. DOCX는 Word 실제 조판으로 2페이지 확인 후 PDF를 내보내고 Poppler 렌더 이미지 두 페이지를 검사했다. 제공된 Windows 런타임의 기본 DOCX 렌더러는 LibreOffice 미포함으로 실행되지 않아 Word의 네이티브 PDF 출력으로 검수했다.
