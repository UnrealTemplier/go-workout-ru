# 🏋️ Go Workout: 7 666 практических инженерных упражнений по Go

> *«Практика без теории слепа, теория без практики мертва. Единственный способ стать высококлассным инженером — писать много качественного, идиоматичного кода».*

[![Status](https://img.shields.io/badge/Status-100%25_Completed-10b981?style=for-the-badge&logo=git)](sources/)
[![Chapters](https://img.shields.io/badge/Chapters-100_из_100-6366f1?style=for-the-badge)](sources/)
[![Exercises](https://img.shields.io/badge/Exercises-7_666_задач-f59e0b?style=for-the-badge)](sources/)
[![Go Versions](https://img.shields.io/badge/Go_Versions-1.22_--_1.24+-00ADD8?style=for-the-badge&logo=go)](https://go.dev/)
[![Offline First](https://img.shields.io/badge/Offline_First-100%25_Static-10b981?style=for-the-badge&logo=html5)](sources/)

Интерактивный веб-тренажер и исчерпывающий задачник на русском языке, охватывающий **100 глав** и **7 666 детально разобранных упражнений** с теорией, пошаговыми действиями, компилируемым кодом, разбором низкоуровневой механики (GMP, аллокатор mcache/mcentral/mheap, GC триколор, epoll/netpoller), частыми ловушками и вопросами с реальных собеседований в BigTech (**Яндекс, Ozon, Авито, Т-Банк, VK, Wildberries, Lamoda, Касперский**).

---

## 🧭 Архитектура проекта

Контент хранится в Markdown в `sources/`, сайт собирает движок [html-textbook-engine](https://github.com/UnrealTemplier/html-textbook-engine) в GitHub Actions и публикует на GitHub Pages только после успешного аудита. Подробности — `AGENTS.md`.

```text
go-workout/
├── sources/                          # Источник правды: весь контент в Markdown
│   ├── 001. Пакеты и модули/
│   │   ├── 000. О главе.md           # Описание и итог главы
│   │   ├── 01. Введение, Окружение, Компиляция и Базовые Пакеты/
│   │   │   ├── 00. О разделе.md      # Полное название и описание раздела
│   │   │   ├── 001. Первый запуск Go-программы и концепция модулей.md
│   │   │   └── ...
│   │   └── ...
│   └── 100. Архитектурный Capstone. Проектирование/
├── engine/                           # Копия ядра html-textbook-engine (не редактируется)
├── book.toml                         # Настройки книги для движка: траектории, тексты главной, формулы
├── book/hooks.py                     # Хук аудита: gofmt -e по всем блокам Go
├── tools/                            # Отчёты разового переноса в Markdown
├── fact-checks/                      # Отчёты фактчека: fact-checks/<номер главы>/
├── .github/workflows/pages.yml       # CI: сборка → аудит → GitHub Pages
├── requirements.txt                  # markdown>=3.10,<3.11
├── scripts/                          # REBUILD_ALL.sh / REBUILD_ALL.bat — всё сразу; linux/, windows/ — отдельные команды
├── AGENTS.md                         # Инструкции для разработчиков и ИИ-агентов
└── README.md
```

---

## 🗺️ 7 Сквозных образовательных траекторий (Learning Paths)

1. **🔷 Core Go & Idiomatic Engineering** (Главы 1–19, Junior → Middle)
   * Синтаксис, система модулей, срезы, хэш-таблицы, полиморфизм интерфейсов, дженерики, обработка ошибок `errors.Is/As/Join`, `slog`.
2. **⚡ High-Concurrency & Low-Latency Network** (Главы 20–26, 74–77, 82, Middle+ → Senior)
   * Модель памяти Go, горутины, каналы, select, `context`, сокеты TCP/UDP, пул воркеров, lock-free (CAS), DoS-защита сокетов.
3. **💾 Storage, Caching & Data Consistency** (Главы 27–28, 61–64, 85, 96–97, Middle+ → Senior+)
   * PostgreSQL (`pgx`, connection pool), Redis NoSQL, ClickHouse OLAP, MongoDB, Elasticsearch, CDC-репликация, L1/L2 кэширование, Expand-Contract миграции.
4. **🌐 Distributed Systems & Event-Driven Architecture** (Главы 32–38, 68–73, 84, 86–87, 95, Senior → Staff/Principal)
   * gRPC / Protobuf, Kafka, RabbitMQ, NATS JetStream, Saga, Outbox, Raft консенсус, etcd v3, CQRS/ES, очереди River/Asynq, Temporal.io.
5. **📊 Enterprise Observability & Reliability Engineering** (Главы 29–31, 39–44, 80, 89, 94, Senior → Tech Lead)
   * Testcontainers, фаззинг-тестирование, Prometheus метрики, OpenTelemetry распределенная трассировка, pprof профилирование, Clean Architecture, хаос-инженерия Toxiproxy.
6. **🛡️ Cloud-Native, DevOps & Platform Security** (Главы 45–47, 78–83, 90–93, Senior → Platform Lead)
   * Multi-stage Docker (Scratch от 5 МБ), Kubernetes Operators/CRD, Service Mesh Istio/mTLS, Reverse Proxy, Cloud KMS Envelope Encryption, SBOM, Seccomp.
7. **🧠 Go Internals, Compilers, Tooling & AI** (Главы 48–56, 92, 98–100, Staff / Principal Engineer)
   * GMP рантайм планировщик, аллокатор памяти mcache/mcentral/mheap, триколор GC, unsafe, CGO, AST-парсер, Wasm Wazero, кастомные линтеры `go/analysis`, LLM/pgvector RAG и Grand Capstone.

---

## 🚀 Сборка и валидация проекта

### Требования
* Python 3.11+ и `pip install "markdown>=3.10,<3.11"`
* Go (для проверки `gofmt -e` в аудите)
* Firefox — по желанию, для рантайм-проверки формул

### Сборка и аудит
```bash
pip install -r requirements.txt
python3 -m engine.build --all --strict
python3 -m engine.audit --strict
```
Сборка занимает ~16 секунд и кладёт 8 136 страниц в `dist/` (в Git не хранится). Аудит проверяет ссылки и якоря всех страниц, отсутствие обращений к внешней сети, совместимость имён файлов и синтаксис всех блоков Go (`gofmt -e`).

Всё сразу одним щелчком — `scripts/REBUILD_ALL.sh` (Linux) или `scripts/REBUILD_ALL.bat` (Windows): зависимости, тесты, чистая пересборка `dist/`, строгий аудит. Отдельные команды — `scripts/linux/*.sh` и `scripts/windows/*.bat` (например, `scripts/linux/check.sh`); меню — `scripts/linux/menu.sh` / `scripts/windows/menu.bat`.

### Локальный просмотр
Откройте `dist/index.html` прямо в браузере: сайт работает по `file:///` без веб-сервера и без сети.
