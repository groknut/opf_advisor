from dataclasses import dataclass
from src.models import BusinessScale, ActivityType, Opf

@dataclass
class Answers:
    activity: ActivityType
    scale: BusinessScale
    founders_count: int
    need_investments: bool
    unlimited_liability_ok: bool  # готов ли рисковать личным имуществом

def recommend(answers: Answers) -> tuple[Opf, str]:
    """Возвращает рекомендованную ОПФ и краткое обоснование."""
    reasons = []

    # 1. Один учредитель + малый масштаб + нет инвестиций + готовность к личной ответственности
    if (answers.founders_count == 1
        and answers.scale == BusinessScale.SMALL
        and not answers.need_investments
        and answers.unlimited_liability_ok):
        return Opf.IP, (
            "ИП подходит для единственного собственника малого бизнеса. "
            "Регистрация проще, налоговая отчётность легче. "
            "Однако вы рискуете личным имуществом."
        )

    # 2. Несколько учредителей или потребность в инвестициях -> ООО
    if (answers.founders_count > 1
        or answers.need_investments
        or answers.scale == BusinessScale.MEDIUM
        or not answers.unlimited_liability_ok):
        if answers.scale == BusinessScale.LARGE or answers.need_investments:
            return Opf.JSC, (
                "Для крупного бизнеса и привлечения инвестиций лучше подходит АО. "
                "Акционерное общество может выпускать акции, что облегчает привлечение капитала. "
                "Участники несут ограниченную ответственность."
            )
        return Opf.LLC, (
            "ООО — оптимальный выбор при наличии партнёров или необходимости "
            "в инвестициях. Участники несут ответственность только в пределах "
            "уставного капитала (от 10 000 ₽)."
        )

    # 3. Если ничего не подошло — ИП как базовый вариант
    return Opf.IP, "ИП — наиболее простой вариант для старта. Оцените риски личной ответственности."
