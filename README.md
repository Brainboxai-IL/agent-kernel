<p align="center">
  <img src="./assets/readme/hero.svg" width="100%"
       alt="agent-kernel by BrainboxAI — five behavioral modules composed into ready-to-use agent profiles, with documented rationale and compliance probes">
</p>

<div dir="rtl">

## מה זה

רוב ה-system prompts ל-agents הם ערימת הנחיות שאף אחד לא יודע למה היא שם ואם היא בכלל עובדת. **agent-kernel** מפרק את ההתנהגות לחמישה מודולים ממוקדים, מרכיב מהם פרופילים מוכנים להדבקה, ומצרף את שני הדברים שכמעט אף ריפו של פרומפטים לא מספק: **נימוק לכל כלל** ו-**דרך לבדוק שה-agent באמת מציית**.

## הארכיטקטורה

| שכבה | מה יש בה |
|------|----------|
| [`modules/`](modules) | חמישה מודולי התנהגות עם כללים ממוספרים: [communication](modules/communication.md) (C1–C8), [autonomy](modules/autonomy.md) (A1–A6), [integrity](modules/integrity.md) (I1–I6), [caution](modules/caution.md) (S1–S6), [code](modules/code.md) (K1–K6) |
| [`profiles/`](profiles) | פרופילים מורכבים מוכנים להדבקה: `assistant`, `coding-agent`, `autonomous-agent` — נבנים מהמודולים עם `build.py` |
| [`RATIONALE.md`](RATIONALE.md) | לכל כלל: מצב הכשל הקונקרטי שהוא מונע. כלל בלי נימוק הוא פולקלור |
| [`EVALS.md`](EVALS.md) | 15 probes התנהגותיים — תרחיש, מה עושה agent תקין, מה עושה agent שמפר |

## למה זה שונה מעוד ריפו של פרומפטים

1. **כללים ממוספרים וניתנים לציטוט.** ‏"ה-agent הפר את I4" זו שיחת דיבאג; "הפרומפט לא עבד" זו תלונה.
2. **נימוק מתועד.** כל כלל ב-[`RATIONALE.md`](RATIONALE.md) ממופה לכשל אמיתי שנצפה ב-agents — אפשר לערער, לבדוק ולמחוק כללים במקום לצבור אותם.
3. **ציות נבדק, לא מונח.** ‏[`EVALS.md`](EVALS.md) הופך את הספק למדיד: מריצים את ה-probes לפני ואחרי כל שינוי פרומפט.
4. **מקור אמיתי.** הכללים זוקקו מהתנהגות בפועל של agent ברמת frontier‏ (Claude Fable 5 בתוך Claude Code, יולי 2026) — ע"י המודל עצמו, לא מ"הדלפה" משוחזרת.

## שימוש

בוחרים פרופיל ומדביקים כ-system prompt:

</div>

```python
system = open("profiles/coding-agent.md", encoding="utf-8").read()
# Anthropic / OpenAI / Gemini / LM Studio / Ollama — כל ספק עם שדה system
```

<div dir="rtl">

מרכיבים וריאציה משלכם — עורכים את `PROFILE_SPECS` ובונים מחדש:

</div>

```bash
python build.py
```

<div dir="rtl">

עורכים תמיד את `modules/` — קבצי `profiles/` נוצרים אוטומטית ונדרסים בבנייה.

## מגבלה שכדאי להכיר

פרומפט התנהגותי משפר תקשורת ושיפוט; הוא לא מחליף harness. כלים, לולאת agent, הרשאות ו-sandboxing קובעים לא פחות ממה שכתוב ב-system prompt — ולכן יש EVALS: אל תניחו ציות, תמדדו אותו.

</div>

<p align="center">
  <img src="./assets/readme/brainbox-footer.svg" width="320"
       alt="Built by BrainboxAI — brainboxai.io">
</p>
