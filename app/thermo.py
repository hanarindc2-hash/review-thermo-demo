"""리뷰 온도 규칙 3개. 규칙은 SPEC.md 2장을 보세요. (세션 2에서 AI와 함께 구현)"""


def to_label(score: float) -> str:
    """score를 "positive" / "negative" 로 바꾼다. 규칙: SPEC.md 2장."""
    return "positive" if score >= 0.5 else "negative"


def to_temperature(score: float) -> float:
    """score를 리뷰 온도(0~100)로 바꾼다. 규칙: SPEC.md 2장."""
    return round(score * 100, 1)


def is_mismatch(rating: int, label: str) -> bool:
    """별점과 내용이 반대인지 알려 준다. 규칙: SPEC.md 2장."""
    if rating >= 4 and label == "negative":
        return True
    if rating <= 2 and label == "positive":
        return True
    return False

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
