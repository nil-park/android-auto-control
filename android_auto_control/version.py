from importlib.metadata import version

DISPLAY_NAME = "Android Auto Control"
PACKAGE_NAME = "android-auto-control"


def get_version() -> str:
    return version(PACKAGE_NAME)
