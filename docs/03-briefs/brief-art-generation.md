# Бриф: генерация карикатур (10 картинок)

Исполнитель: art-director. Deliverable: `deliverables/art/level-01.png … level-10.png` + `art-log.md`.

## Инструмент (проверен в фазе 0)

Higgsfield MCP, tool `mcp__higgsfield__generate_image` (если tools deferred — загрузить через ToolSearch
`select:mcp__higgsfield__generate_image,mcp__higgsfield__job_status,mcp__higgsfield__balance`).

Рецепт рабочего вызова:
```json
{"params": {"model": "gpt_image_2", "prompt": "<промпт>", "aspect_ratio": "3:4", "quality": "medium", "count": 1}}
```
- Стоимость: ~0.5–1 кредит/картинку при medium (баланс на 2026-07-07: 1170 кредитов — хватает с запасом).
- Результат: `job_status` с `sync:true` → скачать `rawUrl` через curl.
- Тест-образец стиля: `docs/04-tools/test-cartoon-gpt-image-2.png` (ч/б газетный стиль — попадание отличное).

## Стайл-гайд

Базовый шаблон промпта (ч/б аутентичный вариант):
> Black and white newspaper comic cartoon: simple bold ink linework, halftone dot shading, single panel.
> [СЦЕНА]. Speech bubble: "[РЕПЛИКА]". Clean white background, retro newspaper gag-cartoon aesthetic, no color.

Цветной «мобильный» вариант (если пользователь выберет его):
> Cheerful flat-color cartoon illustration for a casual mobile puzzle game, single panel gag comic,
> bold clean outlines, soft warm palette, simple background. [СЦЕНА]. Speech bubble: "[РЕПЛИКА]".

Правила:
1. **НЕ упоминать «Jumble» в промпте** — модель дорисовывает трейдмарк-шапку «JUMBLE by David L. Hoyt…»
   (проверено на тесте). Добавлять в промпт: `no title, no logo, no header text, no watermark`.
2. Картинка должна **иллюстрировать ответ-сюрприз, не выдавая его текстом**: сцена + эмоция + реплика.
   Текст внутри — только короткие реплики в bubble (модель хорошо рендерит короткий EN-текст;
   RU-текст в bubble проверить на первом уровне — если артефачит, убирать текст из картинки вовсе
   и оставлять реплику в UI).
3. Прозрачность подсказки = параметр сложности P8: у ранних уровней сцена почти показывает ответ,
   у поздних — косвенный намёк (управляется детализацией сцены в промпте, поле в levels.json).
4. Единообразие: один шаблон промпта на все 10; менять только [СЦЕНА]/[РЕПЛИКА]; aspect_ratio 3:4 всюду.
5. Семейный тон, без брендов, без известных личностей.

## Процесс

1. Взять промпты из `deliverables/levels/levels.json` (поле cartoon.prompt).
2. Генерировать по одному, просматривать Read'ом; брак (лишний текст, кривые руки, шум) — регенерация
   с уточнением промпта; допускается count:2 и отбор.
3. Сохранять в `deliverables/art/level-NN.png`; вести `art-log.md`: уровень → финальный промпт →
   число попыток → job id.
4. После 10 картинок — общий контактный лист (можно склеить Python/PIL) и показ пользователю.

## Чек-лист сдачи

- [ ] 10 файлов level-01…10.png, единый стиль и aspect ratio.
- [ ] Ни на одной нет логотипов/заголовков/watermark и мусорного текста.
- [ ] Каждая картинка читается как намёк на ответ своего уровня (проверка: qa-playtester угадывает связь).
- [ ] art-log.md заполнен; расход кредитов зафиксирован.
