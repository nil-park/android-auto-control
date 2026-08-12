from pathlib import Path

import pytest

from android_auto_control.capture import locate_server, server_version


def test_server_version_reads_from_parent_dir_name(tmp_path: Path) -> None:
    jar = tmp_path / "scrcpy-win64-v3.3.4" / "scrcpy-server"
    assert server_version(jar) == "3.3.4"


def test_server_version_without_version_in_name_raises(tmp_path: Path) -> None:
    jar = tmp_path / "scrcpy" / "scrcpy-server"
    with pytest.raises(ValueError):
        server_version(jar)


def test_locate_server_returns_existing_override(tmp_path: Path) -> None:
    jar = tmp_path / "scrcpy-server"
    jar.touch()
    assert locate_server(jar) == jar


def test_locate_server_missing_override_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        locate_server(tmp_path / "absent")
