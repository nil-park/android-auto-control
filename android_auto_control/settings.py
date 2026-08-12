import logging
from logging import Logger
from pathlib import Path

from pydantic import Field, field_serializer, field_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

from .log_formatter import ColorFormatter


class YamlBaseSettings(BaseSettings):
    """yaml_file을 소스 체인에 자동으로 포함시키는 공통 부모 클래스.

    pydantic-settings의 기본 소스 체인에는 YamlConfigSettingsSource가 포함되지 않아
    SettingsConfigDict에 yaml_file을 선언해도 값이 반영되지 않는 문제를 해결한다.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


class AndroidAutoControlSettings(YamlBaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=".data/settings.yaml",
        env_nested_delimiter="__",
        cli_prog_name="android-auto-control",
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_ignore_unknown_args=True,
        cli_implicit_flags=True,
    )

    log_level: int = Field(
        "info",  # type: ignore
        description=f"Log level. must be one of {[k.lower() for k in logging._nameToLevel]}",  # type: ignore[attr-defined]
        examples=["info", "debug", "warning", "error", "critical"],
        alias="LOG_LEVEL",
    )

    scrcpy_server: Path | None = Field(
        None,
        description="Path to scrcpy-server; auto-discovered next to scrcpy on PATH when unset",
        alias="SCRCPY_SERVER",
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str | int) -> int:
        if isinstance(v, int):
            return v
        return logging._nameToLevel[v.upper()]  # type: ignore[attr-defined]

    @field_serializer("log_level")
    @classmethod
    def serialize_log_level_to_str(cls, v: int) -> str:
        return logging._levelToName[v]  # type: ignore[attr-defined]

    def setup_logger(self, app_name: str, app_version: str) -> Logger:
        return setup_logging(self.log_level, app_name=app_name, app_version=app_version)


def setup_logging(log_level: int, *, app_name: str, app_version: str) -> Logger:
    """루트 로거를 구성하고 기동 메시지를 찍은 startup 로거를 반환한다."""
    handler = logging.StreamHandler()

    formatter = ColorFormatter()

    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(log_level)

    # Print the startup message and settings
    startup_logger = logging.getLogger("startup-logger")
    startup_logger.setLevel(logging.INFO)
    startup_logger.info(f"Starting {app_name} version {app_version}...")
    return startup_logger
