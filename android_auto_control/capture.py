import contextlib
import re
import shutil
import socket
from collections.abc import Iterator
from pathlib import Path
from secrets import randbelow
from types import TracebackType
from typing import Self, cast

import adbutils  # pyright: ignore[reportMissingTypeStubs]  # adbutils ships no type stubs
import av
import numpy as np
from av.container import InputContainer
from numpy.typing import NDArray

_SERVER_REMOTE = "/data/local/tmp/scrcpy-server.jar"
_VERSION_IN_DIR = re.compile(r"v(\d+\.\d+\.\d+)")
_ACCEPT_TIMEOUT_SECONDS = 10.0

BgrFrame = NDArray[np.uint8]


def locate_server(override: Path | None) -> Path:
    """scrcpy-server 경로를 정한다. override가 있으면 그것, 없으면 PATH의 scrcpy 옆에서 찾는다."""
    if override is not None:
        if not override.is_file():
            raise FileNotFoundError(f"scrcpy-server not found at {override}")
        return override
    scrcpy = shutil.which("scrcpy")
    if scrcpy is None:
        raise FileNotFoundError("scrcpy not found on PATH; set the server path in settings")
    jar = Path(scrcpy).with_name("scrcpy-server")
    if not jar.is_file():
        raise FileNotFoundError(f"scrcpy-server not found next to {scrcpy}")
    return jar


def server_version(jar: Path) -> str:
    """클라이언트가 넘기는 버전은 서버 jar과 일치해야 하므로 설치 폴더 이름에서 읽는다."""
    match = _VERSION_IN_DIR.search(jar.parent.name)
    if match is None:
        raise ValueError(f"cannot read scrcpy version from {jar.parent.name!r}")
    return match.group(1)


class ScreenCapture:
    """scrcpy 서버를 reverse 터널로 띄우고 영상 소켓에서 BGR 프레임을 낸다."""

    def __init__(self, jar: Path, version: str) -> None:
        self._jar = jar
        self._version = version
        self._scid = randbelow(0x80000000)
        self._device: adbutils.AdbDevice = adbutils.adb.device()
        self._listener: socket.socket | None = None
        self._conn: socket.socket | None = None
        self._server: adbutils.AdbConnection | None = None
        self._container: InputContainer | None = None

    @property
    def _remote_socket(self) -> str:
        return f"localabstract:scrcpy_{self._scid:08x}"

    def __enter__(self) -> Self:
        try:
            self._start()
        except BaseException:
            self._cleanup()
            raise
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._cleanup()

    def frames(self) -> Iterator[BgrFrame]:
        if self._container is None:
            raise RuntimeError("capture is not started")
        for frame in self._container.decode(video=0):
            yield cast(BgrFrame, frame.to_ndarray(format="bgr24"))

    def _start(self) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener = listener
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(_ACCEPT_TIMEOUT_SECONDS)
        port: int = listener.getsockname()[1]

        # reverse 터널을 먼저 걸어야 서버가 기동 직후 접속할 수 있다.
        self._device.reverse(self._remote_socket, f"tcp:{port}")
        self._device.push(str(self._jar), _SERVER_REMOTE)
        self._server = self._device.shell(  # pyright: ignore[reportUnknownMemberType]  # adbutils shell overload is untyped
            self._launch_command(), stream=True
        )

        try:
            conn, _ = listener.accept()
        except TimeoutError as error:
            raise RuntimeError("scrcpy server did not connect; check the USB connection and scrcpy version") from error
        self._conn = conn
        conn.settimeout(None)  # accept()가 리스너의 타임아웃을 물려받아 스트리밍 중 끊기지 않게 한다.
        self._container = av.open(conn.makefile("rb"), format="h264", mode="r")

    def _launch_command(self) -> str:
        # 영상만 받는다. 메타를 모두 끄면 순수 H.264 스트림이 되어 그대로 디코딩할 수 있다.
        return (
            f"CLASSPATH={_SERVER_REMOTE} app_process / com.genymobile.scrcpy.Server {self._version} "
            f"scid={self._scid:08x} log_level=info video=true audio=false control=false "
            f"video_codec=h264 send_device_meta=false send_codec_meta=false send_frame_meta=false"
        )

    def _cleanup(self) -> None:
        # 정리 중 한 리소스의 실패가 나머지 해제를 막지 않도록 각각 best-effort로 닫는다.
        if self._container is not None:
            with contextlib.suppress(Exception):
                self._container.close()
            self._container = None
        if self._conn is not None:
            with contextlib.suppress(OSError):
                self._conn.close()
            self._conn = None
        if self._server is not None:
            with contextlib.suppress(Exception):
                self._server.close()
            self._server = None
        with contextlib.suppress(adbutils.AdbError):
            self._device.reverse_remove(self._remote_socket)
        if self._listener is not None:
            with contextlib.suppress(OSError):
                self._listener.close()
            self._listener = None
