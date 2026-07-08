# Scroll Puzzle (Multicast Games) — аналитический отчёт

Дата исследования: 2026-07-07. Игра очень свежая (на Google Play ~с середины мая 2026, «7 недель» по данным AppBrain на начало июля), поэтому публичной аналитики (Sensor Tower / AppMagic revenue) почти нет — часть выводов помечена как **inference**.

---

## Кор-геймплей

**Жанр:** tile-matching / sliding puzzle с элементами jigsaw и коллекционирования. Официальное описание: «slide colorful 3D tiles across the board to assemble hidden pictures».

**Что делает игрок:**
- Двигает («скроллит») ряды/столбцы цветных 3D-плиток по полю — вверх, вниз, влево, вправо.
- Задача — свести вместе **4 фрагмента одной картинки**; собранная картинка «схлопывается» и отправляется в галерею.
- Уровень пройден, когда поле полностью очищено.
- За уровень начисляются **coins** (на что тратятся — из открытых источников не видно; **inference:** бустеры/подсказки или коллекции).

**Структура уровней:**
- **300+ уровней ручной сборки**, после 300-го — **бесконечные процедурно генерируемые**.
- Позиционирование — «no stress, no timers».

**Длина сессии:** прямых данных нет. По отзыву («уровни короткие, поэтому тратить время на просмотр рекламы не интересно») уровни ~**1–3 минуты** (**inference**); сессия казуального тайл-матчинга 5–15 минут (**inference**).

## Мета и прогрессия

Мета минимальная, чисто коллекционная:
- **200+ коллекционных 3D-персонажей** в **20 тематических коллекциях** (коты, динозавры, космос, роботы…).
- **Галерея** собранных картинок.
- Coins за уровни.
- Признаков декораций/метастройки, ивентов, battle pass, лидербордов **не обнаружено**. Классический hybrid-casual каркас «кор-луп + коллекция» без глубокой меты.

## Текущая монетизация

**Важный факт, корректирующий формулировку задания:** листинг Google Play содержит **обе** пометки — **«Есть реклама» И «Покупки в приложении»**. При этом:
- Диапазон цен IAP не отображается, ни один отзыв покупок не упоминает. **Inference:** флаг «про запас» либо remove-ads/монеты с минимальным весом; фактически монетизация **ad-first**.

**Подтверждённые рекламные размещения (из отзывов):**
- **Interstitial после уровня** — основной формат.
- **Interstitial посреди уровня** — отзыв (RU, май 2026): «полезло очень много рекламы — не только после прохождения очередного этапа, но и прямо посреди уровня». Отзыв (EN, апрель 2026): «once I reached level 14, the puzzle was repeatedly interrupted by adverts».
- **Ad-free onboarding:** реклама включается примерно с 14-го уровня (**inference** по отзыву).
- **Rewarded video и banner** — прямых подтверждений нет; rewarded вероятен (стандарт жанра + coins), banner не подтверждён (**inference**).

## Издатель: Multicast Games

- Студия из Пафоса (Кипр), MULTICAST GAMES LIMITED, основана ~2019–2021. На Android ~**29 игр**, на iOS 11; **Scroll Puzzle — Android-only**.
- **Портфель:** Scroll Puzzle (4.6★), Idle Fish 2 (5M+), Butcher Hero, Desert Worm / Devour Idle RPG, Idle Human Evolution, Art Puzzle World (4.7★), Categories Solitaire (4.7★), Zoo/Dog/Bubble Sort, TileMatch и др. Профиль — **hybrid-casual конвейер**.
- **Флагманский хит — Alien Invasion: RPG Idle Space.** Кейс Persona.ly: **гибрид ~50/50 IAP/IAA**, вся ad-выручка — **только rewarded** (без принудительных interstitial). Порядок цифр: ~600K загрузок и ~$100K выручки/мес (оценки). Игру студия впоследствии продала.
- **UA:** кейс AppMetrica — $1–2M годового спенда при **ROAS 200%** силами 2 UA-менеджеров; Unity, AppLovin, Mintegral, Google, Reddit, Twitter.
- **«Cats & Seek» НЕ принадлежит Multicast** (это Noobzilla) — не использовать как референс издателя.
- **Вывод:** Multicast умеет и практикует гибрид (Alien Invasion 50/50); Scroll Puzzle с ad-first стартом — типичный плейбук: выпустить, разогнать UA на рекламе, IAP подключить при росте (**inference**).

## Аудитория и отзывы

- **Рейтинг:** 4.6–4.7★ (~240–315 оценок). **Загрузки:** «10 тыс.+»; AppBrain ~18K всего, ~9K/30 дней (~300/день) — фаза раннего разгона.
- Everyone / «Для всех»; ~110–126 MB; Android 7.0+.
- **Позитив:** «Fun, fun, fun», «для тех, кто любит искусство, но не умеет рисовать», расслабляющий геймплей, коллекции.
- **Главная жалоба — частота рекламы** (interstitial после каждого короткого уровня и посреди уровня); при крошечной базе отзывов это заметная доля негатива, есть «Удаляю».
- **Демография:** данных нет. **Inference:** взрослая казуальная 35+, скорее женская — классический relaxing-puzzle профиль.

## Референсы гибридной монетизации (ads + IAP)

| Игра | Модель | IAP-структура |
|---|---|---|
| **Wordscapes** (PeopleFun) | Гибрид, ads-heavy для неплательщиков | Coins, **remove ads** (в т.ч. временный), **piggy bank**, бустеры; ad-стек на AppLovin MAX bidding |
| **Words of Wonders / Word Cookies / Word Trip** | Гибрид word-жанра | Монеты, подсказки, remove ads, starter packs (**частично inference**) |
| **Alien Invasion** (сам Multicast) | **50/50 IAP/IAA** | IAP + только rewarded, без interstitial — мягкая модель, ROAS 200% |
| **Block Blast** (Hungry Studio) | Контр-пример: **ads-only** | Без IAP; ~$17.5M/мес на рекламе при 200M MAU — ads-only работает только на экстремальном масштабе |

**Бенчмарки для гибрида в puzzle:**
- Платят ~1.8% игроков F2P → чистый IAP оставляет 98% немонетизированными; чистый ads даёт ARPDAU ~$0.03–0.08; гибрид — блендед ~$0.15–0.50.
- В word-играх **rewarded даёт ~70% ad-выручки**; в лёгких пазлах ~60% даёт interstitial — но тогда обязательна IAP-опция remove ads.
- Типовой гибридный IAP-набор: coins → бустеры/подсказки → remove ads ($3–10) → starter pack → piggy bank → season pass (зрелый LiveOps).

**Применительно к Scroll Puzzle:** сейчас — агрессивные interstitial при отсутствии видимого IAP-магазина; ровно та конфигурация, где remove-ads + coins/бустеры + rewarded-размещения («удвоить монеты», «бустер за просмотр») дают прирост без ущерба ретеншену (**inference/рекомендация**).

## Источники

- https://play.google.com/store/apps/details?id=com.multicastgames.scrollpuzzle&hl=en (+ русская версия страницы)
- https://www.appbrain.com/app/scroll-puzzle/com.multicastgames.scrollpuzzle
- https://apkpure.com/scroll-puzzle/com.multicastgames.scrollpuzzle
- https://play.google.com/store/apps/developer?id=MULTICAST+GAMES
- https://apps.apple.com/us/developer/multicast-games-limited/id1597996449
- https://multicastgames.com/
- https://appmetrica.yandex.com/about/blog/appmetrica-x-multicast-games
- https://persona.ly/blog/2023/05/iap-or-iaa-why-not-both-alien-invasion-hybrid-casual-case-study/
- https://www.gamigion.com/alien-invasion-case-study-how-to-scale-a-game-with-a-small-ua-team/
- https://balancy.co/blog/2025/03/26/how-could-block-blast-by-hungry-studio-earn-more-monetization-and-gameplay-deconstruction/
- https://felixbraberg.substack.com/p/the-biggest-ad-monetized-game-on
- https://peoplefun.helpshift.com/hc/en/6-wordscapes/faq/320-how-can-i-remove-ads/
- https://www.playbite.com/q/how-to-get-rid-of-piggy-bank-in-wordscapes
- https://medium.com/@UPLTV/how-to-monetize-word-games-effectively-43829d146a09
- https://gamegrowthadvisor.com/blog/2026-04-02-f2p-monetization-models-comparison-2026/
- https://cas.ai/2025/10/09/hybrid-monetization-mobile-games-guide-2-2-2-8-2-2-2-8-3-3-4-5-6-7-2/

**Ключевые оговорки:** (1) флаг IAP в листинге есть, но состав IAP не подтверждён; (2) «Cats & Seek» не Multicast; (3) revenue-оценок по Scroll Puzzle нет — игра слишком новая.
