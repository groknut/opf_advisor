"""
Генерация PDF-отчёта о рекомендации ОПФ.
Шрифт: Times New Roman (системный).
Библиотека: fpdf2
"""
from datetime import datetime
from io import BytesIO
import os
import sys
from pathlib import Path

from fpdf import FPDF

from src.services.recommender import Answers, Recommendation


def _times_new_roman_paths() -> tuple[str, str]:
    """Пути к Times New Roman (regular + bold)."""
    if sys.platform == "win32":
        fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        regular = fonts / "times.ttf"
        bold = fonts / "timesbd.ttf"
    else:
        # Linux: Liberation Serif — метрический аналог Times New Roman
        regular = Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf")
        bold = Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf")
        if not regular.is_file():
            regular = Path("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf")
            bold = Path("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf")

    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError(
            f"Не найден Times New Roman.\n"
            f"Ожидались файлы:\n  {regular}\n  {bold}"
        )
    return str(regular), str(bold)


# Поля (мм) — ориентир на ГОСТ
MARGIN_LEFT = 30
MARGIN_RIGHT = 15
MARGIN_TOP = 20
MARGIN_BOTTOM = 20
PAGE_WIDTH = 210  # A4


class RecommendationPDF(FPDF):
    def __init__(self, date_str: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.date_str = date_str
        self.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
        self.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)

        regular, bold = _times_new_roman_paths()
        self.add_font("TimesNR", style="", fname=regular)
        self.add_font("TimesNR", style="B", fname=bold)

    def header(self):
        self.set_font("TimesNR", "", 8)
        self.set_text_color(80, 80, 80)
        self.set_x(MARGIN_LEFT)
        self.cell(0, 5, "OPF Advisor — рекомендация по ОПФ", align="L")
        self.set_x(MARGIN_LEFT)
        self.cell(0, 5, self.date_str, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        y = self.get_y() + 1
        self.line(MARGIN_LEFT, y, PAGE_WIDTH - MARGIN_RIGHT, y)
        self.ln(6)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("TimesNR", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, f"Страница {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def section_title(self, text: str):
        self.ln(3)
        self.set_font("TimesNR", "B", 12)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body_text(self, text: str):
        """Текст с абзацным отступом ~1.25 см."""
        self.set_font("TimesNR", "", 11)
        self.set_x(MARGIN_LEFT + 12.5)
        usable = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - 12.5
        self.multi_cell(usable, 6, text)
        self.ln(1)

    def body_text_no_indent(self, text: str):
        self.set_font("TimesNR", "", 11)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bold_text(self, text: str):
        self.set_font("TimesNR", "B", 11)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def list_item(self, number: int, text: str):
        self.set_font("TimesNR", "", 11)
        self.set_x(MARGIN_LEFT + 5)
        usable = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - 5
        self.multi_cell(usable, 6, f"{number}. {text}")
        self.ln(0.5)


def _yes_no(value: bool) -> str:
    return "Да" if value else "Нет"


def generate_recommendation_pdf(
    answers: Answers,
    recommendation: Recommendation,
) -> bytes:
    """Формирует PDF-документ с рекомендацией и возвращает байты."""
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")

    pdf = RecommendationPDF(date_str=date_str)
    pdf.add_page()

    content_w = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

    # --- Шапка ---
    pdf.set_font("TimesNR", "B", 11)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(content_w, 6, "ОПФ ADVISOR", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("TimesNR", "", 10)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(
        content_w, 5,
        "Сервис подбора организационно-правовой формы юридического лица / ИП",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(2)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(MARGIN_LEFT, pdf.get_y(), PAGE_WIDTH - MARGIN_RIGHT, pdf.get_y())
    pdf.ln(4)

    # Дата
    pdf.set_font("TimesNR", "", 10)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(content_w, 5, f"Дата формирования: {date_str}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Заголовок
    pdf.set_font("TimesNR", "B", 14)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(content_w, 8, "РЕКОМЕНДАЦИЯ", align="C")
    pdf.set_font("TimesNR", "B", 12)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(content_w, 7, "по выбору организационно-правовой формы ведения бизнеса", align="C")
    pdf.ln(4)

    # 1. Исходные данные
    pdf.section_title("1. Исходные данные")

    col_w = [95, 70]
    row_h = 7
    headers = ["Параметр", "Значение"]
    rows = [
        ["Вид деятельности", answers.activity.label],
        ["Масштаб бизнеса", answers.scale.label],
        ["Количество учредителей", str(answers.founders_count)],
        ["Потребность в привлечении инвестиций", _yes_no(answers.need_investments)],
        ["Готовность к неограниченной личной ответственности",
         _yes_no(answers.unlimited_liability_ok)],
    ]

    pdf.set_font("TimesNR", "B", 10)
    pdf.set_fill_color(238, 238, 238)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(col_w[0], row_h, headers[0], border=1, fill=True)
    pdf.cell(col_w[1], row_h, headers[1], border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("TimesNR", "", 10)
    for row in rows:
        pdf.set_x(MARGIN_LEFT)
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        pdf.multi_cell(col_w[0], row_h, row[0], border=1)
        h1 = pdf.get_y() - y_start
        pdf.set_xy(x_start + col_w[0], y_start)
        pdf.multi_cell(col_w[1], row_h, row[1], border=1)
        h2 = pdf.get_y() - y_start
        pdf.set_y(y_start + max(h1, h2))

    pdf.ln(3)

    # 2. Рекомендуемая форма
    pdf.section_title("2. Рекомендуемая организационно-правовая форма")
    pdf.bold_text(f"{recommendation.opf.value} — {recommendation.opf.full_name}")
    pdf.body_text_no_indent(f"Уровень риска: {recommendation.risk_level}")

    # 3. Обоснование
    pdf.section_title("3. Обоснование рекомендации")
    pdf.body_text(recommendation.reason)

    # 4. Налоговый режим
    pdf.section_title("4. Рекомендуемый налоговый режим")
    pdf.bold_text(recommendation.tax_regime.value)
    pdf.body_text(recommendation.tax_comment)

    # 5. Преимущества
    pdf.section_title("5. Преимущества выбранной формы")
    for i, item in enumerate(recommendation.pros, 1):
        pdf.list_item(i, item)

    # 6. Недостатки / риски
    pdf.section_title("6. Недостатки и риски")
    for i, item in enumerate(recommendation.cons, 1):
        pdf.list_item(i, item)

    # 7. Следующие шаги
    pdf.section_title("7. Рекомендуемые следующие шаги")
    for i, item in enumerate(recommendation.next_steps, 1):
        pdf.list_item(i, item)

    # 8. Альтернативы
    if recommendation.alternatives:
        pdf.section_title("8. Возможные альтернативы")
        pdf.body_text("; ".join(recommendation.alternatives) + ".")

    # Дисклеймер
    pdf.ln(4)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(MARGIN_LEFT, pdf.get_y(), PAGE_WIDTH - MARGIN_RIGHT, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("TimesNR", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(
        content_w, 5,
        "Настоящая рекомендация сформирована автоматически на основании введённых пользователем "
        "параметров и носит информационно-справочный характер. Перед принятием окончательного "
        "решения рекомендуется проконсультироваться с юристом и налоговым консультантом с учётом "
        "конкретных обстоятельств планируемой деятельности.",
    )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)

    # Подпись
    pdf.set_font("TimesNR", "", 10)
    sig_w = 80
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(sig_w, 6, "_________________________", align="C")
    pdf.cell(10, 6, "")
    pdf.cell(sig_w, 6, "_________________________", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("TimesNR", "", 9)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(sig_w, 5, "(подпись)", align="C")
    pdf.cell(10, 5, "")
    pdf.cell(sig_w, 5, "(расшифровка подписи)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("TimesNR", "", 10)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(content_w, 6, f"г. _____________     «{now.day}» _____________ {now.year} г.", align="C")

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()
