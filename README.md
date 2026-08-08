# android-auto-control

안드로이드 화면을 PC에서 수신하여 BLE 개발 보드를 경유해 자동으로 제어하는 기본 틀입니다.

폰 화면을 PC가 Wi-Fi로 받아 분석하고, 눌러야 할 좌표를 USB 시리얼로 ESP32에 넘기면, ESP32가
블루투스 터치스크린 장치로서 폰에 입력을 넣습니다. 화면을 내보내는 경로와 입력이 들어오는
경로가 분리되어 있는 것이 이 구조의 핵심입니다. 자세한 형상은
[docs/architecture/pipeline.md](docs/architecture/pipeline.md)에 있습니다.

## 구성

- **화면 수신** — scrcpy로 폰 화면을 프레임 단위로 받습니다
- **화면 분석** — OpenCV 템플릿 매칭으로 찾는 대상의 좌표를 구합니다
- **터치 입력** — 좌표를 시리얼 명령으로 ESP32에 보내고, ESP32가 BLE HID 터치로 바꿔 폰에 넣습니다

이 리포지토리는 위 세 구간 중 PC에서 도는 부분을 담습니다. ESP32 펌웨어는 별도 리포지토리에서
관리합니다.

## 시작하기

개발 환경 구축은 [docs/setup/getting-started.md](docs/setup/getting-started.md)를 따릅니다.

```bash
uv sync
uv run android-auto-control
```

## 개발

```bash
make format   # 포매팅과 검사를 한 번에 (로컬)
make test     # 검사만 (CI)
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Attribution

Original work by [Nil Park](https://github.com/nil-park).
