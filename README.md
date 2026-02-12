## Лабораторная работа №1

Разработка агентного LLM-приложения на базе LangGraph

Проект: Ассистент для анализа научных публикаций

1. #### Постановка задачи

Необходимо реализовать интеллектуального ассистента, который:

Принимает тему исследования и временной диапазон.

Выполняет поиск релевантных публикаций через arXiv API.

Анализирует:

* ключевые тренды,

* наиболее активных авторов.

* Генерирует структурированный литературный обзор.

* Проводит автоматическое рецензирование результата.

* Возвращает финальный улучшенный отчёт в строго определённом формате.

2. #### Архитектура решения

Приложение построено с использованием LangGraph и реализует агентный pipeline:

User Request

     ↓

  Planner Node

     ↓
 ┌───────────────┐┌──────────────┐

Paper Search _____ Author Analysis   _________Trend Analysis

 └───────────────┴───────────────┘

             ↓
        Writer Node
             ↓
        Reviewer Node
             ↓
        Final Output

3. #### Описание компонентов

3.1 Planner Node

Анализирует пользовательский запрос.

Формирует структурированный план (PlannerOutput).

Использует PydanticOutputParser.

3.2 Tools Layer
- Поиск публикаций

Используется реальный arXiv API.

Реализована retry-логика через tenacity.

Результат приводится к модели Paper.

- Анализ трендов (параллельная ветка)

Выделяются основные направления исследований.

Формируется список трендов (Trend).

- Анализ авторов (параллельная ветка)

Определяются наиболее активные авторы.

Формируется список (AuthorStats).

3.3 Writer Node

Генерирует структурированный литературный обзор.

Использует PydanticOutputParser.

Возвращает объект LiteratureReview.

Структура результата:

{
  "key_papers": [],
  "main_trends": [],
  "top_authors": [],
  "open_questions": []
}

3.4 Reviewer Node

Выполняет автоматическую рецензию.

Улучшает структуру и формулировки.

Возвращает валидированный LiteratureReview.


4. #### Реализация ReAct-логики

Приложение реализует концепцию ReAct:

Reason (Planner) — анализ задачи

Act (Tools) — обращение к arXiv API

Reason (Writer) — формирование отчёта

Reflect (Reviewer) — улучшение результата

5. #### Реализация retry-логики

Используется tenacity:

* повтор запроса при ошибках API,

* обработка пустых результатов,

* защита от временных сбоев сети.

6. #### Пример работы системы

Вход:

UserRequest(

    topic="Large Language Models in Education",
    year_from=2020,
    year_to=2024,
    need_trend_analysis=True,
    need_author_analysis=True
)

Выход:

=== FINAL LITERATURE REVIEW ===

Key papers:
- An Open Natural Language Processing Development Framework for EHR-based Clinical Research: A case demonstration using the National COVID Cohort Collaborative (N3C)
- A Comprehensive Review of State-of-The-Art Methods for Java Code Generation from Natural Language Text
- SpeechPrompt: Prompting Speech Language Models for Speech Processing Tasks
- BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- LLaMA: Open and Efficient Foundation Language Models
- Towards the Study of Morphological Processing of the Tangkhul Language
- An Automated Multiple-Choice Question Generation Using Natural Language Processing Techniques

Main trends:
- Multimodal integration of speech and text processing in LLMs
- Ethical AI development with focus on bias mitigation and hallucination control
- Low-resource language processing for marginalized languages like Tangkhul
- Clinical NLP applications for real-time EHR analysis
- Code generation advancements for complex programming tasks

Top authors:
- Sijia Liu
- Andrew Wen
- Liwei Wang
- Huan He
- Sunyang Fu
- Robert Miller
- Andrew Williams
- Daniel Harris
- Ramakanth Kavuluru
- Mei Liu
- Jacob Devlin (BERT author)
- Thibaut Lavril (LLaMA team)

Open research questions:
- How can transfer learning be optimized for low-resource languages like Tangkhul in LLM frameworks?
- What are the most effective techniques for integrating speech and text processing in multimodal LLMs?
- How can ethical concerns such as bias and hallucination in LLMs be systematically mitigated?
- What are the challenges in deploying LLMs for real-time clinical decision-making in EHR systems?
- How can code generation from natural language be improved for complex programming tasks?
- What are the trade-offs between model size and efficiency for real-time clinical applications?