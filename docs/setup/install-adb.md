# adb 설치

폰을 USB로 붙이고 연결 상태를 확인하는 도구다. Android SDK platform-tools에 들어 있다. 받는 곳은 [필수 도구](required-tools.md)에 있다.

## 1. 설치 여부 확인

```bash
adb version
```

버전이 나오면 끝이다. `command not found`면 아래로 간다.

## 2. 내려받기와 압축 풀기

platform-tools zip을 받아 도구 디렉터리에 푼다.

```bash
mkdir -p ~/.local/android-sdk
unzip ~/Downloads/platform-tools-latest-windows.zip -d ~/.local/android-sdk/
```

`~/.local/android-sdk/platform-tools/`에 `adb.exe`가 풀린다.

## 3. PATH 등록

`~/.bashrc`에 platform-tools 폴더를 PATH에 추가한다.

```bash
export PATH="$HOME/.local/android-sdk/platform-tools:$PATH"
```

## 4. 확인

새 터미널을 열어 확인한다.

```bash
adb version
which adb            # platform-tools를 가리켜야 한다
```
