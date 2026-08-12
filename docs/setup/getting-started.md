# 개발 환경 구축

도구를 먼저 갖춘다. 목록과 받는 곳은 [필수 도구](required-tools.md)에 있다.

## 프로젝트

```bash
uv sync
```

`.venv/`가 만들어지고 의존성이 잡힌다.

## 폰

### USB 드라이버

삼성 폰이면 [Samsung USB Driver](https://developer.samsung.com/android-usb-driver)를 설치한다.
다른 제조사는 Windows가 기본 드라이버로 인식하는 경우가 많다.

### USB 디버깅

설정 → 휴대전화 정보 → 빌드 번호를 일곱 번 눌러 개발자 옵션을 켜고, 개발자 옵션에서 USB
디버깅을 켠다. 삼성 폰은 `adb devices`가 폰을 못 잡으면 설정 → 보안 및 개인정보 보호 → 보안
위험 자동 차단을 끈다.

### USB 연결

USB로 연결하고 인식되는지 확인한다.

```bash
adb devices          # unauthorized면 폰에 뜬 대화상자에서 허용한다
```

`device` 상태로 뜨면 준비된 것이다.

### 화면 확인

```bash
scrcpy
```

폰 화면이 PC 창에 뜨면 캡처 경로가 준비된 것이다.
