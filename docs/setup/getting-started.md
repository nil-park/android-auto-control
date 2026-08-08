# 개발 환경 구축

## PC

### uv

Python 런타임과 의존성을 모두 uv가 관리한다. 설치는
<https://docs.astral.sh/uv/getting-started/installation>을 따른다.

```bash
uv sync
```

`.python-version`에 적힌 버전을 uv가 내려받아 `.venv/`를 만든다. Python을 따로 설치하지 않는다.

### adb

Android SDK Platform Tools에 들어 있다. <https://developer.android.com/tools/releases/platform-tools>에서
받아 압축을 풀고, 그 디렉터리를 `PATH`에 넣는다.

```bash
adb version
```

### scrcpy

<https://github.com/Genymobile/scrcpy/releases>에서 Windows 빌드를 받아 압축을 풀고 `PATH`에 넣는다.
화면 수신은 Python 패키지가 하지만, 연결이 되는지 눈으로 먼저 확인할 때 쓴다.

```bash
scrcpy --version
```

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

## ESP32

펌웨어는 별도 리포지토리에서 관리한다. PC 쪽에서는 보드가 꽂힌 COM 포트 번호만 알면 된다.

```powershell
Get-CimInstance Win32_SerialPort | Select-Object DeviceID, Description
```
