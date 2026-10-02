# AGENTS.md — Исчерпывающее руководство для ИИ-агентов по генерации учебника Go

Данный файл является **главным архитектурным стандартом и технической инструкцией** для ИИ-агентов (Antigravity, Claude, ChatGPT, Cursor и др.) по разработке, расширению и поддержке интерактивного учебника-тренажера по языку **Go (Golang)**.

---

## 🎯 1. Цель проекта и Целевая аудитория

* **Цель проекта:** Создать полноценный, интерактивный, глубокий веб-учебник на русском языке, состоящий из **100 глав** (83 завершенные главы фундаментального курса + 17 глав расширения до уровня Staff / Principal Engineer).
* **Целевая аудитория:** Уверенно-начинающие бэкенд-разработчики с базовым опытом в C/C++, Python, PHP или JS, изучающие Go для трудоустройства на позиции Middle/Senior/Staff Go Developer в ведущие российские технологические компании и BigTech (**Яндекс, Ozon, Авито, Т-Банк, VK, Wildberries, Lamoda, Касперский**).
* **Стиль изложения:** Живой, структурированный, инженерно-строгий, с глубоким погружением в механику компилятора, рантайма (GMP планировщик, GC триколор, epoll/netpoller, mcache/mcentral/mheap аллокатор памяти), сетевого стека, конкурентности и лучших практик HighLoad/DevSecOps/Kubernetes.

---

## 📊 2. Текущий статус проекта (Все 100 глав завершены на 100%!)

* **Целевой объем курса:** 100 глав (7 666 упражнений)
* **Готово задачников (Markdown):** 100 из 100 (все 7 666 упражнений полностью сформулированы)
* **Готово интерактивных глав (HTML):** 100 из 100 (все 7 666 интерактивных упражнений с решениями, теорией и валидацией)
* **В очереди генерации интерактивных глав:** 0 глав (Курс полностью завершен!)
* **Качество кода:** 100% валидация синтаксиса Go (`gofmt -e`), нулевые пропуски, единый дизайн, проверенная сквозная навигация и аудит всех HTML-страниц.

### 🧭 Архитектура навигации: Портал + Главы курса (`dist/`)
* **`dist/index.html` — Главный портал курса и навигация по Learning Paths:** Визитная карточка проекта, сводные метрики, 7 сквозных специализаций (Learning Paths), 22 тематических кластера и интерактивный поиск по всем 100 главам.
* **`dist/001-pakety-i-moduli.html` — Глава 01 «Пакеты и модули»:** Полноценная страница первой главы со всеми 91 упражнениями.
* **`dist/002-kompilyatsiya-sborka-i-zapusk.html` .. `dist/100-arkhitekturnyy-capstone-proektirovanie-i-skvoznoy-zapusk-otkazoustoychivoy-highload-platformy.html` — Последовательные страницы глав курса.**

---

### 🗺️ 2.1. Сквозные образовательные траектории (7 Learning Paths)

Для гибкого обучения в зависимости от текущего грейда и карьерной цели курс разделен на 7 сквозных специализаций:

* **🔷 Core Go & Idiomatic Engineering** (Junior → Middle)
  * **Охват:** Главы 1–19
  * **Суть и компетенции:** Синтаксис, система модулей, структуры данных, полиморфизм интерфейсов, дженерики, идиоматичная обработка ошибок и файловые операции.
  * **Ключевой стек:** `go.mod`, `slices`, `maps`, `interfaces`, `generics`, `errors`, `slog`
* **⚡ High-Concurrency & Low-Latency Network** (Middle+ → Senior)
  * **Охват:** Главы 20, 21, 22, 23, 24, 25, 26, 74, 75, 76, 77, 82
  * **Суть и компетенции:** Многопоточность без гонок данных, каналы и select, context, низкоуровневые сокеты TCP/UDP, event-loop gnet, lock-free и DoS-защита.
  * **Ключевой стек:** `goroutines`, `channels`, `sync`, `TCP/UDP`, `gnet`, `lock-free`, `SO_REUSEPORT`
* **💾 Storage, Caching & Data Consistency** (Middle+ → Senior+)
  * **Охват:** Главы 27, 28, 61, 62, 63, 64, 85, 96, 97
  * **Суть и компетенции:** Реляционные и NoSQL хранилища: пул pgx, Redis, ClickHouse, Mongo, CDC репликация, двухуровневый L1/L2 кэш с XFetch и Zero-Downtime миграции.
  * **Ключевой стек:** `PostgreSQL`, `pgx`, `Redis`, `ClickHouse`, `Elasticsearch`, `CDC`, `XFetch`
* **🌐 Distributed Systems & Event-Driven Architecture** (Senior → Staff/Principal)
  * **Охват:** Главы 32, 33, 34, 35, 36, 37, 38, 68, 69, 70, 71, 72, 73, 84, 86, 87, 95
  * **Суть и компетенции:** Распределенные платформы: gRPC, Kafka, RabbitMQ, Saga, Outbox, консенсус Raft, etcd, CQRS/ES, очереди River/Asynq и Temporal.io.
  * **Ключевой стек:** `gRPC`, `Kafka`, `RabbitMQ`, `NATS`, `Raft`, `Temporal`, `etcd`, `CQRS`
* **📊 Enterprise Observability & Reliability Engineering** (Senior → Tech Lead)
  * **Охват:** Главы 29, 30, 31, 39, 40, 41, 42, 43, 44, 80, 89, 94
  * **Суть и компетенции:** Полный стек надежности: Testcontainers, фаззинг, метрики Prometheus, OTel трассировка, pprof профилирование, Чистая архитектура, хаос-инженерия Toxiproxy.
  * **Ключевой стек:** `testcontainers`, `fuzzing`, `Prometheus`, `OpenTelemetry`, `pprof`, `Toxiproxy`, `OpenFeature`
* **🛡️ Cloud-Native, DevOps & Platform Security** (Senior → Platform Lead)
  * **Охват:** Главы 45, 46, 47, 78, 79, 81, 83, 90, 91, 93
  * **Суть и компетенции:** Инфраструктура и безопасность: Docker, Kubernetes, K8s Operators/CRD, Service Mesh, gRPC-Gateway, Reverse Proxy, Cloud KMS, SBOM, Seccomp.
  * **Ключевой стек:** `Docker`, `Kubernetes`, `Kubebuilder`, `Service Mesh`, `KMS`, `SBOM`, `Seccomp`
* **🧠 Go Internals, Compilers, Tooling & AI** (Staff / Principal Engineer)
  * **Охват:** Главы 48, 49, 50, 51, 52, 53, 54, 55, 56, 92, 98, 99, 100
  * **Суть и компетенции:** Элитный рантайм: планировщик GMP, аллокатор mcache/mheap, GC, unsafe, CGO, AST, WebAssembly Wazero, корпоративные линтеры `go/analysis`, LLM RAG и Capstone.
  * **Ключевой стек:** `GMP`, `Heap Allocator`, `GC`, `unsafe`, `AST`, `Wazero Wasm`, `go/analysis`, `Ollama/pgvector`

---

### 🏛️ 2.2. Архитектура 22 Тематических кластеров знаний (Knowledge Clusters)

* **Блок 01: Синтаксис и модульная структура** (Главы 01–04)
  * *Содержание:* Пакеты, go.mod, компилятор, ввод-вывод fmt, базовые типы и константы
* **Блок 02: Управляющие структуры и коллекции** (Главы 05–09)
  * *Содержание:* Условия if/switch, циклы for/range, массивы, слайсы (SliceHeader), мапы (hmap)
* **Блок 03: Функции, указатели и структуры данных** (Главы 10–14)
  * *Содержание:* Замыкания, defer, escape-анализ указателей, структуры, выравнивание, интерфейсы (iface/eface)
* **Блок 04: Парадигмы, полиморфизм и надежность кода** (Главы 15–19)
  * *Содержание:* ООП-композиция, дженерики (Go 1.18+), ошибки errors.Is/As/Join, файлы, log/slog
* **Блок 05: Конкурентность, синхронизация и контекст** (Главы 20–23)
  * *Содержание:* Горутины, sync/atomic, буферизованные каналы, select, context таймауты, конкурентные паттерны
* **Блок 06: Сетевой стек и веб-сервисы** (Главы 24–26)
  * *Содержание:* Низкоуровневые сокеты TCP/UDP, http.Client (keep-alive, transport), REST API серверы и middleware
* **Блок 07: Хранилища данных, кэш и транзакции** (Главы 27–28)
  * *Содержание:* PostgreSQL (jackc/pgx, connection pool, ACID), Redis NoSQL (структуры данных, Pub/Sub, Streams)
* **Блок 08: Тестирование, бенчмаркинг и фаззинг** (Главы 29–31)
  * *Содержание:* Юнит-тесты (testify), Testcontainers в Docker, бенчмарки testing.B (аллокации памяти), фаззинг
* **Блок 09: Межсервисное взаимодействие и RPC** (Главы 32–35)
  * *Содержание:* Protocol Buffers proto3, gRPC стриминг и интерцепторы, микросервисные паттерны, GraphQL, WebSockets
* **Блок 10: Асинхронные шины сообщений и брокеры** (Главы 36–38)
  * *Содержание:* RabbitMQ (AMQP 0-9-1, exchanges, DLQ), Apache Kafka (consumer groups, partitions), NATS JetStream
* **Блок 11: Мониторинг, трассировка и диагностика** (Главы 39–41)
  * *Содержание:* Prometheus метрики, распределенная трассировка OpenTelemetry, pprof профилирование CPU/памяти
* **Блок 12: Чистая архитектура, DDD и HighLoad** (Главы 42–44)
  * *Содержание:* Onion/Clean Architecture, DDD aggregates, enterprise-шаблоны проектирования, HighLoad отказоустойчивость
* **Блок 13: Контейнеризация и оркестрация** (Главы 45–47)
  * *Содержание:* Multi-stage Docker (Scratch от 5 МБ), CI/CD автоматизация, Kubernetes (Pods, Deployments, Services, HPA)
* **Блок 14: Внутренности рантайма Go и компилятор** (Главы 48–56)
  * *Содержание:* Планировщик GMP (work stealing), аллокатор кучи mcache/mheap, триколор GC, unsafe, CGO, syscalls, AST, кодогенерация
* **Блок 15: Криптография, аутентификация и веб-безопасность** (Главы 57–60)
  * *Содержание:* AES-GCM/RSA/Ed25519 шифрование, хеширование паролей Argon2id/bcrypt, JWT/OAuth2 токены, OWASP защита
* **Блок 16: Специализированные базы данных и CDC** (Главы 61–64)
  * *Содержание:* MongoDB NoSQL, аналитическая СУБД ClickHouse (MergeTree OLAP), Elasticsearch поиск, Change Data Capture (CDC)
* **Блок 17: Real-time коммуникации и альтернативные протоколы** (Главы 65–67)
  * *Содержание:* Платформы вебхуков с HMAC, Server-Sent Events (SSE), RPC альтернативы (Twirp, Cap'n Proto, FlatBuffers)
* **Блок 18: Распределенные транзакции и консенсус** (Главы 68–73)
  * *Содержание:* Паттерн Saga, Transactional Outbox/Inbox, идемпотентные API, Leader Election, консенсус Raft, Distributed Locks
* **Блок 19: Экстремальная оптимизация и системное программирование** (Главы 74–77)
  * *Содержание:* Cache-friendly структуры (L1/L2 линии, false sharing), Lock-free (CAS), Plan 9 Ассемблер, сетевой движок gnet
* **Блок 20: Системный харденинг и безопасность окружения** (Главы 78–83)
  * *Содержание:* Envelope Encryption / KMS, Service Mesh (Istio/mTLS), W3C Trace Context, SBOM / Cosign, DoS-защита сокетов, Seccomp/Capabilities
* **Блок 21: Распределенная надежность, потоки и облачные платформы** (Главы 84–93)
  * *Содержание:* CQRS/Event Sourcing, L1/L2 XFetch кэш, очереди Asynq/River, Temporal.io, Stream Processing, Chaos Toxiproxy, gRPC-Gateway, K8s Operators, Wasm Wazero, Reverse Proxy
* **Блок 22: Enterprise-инженерия, ИИ и Capstone** (Главы 94–100)
  * *Содержание:* OpenFeature флаги, etcd v3 координация, Zero-Downtime миграции, Time-Series Gorilla, кастомные линтеры go/analysis, LLM/pgvector RAG, Grand Architecture Capstone

---

### 🛡️ 2.3. Стандарт неизменности нумерации существующих глав (Immutability Rule)

> [!IMPORTANT]
> **ПРАВИЛО СТАБИЛЬНОСТИ БАЗЫ (APPEND-ONLY):**
> Категорически запрещено перетасовывать, физически переименовывать или сдвигать нумерацию существующих файлов глав 1–83 (`1. Пакеты и модули.md` .. `83. Системная изоляция...md`)!
> 1. В 7 071 готовом упражнении содержатся сотни перекрестных ссылок на конкретные главы (*«как мы разбирали в Главе 20...»*, *«в Главе 27 по PostgreSQL...»*). Любая перенумерация приведет к каскадному разрушению ссылочной целостности.
> 2. Репозиторий имеет чистую историю из 83 атомарных коммитов (`Module 1` .. `Module 83`). Переименования сотрут прозрачность истории Git.
> 3. Расширение курса до 100 глав выполняется **строго в режиме Append-Only**: новые модули создаются как главы **84–100**.
> 4. Тематическая группировка курса обеспечивается **на уровне навигации и UI** (в оглавлении на портале `index.html` и в сайдбаре), что дает 100% структурную ясность без малейших рисков регрессий.

---

### Сводная таблица всех 100 глав учебника:

| № | Название главы | Markdown файл | HTML страница | Кол-во упр. | Статус |
| :-: | :--- | :--- | :--- | :-: | :-: |
| **01** | Пакеты и модули | `1. Пакеты и модули.md` | `001-pakety-i-moduli.html` | 91 | ✅ Готово (91/91) |
| **02** | Компиляция, сборка и запуск | `2. Компиляция, сборка и запуск.md` | `002-kompilyatsiya-sborka-i-zapusk.html` | 25 | ✅ Готово (25/25) |
| **03** | Пакет fmt и консольный ввод-вывод | `3. Пакет fmt и консольный ввод-вывод.md` | `003-paket-fmt-i-konsolnyy-vvod-vyvod.html` | 65 | ✅ Готово (65/65) |
| **04** | Базовые типы, переменные и константы | `4. Базовые типы, переменные и константы.md` | `004-bazovye-tipy-peremennye-i-konstanty.html` | 111 | ✅ Готово (111/111) |
| **05** | Условные конструкции | `5. Условные конструкции.md` | `005-uslovnye-konstruktsii.html` | 64 | ✅ Готово (64/64) |
| **06** | Циклы | `6. Циклы.md` | `006-tsikly.html` | 64 | ✅ Готово (64/64) |
| **07** | Массивы | `7. Массивы.md` | `007-massivy.html` | 32 | ✅ Готово (32/32) |
| **08** | Слайсы | `8. Слайсы.md` | `008-slaysy.html` | 74 | ✅ Готово (74/74) |
| **09** | Мапы | `9. Мапы.md` | `009-mapy.html` | 62 | ✅ Готово (62/62) |
| **10** | Функции | `10. Функции.md` | `010-funktsii.html` | 100 | ✅ Готово (100/100) |
| **11** | Указатели | `11. Указатели.md` | `011-ukazateli.html` | 49 | ✅ Готово (49/49) |
| **12** | Передача аргументов | `12. Передача аргументов.md` | `012-peredacha-argumentov.html` | 67 | ✅ Готово (67/67) |
| **13** | Структуры | `13. Структуры.md` | `013-struktury.html` | 71 | ✅ Готово (71/71) |
| **14** | Интерфейсы | `14. Интерфейсы.md` | `014-interfeysy.html` | 77 | ✅ Готово (77/77) |
| **15** | ООП в Go | `15. ООП в Go.md` | `015-oop-v-go.html` | 127 | ✅ Готово (127/127) |
| **16** | Дженерики | `16. Дженерики.md` | `016-dzheneriki.html` | 131 | ✅ Готово (131/131) |
| **17** | Обработка ошибок | `17. Обработка ошибок.md` | `017-obrabotka-oshibok.html` | 58 | ✅ Готово (58/58) |
| **18** | Работа с файлами | `18. Работа с файлами.md` | `018-rabota-s-faylami.html` | 100 | ✅ Готово (100/100) |
| **19** | Логирование | `19. Логирование.md` | `019-logirovanie.html` | 84 | ✅ Готово (84/84) |
| **20** | Горутины и синхронизация | `20. Горутины и синхронизация.md` | `020-gorutiny-i-sinkhronizatsiya.html` | 124 | ✅ Готово (124/124) |
| **21** | Каналы и select | `21. Каналы и select.md` | `021-kanaly-i-select.html` | 95 | ✅ Готово (95/95) |
| **22** | Контекст | `22. Контекст.md` | `022-paket-context.html` | 52 | ✅ Готово (52/52) |
| **23** | Паттерны конкурентности | `23. Паттерны конкурентности.md` | `023-patterny-i-kaverznye-sluchai-konkurentnosti.html` | 132 | ✅ Готово (132/132) |
| **24** | Низкоуровневая сеть | `24. Низкоуровневая сеть.md` | `024-nizkourovnevaya-set-tcp-i-udp.html` | 63 | ✅ Готово (63/63) |
| **25** | HTTP-клиент | `25. HTTP-клиент.md` | `025-http-klient.html` | 45 | ✅ Готово (45/45) |
| **26** | HTTP-сервер, REST API и Middleware | `26. HTTP-сервер, REST API и Middleware.md` | `026-http-server-rest-api-i-middleware.html` | 158 | ✅ Готово (158/158) |
| **27** | Реляционные базы данных (SQL и PostgreSQL) | `27. Реляционные базы данных (SQL и PostgreSQL).md` | `027-relyatsionnye-bazy-dannykh-sql-i-postgresql.html` | 163 | ✅ Готово (163/163) |
| **28** | Базы данных NoSQL и кэширование (Redis) | `28. Базы данных NoSQL и кэширование (Redis).md` | `028-bazy-dannykh-nosql-i-keshirovanie-redis.html` | 115 | ✅ Готово (115/115) |
| **29** | Модульное тестирование (Unit Testing) и Assertions | `29. Модульное тестирование (Unit Testing) и Assertions.md` | `029-modulnoe-testirovanie-unit-testing-i-assertions.html` | 96 | ✅ Готово (96/96) |
| **30** | Мокирование и интеграционное тестирование | `30. Мокирование и интеграционное тестирование.md` | `030-mokirovanie-i-integratsionnoe-testirovanie.html` | 107 | ✅ Готово (107/107) |
| **31** | Бенчмарки, фаззинг и продвинутые методы тестирования | `31. Бенчмарки, фаззинг и продвинутые методы тестирования.md` | `031-benchmarki-fazzing-i-prodvinutye-metody-testirovaniya.html` | 120 | ✅ Готово (120/120) |
| **32** | Protocol Buffers и gRPC | `32. Protocol Buffers и gRPC.md` | `032-protocol-buffers-i-grpc.html` | 189 | ✅ Готово (189/189) |
| **33** | Микросервисная архитектура и паттерны | `33. Микросервисная архитектура и паттерны.md` | `033-mikroservisnaya-arkhitektura-i-patterny.html` | 89 | ✅ Готово (89/89) |
| **34** | GraphQL | `34. GraphQL.md` | `034-graphql.html` | 78 | ✅ Готово (78/78) |
| **35** | WebSockets и Real-time | `35. WebSockets и Real-time.md` | `035-websockets-i-real-time.html` | 78 | ✅ Готово (78/78) |
| **36** | RabbitMQ | `36. RabbitMQ.md` | `036-rabbitmq.html` | 130 | ✅ Готово (130/130) |
| **37** | Apache Kafka | `37. Apache Kafka.md` | `037-apache-kafka.html` | 88 | ✅ Готово (88/88) |
| **38** | NATS и NATS JetStream | `38. NATS и NATS JetStream.md` | `038-nats-i-nats-jetstream.html` | 77 | ✅ Готово (77/77) |
| **39** | Метрики и мониторинг (Prometheus) | `39. Метрики и мониторинг (Prometheus).md` | `039-metriki-i-monitoring-prometheus.html` | 114 | ✅ Готово (114/114) |
| **40** | Распределенная трассировка (OpenTelemetry) | `40. Распределенная трассировка (OpenTelemetry).md` | `040-raspredelennaya-trassirovka-opentelemetry.html` | 79 | ✅ Готово (79/79) |
| **41** | Профилирование и рантайм-диагностика | `41. Профилирование и рантайм-диагностика.md` | `041-profilirovanie-i-rantaym-diagnostika.html` | 24 | ✅ Готово (24/24) |
| **42** | Проектирование чистой архитектуры и DDD | `42. Проектирование чистой архитектуры и DDD.md` | `042-proektirovanie-chistoy-arkhitektury-i-ddd.html` | 98 | ✅ Готово (98/98) |
| **43** | Шаблоны проектирования распределенных и enterprise-систем | `43. Шаблоны проектирования распределенных и enterprise-систем.md` | `043-shablony-proektirovaniya-raspredelennykh-i-enterprise-sistem.html` | 112 | ✅ Готово (112/112) |
| **44** | Проектирование высоконагруженных и отказоустойчивых систем | `44. Проектирование высоконагруженных и отказоустойчивых систем.md` | `044-proektirovanie-vysokonagruzhennykh-i-otkazoustoychivykh-sistem.html` | 64 | ✅ Готово (64/64) |
| **45** | Контейнеризация и Docker | `45. Контейнеризация и Docker.md` | `045-konteynerizatsiya-i-docker.html` | 75 | ✅ Готово (75/75) |
| **46** | Автоматизация CI-CD | `46. Автоматизация CI-CD.md` | `046-avtomatizatsiya-ci-cd.html` | 57 | ✅ Готово (57/57) |
| **47** | Оркестрация в Kubernetes | `47. Оркестрация в Kubernetes.md` | `047-orkestratsiya-v-kubernetes.html` | 180 | ✅ Готово (180/180) |
| **48** | Планировщик GMP | `48. Планировщик GMP.md` | `048-planirovshchik-gmp.html` | 93 | ✅ Готово (93/93) |
| **49** | Аллокатор кучи и управление памятью | `49. Аллокатор кучи и управление памятью.md` | `049-allokator-kuchi-i-upravlenie-pamyatyu.html` | 66 | ✅ Готово (66/66) |
| **50** | Garbage Collector и тюнинг памяти | `50. Garbage Collector и тюнинг памяти.md` | `050-garbage-collector-i-tyuning-pamyati.html` | 87 | ✅ Готово (87/87) |
| **51** | Работа с unsafe и низкоуровневой памятью | `51. Работа с unsafe и низкоуровневой памятью.md` | `051-rabota-s-unsafe-i-nizkourovnevoy-pamyatyu.html` | 85 | ✅ Готово (85/85) |
| **52** | Интеграция с C-кодом через CGO | `52. Интеграция с C-кодом через CGO.md` | `052-integratsiya-s-c-kodom-cherez-cgo.html` | 70 | ✅ Готово (70/70) |
| **53** | Системные вызовы и взаимодействие с ОС | `53. Системные вызовы и взаимодействие с ОС.md` | `053-sistemnye-vyzovy-i-vzaimodeystvie-s-os.html` | 75 | ✅ Готово (75/75) |
| **54** | Продвинутая рефлексия (reflect) | `54. Продвинутая рефлексия (reflect).md` | `054-prodvinutaya-refleksiya-reflect.html` | 114 | ✅ Готово (114/114) |
| **55** | Анализ AST и статический анализ кода | `55. Анализ AST и статический анализ кода.md` | `055-analiz-ast-i-staticheskiy-analiz-koda.html` | 85 | ✅ Готово (85/85) |
| **56** | Кодогенерация и шаблонизация | `56. Кодогенерация и шаблонизация.md` | `056-kodogeneratsiya-i-shablonizatsiya.html` | 77 | ✅ Готово (77/77) |
| **57** | Симметричное и асимметричное шифрование | `57. Симметричное и асимметричное шифрование.md` | `057-simmetrichnoe-i-asimmetrichnoe-shifrovanie.html` | 100 | ✅ Готово (100/100) |
| **58** | Хеширование паролей и криптографическая стойкость | `58. Хеширование паролей и криптографическая стойкость.md` | `058-kheshirovanie-paroley-i-kriptograficheskaya-stoykost.html` | 56 | ✅ Готово (56/56) |
| **59** | Токены аутентификации и авторизация | `59. Токены аутентификации и авторизация.md` | `059-tokeny-autentifikatsii-i-avtorizatsiya.html` | 66 | ✅ Готово (66/66) |
| **60** | Безопасность веб-приложений и защита API | `60. Безопасность веб-приложений и защита API.md` | `060-bezopasnost-veb-prilozheniy-i-zashchita-api.html` | 63 | ✅ Готово (63/63) |
| **61** | Документоориентированная база данных MongoDB | `61. Документоориентированная база данных MongoDB.md` | `061-dokumentoorientirovannaya-baza-dannykh-mongodb.html` | 113 | ✅ Готово (113/113) |
| **62** | Аналитическая СУБД ClickHouse | `62. Аналитическая СУБД ClickHouse.md` | `062-analiticheskaya-subd-clickhouse.html` | 71 | ✅ Готово (71/71) |
| **63** | Поисковые движки Elasticsearch и OpenSearch | `63. Поисковые движки Elasticsearch и OpenSearch.md` | `063-poiskovye-dvizhki-elasticsearch-i-opensearch.html` | 60 | ✅ Готово (60/60) |
| **64** | Логическая репликация и Change Data Capture | `64. Логическая репликация и Change Data Capture.md` | `064-logicheskaya-replikatsiya-i-change-data-capture.html` | 57 | ✅ Готово (57/57) |
| **65** | Вебхуки и платформы обратных вызовов | `65. Вебхуки и платформы обратных вызовов.md` | `065-vebkhuki-i-platformy-obratnykh-vyzovov.html` | 116 | ✅ Готово (116/116) |
| **66** | Server-Sent Events | `66. Server-Sent Events.md` | `066-server-sent-events.html` | 69 | ✅ Готово (69/69) |
| **67** | Альтернативные RPC-протоколы | `67. Альтернативные RPC-протоколы.md` | `067-alternativnye-rpc-protokoly.html` | 92 | ✅ Готово (92/92) |
| **68** | Паттерн Saga и компенсационные транзакции | `68. Паттерн Saga и компенсационные транзакции.md` | `068-pattern-saga-i-kompensatsionnye-tranzaktsii.html` | 104 | ✅ Готово (104/104) |
| **69** | Паттерны Outbox и Inbox для надежной доставки сообщений | `69. Паттерны Outbox и Inbox для надежной доставки сообщений.md` | `069-patterny-outbox-i-inbox-dlya-nadezhnoy-dostavki-soobshcheniy.html` | 72 | ✅ Готово (72/72) |
| **70** | Проектирование идемпотентных API | `70. Проектирование идемпотентных API.md` | `070-proektirovanie-idempotentnykh-api.html` | 74 | ✅ Готово (74/74) |
| **71** | Выборы лидера (Leader Election) в распределенных системах | `71. Выборы лидера (Leader Election) в распределенных системах.md` | `071-vybory-lidera-leader-election-v-raspredelennykh-sistemakh.html` | 90 | ✅ Готово (90/90) |
| **72** | Протокол консенсуса Raft | `72. Протокол консенсуса Raft.md` | `072-protokol-konsensusa-raft.html` | 83 | ✅ Готово (83/83) |
| **73** | Распределенные блокировки и Fencing Tokens | `73. Распределенные блокировки и Fencing Tokens.md` | `073-raspredelennye-blokirovki-i-fencing-tokens.html` | 68 | ✅ Готово (68/68) |
| **74** | Cache-friendly структуры данных и выравнивание памяти | `74. Cache-friendly структуры данных и выравнивание памяти.md` | `074-cache-friendly-struktury-dannykh-i-vyravnivanie-pamyati.html` | 99 | ✅ Готово (99/99) |
| **75** | Lock-free структуры данных | `75. Lock-free структуры данных.md` | `075-lock-free-struktury-dannykh.html` | 75 | ✅ Готово (75/75) |
| **76** | Ассемблер Go (Plan 9 Assembly) и SIMD | `76. Ассемблер Go (Plan 9 Assembly) и SIMD.md` | `076-assembler-go-plan-9-assembly-i-simd.html` | 35 | ✅ Готово (35/35) |
| **77** | Высокопроизводительные сетевые фреймворки (gnet, evio) | `77. Высокопроизводительные сетевые фреймворки (gnet, evio).md` | `077-vysokoproizvoditelnye-setevye-freymvorki-gnet-evio.html` | 32 | ✅ Готово (32/32) |
| **78** | Облачные хранилища, Envelope Encryption и KMS | `78. Облачные хранилища, Envelope Encryption и KMS.md` | `078-oblachnye-khranilishcha-envelope-encryption-i-kms.html` | 95 | ✅ Готово (95/95) |
| **79** | Интеграция с Service Mesh (Istio, Linkerd) и mTLS | `79. Интеграция с Service Mesh (Istio, Linkerd) и mTLS.md` | `079-integratsiya-s-service-mesh-istio-linkerd-i-mtls.html` | 80 | ✅ Готово (80/80) |
| **80** | Контекст трассировки (W3C Trace Context, B3) и gRPC Keepalive | `80. Контекст трассировки (W3C Trace Context, B3) и gRPC Keepalive.md` | `080-kontekst-trassirovki-w3c-trace-context-b3-i-grpc-keepalive.html` | 76 | ✅ Готово (76/76) |
| **81** | Безопасность цепочки поставок (Supply Chain Security) и SBOM | `81. Безопасность цепочки поставок (Supply Chain Security) и SBOM.md` | `081-bezopasnost-tsepochki-postavok-supply-chain-security-i-sbom.html` | 136 | ✅ Готово (136/136) |
| **82** | Защита сетевых сокетов и противодействие DoS-атакам | `82. Защита сетевых сокетов и противодействие DoS-атакам.md` | `082-zashchita-setevykh-soketov-i-protivodeystvie-dos-atakam.html` | 55 | ✅ Готово (55/55) |
| **83** | Системная изоляция, Seccomp и Linux Capabilities | `83. Системная изоляция, Seccomp и Linux Capabilities.md` | `083-sistemnaya-izolyatsiya-seccomp-i-linux-capabilities.html` | 28 | ✅ Готово (28/28) |
| **84** | CQRS и Event Sourcing на Go | `84. CQRS и Event Sourcing на Go.md` | `084-cqrs-i-event-sourcing-na-go.html` | 45 | ✅ Готово (45/45) |
| **85** | Многоуровневое кэширование (L1-L2) и распределенная когерентность | `85. Многоуровневое кэширование (L1-L2) и распределенная когерентность.md` | `085-mnogourovnevoe-keshirovanie-l1-l2-i-raspredelennaya-kogerentnost.html` | 30 | ✅ Готово (30/30) |
| **86** | Масштабируемые распределенные планировщики и очереди задач | `86. Масштабируемые распределенные планировщики и очереди задач.md` | `086-masshtabiruemye-raspredelennye-planirovshchiki-i-ocheredi-zadach.html` | 30 | ✅ Готово (30/30) |
| **87** | Оркестрация распределенных процессов (Durable Execution) на Temporal.io | `87. Оркестрация распределенных процессов (Durable Execution) на Temporal.io.md` | `087-orkestratsiya-raspredelennykh-protsessov-durable-execution-na-temporal-io.html` | 50 | ✅ Готово (50/50) |
| **88** | Потоковая обработка данных в реальном времени (Stream Processing) | `88. Потоковая обработка данных в реальном времени (Stream Processing).md` | `088-potokovaya-obrabotka-dannykh-v-realnom-vremeni-stream-processing.html` | 30 | ✅ Готово (30/30) |
| **89** | Хаос-инженерия и нагрузочное тестирование на Go | `89. Хаос-инженерия и нагрузочное тестирование на Go.md` | `089-khaos-inzheneriya-i-nagruzochnoe-testirovanie-na-go.html` | 30 | ✅ Готово (30/30) |
| **90** | Контракт-ориентированные API-шлюзы: gRPC-Gateway, gRPC-Web и OpenAPI | `90. Контракт-ориентированные API-шлюзы. gRPC-Gateway, gRPC-Web и OpenAPI.md` | `090-kontrakt-orientirovannye-api-shlyuzy-grpc-gateway-grpc-web-i-openapi.html` | 30 | ✅ Готово (30/30) |
| **91** | Разработка собственных Kubernetes Operators и CRD на Go | `91. Разработка собственных Kubernetes Operators и CRD на Go.md` | `091-razrabotka-sobstvennykh-kubernetes-operators-i-crd-na-go.html` | 45 | ✅ Готово (45/45) |
| **92** | Расширяемость систем: Plugins, IPC и WebAssembly (Wazero) | `92. Расширяемость систем. Plugins, IPC и WebAssembly (Wazero).md` | `092-rasshiryaemost-sistem-plugins-ipc-i-webassembly-wazero.html` | 30 | ✅ Готово (30/30) |
| **93** | Высокопроизводительные API Gateway и Reverse Proxy на чистом Go | `93. Высокопроизводительные API Gateway и Reverse Proxy на чистом Go.md` | `093-vysokoproizvoditelnye-api-gateway-i-reverse-proxy-na-chistom-go.html` | 30 | ✅ Готово (30/30) |
| **94** | Enterprise Release Engineering: Feature Flags, динамический конфиг и Canary Routing | `94. Enterprise Release Engineering. Feature Flags, динамический конфиг и Canary Routing.md` | `094-enterprise-release-engineering-feature-flags-dinamicheskiy-konfig-i-canary-routing.html` | 30 | ✅ Готово (30/30) |
| **95** | Распределенная координация и хранилище метаданных etcd v3 | `95. Распределенная координация и хранилище метаданных etcd v3.md` | `095-raspredelennaya-koordinatsiya-i-khranilishche-metadannykh-etcd-v3.html` | 30 | ✅ Готово (30/30) |
| **96** | Zero-Downtime миграции баз данных и паттерн Expand-Contract на Go | `96. Zero-Downtime миграции баз данных и паттерн Expand-Contract на Go.md` | `096-zero-downtime-migratsii-baz-dannykh-i-pattern-expand-contract-na-go.html` | 30 | ✅ Готово (30/30) |
| **97** | Time-Series СУБД, сжатие Gorilla и IoT-телеметрия на Go | `97. Time-Series СУБД, сжатие Gorilla и IoT-телеметрия на Go.md` | `097-time-series-subd-szhatie-gorilla-i-iot-telemetriya-na-go.html` | 30 | ✅ Готово (30/30) |
| **98** | Архитектурный контроль: Разработка корпоративных линтеров для golangci-lint | `98. Архитектурный контроль. Разработка корпоративных линтеров для golangci-lint.md` | `098-arkhitekturnyy-kontrol-razrabotka-korporativnykh-linterov-dlya-golangci-lint.html` | 30 | ✅ Готово (30/30) |
| **99** | Интеграция с ИИ, LLM-оркестрация и векторный поиск на Go | `99. Интеграция с ИИ, LLM-оркестрация и векторный поиск на Go.md` | `099-integratsiya-s-ii-llm-orkestratsiya-i-vektornyy-poisk-na-go.html` | 45 | ✅ Готово (45/45) |
| **100** | Архитектурный Capstone: Проектирование и сквозной запуск отказоустойчивой HighLoad-платформы | `100. Архитектурный Capstone. Проектирование и сквозной запуск отказоустойчивой HighLoad-платформы.md` | `100-arkhitekturnyy-capstone-proektirovanie-i-skvoznoy-zapusk-otkazoustoychivoy-highload-platformy.html` | 50 | ✅ Готово (50/50) |

---

## 🏗 3. Архитектура проекта и генератора (`builder/`)

Все HTML-страницы собираются модульным скриптом на Python:

```text
/home/ut/work/go-workout/
├── dist/                             # Скомпилированный статический веб-сайт курса
│   ├── index.html                    # Главный портал курса и Learning Paths
│   ├── 001-pakety-i-moduli.html      # Глава 01 (Пакеты и модули — 91 упр.)
│   ├── 002-kompilyatsiya-sborka-i-zapusk.html # Глава 02 (25 упр.)
│   ├── ...
│   ├── 100-arkhitekturnyy-capstone-proektirovanie-i-skvoznoy-zapusk-otkazoustoychivoy-highload-platformy.html # Глава 100 (Capstone — 50 упр.)
│   ├── favicon.ico                   # Фавикон ICO
│   └── favicon.svg                   # Фавикон SVG
├── sources/                          # Исходные задачники глав (Markdown)
│   ├── 1. Пакеты и модули.md        # Исходный задачник главы 1
│   ├── ...
│   └── 100. Архитектурный Capstone...md
├── builder/                          # Ядро генерации и данные глав
│   ├── chapters.py                   # Динамическое сканирование sources/*.md
│   ├── template.py                   # HTML_HEAD, HTML_FOOTER, стили, скрипты, Prism.js CDN
│   ├── build_all.py                  # Главный сборочный скрипт в dist/
│   ├── audit_all.py                  # Валидатор синтаксиса Go (gofmt -e), HTML-якорей в dist/
│   ├── section[1-6].py               # Данные упражнений 1-й главы
│   ├── chapterX_data.json            # Каноничный JSON с упражнениями главы X (X = 2..100)
│   └── gen_chX_pY.py                 # Генераторы частей глав
├── .github/
│   └── workflows/
│       └── pages.yml                 # Деплой dist/ на GitHub Pages
├── favicon.ico                       # Favicon (корень)
├── favicon.svg                       # Favicon SVG (корень)
├── AGENTS.md                         # Данный файл инструкций
└── README.md                         # Документация проекта
```

### 🧹 Правило чистоты репозитория:
1. **Никаких промежуточных микро-скриптов в `builder/`:** Скрипты генерации промежуточных партий (`make_ch*.py`, `_batch*.json`, одноразовые патчеры) **категорически запрещено** сохранять в папке `builder/` и коммитить в Git. Все вспомогательные/черновые утилиты обязаны создаваться в scratch-директории агента (`brain/<id>/scratch/`).
2. В `builder/` хранятся **только**:
   - Ядро генератора: `chapters.py`, `template.py`, `build_all.py`, `audit_all.py`.
   - Исходные данные главы 1: `section1.py` .. `section6.py`.
   - Сгенерированные каноничные JSON: `chapterX_data.json`.
   - Модули генерации частей: `gen_chX_pY.py`.

---

## ⚡ 4. Скоростной конвейер генерации (Fast-Track Pipeline)

> **⚠️ КРИТИЧЕСКИ ВАЖНО ДЛЯ ПРОИЗВОДИТЕЛЬНОСТИ ИИ:**
> Во избежание зависаний среды выполнения (30-секундный таймаут команд bash) и разрастания контекста диалога, генерация обязана выполняться **строго за 5 быстрых шагов** без создания десятков микро-батчей (`_batch_N`)!

### Шаг 1: Анализ исходного файла
1. Прочитать файл `N. <Тема>.md`.
2. Подсчитать общее число упражнений $K$.
3. Разбить главу на **2 или 3 крупные части** (например, по 30–50 упражнений в каждой):
   - Часть 1: Упражнения $1 \dots M$
   - Часть 2: Упражнения $M+1 \dots K$ (для очень больших глав от 100 упр. допустима Часть 3).

### Шаг 2: Генерация частей данных (`gen_chN_p1.py` и `gen_chN_p2.py`)
Создавать файлы напрямую на Python с raw-строками `r"""..."""`, чтобы исключить любые проблемы с экранированием кавычек, обратных слэшей и переводов строк:

```python
# builder/gen_chN_p1.py
exercises = [
    {
        "num": 1,
        "title": "Краткий емкий заголовок темы",
        "task": "Оригинальный текст задачи из markdown-файла",
        "theory": r"""Теоретический фундамент: концепция, сравнение с C++/Python, стандарты Go 1.22+""",
        "step_by_step": r"""Пошаговый ход мысли инженера, порядок действий в терминале и IDE""",
        "code_blocks": [
            {
                "filename": "main.go",
                "lang": "go",
                "code": r"""package main

import "fmt"

func main() {
	fmt.Println("Полный рабочий компилируемый код")
}""",
                "note": "Пояснение к коду"
            },
            {
                "filename": "Терминал",
                "lang": "bash",
                "code": r"""go run main.go
# Полный рабочий компилируемый код"""
            }
        ],
        "under_the_hood": r"""Низкоуровневая механика: компилятор (AST/SSA), рантайм (GMP, GC), память""",
        "pitfalls": r"""Частые ошибки новичков, ловушки, утечки памяти, гонки данных""",
        "bigtech_interview": r"""**Вопрос с собеседования:** «...»
**Ответ:** ..."""
    },
    # ... следующие упражнения части 1
]
```

> **⚡ ВАЖНОЕ ПРАВИЛО ЗАКРЫТИЯ КАВЫЧЕК В RAW-СТРОКАХ:**
> Если строка или блок кода оканчивается на символ двойной кавычки `"`, закрытие `r"""...""""` превращается в 4 кавычки подряд и приводит к фатальной ошибке Python `SyntaxError: unterminated triple-quoted string literal`. Всегда добавляйте перевод строки `\n` или пробел перед закрывающими кавычками `r"""..."\n"""` или экранируйте: `\""""`.

### Шаг 3: Слияние в `chapterN_data.json` и проверка `gofmt -e`
Выполнить компактный скрипт слияния и мгновенной проверки синтаксиса всего Go-кода:

```python
import sys, json, subprocess, tempfile, os
sys.path.insert(0, 'builder')
import gen_chN_p1, gen_chN_p2

all_ex = gen_chN_p1.exercises + gen_chN_p2.exercises
assert [e['num'] for e in all_ex] == list(range(1, len(all_ex) + 1)), "Ошибка нумерации!"

# Валидация gofmt -e:
for ex in all_ex:
    for block in ex.get('code_blocks', []):
        if block.get('lang') == 'go':
            with tempfile.NamedTemporaryFile('w', suffix='.go', delete=False) as tf:
                tf.write(block['code'])
                p = tf.name
            res = subprocess.run(['gofmt', '-e', p], capture_output=True, text=True)
            os.remove(p)
            if res.returncode != 0:
                raise ValueError(f"gofmt error in Ex {ex['num']}: {res.stderr}")

with open('builder/chapterN_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_ex, f, ensure_ascii=False, indent=2)
print(f"✅ chapterN_data.json готов ({len(all_ex)} упр.)")
```

### Шаг 4: Обновление `builder/build_all.py` и компиляция всех HTML страниц
1. Загрузить `chapterN_data.json` в `build_all.py`.
2. Добавить `N: ('NNN-slug.html', 'K/K')` в `status_map` внутри `build_sidebar()`.
3. Обновить ссылку в футере главы $N-1$ с `(Скоро)` на активную ссылку `Глава N Название →` (стиль фона `#00ADD8`, цвет текста `#000`, жирный шрифт, **без скобок в названии**).
4. Создать функцию `build_chapterN_html(chapters)`:
   - **Hero-блок:** `hero-tag`, `hero-title`, `hero-desc` (лаконичное введение на полную ширину, **без блока hero-stats**).
   - **Секционные группы:** 3–4 логических раздела с разделителями `section-separator`.
   - **Карточки упражнений:** вызов `build_exercise_card(ex)`.
   - **Футер:** блок поздравления с кнопкой возврата на главу $N-1$ (`← Глава N-1 Название`) и ссылкой на следующую главу $N+1$ (`Глава N+1 Название (Скоро) →`). **Никаких круглых скобок вокруг названий глав в ссылках!**
5. Добавить `('NNN-slug.html', build_chapterN_html)` в список `pages` в `main()`.
6. Запустить `python3 builder/build_all.py` — это пересоберет **все страницы** (`index.html` и все `NNN-slug.html`), обеспечив 100% синхронизацию сайдбаров и ссылок.

### Шаг 5: Финальный технический аудит (`builder/audit_all.py`)
1. Добавить `chapterN_data.json` в `builder/audit_all.py`.
2. Добавить `('NNN-slug.html', N, len(all_chN))` в список `html_files`.
3. Запустить `python3 builder/audit_all.py` и убедиться в выводе:
   ```text
   ✅ ИДЕАЛЬНО: Все M упражнений в N главах успешно прошли синтаксический, структурный и HTML-аудит!
   ```

### Шаг 6: Фиксация в Git
- При последовательной генерации глав коммитить строго по одной главе с сообщением `Module N` (без кавычек внутри строки, например `git commit -m "Module 48"`).
- Перед коммитом удалять любые временные файлы и очищать кэш Python (`rm -rf builder/__pycache__`).

---

## 🎨 5. Стандарты дизайна, UI и верстки

* **Цветовая палитра (Dark Theme):**
  - Фон страницы: `#090d16` (глубокий темный)
  - Сайдбар и панели: `#0f172a`
  - Карточки упражнений: `#131d33` (бордер `#1e293b`, hover `#334155`)
  - Акцентный цвет Go: `#00ADD8` (Go Cyan) / `#38bdf8`
  - Статус "Готово": `rgba(16, 185, 129, 0.15)` (`#34d399`)
* **Типографика:**
  - Основной текст: шрифт **Roboto** (400, 500, 700)
  - Код и команды терминала: шрифт **Cascadia Code** / **Roboto Mono**
* **Подсветка синтаксиса:** Prism.js Tomorrow Dark (`prism-go`, `prism-bash`, `prism-json`, `prism-makefile`, `prism-yaml`).
* **Интерактивные элементы:**
  - Кнопка «Копировать» у каждого блока кода (с переключением на «Скопировано!» на 1.8 сек).
  - Полоса прогресса чтения в самом верху окна (`#progress-bar`).
  - Плавающая кнопка возврата наверх (`#back-to-top`).
  - Живой поиск по темам и упражнениям (`#search-input`).
* **Структура упражнения (обязательные поля):**
  1. `num` (int) — порядковый номер упражнения (1..K).
  2. `title` (str) — краткий ёмкий заголовок темы.
  3. `task` (str) — точный оригинальный текст задачи из исходного `.md`.
  4. `theory` (str) — глубокая теория, рантайм, модель памяти, сравнение со смежными стеками.
  5. `step_by_step` (str) — ход мысли разработчика, пошаговые команды и действия в IDE.
  6. `code_blocks` (list) — компилируемый Go-код (`lang: go`) и вывод терминала (`lang: bash`, `yaml`, `dockerfile`, `json`).
  7. `under_the_hood` (str) — низкоуровневая механика (AST, SSA, GMP, GC, аллокатор, сокеты, syscalls).
  8. `pitfalls` (str) — ловушки, частые ошибки, гонки данных, утечки горутин/памяти.
  9. `bigtech_interview` (str) — вопрос с реального собеседования в BigTech и развернутый ответ.

---

## ⚠️ 6. Свод правил и защита от ошибок (Чего НЕЛЬЗЯ делать)

| ❌ Как НЕЛЬЗЯ делать | ✅ Как НАДО делать | Причина / Обоснование |
| :--- | :--- | :--- |
| **Дробить главу на 10+ мелких `_batch_N` скриптов** | Делить главу строго на **2–3 крупные части** (`p1.py`, `p2.py`) | Исключает перегрузку контекста и сокращает цикл генерации с 35 до 5 шагов. |
| **Оставлять временные скрипты генерации в `builder/`** | Писать вспомогательные скрипты в `scratch/` агента | Сохраняет репозиторий в чистоте, исключает попадание мусорных файлов в Git. |
| **Писать огромные Bash Heredoc `cat << 'EOF'` без raw-строк** | Писать Python-файлы напрямую с `r"""..."""` | Предотвращает 30-секундный таймаут и ошибки синтаксиса `unterminated string literal`. |
| **Заканчивать raw-строку кавычкой `r"""..." """` без переноса или экранирования** | Писать `r"""...\"\n"""` или отступать пробелом/переводом строки | Четыре двойные кавычки `""""` ломают синтаксис Python при парсинге модулей. |
| **Добавлять устаревший блок `hero-stats` в Hero-секцию** | Использовать только чистый Hero: `hero-tag`, `hero-title`, `hero-desc` | Блок `hero-stats` устарел, ломает единообразие верстки и адаптивность страниц. |
| **Писать круглые скобки вокруг названия главы в футере** | Писать строго `← Глава N Название` и `Глава N+1 Название (Скоро) →` | Названия в скобках `(Название)` выглядят неряшливо и нарушают дизайн-систему проекта. |
| **Добавлять шевроны `▼`/`▶` в заголовок активного модуля** | Заголовок модуля в сайдбаре должен быть **чистым текстом** `<span><strong>N. Название</strong></span>` | Любые иконки перед текстом смещают выравнивание, и заголовок визуально прыгает по сравнению с другими главами. |
| **Скроллить страницу при клике на заголовок в сайдбаре** | Использовать `e.preventDefault()` и `e.stopPropagation()` в JS, переключая только CSS-класс `.collapsed` у `.sub-exercises-list`. | Пользователь кликает по модулю в сайдбаре только для управления меню, контент справа не должен дергаться. |
| **Оставлять подсписок свернутым при поиске** | При вводе текста в `#search-input` JS обязан автоматически снять класс `collapsed`. | Иначе отфильтрованные поиском упражнения останутся невидимыми внутри скрытого аккордеона. |
| **Писать псевдокод вида `// ... здесь логика`** | Писать **полный, самодостаточный, рабочий код** с импортами и обработкой ошибок. | Учебник ориентирован на практику; разработчик должен иметь возможность скопировать код и сразу запустить его в терминале. |
| **Игнорировать `if err != nil`** | Всегда явно обрабатывать ошибки через `fmt.Errorf`, логирование или возврат. | В Go и на собеседованиях в BigTech пропуск проверки ошибок считается критическим антипаттерном. |
| **Создавать канал сигналов без буфера `make(chan os.Signal)`** | Всегда создавать `make(chan os.Signal, 1)`. | Небуферизированный канал может потерять сигнал ОС (`SIGINT`/`SIGTERM`), если горутина не успела встать на чтение. |
| **Копировать `sync.Mutex` по значению** | Всегда использовать Pointer Receiver `(s *SafeStruct)` или указатель `*sync.Mutex`. | Копирование структуры с мьютексом копирует его внутреннее битовое состояние, вызывая Data Race и дедлоки (`go vet copylocks`). |
| **Возвращать типизированный `nil` в интерфейсе `error`** | Всегда явно возвращать `return nil`, если ошибки нет. | `(*MyError)(nil)` внутри интерфейса `error` имеет ненулевой тип `itab`, из-за чего проверка `if err != nil` ошибочно возвращает `true`. |
| **Генерировать только HTML новой главы без пересборки старых** | Запускать `build_all.py` для пересборки **всех страниц** (`index.html` и всех глав курса). | Обеспечивает единую синхронизацию сайдбара, счетчиков и ссылок навигации во всем учебнике. |

---

## 🚀 7. Быстрый шаблон промпта для ИИ

Если вы передаете задачу следующему агенту или начинаете новый диалог:

```text
Сгенерируй главу N учебника по файлу "N. <Название>.md" строго по Fast-Track пайплайну из AGENTS.md.
1. Прочитай файл "N. <Название>.md" и извлеки все упражнения без исключения (номера 1..K).
2. Создай builder/gen_chN_p1.py и builder/gen_chN_p2.py со всеми обязательными блоками для каждого упражнения через r"""...""".
3. Слей части в builder/chapterN_data.json и выполни валидацию синтаксиса через gofmt -e.
4. Обнови builder/build_all.py (добавь chapterN_data.json, build_chapterN_html, обнови сайдбар и футеры) и пересобери все страницы.
5. Обнови builder/audit_all.py и запусти финальный аудит всех глав (синтаксис Go, якоря #ex-*, структура).
6. Закоммить результат с сообщением "Module N".
```

---
*Документ актуален для Go 1.22+ и поддерживается в рамках проекта Go Workout Exercises.*
