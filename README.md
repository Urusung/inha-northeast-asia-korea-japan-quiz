# inha-northeast-asia-korea-japan-quiz

인하대 동북아와 한일관계 시험 대비용 정적 퀴즈 페이지입니다. 첫 화면에서는 중간고사/기말고사 개념 퀴즈만 선택할 수 있게 구성했습니다.

## 방향

- 중간고사와 기말고사를 별도 페이지로 분리합니다.
- 문제는 시험 대비 개념 퀴즈 중심으로 구성합니다.
- `index.html`에는 중간고사/기말고사 카드만 노출합니다.

## 범위

- 중간고사: 6~10주차, 120문제 풀에서 주차별 랜덤 10문제씩 총 50문제
- 기말고사: 11~14주차, 60문제 풀에서 주차별 랜덤 10문제씩 총 40문제

## Local

브라우저에서 `index.html`을 열면 바로 실행됩니다.

## 공개 주소

- GitHub Pages: `https://urusung.github.io/inha-northeast-asia-korea-japan-quiz/`

## 구성

- `index.html`: 중간고사/기말고사 선택 첫 화면
- `midterm.html`: 중간고사 대비 개념 퀴즈
- `final.html`: 기말고사 대비 개념 퀴즈
- `quiz.html`: 전체 범위 문제 풀이 UI와 채점 로직
- `questions.js`: 문제 데이터
- `scripts/`: 문제 데이터 생성 및 정리 스크립트
- `files/`: 원본 수업 자료 및 참고 파일
