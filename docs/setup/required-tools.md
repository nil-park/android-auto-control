# 필수 도구

이 저장소에서 작업할 때 필요한 CLI 도구 목록. 설치한 뒤 `PATH`에 넣는다.

| 도구     | 용도                                                        | 버전 확인          | 받는 곳                                                       |
| -------- | ----------------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| `uv`     | Python 런타임과 의존성 관리, `ruff`·`pyright`·`pytest` 실행 | `uv --version`     | <https://docs.astral.sh/uv/getting-started/installation>      |
| `make`   | Makefile 타깃(`make format`, `make test`) 실행              | `make --version`   | <https://gnuwin32.sourceforge.net/packages/make.htm>          |
| `npx`    | `make format`이 호출하는 Prettier 실행 (Node.js에 번들)     | `npx --version`    | <https://nodejs.org>                                          |
| `adb`    | 폰을 무선으로 붙이고 연결 상태를 확인한다                   | `adb version`      | <https://developer.android.com/tools/releases/platform-tools> |
| `scrcpy` | 폰 화면이 실제로 넘어오는지 눈으로 확인한다                 | `scrcpy --version` | <https://github.com/Genymobile/scrcpy/releases>               |
| `eza`    | 세션 시작 시 프로젝트 구조 확인                             | `eza --version`    | <https://github.com/eza-community/eza/releases>               |

Python은 따로 설치하지 않는다. `.python-version`에 적힌 버전을 uv가 내려받는다.
