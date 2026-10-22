# Глава 1 «Пакеты и модули» — фактчек по первоисточникам и запуском кода

Дата: 2026-10-22. Вход: `fact-checks/1/1-opus-judge.md` (бриф, находки `J-01…J-62`). Файла `1-opus-blind-spot.md` нет. Все цитаты сверены с текущими файлами `sources/001. Пакеты и модули/`.

## 1. Сводка

| Статус | Находки брифа (J) | Новые (F) |
|---|---|---|
| VERIFIED | 57 | — |
| INCORRECT | 0 | 7 (F-02, F-03, F-06, F-07, F-08, F-09, F-11) |
| PARTIALLY CORRECT | 2 (J-25, J-58) | 1 (F-01) |
| OUTDATED | 0 | 2 (F-04, F-05) |
| CONTEXT-DEPENDENT | 2 (J-38, J-49) | 1 (F-10) |
| OPINION / NOT A FACT CLAIM | 1 (J-45) | — |
| NOT CHECKED | 0 целиком (отдельные подпункты — в § 3) | — |

Статус у `J-…` означает: подтверждена ли **находка брифа** (VERIFIED — находка верна, текст книги нужно править). Статус у `F-…` относится к **утверждению книги**.

- `go version go1.27.1 linux/amd64`, Linux 7.2.11 (Fedora 44), x86-64 (i9-12900K). `GOPROXY=https://proxy.golang.org,direct`, сеть доступна.
- Код всех 91 задачи извлечён из «## Код решения» в `/tmp/gw1/gw-1-KKK/` (файлы — по подписям блоков). Для каждой: `go mod init` (если `go.mod` не дан), `go mod tidy`, `gofmt -l`, `go vet ./...`, `go build ./...`, `go run`/`go test`. Конкурентный код (026, 076, 077, 084) запущен с `-race`, детерминированные программы — по 3 раза (хэши вывода совпали). Эксперименты — в отдельных каталогах `/tmp/gw1/x*`.
- Итог прогона: собираются и запускаются все задачи с самодостаточным кодом. Не собираются: 009, 048, 052, 053, 056 (импорт пакетов из других задач — J-28), 051 (API tablewriter v1 — J-52); `go build ./...` падает в 060, 084, 086 (`package main` без `main` — J-24). Вывод совпал с книгой в 001, 003 (кроме позиции ошибки), 007, 010, 012–016, 020–023, 026, 029, 030, 032, 033, 042, 050, 058, 075, 076, 082, 083, 088, 090 (кроме хэша — J-21), 091 (кроме HTTP — J-22).

**Две поправки к самому брифу** (подробно — F-04, F-11):
1. В § 4 (отсев A-81(в)) и § 5.7 бриф цитирует правило `exclude` «replaced by the next higher version». Это поведение **до Go 1.16**. С Go 1.16 требование на исключённую версию просто игнорируется; `go build` в таком модуле падает, а `go mod tidy` берёт **последнюю** версию, а не «следующую».
2. В К-1 для 017 бриф ждёт `undefined: …`. Фактически gc печатает `name isValidRadius not exported by package shapes`: формулировка зависит от того, попал ли символ в export data.

---

## 2. Находки

Пути — от `sources/`. Сокращение: `001/01…06` = `001. Пакеты и модули/<раздел>`:
`01. Введение, Окружение, Компиляция и Базовые Пакеты`, `02. Внешние Зависимости, Инкапсуляция, Init()`, `03. SemVer, Локальный Replace, Кросс-компиляция и UUID`, `04. CLI на Cobra, Структурированные Логи, Дженерики`, `05. Анатомия go.mod, Безопасность govulncheck`, `06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor`.

### J-01 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/060. Тестовые зависимости github.com_stretchr_testify.md`, «## Условие»: «Убедись, что она попадает в `go.mod` с директивой `// indirect`».
- **Вердикт:** testify, импортированный из `_test.go` главного модуля, — прямая зависимость, без `// indirect`. Условие требует невозможного.
- **Доказательство:** `/tmp/gw1/gw-1-060`, `go mod tidy` → `require github.com/stretchr/testify v1.12.1` (без комментария), `require go.yaml.in/yaml/v3 v3.0.5 // indirect`. Go Modules Reference, «require directive»: «An `// indirect` comment indicates that no package from the required module is directly imported by any package in the main module»; при `go 1.17+` учитываются импорты «by a package or test in the main module».
- **Предлагаемая правка:** «Убедись, что `go mod tidy` записал её в `go.mod` как прямую зависимость (без `// indirect`): тесты — часть главного модуля. Пометку `// indirect` получат только её собственные зависимости (например, `gopkg.in/yaml.v3` / `go.yaml.in/yaml/v3`)».

### J-02 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/009. Вложенные подпакеты (utils_strings).md`: «Это гарантирует корректную работу с любыми Unicode-символами и эмодзи» (строка 84); вывод `# Развернутая: !кичтобазрар-oG ,тевирП` (строка 77).
- **Вердикт:** (а) руна — кодовая точка, не графема; разворот по рунам ломает комбинирующие знаки, флаги, модификаторы тона и ZWJ-последовательности. (б) Вывод в книге с опечаткой.
- **Доказательство:** запуск `Reverse` из задачи (`/tmp/gw1/x009`): `"éa"` (e + U+0301) → `"áe"`; `"🇷🇺"` → `"🇺🇷"`; `"👍🏽"` → `"🏽👍"`; `"👨‍👩‍👧"` → `"👧‍👩‍👨"`. Задача, собранная в модуле `hello_mod` (с `utils` из 007): `Развернутая: !кичтобарзар-oG ,тевирП`. Источник: блог Go «Strings, bytes, runes and characters in Go»; Unicode UAX #29.
- **Предлагаемая правка:** вывод — `# Развернутая: !кичтобарзар-oG ,тевирП`. «Под капотом»: «Разворот по рунам корректен для символов из одной кодовой точки (кириллица, большинство иероглифов). Символы из нескольких кодовых точек — буквы с комбинирующими знаками, флаги, эмодзи с модификатором тона или ZWJ — он ломает; для них нужна сегментация на графемы (UAX #29, например `github.com/rivo/uniseg`)». H1: «…и разворот UTF-8 строк по рунам». См. также F-01.

### J-03 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/062. Полный справочник директив go.mod.md`: «поддерживаются **ровно 5 ключевых директив**»; шаг 3 «Запускаем `go build .` — компилятор проигнорирует версию v1.5.0 и выберет следующую подходящую версию (v1.6.0)»; «алгоритм компилятора отфильтровывает…»; «уязвимость 0-day (CVE)».
- **Вердикт:** (а) директив 10: `module`, `go`, `toolchain` (Go 1.21), `godebug` (Go 1.23), `require`, `tool` (Go 1.24), `ignore` (Go 1.25), `exclude`, `replace`, `retract` (Go 1.16). (б) В примере `require uuid v1.6.0`, поэтому `exclude v1.5.0` ничего не меняет. (в) MVS и `exclude` выполняет команда `go`, не компилятор. (г) «0-day» и «CVE» — разные понятия. Шаг 3 неверен ещё и по механике — см. F-04.
- **Доказательство:** `go1.27.1 src/cmd/vendor/golang.org/x/mod/modfile/rule.go`, строки 380–544: ветки `case "go"`, `"toolchain"`, `"module"`, `"godebug"`, `"require", "exclude"`, `"replace"`, `"retract"`, `"tool"`, `"ignore"`. Go Modules Reference: разделы `toolchain`, `godebug`, `tool` («Since Go 1.24…»), `ignore`, `retract` («added in Go 1.16»). Release notes: Go 1.21 («The new `toolchain` directive…»), Go 1.23 («The new `godebug` directive in `go.mod` and `go.work`…»), Go 1.25 («The new `go.mod` `ignore` directive…»). Опыт (`/tmp/gw1/x062`): с `require … v1.6.0` + `exclude … v1.5.0` → `go list -m` = `v1.6.0`.
- **Предлагаемая правка:** «В `go.mod` десять директив: `module`, `go`, `toolchain` (1.21+), `godebug` (1.23+), `require`, `tool` (1.24+), `ignore` (1.25+), `exclude`, `replace`, `retract` (1.16+). Здесь разбираем пять основных». Пример: `require github.com/google/uuid v1.5.0` + `exclude github.com/google/uuid v1.5.0`, шаги — по F-04. «Под капотом»: «…команда `go` (`cmd/go`) при построении графа…». Ответ: «…обнаружена критическая уязвимость (CVE) или утечка памяти…».

### J-04 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/049. Автоматическая нормализация зависимостей через go.md`, «## Условие»: «оставьте её в импортах. Выполните команду `go mod tidy`. Посмотрите, как изменились файлы»; «## Теория», п. 2; п. 1: `imported and not used: "github.com/google/uuid"`.
- **Вердикт:** пока строка импорта есть, `tidy` сохраняет `require`. Текст ошибки в теории устарел.
- **Доказательство:** `/tmp/gw1/x049`: после удаления вызова `uuid` при оставленном импорте `go mod tidy` → rc=0, `go.mod unchanged`; `go build` → `./main.go:6:2: "github.com/google/uuid" imported and not used`. `go help mod tidy`: tidy «removes unused modules that don't provide any relevant packages» — решают импорты, а не вызовы.
- **Предлагаемая правка:** условие: «Удалите использование `uuid` и **строку импорта**, затем выполните `go mod tidy`». Теория п. 1: `"github.com/google/uuid" imported and not used`. П. 2: «`go mod tidy` смотрит на объявления `import`, а не на вызовы: пока строка импорта есть хотя бы в одном файле, `require` останется (а сборка упадёт с ошибкой выше). Удалите импорт — и `tidy` уберёт `require` и строки `go.sum`».

### J-05 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/040. Разница между go build, go install, go run.md`: «Создай модуль `mymod` с пакетом `api`. Сделай `go build` для получения исполняемого файла»; «компилятор кэширует скомпилированные объектные файлы `.a` в кэш сборки `GOCACHE`»; `go install github.com/golang/mock/mockgen@v1.6.0`.
- **Вердикт:** (а) исполняемый файл получится только из `package main`. (б) «`.a`» — неточно: в `GOCACHE` лежат объекты по content-ID, готовых `.a` стандартной библиотеки нет с Go 1.20. (в) `github.com/golang/mock` — в архиве (бриф; страница не открывалась, см. § 3).
- **Доказательство:** `/tmp/gw1/x040.Q2Ib` (`package api`): `go build .` → rc=0, файлов не появилось; `go build -o mymod .` → `mymod: current ar archive` (архив, не исполняемый файл); `GOBIN=… go install .` → rc=0, каталог `bin` не создан. `ls $(go env GOROOT)/pkg` → только `include`, `tool`. Release notes Go 1.20: «The directory `$GOROOT/pkg` no longer stores pre-compiled package archives for the standard library…».
- **Предлагаемая правка:** условие: «Создай модуль `mymod` с `package main` и библиотечным пакетом `api`…». «Под капотом»: «Для библиотечного пакета `go build`/`go install` только компилируют его и кладут результат в кэш сборки (`GOCACHE`); исполняемый файл создаётся только для `package main`. (С Go 1.20 и стандартная библиотека не поставляется готовыми `.a`, а собирается в тот же кэш.)». Ответ: `go install go.uber.org/mock/mockgen@latest` (сопровождаемый форк).

### J-06 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/083. Продвинутый POSIX-совместимый парсинг флагов.md`: «Стандартный пакет `flag` не поддерживает: Разделение на короткие (`-p`) и длинные (`--port`) флаги»; ответ «не поддерживает синтаксис `--flag` и `-f`»; «является 100% совместимой POSIX/GNU-заменой».
- **Вердикт:** `flag` принимает и `-port`, и `--port`. «100% совместимой» — ложно: pflag не понимает `-port` (одно тире, длинное имя), который понимает `flag`.
- **Доказательство:** `go doc flag`: «One or two dashes may be used; they are equivalent». Запуск (`/tmp/gw1/x083flag`): `--port=9000` → 9000, `--port 9001` → 9001, `-port 9002` → 9002; `./app a --port 1` → флаг не разобран (остановка на позиционном аргументе). pflag v1.0.10, код 083: `./app -port 9000` → `invalid argument "ort" for "-p, --port" flag`, rc=2.
- **Предлагаемая правка:** теория: «Стандартный `flag` принимает `-port` и `--port` как одно и то же, но не умеет: короткий алиас того же флага (`-p` ↔ `--port`), склейку булевых флагов (`-vd`), разбор флагов после позиционных аргументов». «`pflag` — почти совместимая (drop-in) замена в стиле POSIX/GNU; отличие: длинные флаги пишутся только через `--` (`-port` pflag разберёт как `-p ort`)». Ответ: «…стандартный `flag` не поддерживает короткие алиасы и склейку `-abc`, принятые в Unix…».

### J-07 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/026. Пакет config, функция init().md`: «Рантайм выполняет их строго в одном основном потоке ОС до запуска планировщика»; ответ: «горутина не начнет реально исполняться, пока текущий поток инициализации не передаст управление или не завершится инициализация пакета».
- **Вердикт:** планировщик уже работает; горутина из `init()` выполняется, как только `init` блокируется, или параллельно. Верно только то, что основная горутина на время `init` закреплена за потоком `m0`.
- **Доказательство:** `go1.27.1 src/runtime/proc.go`, `func main()`: `newm(sysmon, …)` и `lockOSThread()` («Lock the main goroutine onto this, the main OS thread, during initialization») стоят **до** `doInit(runtime_inittasks)`. Запуск (`/tmp/gw1/x026`): `init` печатает, запускает `go fmt.Println(...)`, спит 100 мс → при `GOMAXPROCS=1` и `=2` порядок `init a.go start` → `goroutine from init runs` → `init a.go done`. Спецификация, «Package initialization»: «An init function may launch other goroutines, which can run concurrently with the initialization code. However, initialization always sequences the init functions».
- **Предлагаемая правка:** «Под капотом»: «…`runtime.main` уже после запуска планировщика вызывает `doInit` для всех пакетов в одной (главной) горутине; на время инициализации она закреплена за основным потоком ОС». Ответ: «Да. Горутина, запущенная в `init()`, может выполняться параллельно с инициализацией (или как только `init()` заблокируется), но инициализация пакетов не ждёт её. Синхронизируйтесь явно. Паника в `init()` завершает программу до `main()`».

### J-08 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/039. Углубленный статический анализ проекта через go.md`: «2. Забытые `time.Sleep` в бесконечных циклах»; вывод `./main.go:13:20: … main.Counter …`, `./main.go:21:2: fmt.Printf …`; условие «исправьте найденные предупреждения».
- **Вердикт:** анализатора про `time.Sleep` нет; исправленного кода нет; позиции и имя типа в выводе не совпадают.
- **Доказательство:** `go tool vet help` (Go 1.27.1): 35 анализаторов (`appends`…`waitgroup`), про `time.Sleep` — ни одного. `go vet ./...` на коде задачи: `main.go:14:21: incrementBad passes lock by value: example.com/gw039.Counter contains sync.Mutex` и `main.go:22:24: fmt.Printf format %d has arg "8080" of wrong type string`. Имя типа берётся из пути модуля (у ученика — его модуль). Утверждение «`copylocks` … ищет типы, реализующие `sync.Locker`» по сути верно: `go/analysis/passes/copylock/copylock.go` проверяет наличие методов `Lock`/`Unlock` (строки 387–388) и отдельно `sync.noCopy`.
- **Предлагаемая правка:** п. 2 заменить на «`defer` в цикле / потерянный `cancel` из `context.WithCancel` (`lostcancel`)» или удалить. Вывод: `# ./main.go:14:21: incrementBad passes lock by value: <модуль>.Counter contains sync.Mutex` и `# ./main.go:22:24: fmt.Printf format %d has arg "8080" of wrong type string`. Добавить блок «`main.go` (исправленный)»: `func incrementGood(c *Counter)` и `fmt.Printf("Порт: %s\n", port)`; ожидаемый вывод `go vet ./...` — пустой.

### J-09 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/036. Семантическое версионирование и мажорные версии.md`: код без `go.mod`; «полностью исключает проблему «ада зависимостей»»; «Go выбирает **минимальную версию**, указанную в графе»; камень: «`go get` … выдаст ошибку `module declares its path as ... but was required as ...`».
- **Вердикт:** (а) без `go.mod`, `require` и `replace` (или тегов) код не собирается. (б) «Ад зависимостей» решают версии в путях импорта и MVS, а не префиксы символов. (в) MVS берёт наибольшую из минимально требуемых версий. (г) Для тега `v2.0.0` при `module` без `/v2` у `go get` другая ошибка.
- **Доказательство:** `/tmp/gw1/x036`: `mathlib/go.mod` (`example.com/mathlib`), `mathlib/v2/go.mod` (`example.com/mathlib/v2`), `app` без `replace` → `cannot find module providing package example.com/mathlib`. После `go mod edit -replace …=../mathlib -replace …/v2=../mathlib/v2 -require …@v1.0.0 -require …/v2@v2.0.0` → `Результат через v1: 30`, `Результат через v2: 100`. Go Modules Reference, «Minimal version selection»: «tracking the highest required version of each module… they are the minimum versions that satisfy all requirements». `go1.27.1 src/cmd/go/internal/modfetch/coderepo.go:498`: `module contains a go.mod file, so module path must match major version (%q)`.
- **Предлагаемая правка:** добавить в «Код решения» три `go.mod`: `mathlib/go.mod` → `module example.com/mathlib`; `mathlib/v2/go.mod` → `module example.com/mathlib/v2`; `app/go.mod`:
  ```text
  module example.com/app

  go 1.22

  require (
      example.com/mathlib v1.0.0
      example.com/mathlib/v2 v2.0.0
  )

  replace example.com/mathlib => ../mathlib
  replace example.com/mathlib/v2 => ../mathlib/v2
  ```
  Вывод: `Результат через v1: 30` / `Результат через v2: 100`. «Под капотом»: «…разные пути — разные пакеты, поэтому v1 и v2 сосуществуют в одной сборке без конфликта символов». Ответ: «MVS берёт для каждого модуля наибольшую из версий, которые требуют модули графа (минимально достаточную), а не новейшую доступную. Результат детерминирован без lock-файла». Камень: «…`go get example.com/mathlib@v2.0.0` откажет: `invalid version: module contains a go.mod file, so module path must match major version ("example.com/mathlib/v2")`».

### J-10 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/066. Поиск уязвимостей в зависимостях через govulncheck.md`: условие «Создай модуль с уязвимой зависимостью»; вывод `# === Govulncheck ===`, `# No vulnerabilities found.`, `# Your code is safe!`.
- **Вердикт:** уязвимый сценарий не показан; строк `=== Govulncheck ===` и `Your code is safe!` в govulncheck нет. Утверждения про SSA и достижимость верны.
- **Доказательство:** `grep` в `golang.org/x/vuln@v1.4.0/internal/scan`: есть только `=== Symbol Results ===`, `safe!` не найдено; `internal/vulncheck/entries.go` работает с `*ssa.Function` (SSA подтверждён). Запуск `go run golang.org/x/vuln/cmd/govulncheck@v1.4.0 ./...` (`/tmp/gw1/x066`, `golang.org/x/text v0.3.5`, вызов `language.Parse`):
  ```text
  === Symbol Results ===

  Vulnerability #1: GO-2021-0113
      Out-of-bounds read in golang.org/x/text/language
    More info: https://pkg.go.dev/vuln/GO-2021-0113
    Module: golang.org/x/text
      Found in: golang.org/x/text@v0.3.5
      Fixed in: golang.org/x/text@v0.3.7
      Example traces found:
        #1: main.go:10:26: xv.main calls language.Parse

  Your code is affected by 1 vulnerability from 1 module.
  ```
  код выхода 3. На чистом модуле: `=== Symbol Results ===` / `No vulnerabilities found.` / `Your code is affected by 0 vulnerabilities.`
- **Предлагаемая правка:** показать модуль с `require golang.org/x/text v0.3.5` и `main.go`, вызывающим `language.Parse("en-US")`; вывод — блок выше; шаг «исправление: `go get golang.org/x/text@v0.3.7` (или новее) → `No vulnerabilities found.`». Удалить `Your code is safe!`. Добавить: «Пустой отчёт значит лишь, что в коде нет вызовов **известных** уязвимостей из базы vuln.go.dev».

### J-11 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/077. Профилирование сервиса через net_http_pprof.md`: цикл `for i := 1; i <= 3; i++ { … time.Sleep(1 * time.Second) }`; `go tool pprof …/profile?seconds=5`; «`net/http/pprof` переводит ядро рантайма Go в режим профилирования… перехватывает стек вызовов всех активных горутин».
- **Вердикт:** (а) процесс живёт около 3 с, 5-секундный профиль снять нельзя. (б) Импорт `net/http/pprof` лишь регистрирует обработчики; CPU-профилирование включается запросом к `/debug/pprof/profile`; по `SIGPROF` берётся стек горутины, выполнявшейся на потоке в момент сигнала, а не всех горутин. (в) `nil` → `DefaultServeMux` — практика, не ошибка.
- **Доказательство:** запуск (`/tmp/gw1/gw-1-077`): сервис стартовал, через 1 с `go tool pprof -top 'http://localhost:6060/debug/pprof/profile?seconds=5'` → `Get "…": EOF`, `failed to fetch any source profiles`; сервис завершился после «Итерация 3». `-race`: 0 гонок.
- **Предлагаемая правка:** цикл заменить на бесконечную работу до сигнала (`signal.NotifyContext(ctx, os.Interrupt)`, `for ctx.Err() == nil { busyWork() }`) или сделать 30 итераций. «Под капотом»: «Импорт `net/http/pprof` регистрирует обработчики `/debug/pprof/*` в `http.DefaultServeMux`. Запрос `/debug/pprof/profile?seconds=N` включает CPU-профилировщик на N секунд: около 100 раз в секунду рантайм получает `SIGPROF` и записывает стек горутины, которая в этот момент выполнялась. Стеки всех горутин — это отдельный профиль `/debug/pprof/goroutine`».

### J-12 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/017. Пакет shapes. инкапсуляция и ошибки компиляции.md`: ответ про `//go:linkname`; «`cmd/compile/internal/typecheck` … `sym.IsExported()`»; вывод `./main.go:13:8: cannot refer to unexported name shapes.isValidRadius`; `area, _ := shapes.Area(5)`.
- **Вердикт:** все четыре подпункта подтверждены.
- **Доказательство:** release notes Go 1.23 (Linker): «The linker now disallows using a `//go:linkname` directive to refer to internal symbols in the standard library (including the runtime) that are not marked with `//go:linkname` on their definitions… `-checklinkname=0` can be used to disable this check». Запуск (`/tmp/gw1/x017`): `//go:linkname stackpool runtime.stackpool` → `link: main: invalid reference to runtime.stackpool`; с `-ldflags=-checklinkname=0` — собирается. Раскомментирован вызов (`/tmp/gw1/x017b`) → `./main.go:14:9: name isValidRadius not exported by package shapes`; источник — `go1.27.1 src/cmd/compile/internal/types2/call.go:747`.
- **Предлагаемая правка:** вывод: `./main.go:14:9: name isValidRadius not exported by package shapes`. «Под капотом»: «…проверка типов (`cmd/compile/internal/types2`) находит, что объект не экспортирован, и сообщает об ошибке». Ответ: «…`//go:linkname` (нужен `import _ "unsafe"`) обходит приватность лишь на уровне линкера. С Go 1.23 ссылки на внутренние символы стандартной библиотеки запрещены, если те не помечены разрешёнными; приём непереносим и ломается между версиями». Код: `area, err := shapes.Area(5); if err != nil { fmt.Println("ошибка:", err); return }`.

### J-13 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/019. Диагностика версии Go и гарантии совместимости.md`: «**гарантированно скомпилируется и будет работать**… Разработчики языка никогда не ломают обратную совместимость»; ответ: «Go вшивает в бинарник полный список модулей, их версии и хэши коммитов, что позволяет моментально проводить аудит уязвимостей».
- **Вердикт:** документ go1compat прямо говорит об отсутствии абсолютной гарантии. В `go version -m` у зависимостей — `h1:`-хэши модулей (как в `go.sum`), а не хэши коммитов; `vcs.revision` есть только для главного модуля при сборке из репозитория.
- **Доказательство:** https://go.dev/doc/go1compat: «It is intended that programs written to the Go 1 specification will continue to compile and run correctly, unchanged…»; «it is impossible to guarantee that no future change will break any program»; исключения: Security, Unspecified behavior, Specification errors, Bugs, Struct literals, Methods, Dot imports, Use of package unsafe. `go version -m` на бинарнике 016: строки `dep github.com/fatih/color v1.19.0 h1:Zp3P…`, строки `vcs.*` нет (сборка вне git).
- **Предлагаемая правка:** «Go 1 Compatibility Promise: программы, написанные по спецификации Go 1, задуманы так, чтобы компилироваться и работать без изменений. Исключения оговорены явно: исправления безопасности и багов, неопределённое поведение, `unsafe` и др.; часть изменений поведения регулируется `GODEBUG`». Ответ: «`go version -m <бинарник>` покажет версию Go, модули с версиями и `h1:`-хэшами из `go.sum`, флаги сборки, а при сборке из git — `vcs.revision`. Для аудита уязвимостей бинарника — `govulncheck -mode=binary <файл>`».

### J-14 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/035. Генерация UUID v4 через библиотеку.md`: `# Сгенерированный UUID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8` + `Версия UUID: 4`; «Официальная и самая популярная библиотека».
- **Вердикт:** показанный UUID — `NameSpaceDNS` версии 1. В `google/uuid` v1.6.0 есть `NewV7`.
- **Доказательство:** `/tmp/gw1/x035`: `uuid.MustParse("6ba7b810-…").Version()` → `VERSION_1`, `== uuid.NameSpaceDNS` → `true`; `uuid.NewV7()` → `VERSION_7 <nil>`. Запуск кода задачи: `Сгенерированный UUID: 4f1cbd9d-1805-4514-a816-ab2cbc383fec` / `Версия UUID: 4`.
- **Предлагаемая правка:** вывод `# Сгенерированный UUID: 4f1cbd9d-1805-4514-a816-ab2cbc383fec (каждый запуск — новый)`. «Самая популярная библиотека для Go — `github.com/google/uuid` (от Google, но вне стандартной библиотеки и проекта Go)». В ответ про v7: «в `google/uuid` с v1.6.0 есть `uuid.NewV7()`».

### J-15 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/045. Использование стороннего пакета google_uuid.md`, строка 77: «…составила \(50%\)…»; строка 72 «экономит гигабайты RAM».
- **Вердикт:** `%` в KaTeX — комментарий, процент пропадает. Арифметика верна.
- **Доказательство:** `node` с `dist/assets/vendor/katex/katex.min.js`: `renderToString("50%")` → предупреждение `commentAtEnd`, видимый текст `50`; `"50\\%"` → `50%`. Других формул с `%` в главе нет (`grep`). Проверка: \(\sqrt{2 \cdot 2^{122} \ln 2} \approx 2{,}715 \cdot 10^{18}\) UUID ≈ 86 лет при 10⁹/с (в тексте «85» — допустимое округление).
- **Предлагаемая правка:** «…составила 50 %, необходимо генерировать 1 миллиард UUID в секунду примерно 86 лет» (без формулы или `\(50\%\)`). Камень: «…при сотнях миллионов ключей экономия (20 байт на ключ плюс заголовок строки) — гигабайты».

### J-16 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/041. Управление внешними библиотеками через pkg.go.dev.md`: «кэширующим исходники всех открытых Go-репозиториев в мире…»; «Количество зависимостей и рейтинг безопасности»; `GOPROXY=https://goproxy.company.ru,direct`.
- **Вердикт:** зеркало кэширует запрошенные версии; «рейтинга безопасности» на pkg.go.dev нет.
- **Доказательство:** https://proxy.golang.org (FAQ): «Whenever possible, the mirror aims to cache content in order to avoid breaking builds»; про удалённые релизы — «We suggest creating a new version…», т. е. сохранность касается уже закэшированных версий. https://pkg.go.dev/github.com/google/uuid: Version, Published, License, Imports, Imported by, чек-лист (Valid go.mod, Redistributable license, Tagged version, Stable version); оценки безопасности нет. Go Modules Reference, «Checksum database»: `GOSUMDB` по умолчанию `sum.golang.org`.
- **Предлагаемая правка:** «`proxy.golang.org` кэширует версии модулей, которые хоть раз через него запрашивали; такие версии, как правило, остаются доступны, даже если автор удалил репозиторий». Список: «Лицензия; число импортирующих пакетов (Imported by); история версий; отметки о известных уязвимостях (vuln.go.dev)». Ответ дополнить: «…а если закрыт и `sum.golang.org`, — настроить прокси на проксирование checksum DB или задать `GOSUMDB`/`GONOSUMDB`; для своих модулей — `GOPRIVATE`».

### J-17 — VERIFIED (расширено)
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/087. Криптографическая безопасность цепочки поставок.md`: «фиксирует SHA-256 хэши **каждого файла исходного кода**»; «полностью обесценив защиту»; блок «go.sum (Пример реальных контрольных сумм)».
- **Вердикт:** `h1:` — один хэш на дерево модуля и отдельный на `go.mod`. Без `go.sum` новые загрузки сверяются с `sum.golang.org`. Ненастоящий не только хэш с `Inspection`: **все четыре** строки блока не совпадают с реальным `go.sum` (совпадают лишь первые 8–10 символов). То же в задаче 038 — F-02.
- **Доказательство:** `go1.27.1 src/cmd/vendor/golang.org/x/mod/sumdb/dirhash/hash.go`: «Hash1 is "h1:" followed by the base64-encoded SHA-256 hash of a summary prepared as if by … `sha256sum $(find . -type f | sort) | sha256sum`». Go Modules Reference, «Authenticating modules»: «If the go.sum file is not present… the go command may verify the hash using the checksum database». Реальный `go.sum` (`/tmp/gw1/x087`):
  ```text
  github.com/google/uuid v1.6.0 h1:NIvaJDMOsjHA8n1jAhLSgzrAzy1Hgr+hNrb57e+94F0=
  github.com/google/uuid v1.6.0/go.mod h1:TIyPZe4MgqvfeYDBFedMoGGpEw/LqOeaOT+nhxU+yHo=
  github.com/sirupsen/logrus v1.9.3 h1:dueUQJ1C2q9oE3F7wvmSGAaVtTmUizReu6fjN8uqzbQ=
  github.com/sirupsen/logrus v1.9.3/go.mod h1:naHLuLoDiP4jHNo9R0sCBMtWGeIprob74mVsIT4qYEQ=
  ```
- **Предлагаемая правка:** заменить блок на четыре строки выше. Теория п. 1: «фиксирует хэш `h1:` (SHA-256) всего содержимого каждой версии модуля и отдельный хэш её `go.mod`». П. 2–3: см. F-09. Абзац про коммит: «Без `go.sum` в репозитории сборка на CI сверит скачанное с публичной базой `sum.golang.org`, но потеряет защиту для приватных модулей (`GONOSUMDB`/`GOPRIVATE`) и при `GOSUMDB=off`, а также гарантию, что CI получил ровно то, что проверял разработчик».

### J-18 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/080. Фиксация точной семантической версии зависимости.md`: «`go get github.com/google/uuid@v1.4.0` — точная фиксация релиза».
- **Вердикт:** `require` задаёт минимум; MVS поднимет версию, если её требует другая зависимость.
- **Доказательство:** `/tmp/gw1/x080`: `app` → `go get github.com/google/uuid@v1.4.0`; затем подключён `example.com/dep` (через `replace`), который требует `uuid v1.6.0`; после `go mod tidy` в `go.mod` стало `github.com/google/uuid v1.6.0`, `go list -m` → `v1.6.0`.
- **Предлагаемая правка:** «`go get pkg@v1.4.0` записывает в `go.mod` минимальную требуемую версию. Итоговую выбирает MVS: если другой модуль графа требует v1.6.0, соберётся v1.6.0. Запретить версию можно `exclude` (только в главном модуле), понизить — `go get pkg@v1.4.0` вместе с понижением зависимостей, которые требуют больше. Итоговые версии смотрите в `go list -m all`».

### J-19 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/071. Конфигурация 12-Factor App.md`: `_ = godotenv.Load()`; `isDebug, _ := strconv.ParseBool(...)`; `if p, err := strconv.Atoi(portStr); err == nil { port = p }`; «вызывает системный вызов `os.Setenv()`» (строка 123).
- **Вердикт:** ошибки разбора теряются молча (нарушение AGENTS § 3.2); `os.Setenv` — функция библиотеки.
- **Доказательство:** `APP_PORT=abc APP_DEBUG=yes ./app` (с `.env` из задачи) → `Порт: 8080`, `Debug Mode: false`, без сообщений. `.env` с незакрытой кавычкой и без `.env` → один и тот же вывод `Ошибка конфигурации: обязательная переменная окружения DATABASE_URL не задана`: причина (синтаксис файла) потеряна. Кроме того, программа печатает `Database URL: postgres://user:pass@…` — секрет в выводе (как J-22).
- **Предлагаемая правка:**
  ```go
  if err := godotenv.Load(); err != nil && !errors.Is(err, fs.ErrNotExist) {
  	return Config{}, fmt.Errorf("загрузка .env: %w", err)
  }
  if portStr != "" {
  	p, err := strconv.Atoi(portStr)
  	if err != nil {
  		return Config{}, fmt.Errorf("APP_PORT=%q: %w", portStr, err)
  	}
  	port = p
  }
  if s := os.Getenv("APP_DEBUG"); s != "" {
  	if isDebug, err = strconv.ParseBool(s); err != nil {
  		return Config{}, fmt.Errorf("APP_DEBUG=%q: %w", s, err)
  	}
  }
  ```
  Не печатать `DATABASE_URL` целиком (маскировать пароль). «Под капотом»: «…затем вызывает `os.Setenv` для ещё не заданных переменных (существующие не перезаписывает)». Отсутствие файла через `errors.Is(err, fs.ErrNotExist)` проверено по логике `os.Open`; сам `godotenv.Load` в кэше не открывался (§ 3).

### J-20 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/085. Синтез. форматированный цветной вывод.md`: `ForceColors: true`; «проверяет поддержку цветов через… `os.Stdout.Fd()`»; «снижает нагрузку на Garbage Collector до нуля».
- **Вердикт:** все три подпункта подтверждены.
- **Доказательство:** `logrus@v1.9.3/text_formatter.go:118`: `isColored := f.ForceColors || (f.isTerminal && …)`; `:106` `checkIfTerminal(entry.Logger.Out)`; `logger.go:89` `Out: os.Stderr`. Запуск `./app > out.txt 2>&1` → файл начинается с `033 [ 3 6 m I N F O 033 [ 0 m` (ANSI-коды в файле). Бенчмарк `l.WithFields(logrus.Fields{…}).Info(...)` в `io.Discard`: `1307 ns/op 1223 B/op 20 allocs/op`.
- **Предлагаемая правка:** убрать `ForceColors: true` (или включать по флагу). «Под капотом»: «`TextFormatter` проверяет, терминал ли `logger.Out` (по умолчанию `os.Stderr`), через `Fd()` и `isatty`; `ForceColors` отключает проверку». Ответ: «…структурированные поля уменьшают аллокации на форматирование, но не обнуляют их: `logrus.Fields` — это `map`. Для логов без аллокаций — `log/slog` с `LogAttrs` или zap/zerolog».

### J-21 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/090. Создание автономного локального модуля.md`: `security.HashPassword("SuperSecret2026!")` → `# Хэш пароля: sha256$2cf24dba…9824`; «Подмена `replace` транслирует файловые дескрипторы компилятора…».
- **Вердикт:** хэш в выводе — от строки `hello`; голый SHA-256 для паролей — антипаттерн; `replace` — механизм `cmd/go`.
- **Доказательство:** `printf 'SuperSecret2026!' | sha256sum` → `02a72dc4…b409`; `printf hello | sha256sum` → `2cf24dba…9824`. Запуск `mainapp` (`replace … => ../core_lib`): `Хэш пароля: sha256$02a72dc49efbfadbebf6f36ea3fb2271833c99ce045263d21a4150f33f20b409`.
- **Предлагаемая правка:** вывод — строка выше. Переименовать функцию в `Fingerprint`/`HashToken` или использовать `golang.org/x/crypto/bcrypt` (`bcrypt.GenerateFromPassword([]byte(p), bcrypt.DefaultCost)` с обработкой ошибки; вывод тогда — пример `$2a$10$…`, каждый запуск разный). «Под капотом»: «`replace` подменяет источник модуля при загрузке пакетов командой `go`; компилятор получает уже готовые пути к каталогам».

### J-22 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/091. Эталонная архитектура микросервиса.md`: `dsn = "postgres://postgres:secret@…"`; вывод `[MAIN] HTTP-сервер слушает на :8080`; «В мировом и российском BigTech (Ozon, Yandex, Avito, Tinkoff, WB) де-факто стандартом является…».
- **Вердикт:** подтверждено.
- **Доказательство:** `grep -rn 'http\|ListenAndServe'` по коду задачи: ни одного совпадения; программа печатает строку про `:8080` и завершается. В выводе запуска: `Подключение к пулу PostgreSQL по адресу postgres://postgres:secret@localhost:5432/…`. README `golang-standards/project-layout`: «This is NOT an official standard defined by the core Go dev team».
- **Предлагаемая правка:** убрать значение DSN по умолчанию (обязательная переменная, как в 071), в логе печатать хост и БД без учётных данных. Добавить реальный `http.Server` с `ListenAndServe` и graceful shutdown либо заменить строку на `[MAIN] Конфигурация и зависимости инициализированы`. Теория: «Популярная, но неофициальная конвенция `golang-standards/project-layout`; официальные рекомендации — https://go.dev/doc/modules/layout».

### J-23 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/005. Первый запуск. main.go в корне модуля.md`, строка 49: «антипаттерн, приводящий к утечке памяти»; строка 11: «(миллисекунды для небольших программ)».
- **Вердикт:** утечка памяти не следует из `go run`. «Миллисекунды» — только при тёплом кэше.
- **Доказательство:** `/tmp/gw1/gw-1-005`, пустой `GOCACHE`: 1,55 с; повтор: 0,02 с. С Go 1.24 `go run` кэширует сам исполняемый файл (release notes Go 1.24: «Executables created by `go run`… are now cached in the Go build cache») — второй запуск запускает `~/.cache/go-build/…/gw005`.
- **Предлагаемая правка:** «…антипаттерн: в образ попадает весь Go SDK, при каждом старте контейнера идёт компиляция (холодный кэш — секунды), нет неизменяемого артефакта, лишний процесс-родитель `go`». Теория: «…на тёплом кэше — десятки миллисекунд; первая сборка с пустым кэшем — секунды».

### J-24 — VERIFIED (расширено на 084)
- **Где / цитата:** `…/04…/060. Тестовые зависимости github.com_stretchr_testify.md` (`calc.go`: `package main`), `…/06…/086. Бенчмаркинг производительности.md` (`concat.go`), а также `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/084. Модульное тестирование в Go.md` (`stringutil.go`: `package main`).
- **Вердикт:** во всех трёх `go test` проходит, `go build ./...` падает.
- **Доказательство:** 060, 084, 086: `go build ./...` → `runtime.main_main·f: function main is undeclared in the main package`; `go test -race ./...` → `ok`.
- **Предлагаемая правка:** `package calc` (060), `package stringutil` (084), `package concat` (086) в обоих файлах задачи; в выводе `go test` — `ok <модуль>`.

### J-25 — PARTIALLY CORRECT
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/086. Бенчмаркинг производительности.md`: `_ = ConcatPlus(sampleData)`; «Принято присваивать результат глобальной переменной»; «Go — единственный мейнстрим-язык…»; «(\(O(N^2)\) по памяти)»; висячий пробел.
- **Вердикт:** (а) противоречие кода своему же совету — верно. Но на Go 1.27.1 компилятор цикл **не** выкинул: `_ =`, sink и `b.Loop()` дают одинаковые 10 allocs/op. Риск реален в принципе (функция инлайнится), а не «результат будет нулевым» сейчас. (б) «Единственный» — спорно. (в) Верно: квадратичны суммарные копирование и аллокации. (г) Верно: `gofmt -d` убирает пробел после `"бэкенда",`. Плюс: числа в выводе книги невозможны — F-06.
- **Доказательство:** `go build -gcflags=-m`: `can inline ConcatPlus`. `go test -bench=. -benchmem -count=2` (`/tmp/gw1/x086`): `BenchmarkConcatPlus 272 ns/op 1040 B/op 10 allocs/op`; `BenchmarkConcatPlusSink 284 ns/op 1040 B/op 10 allocs/op`; `BenchmarkConcatPlusLoop` (`for b.Loop()`) `277 ns/op 1040 B/op 10 allocs/op`. Release notes Go 1.24: `b.Loop` — «Function call parameters and results are kept alive, preventing the compiler from fully optimizing away the loop body».
- **Предлагаемая правка:** код: `for b.Loop() { ConcatPlus(sampleData) }` (Go 1.24+) или `var sink string` + `sink = ConcatPlus(sampleData)`; убрать `b.ResetTimer()` при `b.Loop()`. «Go — один из немногих языков со встроенным в стандартный тулчейн инструментом бенчмаркинга». «…суммарный объём копирования и аллокаций \(O(N^2)\)». Убрать висячий пробел.

### J-26 — VERIFIED
- **Где / цитата:** `…/02…/026. Пакет config, функция init().md` строка 22: «Файлы внутри одного пакета компилируются и инициализируются в **лексикографическом… порядке**!»; `…/03…/042. Множественные init-функции в одном файле.md` строка 12; `…/02…/029. Многоуровневая цепочка инициализации.md`; `…/01…/010. Разделение логики пакета. helper.go в пакете main.md` строка 74; 026 строка 16 «(снизу вверх по дереву зависимостей)».
- **Вердикт:** порядок файлов — рекомендация спецификации сборочной системе; `go build .` сортирует, явный список файлов — нет. Порядок пакетов с Go 1.21 задан точнее.
- **Доказательство:** `/tmp/gw1/x026`: `go run .` → `init a.go` раньше `init b.go`; `go run b.go a.go` → первым `init b.go`. Release notes Go 1.21: «Package initialization order is now specified more precisely… Sort all packages by import path… Find the first package in the list for which all imports are already initialized».
- **Предлагаемая правка:** 026/042: «Команда `go` передаёт компилятору файлы пакета в алфавитном порядке, и `init()` разных файлов выполняются в этом порядке. Спецификация лишь рекомендует такой порядок сборочным системам (`go run b.go a.go` выполнит `b.go` первым), поэтому полагаться на него нельзя». 026 п. 2 и 029: «пакет инициализируется только после всех пакетов, которые он импортирует; среди готовых — по возрастанию пути импорта (Go 1.21+)». 010: «Порядок файлов не влияет на видимость: все объявления уровня пакета видны во всех его файлах».

### J-27 — VERIFIED
- **Где / цитата:** `…/06…/083. Продвинутый POSIX-совместимый парсинг флагов.md`: `pflag.StringVarP(&host, "host", "h", "127.0.0.1", "Хост сервера")`.
- **Вердикт:** `-h` перестаёт вызывать справку; `--help` работает. Версия G «ломает `--help`» неверна.
- **Доказательство:** pflag v1.0.10: `./app -h` → справка + `flag needs an argument: 'h' in -h`, rc=2; `./app --help` → rc=0; `./app -p 9090 -v -t 5s` → `Подключение к 127.0.0.1:9090 (Таймаут: 5s, Verbose: true)` (совпадает с книгой); `--host 10.0.0.1 --port 443 --verbose` → `Подключение к 10.0.0.1:443 (Таймаут: 10s, Verbose: true)`.
- **Предлагаемая правка:** `pflag.StringVarP(&host, "host", "H", …)`; в «Подводные камни»: «`-h` по соглашению — справка (в Cobra зарезервирован); не занимайте его».

### J-28 — VERIFIED
- **Где / цитата:** 009 (`"hello_mod/utils"`), 048/050 (`"calculator/mathops"`, `"calculator/mathutils"`), 052/056 (`"hello_mod/calculator"`), 053 (`"hello_mod/mathutils"`), 038 (без своего модуля).
- **Вердикт:** подтверждено.
- **Доказательство:** изолированный прогон: 009, 048, 052, 053, 056 → `package … is not in std`. `grep 'go mod init'`: модули `hello_world` (001), `example.com/myproject` (006/007), `hello_mod` (008), `color_app` (022), `test_dep` (041), `calculator` (046). 009 собирается только при ручном переносе `utils/greeting.go` из 007 в модуль `hello_mod`.
- **Предлагаемая правка:** в каждой задаче, опирающейся на другую, в начале «Решения по шагам» — строка «Продолжаем модуль `hello_mod` из задач 008, 014, 018» и при необходимости блок с кодом зависимого пакета. Либо единый модуль `hello_mod` для 046/048/050 (`"hello_mod/mathops"`, `"hello_mod/mathutils"`).

### J-29 — VERIFIED
- **Где / цитата:** `…/01…/013. Пакет geometry и правила именования пакетов.md` («имя последней директории должно в точности совпадать»); `…/02…/018. Создание подпакета calculator и чистый интерфейс.md` (строка 55); `…/04…/055. Пакеты models_user и models_order.md` («должно совпадать…», строка 14 `user.Entity`).
- **Вердикт:** совпадение — соглашение. В 055 теория говорит о `user.Entity`, а в коде `type User` (строка 30).
- **Доказательство:** `/tmp/gw1/x029`: каталог `go-bar`, `package foobar`, импорт `"hm/go-bar"`, вызов `foobar.X()` → печатает `1`, `go vet` молчит. Effective Go, «Package names»: «Another convention is that the package name is the base name of its source directory».
- **Предлагаемая правка:** «По соглашению (Effective Go) имя пакета совпадает с последним элементом пути импорта; компилятор этого не требует: в коде используется имя из `package`, и при расхождении читателю придётся гадать». 055: `user.User` (или переименовать тип в `Entity`).

### J-30 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/043. Кросс-компиляция без установки кросс-тулчейнов.md`: «Go генерирует системные вызовы напрямую к ядру целевой ОС»; «100% статическим… `FROM scratch` размером всего 0 байт… идеальную безопасность».
- **Вердикт:** напрямую — Linux и часть BSD; macOS — через `libSystem`, Windows — через DLL, OpenBSD — через libc. В `scratch` нет CA-сертификатов и tzdata.
- **Доказательство:** `go1.27.1 src/syscall/syscall_darwin.go:114`: `//go:cgo_import_dynamic libc_getfsstat getfsstat "/usr/lib/libSystem.B.dylib"`; `src/syscall/syscall_openbsd_libc.go` — `cgo_import_dynamic libc_*`; `src/syscall/dll_windows.go`. Запуск в Docker не делался (§ 3).
- **Предлагаемая правка:** «На Linux Go делает системные вызовы напрямую; на macOS и OpenBSD — через системную libc (это не требует cgo), на Windows — через DLL ОС». Ответ: «…может работать в `FROM scratch`. Но туда нужно положить CA-сертификаты (`/etc/ssl/certs/ca-certificates.crt`) для HTTPS и tzdata (или `import _ "time/tzdata"`). Это уменьшает поверхность атаки, но не делает её нулевой».

### J-31 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/024. Стандартная библиотека.md`, строка 58: «Глобальный генератор `math/rand` защищен внутренним мьютексом…».
- **Вердикт:** устарело. С Go 1.20 глобальный генератор по умолчанию — `runtimeSource` без блокировок. Уточнение к брифу: с Go 1.24 `rand.Seed` по умолчанию ничего не делает (`GODEBUG=randseednop`), поэтому `lockedSource` включается только при `GODEBUG=randautoseed=0` или `randseednop=0` + `Seed`.
- **Доказательство:** `go1.27.1 src/math/rand/rand.go`: комментарий к `globalRandGenerator` — «When possible it uses the runtime fastrand64 function to avoid locking»; `globalRand()` — `lockedSource` только при `randautoseed == "0"`; `Seed()` — `if randseednop.Value() != "0" { return }`. Release notes Go 1.20 (math/rand).
- **Предлагаемая правка:** «С Go 1.20 глобальные функции `math/rand` используют быстрый генератор рантайма без мьютекса (если не включён старый режим через `GODEBUG`). `math/rand/v2` (Go 1.22) — новый API с ChaCha8/PCG; для секретов — только `crypto/rand`».

### J-32 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/058. Экспериментальные пакеты golang.org_x_exp.md`: «как **`cmp.Ordered`** и функции `min()` / `max()`»; ответ «`comparable` разрешает передачу только тех типов, которые поддерживают сравнение…».
- **Вердикт:** `min`/`max` — встроенные функции языка; с Go 1.20 интерфейсы удовлетворяют `comparable`, сравнение может паниковать.
- **Доказательство:** release notes Go 1.21: «The new functions `min` and `max`… Go 1.21 adds three new built-ins»; «The new cmp package defines the type constraint `Ordered`». Go 1.20: «Comparable types (such as ordinary interfaces) may now satisfy `comparable` constraints… (comparison may panic at runtime)». Запуск: `Eq[T comparable]` с `any([]int{1})` → `runtime error: comparing uncomparable type []int`.
- **Предлагаемая правка:** «…в Go 1.21 появились пакет `cmp` с `cmp.Ordered` и встроенные функции языка `min`/`max`». Ответ: «…`comparable` допускает типы с `==`; с Go 1.20 сюда входят и интерфейсы, и тогда сравнение может запаниковать в рантайме, если динамический тип несравним». Добавить вариант кода на `cmp.Ordered`.

### J-33 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/078. Спецификация Go.md`: условие «Создайте несколько экспортируемых и неэкспортируемых функций»; шаг 2 «Проверяем доступность из внешнего пакета».
- **Вердикт:** в коде только `Account` с полем `balance` и методами `New`, `Balance`, `Deposit`; неэкспортируемых функций и демонстрации ошибки нет. Пересказ правила в «Теории» точен (спецификация, «Exported identifiers»: оба условия — заглавная буква категории Lu **и** объявление в блоке пакета либо имя поля/метода).
- **Доказательство:** `grep '^func\|^type' account/account.go` → `type Account`, `func New`, `func (a *Account) Balance`, `func (a *Account) Deposit`.
- **Предлагаемая правка:** добавить `func validateAmount(a float64) error` и `main.go` в другом пакете с закомментированной строкой `// account.validateAmount(1)` и выводом ошибки `name validateAmount not exported by package account` или `undefined: account.validateAmount` (на Go 1.27.1 текст зависит от того, попал ли символ в export data — см. F-11).

### J-34 — VERIFIED
- **Где / цитата:** `…/01…/008. Инициализация модуля hello_mod.md`, строка 55: «`go.mod` гарантирует 100% воспроизводимость сборки»; `…/04…/059. Анатомия go.mod. версия Go и requirements.md`, строка 63: «фиксировала точные хэши… они явно фиксируются в `go.mod`».
- **Вердикт:** хэши — в `go.sum`.
- **Доказательство:** Go Modules Reference, «go.sum files»: «Each line in go.sum has three fields… a module path, a version…, and a hash».
- **Предлагаемая правка:** «`go.mod` фиксирует версии зависимостей, `go.sum` — их криптографические хэши; вместе с версией тулчейна (`go`/`toolchain`) они дают воспроизводимую сборку».

### J-35 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/001. Первый запуск Go-программы и концепция модулей.md`, строка 14: «Почему Go требует модуль даже для простого скрипта?»
- **Вердикт:** для одного файла со стандартной библиотекой модуль не нужен.
- **Доказательство:** каталог без `go.mod`: `go run main.go` → `Hello, World!`; `go run .` и `go build` → `go: go.mod file not found in current directory or any parent directory`.
- **Предлагаемая правка:** «Почему Go требует модуль для `go run .`, `go build` и любых внешних зависимостей? (Одиночный файл `go run main.go` со стандартной библиотекой запустится и без него)».

### J-36 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/004. Структура программы main.go и стандартный вывод.md`, строка 53: «Внутри она блокирует мьютекс стандартного потока вывода `os.Stdout`, форматирует аргументы в буфер…»; строка 20: «с типобезопасностью».
- **Вердикт:** подтверждено.
- **Доказательство:** `go1.27.1 src/fmt/print.go`: `Fprintln` — `p := newPrinter(); p.doPrintln(a); n, err = w.Write(p.buf); p.free()`; `ppFree = sync.Pool{…}`. `src/internal/poll/fd_unix.go:365`: `func (fd *FD) Write` → `fd.writeLock()`. `Printf("%d", "8080")` компилируется и печатает `%!d(string=8080)` (запуск 039).
- **Предлагаемая правка:** «`Println` берёт буфер из `sync.Pool`, форматирует в него аргументы и одним вызовом `os.Stdout.Write` отдаёт ОС; на время записи берётся внутренняя блокировка дескриптора (`poll.FD`)». «…с автоматическим определением типов через reflection; несоответствие глаголов и типов ловит `go vet`, а не компилятор».

### J-37 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/006. Инициализация модуля с каноническим доменным.md`, строка 53: «…регистронезависимы, что может приводить к рассинхрону чексумм».
- **Вердикт:** заглавные буквы в кэше экранируются через `!`.
- **Доказательство:** `ls $(go env GOMODCACHE)/github.com` → `!azure`, `!burnt!sushi`, `!d!a!t!a-!d!o!g`, `!masterminds`.
- **Предлагаемая правка:** «…Go-инструменты справляются с заглавными буквами (в кэше `BurntSushi` хранится как `!burnt!sushi`), но пути с разным регистром — разные модули. Строчные буквы избавляют от путаницы и конфликтов при импорте».

### J-38 — CONTEXT-DEPENDENT
- **Где / цитата:** `…/01…/011. Компиляция бинарного файла с кастомным именем.md`, строка 55; `…/04…/047. Автоматизация сборки и запуска через Makefile.md`, строка 97: «уменьшает размер бинарника на 30–40%».
- **Вердикт:** на Go 1.27.1 linux/amd64 цифра подтвердилась: hello world 2 342 489 → 1 511 584 байт (−35%), сервис с `net/http/pprof` (077) 9 637 129 → 6 570 247 (−31%). Но это зависит от программы и платформы, поэтому нужна оговорка.
- **Доказательство:** `go build -o a . && go build -ldflags='-s -w' -o b .` в 005 и 077.
- **Предлагаемая правка:** «…обычно примерно на треть (на linux/amd64, Go 1.27: −31…35%)». В 011 добавить: «для минимального образа также `CGO_ENABLED=0`».

### J-39 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/012. Пакет mathops и идиоматичная обработка ошибок.md`: «В Go нет исключений»; `Div` проверяет `b == 0`.
- **Вердикт:** стоит упомянуть `panic`/`recover`; деление `float64` на ноль в gc даёт `±Inf`/`NaN`.
- **Доказательство:** запуск: `10.0/0.0, -10.0/0.0, 0.0/0.0` → `+Inf -Inf NaN`. Спецификация, «Arithmetic operators»: результат деления с плавающей точкой на ноль определяется IEEE 754; будет ли паника — зависит от реализации.
- **Предлагаемая правка:** «Исключений в стиле try/catch нет; есть `panic`/`recover` для невосстановимых ситуаций, а ожидаемые ошибки возвращают значением `error`». Комментарий к `Div`: «Для `float64` деление на ноль дало бы `+Inf`/`NaN` без паники; проверка — часть контракта функции».

### J-40 — VERIFIED
- **Где / цитата:** `…/01…/015. Многофайловый пакет и компиляция через go build.md` (строки 69, 78); `…/04…/056. Импорт ради побочных эффектов.md` (строка 60: «увеличит размер бинарника»); `…/04…/046. Проектирование чистого API пакета mathops.md` (строка 42); `…/03…/037. Инкапсуляция и Go-стиль геттеров.md` (строка 65).
- **Вердикт:** blank import пакета без `init` размер не увеличивает. Инлайнинг геттера подтверждён, но он происходит до SSA.
- **Доказательство:** `/tmp/gw1/x056`: пакет с `var Table [4096]int` и функцией, без `init`; бинарник без импорта 2 342 473 байт, с `_ "hm/big"` — 2 341 561 (не больше). 037: `go build -gcflags=-m` → `inlining call to mathops.SecretCode`. Остальное (единица компиляции — пакет; export data содержит тела инлайнируемых функций) — по `cmd/compile/README.md`, не открывался (§ 3).
- **Предлагаемая правка:** 015: «Компилятор обрабатывает пакет целиком (все его файлы вместе) и параллелит генерацию кода по функциям». «Линкер выбрасывает недостижимые функции, но сохраняет методы типов, которые могут вызываться через интерфейсы и `reflect`». 056: «…не даст эффекта, а линкер не включит в бинарник неиспользуемый код». 046: «export data содержит сигнатуры, а также тела функций, пригодных для инлайнинга». 037: «…инлайнинг на промежуточном представлении (до SSA), в пределах бюджета».

### J-41 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/021. Пакет data, глобальные переменные.md`, строка 91: «это три инструкции: `MOVQ`, `INCQ`, `MOVQ`».
- **Вердикт:** gc выдаёт одну `INCQ` с операндом в памяти; без `LOCK` она тоже неатомарна. Гонки в решении нет.
- **Доказательство:** `go build -gcflags=-S` для `func inc() { Counter++ }`: `INCQ main.Counter(SB)` / `RET`. Две горутины по 1000 инкрементов, `go run -race` → `WARNING: DATA RACE … main.inc()`.
- **Предлагаемая правка:** «…на amd64 это одна инструкция `INCQ` с памятью, но без префикса `LOCK` она выполняется как чтение-изменение-запись и неатомарна между ядрами». Добавить демонстрацию с двумя горутинами и `go run -race .`, а также исправление через `atomic.Int64` или мьютекс.

### J-42 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/025. Инспекция переменных окружения через go env.md`: строка 14 «кэш скачанных zip-архивов модулей (`$GOPATH/pkg/mod`)»; строка 55 «без повторного парсинга».
- **Вердикт:** подтверждено.
- **Доказательство:** `ls $(go env GOMODCACHE)` → `cache`, `github.com`, `golang.org`… (распакованные исходники); `cache/download/github.com/google/uuid/@v/` → `list`, `v1.4.0.info`, `v1.4.0.mod`, `v1.4.0.zip`. `go help cache`.
- **Предлагаемая правка:** «`GOMODCACHE` — кэш модулей: распакованные исходники (`$GOPATH/pkg/mod/<путь>@<версия>`, только для чтения) и скачанные zip/mod/info в `cache/download`». Ответ: «…ключ — хэш входов действия (исходники, флаги, версия тулчейна, ID зависимостей). При совпадении `go` пропускает компиляцию; загрузка и анализ пакетов всё равно выполняются».

### J-43 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/027. Культура качества кода. утилиты go fmt и go vet.md`, строка 44: «`go vet` строит SSA-представление»; вывод `./main.go:10:2: …` без исходника.
- **Вердикт:** подтверждено.
- **Доказательство:** `go1.27.1 src/cmd/vendor/golang.org/x/tools/go/analysis/passes/printf/printf.go:44` и `…/copylock/copylock.go:35`: `Requires: []*analysis.Analyzer{inspect.Analyzer}` (AST + типы, без `buildssa`). В 039 vet указывает на аргумент (`22:24`), а не на начало вызова.
- **Предлагаемая правка:** «`go vet` запускает набор анализаторов фреймворка `golang.org/x/tools/go/analysis` по AST и информации о типах (отдельные анализаторы дополнительно строят SSA)». Добавить блок `main.go` с `fmt.Printf("%d\n", "строка")` и реальной позицией (колонка аргумента).

### J-44 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/029. Многоуровневая цепочка инициализации.md`: «Создай пакет `logger` с несколькими файлами, каждый со своей `init()`».
- **Вердикт:** в решении один файл `logger/logger_init.go`.
- **Доказательство:** блоки кода задачи: `logger/logger_init.go`, `app/app_init.go`, `main.go`. Вывод совпал с книгой.
- **Предлагаемая правка:** добавить `logger/a_level.go` и `logger/b_output.go` со своими `init()` и строками вывода `[ШАГ 1a]`, `[ШАГ 1b]`, с оговоркой из J-26.

### J-45 — OPINION / NOT A FACT CLAIM
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/030. Алиасы импорта.md`, строка 21: «можно подменить реализацию пакета без изменения сотен строк кода».
- **Вердикт:** это педагогическая формулировка. Технически алиас меняет только локальное имя (подтверждено: после `calc "hello_mod/calculator"` обращение `calculator.Add` → `undefined: calculator`), а «подмена» работает лишь при совместимом API.
- **Предлагаемая правка (по желанию):** «…сменить путь импорта (например, на форк с совместимым API) в одной строке, сохранив прежнее имя в коде».

### J-46 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/034. Чтение аргументов командной строки через os.Args.md`, строка 71: «Рантайм Go в функции `runtime.sysargs` считывает их и конвертирует… в `[]string`».
- **Вердикт:** срез строит `goargs`.
- **Доказательство:** `go1.27.1 src/runtime/os_linux.go:237` `func sysargs(argc int32, argv **byte)`; `src/runtime/runtime1.go:75` `func goargs()` — `argslice = make([]string, argc)`, `gostringnocopy(argv_index(argv, i))` (без копирования байтов); `src/os/proc.go:23` `Args = runtime_args()`.
- **Предлагаемая правка:** «При старте `runtime.args` сохраняет `argc`/`argv` (`sysargs` на Linux ещё читает auxv), затем `runtime.goargs` строит срез `[]string`, ссылающийся на исходные C-строки без копирования; пакет `os` получает его через `runtime_args()` в `os.Args`».

### J-47 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/037. Инкапсуляция и Go-стиль геттеров.md`: условие `GetSecretCode`; шаг 1 `"SUPER_SECRET_KEY_2026"`; код `SecretCode()`; вывод `SEC-9988-AUTH-TOKEN`.
- **Вердикт:** подтверждено; пояснение замены есть в строке 69.
- **Доказательство:** `grep`; запуск: `Секретный ключ успешно получен: SEC-9988-AUTH-TOKEN`.
- **Предлагаемая правка:** условие: «…и геттер `SecretCode()` (в стиле Go, без `Get`)»; шаг 1 — `"SEC-9988-AUTH-TOKEN"`; заменить «секрет» на нейтральное значение (`apiVersion`).

### J-48 — VERIFIED
- **Где / цитата:** «### Исходная формулировка» в 034, 047, 056, 068, 090, 091.
- **Вердикт:** после снятия `` ` `` и `**` тексты совпадают пословно во всех шести.
- **Доказательство:** скрипт: сравнение «Условия» и «Исходной формулировки» по словам → `IDENTICAL` ×6.
- **Предлагаемая правка:** удалить подразделы «### Исходная формулировка» в шести задачах.

### J-49 — CONTEXT-DEPENDENT
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/038. Исследование структуры go.mod и роли go.sum.md`: «Это признак серьезного инцидента безопасности…».
- **Вердикт:** может быть и атакой, и безобидной причиной (переписанный тег, повреждённый кэш, прокси с другим содержимым). Сам `cmd/go` печатает `SECURITY ERROR` (`src/cmd/go/internal/modfetch/fetch.go:1065`) и предлагает расследовать.
- **Предлагаемая правка:** «Это повод для расследования: возможна подмена кода, но чаще — переписанный автором тег, повреждённый локальный кэш (`go clean -modcache`) или прокси с другим содержимым. Сверьте хэш с `sum.golang.org`; `go.sum` не удаляйте».

### J-50 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/044. Функция init() в main.go и гарантия очередности.md`, строка 57.
- **Вердикт:** закрепление за `m0` — деталь реализации; видимость гарантирует модель памяти.
- **Доказательство:** `src/runtime/proc.go` (`lockOSThread()` перед `doInit`, см. J-07); https://go.dev/ref/mem, «Initialization»: «The completion of all init functions is synchronized before the start of the function main.main» (раздел указан по брифу, текст не открывался — § 3).
- **Предлагаемая правка:** «Модель памяти Go гарантирует: завершение всех `init` происходит раньше (happens before) начала `main.main`, поэтому значения из `init()` видны в `main()`. (То, что рантайм на время инициализации закрепляет главную горутину за основным потоком, — деталь реализации)».

### J-51 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/047. Автоматизация сборки и запуска через Makefile.md`: строка 69 `@go clean -cache`; строка 54 `go test -v -race -cover ./...`.
- **Вердикт:** подтверждено.
- **Доказательство:** `CGO_ENABLED=0 go run -race .` → `go: -race requires cgo; enable cgo by setting CGO_ENABLED=1`. `go help clean`: `-cache` удаляет весь кэш сборки.
- **Предлагаемая правка:** цель `clean`: `rm -rf bin/` и `go clean` (без `-cache`); отдельная цель `clean-cache`. В «Подводные камни»: «`-race` требует cgo (C-компилятор) на linux/amd64».

### J-52 — VERIFIED (предлагаю поднять до Medium)
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/051. Красивый табличный вывод в консоль.md`: `go get github.com/olekukonko/tablewriter`; `table.SetHeader(...)`.
- **Вердикт:** на последней версии код не собирается.
- **Доказательство:** `go list -m -versions` → последняя `v1.1.5`; сборка с ней: `table.SetHeader undefined`, `table.SetBorder undefined`, `undefined: tablewriter.Colors` и др. С `@v0.0.5` код собирается и печатает таблицу.
- **Предлагаемая правка:** `go get github.com/olekukonko/tablewriter@v0.0.5` с пометкой «API v0.x; в v1 API переработан». Либо переписать на `table.Header(...)`/`table.Append(...)`/`table.Render()` v1 — нужна отдельная проверка.

### J-53 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/04. CLI на Cobra, Структурированные Логи, Дженерики/057. Структурированное логирование с sirupsen_logrus.md`: шаг 2 `0666`, код `0644`.
- **Доказательство:** `grep` (строки 17 и 37); `logrus@v1.9.3/README.md:6`: «**Logrus is in maintenance-mode.** We will not be introducing new features».
- **Предлагаемая правка:** шаг 2 — `0644`. В «Теорию»: «logrus в режиме поддержки; для нового кода — стандартный `log/slog` (Go 1.21+)».

### J-54 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/061. Удаление пакета и верификация чистоты go.mod.md`: «используется хотя бы в одном не закоммиченном файле»; diff с двумя строками; «`-diff` в Go 1.21+».
- **Вердикт:** подтверждено; `-diff` — Go 1.23.
- **Доказательство:** release notes Go 1.23: «The new `go mod tidy -diff` flag…». `/tmp/gw1/x061`: после удаления импорта `fatih/color` `go mod tidy -diff` (rc=1) убирает `require github.com/fatih/color v1.19.0` и три косвенные (`go-colorable`, `go-isatty`, `golang.org/x/sys`), а из `go.sum` — 9 строк.
- **Предлагаемая правка:** «Если зависимость импортируется хотя бы в одном `.go`-файле модуля (включая `_test.go`), `tidy` её сохранит; статус файла в git значения не имеет». Diff дополнить косвенными строками. Вопрос: «…`-diff` (Go 1.23+)».

### J-55 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/063. Устройство кэша модулей. $GOPATH_pkg_mod.md`, строка 46: «ошибкой файловой системы `Permission denied` (Read-only file system)».
- **Доказательство:** `stat`: `444 -r--r--r-- …/uuid@v1.6.0/uuid.go`, `555 dr-xr-xr-x …/uuid@v1.6.0`. Запись в собственную копию файла с правами 0444 → `Permission denied`. (Запись в сам файл кэша не делалась, чтобы его не портить.)
- **Предлагаемая правка:** «…завершится ошибкой `permission denied`: `go` создаёт файлы кэша только для чтения (0444, каталоги 0555). Это не `read-only file system` — та ошибка про ФС, смонтированную только для чтения».

### J-56 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/065. Локальный модуль myutils и оркестрация.md`: шаг 5 `dev@yandex.ru`, код/вывод `alex@company.ru`; `strings.Contains(email, "@") && strings.Contains(email, ".")`.
- **Доказательство:** `grep`; код валидатора — ровно две проверки `Contains`. Запуск (после `go mod init company.com/myutils` по шагу 2 и `go mod tidy`) → `Email 'alex@company.ru' валиден: true` (совпадает). См. также F-10.
- **Предлагаемая правка:** шаг 5 — `alex@company.ru`. Комментарий «наивная проверка для примера; в проде — `net/mail.ParseAddress`».

### J-57 — VERIFIED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/068. Приватные корпоративные репозитории.md`: вывод `# gitlab.company.ru/* (наследуется от GOPRIVATE)`; «обходит сетевой стек `GOPROXY`».
- **Доказательство:** `GOPRIVATE='gitlab.company.ru/*' go env GONOPROXY GONOSUMDB GOPRIVATE` → три строки `gitlab.company.ru/*` без пояснений. Go Modules Reference: «`GOPRIVATE`… Acts as a default value for `GONOPROXY` and `GONOSUMDB`»; «`GONOPROXY`… The go command will download matching modules from version control repositories… regardless of `GOPROXY`».
- **Предлагаемая правка:** вывод `# gitlab.company.ru/*` (пояснение — в тексте). «Под капотом»: «`GOPRIVATE` задаёт значение по умолчанию для `GONOPROXY` и `GONOSUMDB`: такие модули `go` скачивает напрямую из VCS (`git`) мимо прокси и не сверяет с `sum.golang.org`». Добавить шаг импорта в другой проект или убрать это из условия.

### J-58 — PARTIALLY CORRECT
- **Где / цитата:** `…/05…/069. Инспекция доступных релизов пакета через go list.md`; `…/05…/074. Модуль с пакетами main и greeter.md`; `…/06…/076. Паттерн Driver_Plugin Registry.md`; `…/06…/081. Регулярное обслуживание зависимостей.md`; `…/06…/084. Модульное тестирование в Go.md`.
- **Вердикт:** подтверждены 069 («от ранних `v1.0.0`», а вывод с `v0.1.0`; к тому же список выдуман — F-08), 074 (`Greeter` против `Service`), 076 (`Plugin` в теории, `Driver` в коде; `Register` печатает в stdout), 081 (`govulncheck` в регламенте, в коде нет), 084 (кейс «Пустая строка» с `input: "   "`). **Не подтверждён** подпункт «`d == nil` не ловит типизированный nil (AGENTS § 3.2)»: § 3.2 о возврате типизированного `nil` как `error`, а проверка `driver == nil` — ровно та, что в `database/sql.Register`; это не ошибка.
- **Доказательство:** `grep` по файлам; 076 под `-race` — 3 одинаковых прогона, гонок нет; 084 `go test -cover` → `coverage: 100.0% of statements`, все кейсы проходят.
- **Предлагаемая правка:** 069: «(от ранних `v0.x` до …)» и реальный список (F-08). 074: «структуру `Service` и конструктор `New(prefix string)`». 076: «`Register(name string, d Driver)`», «`driver.Register("postgres", &PostgresDriver{})`»; печать регистрации — в `log` или убрать. 081: добавить `govulncheck ./...` в блок команд. 084: кейс `{name: "Только пробелы", input: "   ", expected: true}` и отдельный `{name: "Пустая строка", input: "", expected: true}`.

### J-59 — VERIFIED
- **Где / цитата:** 072 строка 11 (GPL/AGPL); 073 строка 38 («без ломающих изменений»); 079 строка 75 (`golint`); 088 строки 94–95 («Что появилось в Go 1.18…»); 089 строки 45, 54.
- **Вердикт:** технические подпункты подтверждены; юридический (GPL) — CONTEXT-DEPENDENT, юридически не проверялся.
- **Доказательство:** `go help get`: `-u` — «newer minor or patch releases when available». github.com/golang/lint: «archived by the owner on May 9, 2021»; «NOTE: Golint is deprecated and frozen… Staticcheck and go vet should be used instead». pkg.go.dev/runtime/debug: `ReadBuildInfo` — Added in go1.12, `BuildSetting` — go1.18 (`vcs.revision`, `vcs.modified`). Вендоринг (`/tmp/gw1/x089`): `vendor/modules.txt` = `# github.com/google/uuid v1.6.0` / `## explicit` / `github.com/google/uuid` — лицензий нет (файл `LICENSE` копируется в `vendor/…`); после `go mod edit -require …@v1.5.0` `go build` → `go: inconsistent vendoring in …`.
- **Предлагаемая правка:** 073: «…наибольшую minor/patch-версию в пределах текущего major (о совместимости `go` не знает — полагается на SemVer авторов)». 079: «(`revive`, `staticcheck`; `golint` заморожен с 2021)». 088: «Что `debug.ReadBuildInfo` (Go 1.12) умеет с Go 1.18? — Вшитые сведения VCS: `vcs.revision`, `vcs.time`, `vcs.modified`». 089: «`modules.txt` — список модулей и пакетов с версиями (лицензии лежат файлами в `vendor/<модуль>/`)»; «`-mod=mod` — игнорировать `vendor/`; `-mod=readonly` к вендорингу не относится»; плюс камень про `inconsistent vendoring` после правки `go.mod` (лечится `go mod vendor`). 072: «GPL обязывает раскрыть исходники производного кода при распространении бинарника, AGPL — и при доступе по сети; поэтому их часто запрещают».

### J-60 — VERIFIED
- **Где / цитата:** `…/05…/070. Механизм internal-пакетов.md`, строка 87: «Компилятор Go (`cmd/compile`) при проверке каждого импорта…»; `…/05…/075. Защита внутренней бизнес-логики через каталог.md`, строка 75.
- **Доказательство:** `go1.27.1 src/cmd/go/internal/load/pkg.go:1587`: `ImportErrorf(p.ImportPath, "use of internal package %s not allowed", …)`. `/tmp/gw1/x070`: `external_app` как отдельный модуль без `require`/`replace` → `package hello_mod/internal/secret is not in std`; с `replace hello_mod => ../hello_mod` → `package external_app` / `main.go:5:2: use of internal package hello_mod/internal/secret not allowed`.
- **Предлагаемая правка:** «Команда `go` (`cmd/go/internal/load`) при загрузке пакетов проверяет…». В 070 показать `external_app/go.mod` с `require hello_mod v0.0.0` и `replace hello_mod => ../hello_mod`, вывод — как выше. В 075 добавить попытку импорта извне.

### J-61 — VERIFIED (список уточнён)
- **Где:** блоки Go задач главы.
- **Доказательство:** `gofmt -l` / `gofmt -d` по всем извлечённым файлам. Неканонически отформатированы (кроме намеренного «ДО» в 031): 007, 032 (`app/main.go`), 036 (`app/main.go`), 048, 050, 051, 054, 057, 060 (`calc_test.go`), 065 (`mainapp/main.go`), 071, 083, 085 — порядок импортов в группе; 024 — выравнивание комментариев и висячий пробел; 045 — висячий пробел и порядок импортов; 086 — висячий пробел. Бриф пропустил 024, 050, 057, 065, 071.
- **Предлагаемая правка:** прогнать каждый блок через `gofmt` (стандартные и сторонние импорты — отдельными группами, как делает `goimports`).

### J-62 — VERIFIED
- **Где / цитата:** `…/02…/023. Разделение логики пакета.md` строка 68 («парсит манифест пакета»); `…/02…/028. Экспорт и видимость в calculator (Sub vs multiply).md` строка 62; `…/01…/010. Разделение логики пакета. helper.go в пакете main.md` строка 69 («ошибке линковки `undefined: formatOutput`»).
- **Доказательство:** 010: `go run main.go` → `# command-line-arguments` / `./main.go:6:9: undefined: formatOutput` — ошибка проверки типов компилятора с позицией в исходнике, до линковки. 028: проверка видимости — `types2` (см. J-12).
- **Предлагаемая правка:** 023: «…сканирует `.go`-файлы каталога и отбирает их по build constraints (`go/build`)». 028: «…проверка типов компилятора». 010: «…к ошибке компиляции `./main.go:6:9: undefined: formatOutput`».

---

## 3. Непроверенное (NOT CHECKED)

Ни одна находка не осталась непроверенной целиком. Не проверены отдельные подпункты:
- **J-05(в)** — статус архива `github.com/golang/mock` (страница не открывалась).
- **J-19** — поведение `godotenv.Load` без файла по исходникам (проверено только косвенно: программа продолжает работу).
- **J-30(б)** — запуск в `FROM scratch` (Docker не запускался); утверждение про CA и tzdata — по документации.
- **J-40** — детали фаз компилятора (`cmd/compile/README.md` не открывался); проверены только размер бинарника при blank import и инлайнинг геттера.
- **J-50** — точная цитата раздела «Initialization» модели памяти (страница не открывалась).
- **J-52** — переписанный под tablewriter v1 код не собирался.
- **J-59 (GPL/AGPL)** — юридическая формулировка.
- **066** — `nancy sleuth` не запускался.
- **047** — цели Makefile не выполнялись (проверены только `-race`/CGO и `go help clean`).
- **054** — подкоманды Cobra (`hello`, `time`) не вызывались; проверен только вывод справки.

---

## 4. Пропущенное брифом

### F-01 — PARTIALLY CORRECT
- **Где / цитата:** `001. Пакеты и модули/01. Введение, Окружение, Компиляция и Базовые Пакеты/009. Вложенные подпакеты (utils_strings).md`, строка 84: «Приведение `[]rune(s)`… выделяя память в куче под массив `int32`».
- **Вердикт:** если срез не убегает и в строке ≤ 32 рун, буфер выделяется на стеке. В примере 23 руны — кучи нет. Плюс `slicerunetostring` отвечает за обратное преобразование `string(runes)`, а не за декодирование.
- **Доказательство:** `go1.27.1 src/runtime/string.go:20` `tmpStringBufSize = 32`; `stringtoslicerune(buf *[tmpStringBufSize]rune, s string)`: `if buf != nil && n <= len(buf) { a = buf[:n] } else { a = rawruneslice(n) }`. `go build -gcflags=-m`: `reverse.go:5:18: ([]rune)(s) does not escape`; `string(runes) escapes to heap`.
- **Предлагаемая правка:** «`[]rune(s)` декодирует UTF-8 (`runtime.stringtoslicerune`), `string(runes)` кодирует обратно (`runtime.slicerunetostring`). Для коротких строк (до 32 рун), если срез не покидает функцию, буфер берётся на стеке; иначе — аллокация в куче. Результирующая строка аллоцируется».

### F-02 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/038. Исследование структуры go.mod и роли go.sum.md`, строки 14, 32–33 (блок «go.sum (Фрагмент)»): `github.com/google/uuid v1.6.0 h1:NIvaJDMOLLgnQqtS9L13SiLgXA2zgWUpEvJ8kx4Pzp8=`, `…/go.mod h1:TIyPZe4MgqvFqtWhCDKEIlvZxxxvm618TFiP1UGKOEg=`.
- **Вердикт:** хэши выдуманы; совпадают только первые 8–10 символов. Те же ненастоящие строки — в 087 (J-17).
- **Доказательство:** реальный `go.sum` (`/tmp/gw1/x087`, uuid v1.6.0): `h1:NIvaJDMOsjHA8n1jAhLSgzrAzy1Hgr+hNrb57e+94F0=` и `/go.mod h1:TIyPZe4MgqvfeYDBFedMoGGpEw/LqOeaOT+nhxU+yHo=`.
- **Предлагаемая правка:** в 038 (строки 14, 32, 33) и 087 — реальные строки из J-17.

### F-03 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/02. Внешние Зависимости, Инкапсуляция, Init()/026. Пакет config, функция init().md`, «Жизненный цикл»: «1. Инициализируются переменные импортированных пакетов. 2. Выполняются функции `init()` импортированных пакетов…».
- **Вердикт:** порядок попакетный: переменные пакета A → `init()` A → переменные B → `init()` B, а не «сначала все переменные, потом все `init`».
- **Доказательство:** `/tmp/gw1/xorder`: пакеты `a` и `b` с инициализатором переменной и `init()` → `a: var`, `a: init`, `b: var`, `b: init`, `main 2`. Спецификация, «Package initialization»: пакет инициализируется целиком (переменные, затем `init`) до следующего.
- **Предлагаемая правка:** «1. Для каждого импортированного пакета — по порядку зависимостей (Go 1.21+: среди готовых — по пути импорта): сначала его переменные уровня пакета, затем его `init()`. 2. То же для пакета `main`. 3. Запуск `main.main()`».

### F-04 — OUTDATED
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/062. Полный справочник директив go.mod.md`, шаг 3: «Запускаем `go build .` — компилятор проигнорирует версию v1.5.0 и выберет следующую подходящую версию (v1.6.0)». Это же правило («next higher version») бриф цитирует в § 4 (отсев A-81(в)) и § 5.7.
- **Вердикт:** «следующая версия» — поведение до Go 1.16. Сейчас требование на исключённую версию игнорируется: `go build` падает и просит `go mod tidy`, а `tidy` ищет модуль заново и берёт **последнюю** версию. Тезис брифа «`exclude` действует на весь граф» верен; механизм «поднимается до следующей неисключённой» — нет.
- **Доказательство:** Go Modules Reference, «exclude directive»: «Since Go 1.16, if a version referenced by a require directive in any go.mod file is excluded by an exclude directive in the main module's go.mod file, the requirement is ignored. This may cause commands like `go get` and `go mod tidy` to add new requirements on higher versions…»; «Before Go 1.16… loaded the next higher non-excluded version instead». Запуск (`/tmp/gw1/x062`, `require uuid v1.5.0` + `exclude v1.5.0`): `go build .` → `go: ignoring requirement on excluded version github.com/google/uuid v1.5.0` / `go: updates to go.mod needed; to update it: go mod tidy`, rc=1; `go mod tidy` → `go: dropping requirement on excluded version…` / `go: found github.com/google/uuid in github.com/google/uuid v1.6.0`; `require` стал `v1.6.0`.
- **Предлагаемая правка:** шаги: «2. Добавляем `exclude github.com/google/uuid v1.5.0` (при `require … v1.5.0`). 3. `go build .` откажет: `go: updates to go.mod needed`. 4. `go mod tidy` отбрасывает требование на исключённую версию и заново находит модуль — записывает последнюю доступную версию (сейчас v1.6.0)». Брифу/редактору: в § 4 и § 5.7 заменить цитату на правило Go 1.16+.

### F-05 — OUTDATED
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/040. Разница между go build, go install, go run.md`, таблица: «`go run` | Во временный каталог `/tmp/go-build...` (удаляется после завершения)»; `…/03…/034. Чтение аргументов командной строки через os.Args.md`, вывод: `# Имя исполняемого файла: /tmp/go-build.../exe/main` и блок «Пользовательские аргументы» дважды; `…/01…/003. Многофайловый пакет main и единица компиляции в Go.md`, вывод `./main.go:4:2: undefined: sayGreeting`.
- **Вердикт:** с Go 1.24 исполняемые файлы `go run` кэшируются в `GOCACHE`. В 034 блок вывода продублирован, а имя файла — последний элемент пути модуля, не `main`. В 003 позиция ошибки — `5:2`.
- **Доказательство:** release notes Go 1.24: «Executables created by `go run`… are now cached in the Go build cache». Запуск 034 с `--port=8080 --env=production start`: `Всего элементов в os.Args: 4`, `Имя исполняемого файла: /home/ut/.cache/go-build/f8/f829…-d/gw034`, блок «Пользовательские аргументы» один раз (первый запуск до кэширования дал `/tmp/go-build3063402709/b001/exe/gw034`). В пустом `GOCACHE` после `go run` найден ELF `…/gw005`. 003: `go run main.go` → `./main.go:5:2: undefined: sayGreeting`.
- **Предлагаемая правка:** 040: «`go run` | Собирает во временный каталог и запускает; с Go 1.24 исполняемый файл кэшируется в `GOCACHE`». 034: удалить дубль блока; `# Имя исполняемого файла: <временный путь или путь в кэше сборки>/<имя модуля>`. 003: `# ./main.go:5:2: undefined: sayGreeting`.

### F-06 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/086. Бенчмаркинг производительности.md`, вывод: `BenchmarkConcatPlus-8 … 240 B/op 10 allocs/op`, `BenchmarkConcatBuilder-8 … 96 B/op 3 allocs/op`.
- **Вердикт:** цифры невозможны: `sampleData` — 141 байт UTF-8, поэтому `ConcatBuilder` должен выделить минимум 141 байт (а `+=` — сумму промежуточных строк).
- **Доказательство:** суммарная длина `sampleData` (Python, `len(x.encode())`) = 141. Запуск: `BenchmarkConcatPlus-24 4269604 282.6 ns/op 1040 B/op 10 allocs/op`, `BenchmarkConcatBuilder-24 9315321 120.7 ns/op 344 B/op 4 allocs/op`.
- **Предлагаемая правка:** вывод (пример, числа зависят от машины):
  ```bash
  # BenchmarkConcatPlus-24        4269604    282.6 ns/op    1040 B/op    10 allocs/op
  # BenchmarkConcatBuilder-24     9315321    120.7 ns/op     344 B/op     4 allocs/op
  ```
  и пояснение: «Builder без `Grow` всё равно делает несколько аллокаций при росте буфера; с `sb.Grow(общая длина)` будет одна».

### F-07 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/03. SemVer, Локальный Replace, Кросс-компиляция и UUID/031. Автоматическое форматирование кривого кода.md`, блок «bad_format.go (ПОСЛЕ форматирования)»: `import "fmt"`.
- **Вердикт:** `gofmt` не сворачивает `import ( "fmt" )` в однострочный импорт.
- **Доказательство:** `gofmt bad_format.go | diff - <блок ПОСЛЕ>` → единственное расхождение: gofmt оставляет `import (` / `"fmt"` / `)`.
- **Предлагаемая правка:** в блоке «ПОСЛЕ» — `import (\n\t"fmt"\n)` (остальное совпадает с выводом gofmt).

### F-08 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/069. Инспекция доступных релизов пакета через go list.md`, вывод `go list -m -versions github.com/fatih/color`: `v0.1.0 v1.5.0 v1.6.0 … v1.17.0`.
- **Вердикт:** версии `v0.1.0` нет; пропущены `v0.2.0`, `v1.0.0`–`v1.4.1`, `v1.11.0`, `v1.14.0`.
- **Доказательство:** запуск 2026-10-22: `github.com/fatih/color v0.2.0 v1.0.0 v1.1.0 v1.3.0 v1.4.0 v1.4.1 v1.5.0 v1.6.0 v1.7.0 v1.8.0 v1.9.0 v1.10.0 v1.11.0 v1.12.0 v1.13.0 v1.14.0 v1.14.1 v1.15.0 v1.16.0 v1.17.0 v1.18.0 v1.19.0`.
- **Предлагаемая правка:** вывод — строка выше с пометкой «на октябрь 2026».

### F-09 — INCORRECT
- **Где / цитата:** `001. Пакеты и модули/06. Паттерн Registry, Бенчмаркинг, Ldflags, Vendor/087. Криптографическая безопасность цепочки поставок.md`, теория п. 2–3: «При каждой сборке Go вычисляет хэш скачанных файлов и сверяет его с `go.sum`»; «компилятор Go **немедленно аварийно остановит сборку**: `SECURITY ERROR: checksum mismatch`».
- **Вердикт:** хэш сверяется при **загрузке** модуля в кэш; при обычной сборке уже закэшированные модули не перехэшируются (для этого есть `go mod verify`). Останавливает команда `go`, не компилятор; сообщение — `verifying <модуль>@<версия>: checksum mismatch`, затем `SECURITY ERROR`.
- **Доказательство:** `go help mod verify`: «Verify checks that the dependencies… stored in a local downloaded source cache, have not been modified since being downloaded». `go1.27.1 src/cmd/go/internal/modfetch/fetch.go:1065` — текст `SECURITY ERROR` в блоке checksum mismatch.
- **Предлагаемая правка:** «2. При скачивании модуля `go` вычисляет его хэш и сверяет с `go.sum` (а для новых модулей — с `sum.golang.org`). 3. При расхождении команда `go` останавливается: `verifying …: checksum mismatch` … `SECURITY ERROR`. Целостность уже скачанного кэша проверяет `go mod verify`».

### F-10 — CONTEXT-DEPENDENT
- **Где / цитата:** `001. Пакеты и модули/05. Анатомия go.mod, Безопасность govulncheck/065. Локальный модуль myutils и оркестрация.md` (а также 032, 090): `mainapp/go.mod` с `go 1.22.5`; модуль `myutils` создаётся командой `go mod init` (шаг 2).
- **Вердикт:** на Go ≥ 1.23 `go mod init` пишет в `myutils/go.mod` текущую версию (`go 1.27.1`), и `go run .` в `mainapp` падает: `go: updates to go.mod needed; to update it: go mod tidy`. После `tidy` строка `go` в `mainapp` поднимается до 1.27.1. Это нормальное поведение, но ученик увидит ошибку, которой нет в задаче.
- **Доказательство:** `/tmp/gw1/x065.*`: ошибка выше; после `go mod tidy`: `-go 1.22.5` / `+go 1.27.1`, затем `Email 'alex@company.ru' валиден: true`.
- **Предлагаемая правка:** в шаги: «после `go mod init` в обоих модулях выполните `go mod tidy` в `mainapp`» или показать `myutils/go.mod` с той же строкой `go 1.22.5`.

### F-11 — INCORRECT (относится к брифу, К-1)
- **Где / цитата:** бриф, К-1: «`undefined: utils.sayHello` (а не `cannot refer to unexported name`)». Применено к 017, 028, 037, 007.
- **Вердикт:** gc (types2) печатает одно из двух сообщений. `name X not exported by package P` — если неэкспортированный объект есть в export data пакета (например, его вызывает инлайнируемая экспортированная функция). `undefined: P.X` — если его там нет. Старого `cannot refer to unexported name` нет ни там, ни там.
- **Доказательство:** `go1.27.1 src/cmd/compile/internal/types2/call.go:720–748`: `undefined: %s` при `exp == nil` и `name %s not exported by package %s` при `!exp.Exported()`. Запуск: 017 → `./main.go:14:9: name isValidRadius not exported by package shapes` (`Area` инлайнится и ссылается на `isValidRadius`); отдельный модуль → `undefined: utils.sayHello`, `undefined: calculator.init`, `undefined: calculator.multiply`, `undefined: calculator.secretCode`. Остальные тексты К-1 подтверждены: `"fmt" imported and not used`; `expected 'IDENT', found 2`; `undefined: calculator` (052); цикл → `import cycle not allowed` с цепочкой `imports …`, а импорт `main` → `import "hello_mod" is a program, not an importable package`.
- **Предлагаемая правка:** 007, 028, 037: `undefined: utils.sayHello` и т. п.; 017: `name isValidRadius not exported by package shapes` (J-12). В ответах: «текст зависит от версии Go; суть — неэкспортированное имя недоступно из другого пакета».

---

### Приложение: воспроизведение
- Извлечение и массовый прогон — скрипты в scratchpad сессии; каталоги `/tmp/gw1/gw-1-KKK/` (`_MANIFEST.txt` в каждом связывает блоки с файлами).
- Эксперименты: `/tmp/gw1/x009`, `x017*`, `x021*`, `x026*`, `x029*`, `x035*`, `x036*`, `x040*`, `x049`, `x051*`, `x056*`, `x058*`, `x061*`, `x062`, `x065*`, `x066*`, `x069*`, `x070*`, `x080*`, `x083flag*`, `x085*`, `x086*`, `x087*`, `x089*`, `xk1*`, `xorder*`.
- Репозиторий не менялся, кроме этого отчёта.
