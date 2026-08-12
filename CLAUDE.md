# CLAUDE.md

## 리포지토리 개요

- 원격 주소: https://github.com/nil-park/android-auto-control

## Git & GitLab & Jira

- 브랜치 이름은 `<타입>/<설명>` 형식으로, 타입은 Conventional Commits 타입(`feature`/`fix`/`refactor`/`chore`/`docs` 등)을 prefix로 쓴다.
- 커밋 메시지는
  - `main`이 아닌 브랜치에서는 평문으로
  - `main` 브랜치에는 Conventional Commits 규칙을 따름
- PR 제목은 `#123 제목입니다`처럼 이슈 번호를 접두사로 넣는다
  - 관리 추적이 필요하다고 판단되면 새 이슈를 생성하되, 사용자와 인터랙션 하면서 만든다.
  - 이슈 생성이 필요 없다면 Conventional Commits 규칙을 따름
- GitHub 이슈 및 PR 설명에 체크박스 절대 넣지 말 것.

## 개발 컨벤션

- 개발에 착수하기 전에 `eza --tree --git-ignore -a --ignore-glob='.git' .`와 같은 커맨드로 전체 파일 목록(문서·코드)을 한 번 확인하고, 파일명을 기준으로 작업에 관련된 문서·코드를 골라 정독·파악해 맥락을 놓치지 않도록 할 것.
- 위 방식이 잘 동작하도록 파일·디렉토리 이름은 내용을 명확히 드러내게 지을 것.
- lint/format/test 실행은 `make format` (로컬 개발) 또는 `make test` (CI)를 사용할 것.
- Python뿐 아니라 md, json, yaml 등 파일을 수정 했을 때 대개 커밋 전에 `make format`을 실행할 것 (Prettier로 포매팅)
- Python에서 같은 패키지 내 모듈을 import할 때는 절대 경로(`from android_auto_control.xxx.yyy`) 대신 상대 경로(`from .yyy`)를 사용할 것
- 데이터 모델은 특별한 이유가 없으면 `dataclass` 대신 Pydantic `BaseModel`을 사용할 것
- Pydantic `Field(default_factory=list[T])` 형태는 pyright 타입 추론을 위해 의도적으로 사용한다. `default_factory=list`로 바꾸지 말 것
- 커맨드라인 입력이나 환경변수 설정 입력은 특별한 이유가 없으면 `pydantic-settings`를 사용할 것
- 실제 프로그램을 기동해야 의미 있게 검증되는 로직까지 유닛 테스트로 커버하는 것은 오버엔지니어링으로 판단할 것.
- `adb shell input tap` 쓰지 말 것. 폰 입력은 BLE 장치를 경유할 것.

## 언어

- **커밋 메시지와 PR 제목 및 설명은 영어로 쓸 것.**
- 나머지는 한국어로 쓸 것.

## 레퍼런스 리포지토리

`.refs/` 아래에 클론해 두고 참고한다.

| 클론 URL                             | 용도                                                          |
| ------------------------------------ | ------------------------------------------------------------- |
| https://github.com/Genymobile/scrcpy | scrcpy 서버 기동 옵션과 영상 소켓 프로토콜 참조 (태그 v3.3.4) |
