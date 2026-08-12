# scrcpy 설치

폰 화면을 PC 창으로 받아 캡처 경로를 확인하는 도구다. 받는 곳은 [필수 도구](required-tools.md)에 있다.

## 1. 설치 여부 확인

```bash
scrcpy --version
```

버전이 나오면 끝이다. `command not found`면 아래로 간다.

## 2. 내려받기와 압축 풀기

Windows용 zip을 받아 도구 디렉터리에 푼다. 버전 문자열은 받은 파일에 맞춘다.

```bash
mkdir -p ~/.local/scrcpy
unzip ~/Downloads/scrcpy-win64-v3.3.4.zip -d ~/.local/scrcpy/
```

`~/.local/scrcpy/scrcpy-win64-v3.3.4/`에 `scrcpy.exe`와 DLL이 함께 풀린다.

## 3. 번들 adb 제거

Windows zip에는 adb가 함께 들어 있다. 이 저장소는 adb를 platform-tools 것 하나만 둔다. 풀린 폴더에서 adb 파일 셋을 지운다.

```bash
cd ~/.local/scrcpy/scrcpy-win64-v3.3.4
rm adb.exe AdbWinApi.dll AdbWinUsbApi.dll
```

나머지 DLL(SDL2, avcodec, avformat, avutil, swresample, libusb)은 scrcpy가 쓴다. 그대로 둔다. adb를 지운 scrcpy는 PATH의 adb를 쓴다.

## 4. PATH 등록

`~/.bashrc`에 푼 폴더를 PATH에 추가한다.

```bash
export PATH="$HOME/.local/scrcpy/scrcpy-win64-v3.3.4/:$PATH"
```

`scrcpy.exe`만 따로 `~/.local/bin` 같은 곳에 복사하면 옆에 있어야 할 DLL을 못 찾는다. 폴더째 두고 그 폴더를 PATH에 넣는다.

## 5. 확인

새 터미널을 열어 확인한다.

```bash
scrcpy --version
which adb            # platform-tools의 adb를 가리켜야 한다
```
