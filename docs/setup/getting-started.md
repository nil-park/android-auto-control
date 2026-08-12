# 개발 환경 구축

도구를 먼저 갖춘다. 목록과 받는 곳은 [필수 도구](required-tools.md)에 있다.

## 프로젝트

```bash
uv sync
```

`.venv/`가 만들어지고 의존성이 잡힌다.

## 폰

### USB 디버깅

설정 → 휴대전화 정보 → 빌드 번호를 일곱 번 눌러 개발자 옵션을 켜고, 개발자 옵션에서 USB
디버깅을 켠다.

### 무선 연결

USB로 한 번 연결해 PC를 인증한 뒤 무선으로 넘긴다.

```bash
adb devices          # unauthorized면 폰에 뜬 대화상자에서 허용한다
adb tcpip 5555
adb connect <폰 IP>:5555
```

USB 케이블을 뽑고 `adb devices`에 `<폰 IP>:5555`가 남아 있으면 성공이다. 폰이 재부팅되면
`adb tcpip`부터 다시 한다.

### 화면 확인

```bash
scrcpy
```

폰 화면이 PC 창에 뜨면 캡처 경로가 준비된 것이다.
