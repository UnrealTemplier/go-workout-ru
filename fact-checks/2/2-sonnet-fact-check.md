# Фактчек главы 2. Компиляция, сборка и запуск (`sources/002. Компиляция, сборка и запуск/`)

**Роль:** основной факт-чекер. **Дата:** 2026-10-22.
**Входной отчёт:** `2-opus-judge.md` (Master Fact-Check Brief, находки `J-01…J-35`). Отчёта blind spot для главы 2 нет. Все цитаты брифа сверены с текущими файлами задач: каждая дословно есть в `sources/`.
**Пути** в поле «Где» даны от каталога главы `sources/002. Компиляция, сборка и запуск/`. Разделы сокращены до номера: `01. …` — `01. Базовая Компиляция, go run и go build`, и так далее.

## 1. Сводка

- **Среда:** `go version go1.27.1 linux/amd64`, Linux 7.2.11 (Fedora 44, x86_64, 24 потока, i9-12900K), `/tmp` — tmpfs, `$HOME` — btrfs. `gcc` есть, поэтому `CGO_ENABLED=1` по умолчанию. `GOTOOLCHAIN=local`, если не оговорено иное. `file-5.46`, `podman 5.8.9` (Docker в среде нет, образы собирались podman/buildah), Delve 1.27.2 (поставлен во временный `GOBIN=/tmp/gw-2-dlv/bin`).
- **Каталоги:** `/tmp/gw-2-KKK/` по номеру задачи, дополнительные эксперименты — `/tmp/gw-2-KKKb/`, `/tmp/gw-2-024-nogcc/` и т. п. Репозиторий не менялся, кроме этого отчёта.
- **Запуск кода:** все Go-программы главы (002, 012, 015, 016, 019, 020, 021, 022, 023) проходят `gofmt -l` и `go vet` без замечаний, выполнены `go run`. Конкурентный код запущен с `-race`, по несколько раз. Bash-скрипты 014 и 024 выполнены целиком. Dockerfile 025 собран podman'ом, контейнер запущен. Вывод сверён с блоками «Терминал».
- **Не запускалось:** macOS (`-race` без cgo), сборка 025 под `linux/arm64` (нет qemu/binfmt), настоящий Docker и Kubernetes.

Совпадение блоков «Терминал» с фактическим выводом:

| Задача | Результат |
|---|---|
| 002, 015, 016, 019, 020 (`add --x=15 --y=27`, `sub --x=100 --y=42`), 022, 023 (Ctrl+C) | совпадает |
| 003 | `go build .` без `go.mod` падает (J-09); с модулем `hello_world` бинарник есть, но 2,3 МБ вместо 1,8 МБ (F-08) |
| 006 | программа из 002 печатает другую строку (J-09) |
| 011 | `file` печатает `Go BuildID=…, BuildID[sha1]=…, with debug_info, not stripped` (J-17) |
| 012 | другие строки, 2–3 гонки, есть итог и `exit status 66` (J-17) |
| 017 | `main.go:3:6` верно только для main.go без импортов (F-09) |
| 018 | 2,3 МБ / 1,5 МБ вместо 1,8 МБ / 1,2 МБ, доля −35 % верна (F-08) |
| 025 | 5,86 МБ вместо 12,4 МБ (J-20) |

### Итоговая таблица статусов

Бриф (`J-…`, 35 находок):

| Статус | Кол-во | ID |
|---|---|---|
| VERIFIED | 34 | J-01…J-33, J-35 (у J-06, J-11, J-19 и J-26 правки к деталям брифа; у J-18 подтверждены пп. 2–3, п. 1 — в § 3) |
| OPINION / NOT A FACT CLAIM | 1 | J-34 (упущения; лежащие в основе факты проверены) |
| INCORRECT / PARTIALLY CORRECT / OUTDATED / CONTEXT-DEPENDENT | 0 | — |
| NOT CHECKED | 0 целиком | частично: J-18 п. 1, J-19 (побег из контейнера), J-06 (macOS) — см. § 3 |

Статус относится к утверждению находки. «VERIFIED» значит, что находка подтверждена, то есть текст книги в этом месте ошибочен или неполон так, как описано в брифе.

Новые находки (`F-…`, 10 шт.; бриф их пропустил):

| Статус | Кол-во | ID |
|---|---|---|
| INCORRECT | 1 | F-01 |
| PARTIALLY CORRECT | 5 | F-02, F-03, F-04, F-06, F-07 |
| OUTDATED | 1 | F-08 |
| CONTEXT-DEPENDENT | 1 | F-09 |
| OPINION / NOT A FACT CLAIM | 2 | F-05, F-10 |

---

## 2. Находки брифа

### J-01 — VERIFIED
- **Где / цитата:** `02. …/009. Кастомизация выходного имени бинарника через флаг.md`, «Подводные камни»: «Если передать флаг `-o` без значения (`go build -o .`), компилятор выдаст синтаксическую ошибку флагов.»
- **Вердикт:** утверждение книги неверно. `.` — значение флага: существующий каталог, туда и пишется бинарник. Ошибка бывает только при `-o` без аргумента, и выдаёт её `go`, а не компилятор.
- **Доказательство:** `go help build`: «If the named output is an existing directory or ends with a slash or backslash, then any resulting executables will be written to that directory.» Запуск в модуле `hello_mod`:
  ```
  $ go build -o . ; echo $?      → 0, создан ./hello_mod
  $ go build -o                  → flag needs an argument: -o
                                   usage: go build [-o output] [build flags] [packages]   (exit 2)
  $ go build -o bin .            → exit 0, bin — ФАЙЛ (ELF), каталог не создан
  $ go build -o bin/ .           → exit 0, создан каталог bin/ с bin/hello_mod
  ```
- **Предлагаемая правка:** «Если каталога `bin` нет, `go build -o bin .` создаст **файл** с именем `bin`, а не каталог. Чтобы бинарник лёг в каталог, укажите путь с косой чертой на конце (`-o bin/`) или полное имя файла (`-o bin/myapp`). Флаг `-o` без значения `go` отвергнет: `flag needs an argument: -o`.»

### J-02 — VERIFIED
- **Где / цитата:** `05. …/021. Внедрение версии и времени сборки через -ldflags.md`. «Условие»: «`-X main.Version=1.2.3 -X main.BuildTime=$(date)`». «Подводные камни»: «…иначе шелл разобьет строку на несколько аргументов.»
- **Вердикт:** (1) Команда из условия, подставленная в `-ldflags "…"`, не собирается. (2) Причина в камне названа неверно. Внутри `"…"` шелл ничего не разбивает: `go` получает одну строку и сам делит её по пробелам, понимая вложенные одинарные или двойные кавычки.
- **Доказательство:**
  ```
  $ go build -ldflags "-X main.Version=1.2.3 -X main.BuildTime=$(date)" -o app0 .
  # app
  usage: link [options] main.o            (exit 1)
  $ printf '[%s]\n' -ldflags "-X main.Version=1.2.3 -X main.BuildTime=$(date)"
  [-ldflags]
  [-X main.Version=1.2.3 -X main.BuildTime=Thu Oct 22 06:43:58 PM +04 2026]   ← шелл передал ОДИН аргумент
  $ go build -ldflags "-X main.Version=1.2.3 -X 'main.BuildTime=$(date)'" -o app2 . && ./app2
  Версия приложения: 1.2.3
  Время сборки:      Thu Oct 22 06:43:58 PM +04 2026
  ```
  Вариант из «Кода решения» (`NOW=$(date -u +…)`, `-X 'main.BuildTime=$NOW'`) собирается и выводит `Время сборки:      2026-10-22T14:43:58Z`. `go help build`: «The -asmflags, -gccgoflags, -gcflags, and -ldflags flags accept a space-separated list of arguments … To embed spaces in an element in the list, surround it with either single or double quotes.»
- **Предлагаемая правка:** условие: «…`-ldflags "-X main.Version=1.2.3 -X 'main.BuildTime=$(date -u +%Y-%m-%dT%H:%M:%SZ)'"`…». Камень: «Строку `-ldflags` делит на аргументы сама команда `go`, по пробелам. Значение с пробелами (например, вывод `date`) берите во вложенные кавычки: `-X 'main.BuildTime=…'`. Без них `go` передаст линкеру хвост даты отдельными аргументами, и линкер упадёт с `usage: link [options] main.o`.»

### J-03 — VERIFIED
- **Где / цитата:** `05. …/022. Воспроизведение и устранение Data Race.md`, «Условие»: «Создай data race (два горутины пишут…). Запусти с `-race` и без него, сравни поведение.» В «Коде решения» только `main_fixed.go`.
- **Вердикт:** версии с гонкой и сравнения в решении нет; «два горутины» → «две горутины». Наблюдение судьи подтверждено: код 012 без `-race` 10 запусков из 10 дал ровно `2000`. Добавлю: под `-race` даже «сильная» гонка обычно даёт правильную сумму. Детектор замедляет и упорядочивает доступы, поэтому отличие проявляется в отчёте, а не в числе.
- **Доказательство:** вариант с гонкой (`/tmp/gw-2-022/racy/main.go`, ниже), `go vet` чист.
  ```
  $ go build -o norace . && for i in $(seq 10); do ./norace; done
  Итоговое значение: 144229 (ожидалось 200000)
  Итоговое значение: 187889 …
  Итоговое значение: 200000 …   (3 из 10 запусков — 200000, остальные 100801…187889)
  $ go build -race -o race . && ./race
  WARNING: DATA RACE … main.go:17 … main.go:14 …   (×2)
  Итоговое значение: 200000 (ожидалось 200000)
  Found 2 data race(s)        exit=66
  ```
  Исправленный `main_fixed.go`: `go run -race` три раза → `Итоговое безопасное значение счетчика: 100000`, exit 0, предупреждений нет.
- **Предлагаемая правка:** добавить в «Код решения» перед `main_fixed.go` файл `main_race.go` (в отдельном каталоге, иначе две `main` конфликтуют):
  ```go
  package main

  import (
  	"fmt"
  	"sync"
  )

  func main() {
  	counter := 0
  	var wg sync.WaitGroup

  	for i := 0; i < 2; i++ {
  		wg.Add(1)
  		go func() {
  			defer wg.Done()
  			for j := 0; j < 100_000; j++ {
  				counter++ // гонка: чтение-изменение-запись без синхронизации
  			}
  		}()
  	}

  	wg.Wait()
  	fmt.Printf("Итоговое значение: %d (ожидалось 200000)\n", counter)
  }
  ```
  Терминал (с пометкой «числа меняются от запуска к запуску»):
  ```bash
  go run main_race.go
  # Итоговое значение: 152166 (ожидалось 200000)   ← без -race: тихо теряются обновления
  go run -race main_race.go
  # WARNING: DATA RACE … (стек-трейсы)
  # Итоговое значение: 200000 (ожидалось 200000)
  # Found 2 data race(s)
  # exit status 66
  ```
  Шаги: «1. Пишем программу с гонкой и запускаем без `-race` несколько раз. 2. Запускаем с `-race`. 3. Исправляем `sync.Mutex`…». Исправить «два горутины» на «две горутины».

### J-04 — VERIFIED
- **Где / цитата:** `05. …/022. …md`, «Теория»: «**С `-race`:** программа мгновенно падает с точным стек-трейсом гонки.»; «…повреждение памяти (Silent Memory Corruption)…».
- **Вердикт:** (1) Неверно. По умолчанию детектор печатает отчёт, программа работает дальше, а при выходе возвращает код 66. (2) Для `int` следствие гонки — потерянные обновления (J-03: 100801…187889 вместо 200000). Порча памяти и падения характерны для гонок на многословных значениях: интерфейсах, строках, слайсах, `map`. Это педагогическое упрощение.
- **Доказательство:** код 012 под `-race`: программа дошла до `Итоговое значение: 2000`, потом `Found 2 data race(s)`, exit 66 (30 запусков: 23 × «2 гонки», 7 × «3 гонки», всегда exit 66). С `GORACE=halt_on_error=1`: после первого `WARNING: DATA RACE` строки «Итоговое значение» нет, exit 66. go.dev/doc/articles/race_detector, «Options»: «`exitcode` (default `66`)…»; «`halt_on_error` (default `0`): Controls whether the program exits after reporting first data race.»
- **Предлагаемая правка:** «**С `-race`:** детектор печатает `WARNING: DATA RACE` с двумя стек-трейсами (текущий доступ и предыдущий конфликтующий), программа продолжает работу, а при выходе завершается с кодом 66. Остановиться на первой гонке можно через `GORACE="halt_on_error=1"`.» Для «Без `-race`»: «…для счётчика — тихая потеря обновлений; для гонок на строках, слайсах, интерфейсах и `map` — порча данных и падения в случайном месте (для `map` рантайм сам падает с `fatal error: concurrent map writes`).»

### J-05 — VERIFIED
- **Где / цитата:** `03. …/011. Кросс-компиляция под Linux x86_64.md`, «На собеседовании»: «Он запустится на любом Linux-дистрибутиве (Ubuntu, Alpine, RHEL, Arch)…». `01. …/003. Компиляция в нативный исполняемый файл. go build.md`, «Теория»: «2. Выполняет статическую компоновку (линковку)»; «Полученный бинарный файл является полностью автономным.»
- **Вердикт:** ответ на собеседовании верен для бинарника, который `file` назвал `statically linked`. Но статический он не всегда. При `CGO_ENABLED=1`, по умолчанию на Linux с gcc, программа с `net` или `os/user` линкуется динамически с glibc. Тезис 003 — частный случай. Поправки судьи к G-2.4 верны.
- **Доказательство:** при `CGO_ENABLED=1` (gcc есть):
  ```
  hello (fmt)              → ELF … statically linked …            ldd: not a dynamic executable
  net.LookupHost           → ELF … dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2
                             ldd: libresolv.so.2, libc.so.6, ld-linux-x86-64.so.2
  os/user.Current          → dynamically linked
  net, CGO_ENABLED=0       → statically linked
  net, -tags netgo,osusergo → statically linked
  ```
  Динамический `net`-бинарник в `FROM scratch` (podman/crun): `exec container process (missing dynamic library?) '/app': No such file or directory`, exit 1. Текст ошибки скаута (`/bin/sh: ./app: not found`) неверен: в `scratch` нет `/bin/sh`. Docker пишет `exec /app: no such file or directory`; Docker не проверялся, проверен crun.
- **Предлагаемая правка:** 011: «…не зависит от `.so` и запустится на любом Linux с подходящим ядром. Но статическим Go-бинарник получается не всегда: при `CGO_ENABLED=1` (по умолчанию на Linux с установленным gcc) пакеты `net` и `os/user` линкуются с glibc динамически, и такой бинарник не запустится в `scratch` или на Alpine (musl). Для гарантированно статической сборки — `CGO_ENABLED=0` или `-tags netgo,osusergo`; проверка — `file` / `ldd`.» 003, п. 2: «Выполняет компоновку (линковку). Без cgo — статическую: бинарник не зависит от системных библиотек».

### J-06 — VERIFIED (с поправкой к предложению брифа)
- **Где / цитата:** `02. …/005. Основы кросс-компиляции. переменные GOOS и GOARCH.md`, «Подводные камни»: «Всегда собирайте с `CGO_ENABLED=0`.»; `06. …/024. Автоматизационный сборочный скрипт CI_CD пайплайна.md`, `ci.sh`, шаг 3 `go test -v -race -cover ./...`.
- **Вердикт:** на Linux `-race` требует cgo. С Go 1.20 cgo по умолчанию выключен, если C-компилятора нет в `PATH`, и тогда шаг 3 `ci.sh` падает. Это типичная ситуация в `golang:*-alpine` без `gcc`. Совет «всегда `CGO_ENABLED=0`» противоречит шагу 3. **Поправка к предложению брифа:** явный `CGO_ENABLED=1` без установленного gcc не помогает, ошибка лишь меняется. Нужен сам компилятор (`apk add gcc musl-dev`).
- **Доказательство:**
  ```
  $ CGO_ENABLED=0 go build -race .   → go: -race requires cgo; enable cgo by setting CGO_ENABLED=1  (exit 2)
  # PATH без gcc (только go и coreutils):
  $ go env CGO_ENABLED               → 0
  $ ./ci.sh                          → … --> [3/4] … go: -race requires cgo; enable cgo by setting CGO_ENABLED=1  (exit 2)
  $ CGO_ENABLED=1 go test -race ./... → cgo: C compiler "gcc" not found: exec: "gcc": executable file not found in $PATH
  ```
  macOS: go1.27.1 `src/cmd/go/internal/work/init.go:194`: «Note: On macOS, -race does not require cgo.»; условие `!CgoEnabled && (cfg.Goos != "darwin" || …)`. Статья go.dev/doc/articles/race_detector говорит «requires cgo to be enabled, and on non-Darwin systems requires an installed C compiler» и в части про cgo отстаёт от исходников. На macOS не запускалось. Поддерживаемые платформы (`src/internal/platform/supported.go`, `RaceDetectorSupported`): linux/{amd64, arm64, loong64, ppc64le, riscv64, s390x}, darwin/{amd64, arm64}, {freebsd, netbsd, windows}/amd64. 32-битных среди них нет, так что пункт G-3.3 верен.
- **Предлагаемая правка:** 005: «Для релизной (в т. ч. кросс-) сборки чистого Go-кода — `CGO_ENABLED=0`. Исключение — `go test -race`: на Linux и Windows детектор гонок требует cgo и установленного C-компилятора.» 024: перед шагом 3 комментарий «`-race` требует cgo и gcc; в `golang:*-alpine` установите `apk add gcc musl-dev`», шаг: `CGO_ENABLED=1 go test -v -race -cover ./...`.

### J-07 — VERIFIED
- **Где / цитата:** `01. …/001. Проверка версии Go и архитектура компилятора.md`, «На собеседовании»: «…тулчейн Go автоматически скачает официальный бинарник Go 1.23 в `$GOPATH/bin`…»
- **Вердикт:** неверно. Тулчейн скачивается как модуль `golang.org/toolchain` в кэш модулей (`GOMODCACHE`). Работает это только при `GOTOOLCHAIN=auto` (по умолчанию). При `GOTOOLCHAIN=local` сборка завершается ошибкой.
- **Доказательство:** `GOMODCACHE=/tmp/gw-2-001/modcache GOPATH=/tmp/gw-2-001/gopath GOTOOLCHAIN=go1.26.0 go version` → `go: downloading go1.26.0 (linux/amd64)`, `go version go1.26.0 linux/amd64`. Появился `modcache/golang.org/toolchain@v0.0.1-go1.26.0.linux-amd64/`, каталога `gopath/bin` нет. `go.mod` с `go 1.99.0`, `GOTOOLCHAIN=local go build .` → `go: go.mod requires go >= 1.99.0 (running go 1.27.1; GOTOOLCHAIN=local)`, exit 1. Исходник: `cmd/go/internal/toolchain/select.go:357` «Download and unpack toolchain module into module cache». go.dev/doc/toolchain: «These toolchains are packaged as special modules with module path `golang.org/toolchain`…»; «The default `GOTOOLCHAIN` setting is `auto`…».
- **Предлагаемая правка:** «…если в `go.mod` указано `go 1.23.0` (или `toolchain go1.23.x`), а локально стоит `go1.21.0`, то при `GOTOOLCHAIN=auto` (по умолчанию) команда `go` скачает тулчейн Go 1.23 как модуль `golang.org/toolchain` в кэш модулей (`$(go env GOMODCACHE)`) и перезапустит себя на нём. При `GOTOOLCHAIN=local` сборка завершится ошибкой `go.mod requires go >= 1.23.0`.»

### J-08 — VERIFIED
- **Где / цитата:** `01. …/003. …md`, «На собеседовании»: «…с бадди-аллокатором (tcmalloc-like)…»
- **Вердикт:** неверно. Аллокатор Go устроен на классах размеров (`mcache` → `mcentral` → `mheap`) и вырос из TCMalloc. Buddy-системы в нём нет.
- **Доказательство:** go1.27.1 `src/runtime/malloc.go`, шапка: «This was originally based on tcmalloc, but has diverged quite a bit.»; «Small allocation sizes (up to and including 32 kB) are rounded to one of about 70 size classes…». `grep -il buddy src/runtime/*.go` находит только `proc_test.go`, и к аллокатору это не относится.
- **Предлагаемая правка:** «…менеджер памяти на классах размеров (`mcache`/`mcentral`/`mheap`, вырос из TCMalloc)…».

### J-09 — VERIFIED
- **Где / цитата:** `01. …/003. …md`, «Решение по шагам» / «Код решения»: `go build .` → `ls -lh hello_world`; `02. …/006. Полный цикл компиляции и прямого запуска бинарника.md`: `./app` → `# Hello, World!`.
- **Вердикт:** в 002 создаётся только `main.go`, без `go.mod`. `go build .` в таком каталоге падает. Имя `hello_world` получится, только если модуль так назван. Вывод 006 не совпадает с программой из 002.
- **Доказательство:** `/tmp/gw-2-002` (только `main.go`): `go build .` → `go: go.mod file not found in current directory or any parent directory; see 'go help modules'`, exit 1. `go build main.go` → exit 0, бинарник `main`. С `go mod init hello_world`: бинарник `hello_world`, запуск печатает `Hello, World! Привет из компилятора Go.`
- **Предлагаемая правка:** 003, шаг 1: «Инициализируем модуль `go mod init hello_world` (без `go.mod` команда `go build .` завершится ошибкой `go.mod file not found`) и выполняем `go build .`». В терминал: `go mod init hello_world` перед `go build .`. 006: `# Hello, World! Привет из компилятора Go.`

### J-10 — VERIFIED
- **Где / цитата:** `01. …/004. Сборка модуля hello_mod и прямой запуск из консоли.md`, «Теория»: «…**имя модуля** (или имя текущей директории).»; «Под капотом»: «Имя выходного файла берется из директивы `module <name>`… (последний сегмент пути).»
- **Вердикт:** правило неполно. Имя берётся из последнего элемента пути импорта **пакета** без суффикса мажорной версии, а не модуля. «Имя текущей директории» в режиме модулей неверно: так было только в GOPATH-режиме, где пакет вне GOPATH получал путь `_/abs/dir`.
- **Доказательство:** `go help build`: «…named after the last non-major-version component of the package import path… 'go build example.com/foo/v2' writes 'foo'…». Запуски: модуль `hello_mod` в каталоге `otherdir` → `hello_mod`; модуль `example.com/foo/v2` в каталоге `m1` → `foo`; `go build ./cmd/worker` → `worker`; `go build b.go a.go` → `b` (по первому файлу).
- **Предлагаемая правка:** «Под капотом»: «Имя бинарника — последний элемент пути импорта собираемого пакета без суффикса `/vN`: для пакета в корне модуля `hello_mod` это `hello_mod`, для `./cmd/worker` — `worker`, для модуля `example.com/foo/v2` — `foo`. Если переданы файлы (`go build a.go b.go`), имя берётся по первому файлу.» Из «Теории» убрать «(или имя текущей директории)».

### J-11 — VERIFIED (с дополнением, см. F-01)
- **Где / цитата:** `01. …/002. Мгновенный запуск.md`, «Под капотом»: «`WORK=/tmp/go-build123456789/b001/` … После завершения процесса `go run` автоматически очищает этот каталог.»
- **Вердикт:** с `-work` каталог как раз **не удаляется**. Печатается корень `WORK=/tmp/go-buildNNN` без `/b001/`. Имя `exe/main` верно для `go run main.go`: файл `b001/exe/main`, а у `go build -x` в том же месте `a.out`.
- **Доказательство:** `go help build`: «-work print the name of the temporary work directory and do not delete it when exiting.» С пустым `GOCACHE`: `go run -work main.go` → `WORK=/tmp/go-build539397179`; после выхода существует `/tmp/go-build539397179/b001/exe/main` и ещё ~60 каталогов `bNNN`. С прогретым кэшем каталог `WORK` пуст (F-01).
- **Предлагаемая правка:** «С флагом `-work` (`go run -work main.go`) Go печатает путь вида `WORK=/tmp/go-build123456789` и **не удаляет** этот каталог после выхода: бинарник остаётся в `$WORK/b001/exe/main`. Без `-work` временный каталог удаляется автоматически. С Go 1.24 собранный `go run` бинарник ещё и кэшируется в `GOCACHE`, поэтому при повторном запуске без изменений `WORK` будет пустым.»

### J-12 — VERIFIED
- **Где / цитата:** `04. …/015. Хронология выполнения. функция init() vs main().md`, «На собеседовании»: «…в главном системном потоке `M0` … до запуска горутин пользовательского кода.»; `04. …/017. Ошибка повторного объявления точки входа.md`, «Теория»: «…запрещает переопределение любых идентификаторов на уровне пакета.»
- **Вердикт:** главный поток — верно. «До запуска горутин пользовательского кода» — неверно: `init` может сам запускать горутины. Порядок инициализации не показан. В 017 исключение — `init` и `_`, их можно объявлять многократно.
- **Доказательство:** спецификация go1.27.1 (`doc/go_spec.html:8418`): «An `init` function may launch other goroutines, which can run concurrently with the initialization code.» `src/runtime/proc.go:183`: «Lock the main goroutine onto this, the main OS thread, during initialization.», затем проверка `if mp != &m0 { throw("runtime.main not on m0") }`. Запуск (`/tmp/gw-2-015b`: `a.go` с `var a`, двумя `init`, второй файл `b.go` с `var b` и `init`; в первом `init` горутина отправляет в канал):
  ```
  var a
  var b
  init #1 в a.go
  init #1 получил из горутины: 1
  init #2 в a.go
  init в b.go
  main
  ```
  Файл с `func init() {}` ×2 и `var _ = 1`, `var _ = 2` собирается без ошибок.
- **Предлагаемая правка:** 015: «Функции `init()` выполняются последовательно в главной горутине, привязанной на время инициализации к главному потоку ОС (`m0`). Порядок: сначала переменные пакета (в порядке зависимостей), затем все `init` пакета в порядке файлов, переданных компилятору, и в порядке объявления внутри файла; импортируемые пакеты — раньше импортирующих. `init` может запускать горутины, они работают параллельно с инициализацией, но `main.main` стартует только после завершения всех `init`.» 017: «…запрещает повторное объявление идентификаторов на уровне пакета (исключения — `init`, которых может быть сколько угодно, и пустой идентификатор `_`).»

### J-13 — VERIFIED
- **Где / цитата:** `03. …/013. Статический анализ и проверка антипаттернов.md`, «Теория»: «Потерянный возврат ошибок; Ошибочные булевы условия (`if a == a`).»; «Под капотом»: «`go vet` использует движок AST и SSA-графов…».
- **Вердикт:** `go vet` не ловит ни проигнорированный `error`, ни `if a == a`. SSA в `go vet` не используется. Анализаторы работают по AST и информации о типах, некоторые (`lostcancel`) — по графу потока управления (`go/cfg`). В решении нет кода, на котором vet что-то нашёл бы.
- **Доказательство:** файл `/tmp/gw-2-013/main.go` с `if a == a`, `a > 1 || a > 1`, `os.Remove(...)` без проверки, `Printf("%d", "str")`, `Println("… %d")`, передачей структуры с `sync.Mutex` по значению:
  ```
  main.go:21:5: redundant or: a > 1 || a > 1
  main.go:14:16: byValue passes lock by value: vetdemo.S contains sync.Mutex
  main.go:28:22: call of byValue copies lock value: vetdemo.S contains sync.Mutex
  main.go:25:14: fmt.Printf format %d has arg "str" of wrong type string
  main.go:26:2: fmt.Println call has possible Printf formatting directive %d
  (exit 1)
  ```
  На `if a == a` и `os.Remove` предупреждений нет. В go1.27.1 вендорится только `golang.org/x/tools/go/{analysis,ast,cfg,types}`, пакета `go/ssa` в `src/cmd/vendor` нет, и ни один анализатор `passes/*` не требует `buildssa`. `lostcancel` требует `ctrlflow.Analyzer` (`go/cfg`). Список анализаторов — `go tool vet help`.
- **Предлагаемая правка:** список в «Теории»: «несоответствие спецификаторов и аргументов `Printf` (`printf`); копирование мьютексов по значению (`copylocks`); невызванная `cancel` от `context.WithCancel` (`lostcancel`); избыточные или противоречивые булевы выражения (`a > 1 || a > 1`, `bools`); небуферизованный канал в `signal.Notify` (`sigchanyzer`); недостижимый код (`unreachable`). Проигнорированные ошибки ловит `errcheck`, самосравнение `a == a` — `staticcheck` (SA4000); оба входят в `golangci-lint`.» «Под капотом»: «`go vet` запускает набор анализаторов `golang.org/x/tools/go/analysis` по AST и информации о типах; некоторым (`lostcancel`) нужен граф потока управления (`go/cfg`)». В «Код решения» — файл с дефектами и вывод vet, как выше.

### J-14 — VERIFIED
- **Где / цитата:** `05. …/020. Реализация подкоманд (Subcommands).md`, «Подводные камни»: «Передача в `cmd.Parse(os.Args[1:])` … приведет к ошибке разбора…».
- **Вердикт:** ошибки нет. `add` — не флаг, разбор на нём останавливается, все флаги остаются в `Args()`, `x` и `y` молча равны 0. Ловушка хуже, чем описано. Расхождение «Условие» (`--x 5 --y 3`) ↔ «Терминал» (`--x=15 --y=27`) — вопрос данных, обе формы работают.
- **Доказательство:** `go doc flag`: «Flag parsing stops just before the first non-flag argument…». Код 020 с заменой на `os.Args[1:]`: `./app1 add --x 5 --y 3` → `0 + 0 = 0`, exit 0. При ошибке разбора с `flag.ExitOnError` процесс завершился бы с кодом 2: `./app add --z 1` → `flag provided but not defined: -z`, exit 2. Значит, `Parse` ошибки не вернул. Оригинал: `add --x 5 --y 3` → `5 + 3 = 8`, `sub --x 5 --y 3` → `5 - 3 = 2`; `add --x=15 --y=27` → `15 + 27 = 42`; `sub --x=100 --y=42` → `100 - 42 = 58`.
- **Предлагаемая правка:** «Передача `os.Args[1:]` вместо `os.Args[2:]` не даст никакой ошибки: имя подкоманды `add` — не флаг, `flag` прекратит разбор на нём, все флаги останутся неразобранными в `cmd.Args()`, а `x` и `y` молча сохранят значения по умолчанию (`0 + 0 = 0`).» В «Терминал» добавить пример из условия: `go run . add --x 5 --y 3` → `# 5 + 3 = 8`.

### J-15 — VERIFIED
- **Где / цитата:** `05. …/019. Парсинг аргументов CLI через стандартный пакет.md`, «Подводные камни» (упущение).
- **Вердикт:** ловушка булевых флагов реальна и в книге не описана.
- **Доказательство:** `go doc flag`, «Command line flag syntax»: «`-flag x  // non-boolean flags only` … You must use the -flag=false form to turn off a boolean flag.» Запуск кода 019: `./app -verbose false -name=bob` →
  ```
  [DEBUG] Режим подробного логирования включен
  [DEBUG] Количество переданных аргументов: 1
  Пользователь: Инженер, Возраст: 25 лет
  ```
  `verbose` стал `true`, `-name=bob` не разобран. `./app -verbose=false -name=bob` → `Пользователь: bob, Возраст: 25 лет`. Вывод «Терминала» 019 совпадает побайтно.
- **Предлагаемая правка:** добавить камень: «Булев флаг нельзя выключить через пробел: `-verbose false` включит `verbose`, а `false` станет первым позиционным аргументом, и разбор остальных флагов (`-name=bob`) на нём остановится. Пишите `-verbose=false`.»

### J-16 — VERIFIED
- **Где / цитата:** `05. …/022. …md`, «На собеседовании»: «…`atomic.AddInt64` работает в 2–4 раза быстрее мьютекса, так как не требует аллокации структуры блокировки и переключения контекста горутины.»
- **Вердикт:** причина неверна: `sync.Mutex` ничего не аллоцирует. Цифра зависит от числа конкурирующих горутин: без конкуренции разница около 1,9 раза, при 24 потоках — около 5,3 раза. Ограничение `atomic` (одна переменная, а не инвариант из нескольких полей) не упомянуто.
- **Доказательство:** go1.27.1 `src/sync/mutex.go`: `type Mutex struct { _ noCopy; mu isync.Mutex }`; `src/internal/sync/mutex.go`: `type Mutex struct { state int32; sema uint32 }`; fast path в `Lock`: `atomic.CompareAndSwapInt32(&m.state, 0, mutexLocked)`. Бенчмарк (`b.RunParallel`, `-benchmem -cpu 1,4,8,24`, i9-12900K):
  ```
  BenchmarkMutex        11.61 ns/op  0 B/op  0 allocs/op
  BenchmarkMutex-4      22.16 ns/op  0 B/op  0 allocs/op
  BenchmarkMutex-8      36.91 ns/op  0 B/op  0 allocs/op
  BenchmarkMutex-24     63.29 ns/op  0 B/op  0 allocs/op
  BenchmarkAtomic        6.114 ns/op 0 B/op  0 allocs/op
  BenchmarkAtomic-4      8.639 ns/op
  BenchmarkAtomic-8      9.759 ns/op
  BenchmarkAtomic-24    11.93 ns/op
  ```
- **Предлагаемая правка:** «Для одиночного счётчика `atomic.Int64.Add` (или `atomic.AddInt64`) обычно быстрее мьютекса: это одна атомарная инструкция (`LOCK XADD`), тогда как `Mutex` — минимум CAS на захват и атомарная операция на освобождение, а при конкуренции горутины ещё и паркуются. Ни то ни другое не аллоцирует память. Разница растёт с числом конкурирующих ядер (на 24 потоках — порядка 5 раз, без конкуренции — около 2 раз; меряйте `go test -bench`). Ограничение: атомик защищает одну переменную; инвариант из нескольких полей требует мьютекса.»

### J-17 — VERIFIED
- **Где / цитата:** `03. …/012. Детектор состояний гонки (Data Race Detector).md`, «Терминал»: «Write at … main.go:20 … Previous Write … main.go:13 … Found 1 data race(s)»; `03. …/011. …md`, «Терминал»: «…statically linked, not stripped».
- **Вердикт:** `counter++` стоит в строках 14 и 21, вывод книги не воспроизводится. Число гонок 2 или 3, третья — между горутиной и чтением в `main` (строка 26) из-за синхронизации `time.Sleep`. В книге нет строки итога и кода 66. Вывод `file` в 011 устарел.
- **Доказательство:** `go run -race main.go` (код 012 дословно):
  ```
  WARNING: DATA RACE
  Read at 0x00c00011e028 by goroutine 9:
    main.main.func2()  …/main.go:21 +0x37
  Previous write at 0x00c00011e028 by goroutine 8:
    main.main.func1()  …/main.go:14 +0x49
  Goroutine 9 (running) created at: main.main() …/main.go:19
  Goroutine 8 (finished) created at: main.main() …/main.go:12
  …
  WARNING: DATA RACE
  Read at 0x00c00011e028 by main goroutine:
    main.main()  …/main.go:26 +0x124
  …
  Итоговое значение: 2000
  Found 3 data race(s)
  exit status 66
  ```
  30 запусков: 23 × `Found 2`, 7 × `Found 3`. `file` (5.46): `app-linux: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=…, BuildID[sha1]=…, with debug_info, not stripped`.
- **Предлагаемая правка:** в 012 заменить `time.Sleep` на `sync.WaitGroup` (тогда гонка с `main` исчезнет) и дать фактический вывод с пометкой «адреса, номера горутин и число найденных гонок меняются от запуска к запуску», с заголовками `Goroutine N … created at`, строкой `Итоговое значение: 2000`, `Found 2 data race(s)` и `exit status 66`. В 011: `# app-linux: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=…, with debug_info, not stripped`.

### J-18 — VERIFIED (пп. 2–3; п. 1 — только по документации, см. § 3)
- **Где / цитата:** `06. …/025. Многоэтапная Docker-контейнеризация.md`: `FROM golang:1.22-alpine AS builder`; `RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \`.
- **Вердикт:** (2) Go 1.22 не поддерживается. (3) Без `-trimpath` в бинарник попадают пути сборочного контейнера. (1) Жёсткий `GOARCH=amd64` ломает multi-arch-сборку. Запуском не проверено: нет qemu/binfmt для `--platform linux/arm64`. Код на amd64 корректен: образ собран, контейнер обслужил запрос.
- **Доказательство:** go.dev/doc/devel/release: «Each major Go release is supported until there are two newer major releases.» go1.27.0 вышел 2026-08-19, go1.26.0 — 2026-02-10; последний выпуск 1.22 — go1.22.12 (2025-02-04). Поддержка 1.22 кончилась с выходом 1.24. `podman run golang:1.22-alpine go version` → `go version go1.22.12 linux/amd64`. Сборка `podman build` (сервер из 023): успешно, `/server` внутри образа содержит строку `/app/main.go`. Локально `go build -ldflags="-s -w"` даёт 1 вхождение пути сборки, с `-trimpath` — 0.
- **Предлагаемая правка:**
  ```dockerfile
  FROM --platform=$BUILDPLATFORM golang:1.27-alpine AS builder
  ARG TARGETOS TARGETARCH
  …
  RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build \
      -trimpath -ldflags="-s -w -X main.Version=v1.0.0" \
      -o /bin/server .
  ```
  В «Теории» `golang:1.22-alpine` → `golang:1.27-alpine` (или «актуальная версия»). Если multi-arch не нужен, достаточно убрать `GOARCH=amd64`: тогда архитектура совпадёт с платформой сборочного контейнера.

### J-19 — VERIFIED (с уточнением текста ошибки; про побег из контейнера — NOT CHECKED, § 3)
- **Где / цитата:** `06. …/025. …md`, «На собеседовании»: «…выполнит побег из контейнера (Container Escape), он получит права root на хостовой ноде Kubernetes.»; комментарий `# Запуск от непривилегированного пользователя nobody (UID 65534)`.
- **Вердикт:** «получит root» — преувеличение: UID 0 без user namespaces увеличивает ущерб от побега, но не гарантирует root на ноде. Почему `USER` задан числом, не объяснено. Поправка судьи к G-2.5 верна: в `os/user` при `CGO_ENABLED=0` возвращается **ошибка**, не паника. Точный текст отличается от брифа: в сообщении перечислены только недостающие переменные.
- **Доказательство:** `FROM scratch` + `USER nobody` → `Error: unable to find user nobody: no matching entries in passwd file`, exit 126 (podman). С `USER 65534:65534` программа с `user.Current()` (`CGO_ENABLED=0`) печатает `<nil> user: Current requires cgo or $USER set in environment` и не падает. Исходник go1.27.1 `src/os/user/lookup_stubs.go:65`: `fmt.Errorf("user: Current requires cgo or %s set in environment", missing)`. Образ 025: `podman image inspect` → `User: 65534:65534`.
- **Предлагаемая правка:** «…при побеге из контейнера процесс с UID 0 (если не включены user namespaces / rootless) может получить права root на ноде…». К `USER`: «В `scratch` нет `/etc/passwd`, поэтому пользователь задаётся числом: `USER nobody` даст ошибку запуска `unable to find user nobody`.»

### J-20 — VERIFIED
- **Где / цитата:** `06. …/025. …md`: H1 «…от Alpine к 5 МБ Scratch», «Теория»: «минимальный `alpine` (5 МБ)», «Итоговый размер … **10–15 МБ**», «Терминал»: `12.4MB`; `000. О главе.md`: «от 5 МБ Scratch»; `06. …/00. О разделе.md`: «Dockerfile сборка от 5 МБ».
- **Вердикт:** три разные цифры; измеренный размер образа — около 6 МБ, и он зависит от приложения.
- **Доказательство:** Dockerfile 025 дословно, приложение — сервер из 023. `podman images` → `localhost/go-service:v1 5.86 MB`. Состав: `/server` 4 759 704 байт, `ca-certificates.crt` 222 597 байт, `/usr/share/zoneinfo` 1,4 МБ (`du -sh`). `alpine:latest` (3.24.3) — 8,72 МБ без сжатия. Размеры podman показывает без сжатия; Docker не проверялся.
- **Предлагаемая правка:** «Итоговый размер образа — несколько мегабайт: размер бинарника плюс ~1,5 МБ сертификатов и `zoneinfo` (для HTTP-сервера из задачи 023 — около 6 МБ)». `alpine` — «около 8 МБ в распакованном виде». В «Терминале» — `5.86MB` с пометкой «зависит от приложения». H1 и описания главы и раздела: «≈ 6 МБ» или «несколько МБ». H1 — заголовок страницы, имя файла от него не зависит.

### J-21 — VERIFIED
- **Где / цитата:** `06. …/023. Graceful Shutdown.md`, «Код решения»: `if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed { fmt.Printf("Ошибка сервера: %v\n", err) }`.
- **Вердикт:** при занятом порте процесс жив, но сервера нет: он ждёт сигнал, а получив его, рапортует об успешном graceful shutdown. Ещё одна мелочь: «🚀 Сервер запущен» печатается до успешного `Listen`. `signal.Notify` с буфером 1 не устарел, поправка к G-4.5 верна.
- **Доказательство:** порт 8080 занят другим процессом, `timeout 3 ./srv`:
  ```
  🚀 Сервер запущен на порту :8080...
  Ошибка сервера: listen tcp :8080: bind: address already in use
  ⚠️  Получен сигнал [terminated]. Начинаем Graceful Shutdown...
  ✔ Все клиентские соединения успешно закрыты.
  🛑 Сервер корректно остановлен. Выход.
  exit=124   (висел до SIGTERM от timeout)
  ```
  Штатные сценарии (`-race`): SIGINT в простое → вывод совпадает с «Терминалом», exit 0. SIGTERM при запросе в обработке → `curl` получил `200`, `Запрос успешно обработан!` за 2,0 с, сервер дождался запроса и завершился с кодом 0.
- **Предлагаемая правка:**
  ```go
  	serverErr := make(chan error, 1)
  	go func() {
  		fmt.Println("🚀 Сервер запускается на порту :8080...")
  		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
  			serverErr <- err
  		}
  	}()

  	quit := make(chan os.Signal, 1)
  	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

  	select {
  	case err := <-serverErr:
  		fmt.Fprintf(os.Stderr, "Ошибка сервера: %v\n", err)
  		os.Exit(1)
  	case sig := <-quit:
  		fmt.Printf("\n⚠️  Получен сигнал [%v]. Начинаем Graceful Shutdown...\n", sig)
  	}
  ```
  Плюс импорт `errors`, остальное без изменений. Ожидаемое при занятом порте: `Ошибка сервера: listen tcp :8080: bind: address already in use`, exit 1. Штатный «Терминал» не меняется, кроме первой строки («запускается»). `signal.NotifyContext` (Go 1.16+) можно упомянуть как альтернативу.

### J-22 — VERIFIED
- **Где / цитата:** `06. …/023. …md`, «На собеседовании»: «K8s посылает старому поду сигнал `SIGTERM` и одновременно удаляет его из эндпоинтов…»
- **Вердикт:** сказанное верно (30 с по умолчанию, одновременность). Не хватает следствия: исключение из балансировки распространяется асинхронно, запросы могут приходить после `SIGTERM`. И не упомянут `preStop`, который выполняется **до** `SIGTERM`.
- **Доказательство:** kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/, «Pod Termination Flow»: «A Pod is granted a term to terminate gracefully, which defaults to 30 seconds.»; п. 2.1 — `preStop` выполняется kubelet'ом, п. 2.2 — затем TERM; п. 3: «At the same time as the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects…»; «Any endpoints that represent the terminating Pods are not immediately removed from EndpointSlices…».
- **Предлагаемая правка:** добавить: «Исключение пода из балансировки (EndpointSlice → kube-proxy / ingress) распространяется асинхронно, поэтому после `SIGTERM` ещё несколько секунд могут приходить новые запросы. Практика: `preStop`-хук с короткой паузой (`sleep 5–10`), который kubelet выполняет до отправки `SIGTERM`, и продолжение обслуживания запросов в начале shutdown.»

### J-23 — VERIFIED
- **Где / цитата:** `03. …/012. …md`, «Подводные камни»: «…увеличивает потребление памяти в 5–10 раз и замедляет выполнение в 2–3 раза.»
- **Вердикт:** вторая цифра неверна.
- **Доказательство:** go.dev/doc/articles/race_detector, «Runtime Overhead»: «…memory usage may increase by 5-10x and execution time by 2-20x.»
- **Предлагаемая правка:** «…в 5–10 раз и замедляет выполнение в 2–20 раз (по данным документации Go)».

### J-24 — VERIFIED
- **Где / цитата:** `05. …/022. …md`, «Подводные камни»: «…программа завершится аварийно или не выполнит работу.»
- **Вердикт:** аварийного завершения нет. Возврат из `main` завершает процесс с кодом 0, горутины обрываются.
- **Доказательство:** спецификация, «Program execution»: «When that function invocation returns, the program exits. It does not wait for other (non-main) goroutines to complete.» Запуск (100 горутин × 1000 инкрементов под мьютексом, `wg.Wait()` убран): `n = 3910`, `n = 1552`, `n = 3896`, каждый раз exit 0.
- **Предлагаемая правка:** «Забыть `wg.Wait()`: `main()` вернётся раньше горутин, процесс завершится с кодом 0, а горутины будут молча оборваны: работа не доделана, ошибки нет.»

### J-25 — VERIFIED
- **Где / цитата:** `05. …/021. …md`, «Подводные камни» / «Под капотом» (упущение).
- **Вердикт:** `-X` молча не действует при неконстантной инициализации. `debug.ReadBuildInfo` и `go version -m` дают VCS-данные без `-ldflags`.
- **Доказательство:** `go doc cmd/link`: «This is only effective if the variable is declared in the source code either uninitialized or initialized to a constant string expression. -X will not work if the initializer makes a function call or refers to other variables.» `var V2 = fmt.Sprint("dev")` + `-ldflags "-X main.V2=set"` → вывод `V2 = dev`, сборка без ошибок. В git-репозитории `go version -m app6` → `build vcs=git`, `vcs.revision=1fa9d04…`, `vcs.time=2026-10-22T14:44:06Z`, `vcs.modified=false`. Попутно подтверждён ответ «На собеседовании»: `-X 'app/config.version=v9 beta'` для неэкспортированной переменной другого пакета → `v9 beta`.
- **Предлагаемая правка:** камень: «`-X` работает только для переменной типа `string`, которая не инициализирована или инициализирована константным выражением. При `var Version = getVersion()` флаг молча проигнорируется.» Абзац в «Под капотом»: «С Go 1.18 `go build` в git-репозитории сам вшивает `vcs.revision`, `vcs.time`, `vcs.modified` — их читает `runtime/debug.ReadBuildInfo()` и показывает `go version -m ./app`.»

### J-26 — VERIFIED (вопрос о Delve решён запуском)
- **Где / цитата:** `04. …/018. Стриппинг отладочной информации.md`, «Подводные камни»: «…к нему нельзя будет подключиться интерактивным отладчиком `dlv attach`…»; «Теория»: «`-s` … удаляет таблицу символов; `-w` … DWARF».
- **Вердикт:** (1) Подключиться **можно**, но отлаживать практически нечего: нет символов и DWARF, не работают ни список горутин, ни точки останова по имени. (2) С Go 1.22 `-s` включает `-w`.
- **Доказательство:** Delve 1.27.2, `dlv attach <pid>` к бинарнику `-ldflags="-s -w"`:
  ```
  Warning: no debug info found, some functionality will be missing such as stack traces and variable evaluation.
  (dlv) goroutines        → Command failed: could not find goroutine array
  (dlv) break main.work   → Command failed: location "main.work" not found
  ```
  К обычному бинарнику `goroutines` выводит список (`[6 goroutines]`). `src/cmd/link/internal/ld/main.go:274`: `*FlagW = *FlagS // -s implies -w if not explicitly set`. Размеры (go1.27.1): обычный 2 342 361 байт, `-s -w` и `-s` — по 1 511 584 (идентичны), `-w` — 1 639 487. Секции (`readelf -S`): обычный — `.debug_*`, `.symtab`, `.gopclntab`; `-s` и `-s -w` — только `.gopclntab`; `-w` — `.symtab`, `.gopclntab`. Уменьшение −35,5 % согласуется с «30–40 %». Паника в стрипнутом бинарнике: `main.main() /tmp/gw-2-018/main.go:12 +0x69`, номера строк есть, «На собеседовании» подтверждён.
- **Предлагаемая правка:** «Бинарник `-s -w` можно подключить к `dlv attach`, но Delve предупредит `no debug info found`: не будет ни списка горутин, ни точек останова по именам функций, ни значений переменных. Для отладки собирайте без `-s -w`.» В «Теорию»: «С Go 1.22 `-s` подразумевает `-w`; запись `-s -w` по-прежнему принята как явная.»

### J-27 — VERIFIED
- **Где / цитата:** `02. …/007. Установка утилит в систему через go install.md`, «Под капотом»: «`go install` атомарно записывает бинарник во временный файл в `$GOBIN` и делает операцию `rename`…»
- **Вердикт:** неверно в типичной конфигурации. `go install` переименовывает `$WORK/b001/exe/a.out` прямо в `$GOBIN/<имя>`, только если `rename` возможен. Если каталог `WORK` на другой файловой системе (Fedora: `/tmp` — tmpfs, `~/go/bin` — диск), источник в кэше сборки, это Windows или у каталога setgid, то файл **копируется**: старый удаляется, новый создаётся с `O_TRUNC` и пишется. Временного файла в `$GOBIN` нет; `<dst>-go-tmp-umask` — пустой пробный файл для определения umask.
- **Доказательство:** go1.27.1 `src/cmd/go/internal/work/shell.go`, `moveOrCopyFile` (стр. 119–182) и `CopyFile` (`mayberemovefile(dst)`, затем `os.OpenFile(dst, O_WRONLY|O_CREATE|O_TRUNC)`, затем `io.Copy`). Запуски `go install -a -x .`: `GOBIN=/tmp/gw-2-007/gobin` (та же ФС) → `mv $WORK/b001/exe/a.out /tmp/gw-2-007/gobin/hello_mod`; `GOBIN=$HOME/.cache/gw-2-gobin-test` (btrfs) → `cp $WORK/b001/exe/a.out /home/ut/.cache/gw-2-gobin-test/hello_mod`.
- **Предлагаемая правка:** «`go install` переносит собранный бинарник в `$GOBIN` (или `$GOPATH/bin`): через `rename`, если временный каталог сборки на той же файловой системе, иначе копированием. При копировании старый файл сначала удаляется (unlink), поэтому уже запущенные процессы продолжают работать со старой копией, но сама замена не атомарна.»

### J-28 — VERIFIED
- **Где / цитата:** `02. …/009. …md`, «Под капотом»: «Флаг `-o` передается линкеру `go tool link -o bin/myapp`.»
- **Вердикт:** линкер пишет во временный каталог, затем `go` создаёт каталог назначения и переносит файл.
- **Доказательство:** `go build -a -x -o bin/myapp .`:
  ```
  …/link -o $WORK/b001/exe/a.out -importcfg … $WORK/b001/_pkg_.a
  mkdir -p bin/
  mv $WORK/b001/exe/a.out bin/myapp
  ```
  `go build -o bin/myapp .` без `mkdir -p bin` → exit 0, `./bin/myapp` работает. `go build -o /dev/null .` → exit 0 («На собеседовании» верен).
- **Предлагаемая правка:** «Линкер (`go tool link`) пишет бинарник во временный `$WORK/b001/exe/a.out`; затем команда `go` создаёт каталог `bin` (если его нет) и переносит файл в `bin/myapp`. Это видно в `go build -x`.»

### J-29 — VERIFIED
- **Где / цитата:** `03. …/014. Матричная кросс-компиляция под Windows и Linux.md`, «Под капотом»: «…генератор инструкций Thumb/AArch64 для ARM».
- **Вердикт:** бэкенд `GOARCH=arm` генерирует инструкции ARM (A32), не Thumb.
- **Доказательство:** `grep -rli thumb` по `src/cmd/internal/obj/arm`, `src/cmd/compile/internal/arm`, `src/cmd/link/internal/arm` (go1.27.1) — ни одного совпадения. Скрипт 014 выполнен: 4 бинарника, `file` подтверждает `x86-64`, `ARM aarch64`, `PE32+ … x86-64`, `Mach-O 64-bit arm64`.
- **Предлагаемая правка:** «…(например, генератор инструкций ARM для `GOARCH=arm` и AArch64 для `GOARCH=arm64`)».

### J-30 — VERIFIED
- **Где / цитата:** `04. …/016. Многофайловый пакет main. main.go и utils.go.md`, «Теория»: «…областью видимости неэкспортированных функций является весь пакет… `utils.go` объявляет `func SayHi()`».
- **Вердикт:** `SayHi` экспортирована (заглавная буква). Правило о видимости в пакете верно для любых имён верхнего уровня. Код из условия работает: `go build -o server . && ./server` → `Привет из файла utils.go!`; `go run main.go` → `./main.go:4:2: undefined: SayHi` (подводный камень подтверждён).
- **Доказательство:** спецификация, «Declarations and scope»: «The scope of an identifier denoting a constant, type, variable, or function (but not method) declared at top level (outside any function) is the package block.» (`doc/go_spec.html:2211`)
- **Предлагаемая правка:** «В Go область видимости любого идентификатора верхнего уровня (экспортированного `SayHi` или неэкспортированного `sayHi`) — весь пакет, независимо от разбиения по файлам…».

### J-31 — VERIFIED
- **Где / цитата:** `06. …/024. …md`: «Условие» «bash/powershell»; `echo "✔ Бинарник успешно собран в папку bin/server"`; «На собеседовании»: `go generate ./... && git diff --exit-code`.
- **Вердикт:** (1) Структурный вопрос: «/» допускает выбор, решение на bash формально подходит. (2) `bin/server` — файл. (3) `git diff --exit-code` не видит новые неотслеживаемые файлы.
- **Доказательство:** `ci.sh` выполнен целиком: все 4 шага, exit 0. С неотформатированным `bad.go` → `✖ Ошибка: следующие файлы не отформатированы: bad.go`, exit 1. В git-репозитории после создания нового `gen.go`: `git diff --exit-code` → exit 0, а `git status --porcelain` → `?? gen.go`.
- **Предлагаемая правка:** `echo "✔ Бинарник успешно собран: bin/server"`. «На собеседовании»: «…`go generate ./... && git diff --exit-code && test -z "$(git status --porcelain)"`: `git diff` не видит новые неотслеживаемые файлы, поэтому нужна и проверка `git status --porcelain`.» По (1) — решение за редактором: убрать «powershell» из условия или добавить `ci.ps1`.

### J-32 — VERIFIED
- **Где / цитата:** `02. …/008. Настройка переменной PATH для каталога $GOPATH_bin.md`, «Код решения» (`export PATH=$PATH:$GOPATH/bin`).
- **Вердикт:** если задан `GOBIN`, `go install` пишет туда, и совет 008 не помогает. В этой же среде задан `GOBIN=/home/ut/go/bin`, так что случай типичный.
- **Доказательство:** `GOBIN=/tmp/gw-2-007/gobin go install .` → бинарник в `gobin/`; `GOBIN= GOPATH=/tmp/gw-2-007/gp go install .` → `gp/bin/hello_mod`. `go env GOBIN` на машине проверки → `/home/ut/go/bin`. Ответ «На собеседовании» тоже подтверждён: `GOBIN=/tmp/gw-2-008/bin go install github.com/rakyll/hey@latest` → `go: downloading github.com/rakyll/hey v0.1.5`, бинарник `hey`.
- **Предлагаемая правка:** в `~/.bashrc`: `export PATH="$PATH:$(go env GOPATH)/bin"` и примечание: «если задан `GOBIN`, добавьте в `PATH` его: `$(go env GOBIN)`».

### J-33 — VERIFIED
- **Где / цитата:** `01. …/001. …md`, «Теория» и «Терминал»: `go1.22.5`.
- **Вердикт:** формат вывода не изменился, версия устарела (см. J-18).
- **Доказательство:** `go version` → `go version go1.27.1 linux/amd64`; `go env GOVERSION` → `go1.27.1`. Политика поддержки — см. J-18.
- **Предлагаемая правка:** `go1.22.5` → `go1.27.1` (в «Теории» и обоих местах «Терминала»), либо пометка «пример вывода; версия у вас будет своей».

### J-34 — OPINION / NOT A FACT CLAIM
- **Где:** 018/025 (`-trimpath`), 021 (`debug.ReadBuildInfo`, `-buildvcs`), 001 (`GOTOOLCHAIN`), 011 (`-tags netgo,osusergo`).
- **Вердикт:** предложения по содержанию, не ошибки. Факты, на которые они опираются, проверены запуском: `-trimpath` убирает пути сборки (J-18), VCS-данные в `go version -m` (J-25), скачивание тулчейна (J-07), статическая сборка с `netgo,osusergo` (J-05).
- **Доказательство:** см. указанные находки.
- **Предлагаемая правка:** вносить абзацами в соответствующие задачи вместе с правками J-05, J-07, J-18, J-25.

### J-35 — VERIFIED
- **Где / цитата:** `04. …/018. …md` и `06. …/025. …md`, блок «### Исходная формулировка».
- **Вердикт:** тексты отличаются только разметкой. В 018 — `**Сборка с флагами**:` и бэктики вокруг `-ldflags="-s -w"`, в 025 — бэктики вокруг `scratch` и `alpine`. Смысл одинаков.
- **Доказательство:** построчное сравнение текущих файлов.
- **Предлагаемая правка:** перенести в «Условие» вариант с разметкой (там `-ldflags="-s -w"` в коде, это и для § 3.1 AGENTS лучше), блок «Исходная формулировка» удалить.

---

## 3. Непроверенное (NOT CHECKED)

| Что | Причина |
|---|---|
| J-18 п. 1: amd64-бинарник в образе, помеченном arm64, при `--platform linux/arm64` | в среде нет qemu/binfmt для arm64; вывод сделан по документации Docker (автоматические `TARGETOS`/`TARGETARCH`) и логике `GOARCH` |
| J-19: «побег из контейнера → root на ноде» | требует стенда Kubernetes и эксплойта; утверждение ослаблено по общему знанию о user namespaces, не по запуску |
| J-06: `-race` без cgo на macOS | нет macOS; проверено только по исходнику `cmd/go/internal/work/init.go:194` (статья на go.dev этому противоречит) |
| J-20 / J-05: поведение именно Docker (размеры в `docker images`, текст ошибки `exec … no such file or directory`) | Docker нет; всё проверено podman 5.8.9 / crun. Размеры podman даёт в распакованном виде |
| 025: `COPY go.mod go.sum* ./` без `go.sum` | в podman/buildah проходит (проверено); в Docker BuildKit не проверялось |
| 008: кэш путей `hash` в bash | не проверялось (поведение bash, к Go не относится) |

---

## 4. Пропущенное брифом

### F-01 — INCORRECT
- **Где / цитата:** `01. …/002. Мгновенный запуск.md`, «Теория»: «1. Компиляцию и линковку во временный исполняемый файл; 2. Немедленный запуск этого файла.»; «Под капотом»: «Внутри этого каталога создается скомпилированный бинарник `exe/main`.»
- **Вердикт:** с Go 1.24 `go run` кэширует собранный исполняемый файл в `GOCACHE`. При повторном запуске без изменений ничего не компилируется и не линкуется, бинарник берётся из кэша, а каталог `WORK` (даже с `-work`) пуст. Описание верно только для первого запуска или после изменений.
- **Доказательство:** go1.27.1 `src/cmd/go/internal/run/run.go:175`: `a1.CacheExecutable = true`; `work/buildid.go:756` кладёт результат `link` в кэш, если стоит `CacheExecutable`. Запуск: с пустым `GOCACHE` `go run -work main.go` → в `WORK` есть `b001/exe/main` и ~60 каталогов; второй запуск → `WORK=/tmp/go-build1040929613`, каталог пуст, программа выполнилась.
- **Предлагаемая правка:** в «Теорию»: «С Go 1.24 собранный `go run` бинарник кэшируется в `GOCACHE`: повторный запуск без изменений в коде пропускает компиляцию и линковку.» «Под капотом» — см. правку J-11.

### F-02 — PARTIALLY CORRECT
- **Где / цитата:** `01. …/001. …md`, «Теория»: «2. Целевую операционную систему…; 3. Архитектуру процессора…»; «Под капотом»: «…считывает константу `runtime.Version()`…».
- **Вердикт:** `go version` печатает ОС и архитектуру самого тулчейна, то есть платформу, под которую собран бинарник `go`. Это не цель сборки: переменные `GOOS`/`GOARCH` на вывод не влияют. `runtime.Version()` — функция, а не константа. При переключении тулчейна (J-07) печатается версия запущенного тулчейна.
- **Доказательство:** `GOOS=windows GOARCH=arm64 go version` → `go version go1.27.1 linux/amd64`, а `GOOS=windows go env GOOS` → `windows`. `src/cmd/go/internal/version/version.go:87`: `v := runtime.Version()`. `GOTOOLCHAIN=go1.26.0 go version` → `go version go1.26.0 linux/amd64`.
- **Предлагаемая правка:** «2–3. ОС и архитектуру, для которых собран сам тулчейн (`linux/amd64`, `darwin/arm64`…). Это платформа сборки по умолчанию; цель сборки показывает `go env GOOS GOARCH`.» «Под капотом»: «…печатает значение `runtime.Version()` (версия, вшитая в тулчейн при его сборке) и `runtime.GOOS/runtime.GOARCH`.»

### F-03 — PARTIALLY CORRECT
- **Где / цитата:** `02. …/005. Основы кросс-компиляции. переменные GOOS и GOARCH.md`, «Подводные камни»: «Наличие CGO (`import "C"`). Если включен `CGO_ENABLED=1`, стандартная кросс-компиляция сломается… Всегда собирайте с `CGO_ENABLED=0`.»
- **Вердикт:** при кросс-компиляции cgo по умолчанию выключен (`CGO_ENABLED=0`), поэтому обычная кросс-сборка чистого Go-кода не ломается. Ломается она, если `CGO_ENABLED=1` задан явно. Для кода с `import "C"` `CGO_ENABLED=0` не решение: cgo-файлы исключаются из сборки, а символы из них пропадают. Нужен C-кросс-компилятор (`CC=…`) или отказ от cgo. О `-race` — J-06.
- **Доказательство:** `go doc cmd/cgo`: «The cgo tool is enabled by default for native builds on systems where it is expected to work. It is disabled by default when cross-compiling…». Запуски: `GOOS=linux GOARCH=arm64 go env CGO_ENABLED` → `0`; `GOOS=windows go env CGO_ENABLED` → `0`; программа с `net`: `GOOS=linux GOARCH=arm64 go build` → `ELF … ARM aarch64 … statically linked`; `CGO_ENABLED=1 GOOS=linux GOARCH=arm64 go build` → `gcc_arm64.S:68: Error: no such instruction: 'ldp x21,x22,[sp,'…`, exit 1.
- **Предлагаемая правка:** «При кросс-компиляции cgo по умолчанию выключен, и чистый Go-код собирается без C-компилятора. Сборка сломается, если включить `CGO_ENABLED=1` явно (нужен C-кросс-компилятор под целевую платформу, `CC=aarch64-linux-gnu-gcc`). Код с `import "C"` без cgo не соберётся вообще. Для воспроизводимых релизных сборок задавайте `CGO_ENABLED=0` явно (см. J-06 про исключение `-race`).»

### F-04 — PARTIALLY CORRECT
- **Где / цитата:** `02. …/006. …md`, «Под капотом» / «На собеседовании»: «Что делает системная точка входа `_rt0_amd64_linux`…» — «Она считывает аргументы `argc`/`argv`…, инициализирует структуру `m0`…, `g0`…, настраивает сборщик мусора и запускает планировщик `runtime.schedinit()`.»
- **Вердикт:** по сути цепочка верна, но приписана не той функции. `_rt0_amd64_linux` — одна инструкция `JMP _rt0_amd64`. `_rt0_amd64` берёт `argc`/`argv` со стека и переходит в `runtime·rt0_go`. Уже `rt0_go` настраивает `g0`/`m0` и вызывает `args`, `osinit`, `schedinit` (внутри — `gcinit`), `newproc` (горутина для `runtime.main`) и `mstart`. `schedinit` не «запускает планировщик», планировщик стартует в `mstart`.
- **Доказательство:** go1.27.1 `src/runtime/rt0_linux_amd64.s:7-8` (`TEXT _rt0_amd64_linux … JMP _rt0_amd64(SB)`); `src/runtime/asm_amd64.s:15-18` (`MOVQ 0(SP), DI // argc`, `LEAQ 8(SP), SI // argv`, `JMP runtime·rt0_go`), стр. 338–349 (`CALL runtime·args/osinit/schedinit/newproc/mstart`); `src/runtime/proc.go:912` — `gcinit()` внутри `schedinit`.
- **Предлагаемая правка:** «`_rt0_amd64_linux` лишь передаёт управление в `_rt0_amd64`, который берёт `argc`/`argv` со стека и вызывает `runtime·rt0_go`. Тот настраивает `g0` и `m0`, вызывает `runtime.args`, `runtime.osinit`, `runtime.schedinit` (инициализация аллокатора, GC, P), создаёт горутину для `runtime.main` (`newproc`) и запускает планировщик на текущем потоке (`mstart`).»

### F-05 — OPINION / NOT A FACT CLAIM
- **Где / цитата:** `06. …/023. …md`, «Подводные камни» (небуферизованный канал сигналов); `03. …/013. …md` (список проверок vet).
- **Вердикт:** утверждение 023 верно, и его ловит штатный анализатор `go vet` `sigchanyzer`. Это хорошая связка двух задач главы и аргумент для правки J-13.
- **Доказательство:** код 023 с `make(chan os.Signal)` → `go vet`: `main.go:32:2: misuse of unbuffered os.Signal channel as argument to signal.Notify`. С `make(chan os.Signal, 1)` vet чист.
- **Предлагаемая правка:** в 023 дописать «— это ловит `go vet` (анализатор `sigchanyzer`)»; в 013 добавить пункт в список (см. J-13).

### F-06 — PARTIALLY CORRECT
- **Где / цитата:** `05. …/019. …md`, `main.go`: `fmt.Printf("[DEBUG] Количество переданных аргументов: %d\n", flag.NFlag())`.
- **Вердикт:** `flag.NFlag()` — число **установленных флагов**, а не аргументов. Ответ «На собеседовании» это верно разделяет (`NFlag` / `NArg`), а подпись в коде путает. Вывод «Терминала» (3) верен.
- **Доказательство:** `go doc flag.NFlag`: «NFlag returns the number of command-line flags that have been set.» Запуск `./app -verbose false -name=bob` (4 аргумента) → `Количество переданных аргументов: 1`.
- **Предлагаемая правка:** `"[DEBUG] Количество установленных флагов: %d\n"`; в «Терминале» — `# [DEBUG] Количество установленных флагов: 3`.

### F-07 — PARTIALLY CORRECT
- **Где / цитата:** `01. …/002. …md`, «На собеседовании»: «Все параметры после `.` попадают в срез `os.Args`.»
- **Вердикт:** параметры попадают в `os.Args[1:]`. `os.Args[0]` — путь к временному или закэшированному бинарнику, а не `.` и не имя исходника.
- **Доказательство:** `go run . --port=8080 --env=prod` с `fmt.Printf("%q\n", os.Args)` → `["/tmp/go-build2675946607/b001/exe/args" "--port=8080" "--env=prod"]`.
- **Предлагаемая правка:** «…попадают в `os.Args[1:]` (`os.Args[0]` — путь к временному бинарнику, собранному `go run`). Флаги самой команды `go run` (`-race`, `-work`) пишутся до пакета.»

### F-08 — OUTDATED
- **Где / цитата:** `01. …/003. …md`, «Терминал»: `1.8M … hello_world`; «На собеседовании»: «Hello World на Go весит около 1.5–2 МБ»; `04. …/018. …md`, «Терминал»: `1.8M app-standard`, `1.2M app-stripped`.
- **Вердикт:** на go1.27.1 hello-world весит 2,3 МБ, стрипнутый — 1,5 МБ. Доля уменьшения (−35 %) прежняя.
- **Доказательство:** linux/amd64: `hello_world` 2 342 489 байт (`ls -lh` → `2.3M`); `app-standard` 2 342 361 (`2.3M`), `app-stripped` 1 511 584 (`1.5M`).
- **Предлагаемая правка:** 003: `# -rwxr-xr-x 1 ut ut 2.3M … hello_world`; вопрос: «…около 2 МБ (2,3 МБ на Go 1.27, linux/amd64)…». 018: `2.3M app-standard` / `1.5M app-stripped`. Либо пометить «размеры зависят от версии Go и платформы».

### F-09 — CONTEXT-DEPENDENT
- **Где / цитата:** `04. …/017. …md`, «Терминал (Вывод компилятора)»: `./main.go:3:6: other declaration of main`.
- **Вердикт:** позиция `3:6` верна для `main.go` без импортов (`package main` / пусто / `func main()`). Сам `main.go` в задаче не показан, а читатель, идущий по главе, возьмёт `main.go` из 002 или 015 с `import "fmt"` и получит `5:6`. Позиция `second.go:6:6` верна.
- **Доказательство:** `main.go` с `import "fmt"` + `second.go` из книги → `./second.go:6:6: main redeclared in this block` / `./main.go:5:6: other declaration of main`. С минимальным `main.go` → `./main.go:3:6`.
- **Предлагаемая правка:** показать в «Коде решения» `main.go` (минимальный, 3 строки) или заменить в выводе `3:6` на `5:6` с пометкой «номер строки зависит от вашего main.go».

### F-10 — OPINION / NOT A FACT CLAIM
- **Где / цитата:** `05. …/020. …md`, «Код решения»: `addCmd.Parse(os.Args[2:])`, `subCmd.Parse(os.Args[2:])` — результат не проверяется.
- **Вердикт:** при `flag.ExitOnError` `Parse` при ошибке сам завершает процесс с кодом 2, так что ошибка не теряется и код корректен. Но AGENTS § 3.2 требует обрабатывать ошибки, а `errcheck` в `golangci-lint`, о котором говорит 013, на такой вызов среагирует. Стоит хотя бы прокомментировать.
- **Доказательство:** `./app add --z 1` → `flag provided but not defined: -z` + справка, exit 2. `go vet` чист.
- **Предлагаемая правка:** `_ = addCmd.Parse(os.Args[2:]) // при ExitOnError ошибка завершает процесс с кодом 2` или явная проверка `if err := addCmd.Parse(os.Args[2:]); err != nil { … }`.

---

### Дополнительно проверено (находок нет)
- 004 «Подводные камни»/«На собеседовании»: `go build .` в библиотечном пакете — exit 0, файлов не создаёт.
- 005 «На собеседовании»: суффиксы `_linux.go`/`_amd64.go` — верно. Отбирает файлы не компилятор, а `go/build`; это мелочь.
- 006 «Подводные камни»: запуск arm64-бинарника на x86_64 → `cannot execute binary file: Exec format error` (сообщение bash, exit 126).
- 010: `go help fmt` — «Fmt runs the command 'gofmt -l -w'…», верно.
- 011 «Под капотом»: magic-байты ELF `7f 45 4c 46`, Mach-O 64 `cf fa ed fe`, PE `4d 5a` — сверены через `od` на собранных бинарниках.
- 014: скрипт и `lipo` — верно.
- 018 «Под капотом»/«На собеседовании»: `.gopclntab` сохраняется, номера строк в панике есть.
- 022 «Под капотом»: fast path `Mutex.Lock` — один CAS (`internal/sync/mutex.go:63`).
- 023: `terminationGracePeriodSeconds` = 30 с; вывод «Терминала» совпадает.
- 025 «Подводные камни»: без сертификатов в `scratch` — `tls: failed to verify certificate: x509: certificate signed by unknown authority`; с `ca-certificates.crt` из Dockerfile — `200 OK` (проверено podman).
- 025 «Под капотом»: в `scratch` нет `/bin/sh` (`crun: executable file '/bin/sh' not found`).
