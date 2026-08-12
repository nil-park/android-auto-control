import sys

from .settings import AndroidAutoControlSettings
from .version import PACKAGE_NAME, get_version


def main() -> int:

    settings = AndroidAutoControlSettings()  # type: ignore
    startup_logger = settings.setup_logger(PACKAGE_NAME, get_version())
    startup_logger.info(f"Settings: {settings.model_dump(mode='json', exclude_none=True)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
