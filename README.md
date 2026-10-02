# 🏋️ Go Workout: 7 666 практических инженерных упражнений по Go

> *«Практика без теории слепа, теория без практики мертва. Единственный способ стать высококлассным инженером — писать много качественного, идиоматичного кода».*

[![Status](https://img.shields.io/badge/Status-100%25_Completed-10b981?style=for-the-badge&logo=git)](dist/index.html)
[![Chapters](https://img.shields.io/badge/Chapters-100_из_100-6366f1?style=for-the-badge)](dist/index.html)
[![Exercises](https://img.shields.io/badge/Exercises-7_666_задач-f59e0b?style=for-the-badge)](dist/index.html)
[![Go Versions](https://img.shields.io/badge/Go_Versions-1.22_--_1.24+-00ADD8?style=for-the-badge&logo=go)](https://go.dev/)
[![Offline First](https://img.shields.io/badge/Offline_First-100%25_Static-10b981?style=for-the-badge&logo=html5)](dist/index.html)

Интерактивный веб-тренажер и исчерпывающий задачник на русском языке, охватывающий **100 глав** и **7 666 детально разобранных упражнений** с теорией, пошаговыми действиями, компилируемым кодом, разбором низкоуровневой механики (GMP, аллокатор mcache/mcentral/mheap, GC триколор, epoll/netpoller), частыми ловушками и вопросами с реальных собеседований в BigTech (**Яндекс, Ozon, Авито, Т-Банк, VK, Wildberries, Lamoda, Касперский**).

---

## 🧭 Архитектура проекта

Структура репозитория выстроена по строгому стандарту модульного статического генератора:

```text
go-workout/
├── sources/                          # Исходные задачники всех 100 глав (Markdown)
│   ├── 1. Пакеты и модули.md
│   ├── 2. Компиляция, сборка и запуск.md
│   ├── ...
│   └── 100. Архитектурный Capstone...md
├── dist/                             # Скомпилированный статический веб-сайт курса
│   ├── index.html                    # Главный портал курса, специализации и поиск
│   ├── 001-pakety-i-moduli.html      # Глава 01 (91 упр.)
│   ├── 002-kompilyatsiya-sborka-i-zapusk.html # Глава 02 (25 упр.)
│   ├── ...
│   ├── 100-arhitekturnyy-capstone-...html     # Глава 100 (50 упр.)
│   ├── favicon.ico                   # Иконка портала (ICO)
│   └── favicon.svg                   # Векторный логотип Go (SVG)
├── builder/                          # Ядро сборки, данные и утилиты аудита
│   ├── chapters.py                   # Динамическое сканирование sources/*.md
│   ├── template.py                   # HTML/CSS шаблоны, Dark theme, Prism.js
│   ├── build_all.py                  # Главный компилятор всех страниц в dist/
│   ├── audit_all.py                  # Сквозной аудит gofmt, якорей и ссылок
│   ├── chapter2_data.json            # Каноничные данные упражнений глав 2..100
│   └── section[1-6].py               # Модули упражнений главы 1
├── .github/
│   └── workflows/
│       └── pages.yml                 # CI/CD автоматический деплой dist/ на GitHub Pages
├── favicon.ico                       # Favicon для корня репозитория
├── favicon.svg                       # Favicon SVG для корня репозитория
├── AGENTS.md                         # Исчерпывающий инженерный стандарт и гайдлайн
└── README.md                         # Данный файл описания
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
* Python 3.10+
* Go 1.22+ (для валидации синтаксиса `gofmt -e`)

### 1. Сборка всех статических страниц курса
```bash
python3 builder/build_all.py
```
Скрипт читает markdown-задачники из `sources/`, собирает все 100 глав и главный портал, после чего сохраняет статические страницы в каталог `dist/`.

### 2. Запуск сквозного технического аудита
```bash
python3 builder/audit_all.py
```
Выполняет 100% валидацию:
* Проверка синтаксиса всех блоков Go-кода через компилятор `gofmt -e`.
* Проверка наличия и уникальности HTML-якорей `#ex-{N}` для каждого из 7 666 упражнений.
* Проверка целостности и корректного закрытия HTML-документов.
* Валидация кросс-ссылок навигации портала.

### 3. Локальный просмотр
Откройте файл `dist/index.html` прямо в браузере (поддерживается режим `file:///` без необходимости запуска локального веб-сервера).
