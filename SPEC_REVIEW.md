# 명세서 (내가 AI와 함께 쓰는 버전)

> © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 · [LICENSE.md](LICENSE.md)

> 세션 2 첫 활동입니다. `REQUEST.md`를 읽고, AI와 대화하면서 아래 빈칸을 채워 `MY_SPEC.md`로 저장하세요.
> 정답을 맞히는 활동이 아닙니다. 다 쓰면 강사가 주는 '공식 명세'와 비교합니다.

## 1. 이 기능은 무엇을 하나요? (한 문장)

- 고객이 작성한 리뷰 글(`text`)과 별점(`rating`)을 입력받아, AI 감성 분석 모델을 통해 **긍정/부정 여부(`label`)**, **긍정 확률 점수(`score`)**, **0~100℃ 사이의 리뷰 온도(`temperature`)**, 그리고 **별점과 리뷰 내용의 불일치 여부(`mismatch`)**를 계산하여 돌려줍니다.

## 2. 입력 (무엇을 받나요?)

| 이름 | 종류(글자/숫자) | 허용 범위 | 예 |
|---|---|---|---|
| `text` (리뷰 내용) | 글자 (`str`) | 앞뒤 공백 제거 후 1자 이상 ~ 500자 이하 | `"배송도 빠르고 품질도 좋아요"` |
| `rating` (별점) | 숫자 (`int`, 정수) | 1 ~ 5 (1점부터 5점까지) | `5` |

## 3. 출력 (무엇을 돌려주나요?)

| 이름 | 종류 | 뜻 | 예 |
|---|---|---|---|
| `label` | 글자 (`"positive"` 또는 `"negative"`) | 리뷰 내용이 긍정인지 부정인지 나타내는 판정 결과 | `"positive"` |
| `score` | 숫자 (`float`, 소수점 넷째 자리 반올림) | AI 부품(`app/sentiment.py`)이 계산한 긍정일 확률 (0.0 ~ 1.0) | `0.8732` |
| `temperature` | 숫자 (`float`, 소수점 첫째 자리 반올림) | 얼마나 긍정적인지 보여주는 리뷰 온도 (0.0 ~ 100.0℃) | `87.3` |
| `mismatch` | 참/거짓 (`bool`) | 별점과 리뷰 내용(긍정/부정)이 서로 반대인지 여부 | `False` |

## 4. 규칙 (어떻게 정하나요?)

- **긍정/부정 기준 (`to_label`)**:
  - AI 부품이 반환한 긍정 확률 `score`가 **0.5 이상(`score >= 0.5`)**이면 `"positive"`(긍정), **0.5 미만(`score < 0.5`)**이면 `"negative"`(부정)로 판정합니다.
- **리뷰 온도 계산법 (`to_temperature`)**:
  - 긍정 확률 `score`(0.0 ~ 1.0)에 100을 곱하여 0 ~ 100℃ 범위로 변환한 뒤, 소수점 첫째 자리까지 반올림(`round(score * 100, 1)`)합니다.
- **별점과 내용이 '반대'라는 기준 (`is_mismatch`)**:
  - **높은 별점 + 부정 내용**: 별점이 **4점 이상(`rating >= 4`)**인데 리뷰 판정이 `"negative"`인 경우 → `True`
  - **낮은 별점 + 긍정 내용**: 별점이 **2점 이하(`rating <= 2`)**인데 리뷰 판정이 `"positive"`인 경우 → `True`
  - **그 외 (일치하거나 중간 별점인 경우)**: 별점이 **3점(`rating == 3`)**이거나 별점 방향과 긍정/부정이 일치하는 경우 → `False`

## 5. 예시표 (이 표가 그대로 테스트가 됩니다)

| 입력 | 기대하는 출력 |
|---|---|
| `text="좋아요"`, `rating=5` (AI `score=0.8732`) | `{"label": "positive", "score": 0.8732, "temperature": 87.3, "mismatch": False}` |
| `text="배송 최악"`, `rating=5` (AI `score=0.2`) | `{"label": "negative", "score": 0.2, "temperature": 20.0, "mismatch": True}` |
| `text="생각보다 괜찮네요"`, `rating=1` (AI `score=0.8`) | `{"label": "positive", "score": 0.8, "temperature": 80.0, "mismatch": True}` |
| `text="그냥 보통이에요"`, `rating=3` (AI `score=0.4`) | `{"label": "negative", "score": 0.4, "temperature": 40.0, "mismatch": False}` |
| `text="딱 절반 느낌"`, `rating=4` (AI `score=0.5`) | `{"label": "positive", "score": 0.5, "temperature": 50.0, "mismatch": False}` |

## 6. 이런 입력은 거절합니다

- **빈 문자열 또는 공백만 있는 리뷰 (`text=""`, `text="   "`)**: 앞뒤 공백 제거 후 길이가 0자이므로 거절 (`HTTP 422 Unprocessable Entity`)
- **500자를 초과하는 리뷰 (`len(text) > 500`)**: 최대 허용 글자 수(500자) 초과로 거절 (`HTTP 422`)
- **허용 범위를 벗어난 별점 (`rating < 1` 또는 `rating > 5`, 예: `0`, `6`)**: 1~5 범위를 벗어나므로 거절 (`HTTP 422`)
- **필수 입력값 누락 또는 타입 불일치**: `text`나 `rating`이 없거나 잘못된 형식일 때 거절 (`HTTP 422`)
- *(참고) AI 모델 부품(`app/sentiment.py`) 오류 발생 시*: `HTTP 503 Service Unavailable` 반환

## 7. AI와 대화하면서 새로 알게 된 것, 애매했던 것

- **요청서(`REQUEST.md`)에서 애매했던 점과 코드(`static/app.js`, `app/schemas.py`, `tests/test_api.py`)로 확인한 구체적 기준**:
  1. **필드 이름과 API 경로**: 요청서에는 한글로만 적혀 있었지만, 프론트엔드(`static/app.js`)와 스키마(`app/schemas.py`)를 통해 요청 경로는 `POST /v1/reviews/analyze`, 입력 필드는 `text`, `rating`, 출력 필드는 `label`, `score`, `temperature`, `mismatch`여야 화면이 정상 동작함을 확인했습니다.
  2. **글자 수 제한과 공백 처리**: 요청서에는 글자 수 제한이 없었으나, 화면과 스키마에서 앞뒤 공백을 제거(`strip_whitespace=True`)한 뒤 **1~500자**만 허용한다는 규칙을 확인했습니다.
  3. **경계값 기준**:
     - `score`가 정확히 `0.5`일 때 긍정(`"positive"`)인지 부정(`"negative"`)인지 요청서에 명시되지 않았는데, 일반적으로 `0.5` 이상을 긍정으로 봅니다.
     - 리뷰 온도의 소수점 자리수 역시 테스트 코드(`0.8732` → `87.3`)를 통해 **소수점 첫째 자리 반올림**임을 확인했습니다.
     - 별점과 내용이 반대(`mismatch`)인 기준에서 **별점 3점**은 중립이므로 긍정/부정 어느 쪽이 나와도 불일치(`mismatch=False`)로 보지 않고, **4~5점인데 부정**이거나 **1~2점인데 긍정**일 때만 `True`로 판단해야 함을 구체화했습니다.
