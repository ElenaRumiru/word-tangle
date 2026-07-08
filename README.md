# Word Tangle — мобильная адаптация Jumble (тестовое задание)

Мобильная адаптация журнальной словесной игры **Jumble** + план гибридной монетизации игры
**Scroll Puzzle**. Game Design / Balance & Economy.

## Открыть по ссылке

- **▶ Презентация (case study):** https://elenarumiru.github.io/word-tangle/
- **🎮 Играбельный прототип:** https://elenarumiru.github.io/word-tangle/prototype/

Обе страницы — статические, открываются в браузере без установки. В прототипе кнопка **🐞 ЧИТЫ**
(по центру сверху) открывает панель тестовых читов, включая русское объяснение каламбура каждого уровня.

## Что в репозитории

| Путь | Что это |
|---|---|
| [`index.html`](index.html) | Презентация (case study) — исходник страницы GitHub Pages |
| [`prototype/`](prototype/) | Играбельный прототип (один самодостаточный HTML) |
| [`deliverables/levels/`](deliverables/levels/) | 10 уровней (`levels.json`), обоснование кривой сложности, валидатор |
| [`deliverables/art/`](deliverables/art/) | 10 карикатур (нейросеть, 1:1) + контактный лист |
| [`deliverables/balance/`](deliverables/balance/) | Таблица баланса 100 уровней (`.xlsx`/`.csv`) + формула и веса |
| [`deliverables/monetization/`](deliverables/monetization/) | План гибридной монетизации Scroll Puzzle + расчётная модель |
| [`deliverables/presentation/`](deliverables/presentation/) | Исходник презентации (шаблон + скрипты сборки) |
| [`docs/`](docs/) | Разведка (анализ Jumble, Scroll Puzzle, UX word-games), брифы, план |

## Пункты задания

1. **UX и управление** — `deliverables/levels/ux-concept.md`
2. **10 уровней + картинки нейросетью** — `deliverables/levels/levels.json`, `deliverables/art/`
3. **Интерактивный прототип с читами** — `prototype/`
4. **Логика генератора уровней** — `deliverables/levels/level-generator-design.md`
5. **Таблица баланса 100 уровней** — `deliverables/balance/balance-100-levels.xlsx`
6. **Гибридная монетизация Scroll Puzzle** — `deliverables/monetization/scroll-puzzle-hybrid.md`

## Технические заметки

- Прототип — vanilla HTML/CSS/JS, всё встроено (уровни + картинки в base64), ноль внешних запросов,
  работает офлайн. Собирается из шаблона: `deliverables/prototype/build_prototype.py`.
- Презентация — self-contained HTML (графики и скриншоты встроены base64). Сборка:
  `deliverables/presentation/build_site.py`.
- Контент уровней и весь UI игры — английский (на базе реальных пазлов журнала Jumble);
  по-русски остаётся только панель читов (инструмент тестирования, не часть продукта).
- Факты о Scroll Puzzle — из открытых источников; все числа монетизационной модели — выдуманные
  допущения по условию задания.

_Исходный журнал Jumble (защищён авторским правом) в репозиторий не включён._
