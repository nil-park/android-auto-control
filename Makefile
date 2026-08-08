FG_BOLD := \033[1m
FG_BLACK := \033[30m
FG_WHITE := \033[97m
BG_GREEN := \033[42m
BG_YELLOW := \033[43m
BG_BLUE := \033[44m
BG_PINK := \033[45m
RESET := \033[0m

.PHONY: format test

format: # for local dev
	@echo -e "\n$(BG_BLUE)$(FG_WHITE)$(FG_BOLD) ruff check --fix $(RESET)"
	@uv run ruff check --fix
	@echo -e "\n$(BG_GREEN)$(FG_WHITE)$(FG_BOLD) ruff format $(RESET)"
	@uv run ruff format
	@echo -e "\n$(BG_GREEN)$(FG_WHITE)$(FG_BOLD) prettier $(RESET)"
	@npx --yes prettier --write --no-error-on-unmatched-pattern "**/*.md" "**/*.json" "**/*.yml" "**/*.yaml"
	@echo -e "\n$(BG_YELLOW)$(FG_BLACK)$(FG_BOLD) pyright $(RESET)\n"
	@uv run pyright
	@echo -e "\n$(BG_PINK)$(FG_WHITE)$(FG_BOLD) pytest $(RESET)\n"
	@uv run pytest

test: # for CI
	@echo -e "\n$(BG_BLUE)$(FG_WHITE)$(FG_BOLD) ruff check $(RESET)"
	@uv run ruff check
	@echo -e "\n$(BG_YELLOW)$(FG_BLACK)$(FG_BOLD) pyright $(RESET)\n"
	@uv run pyright
	@echo -e "\n$(BG_PINK)$(FG_WHITE)$(FG_BOLD) pytest $(RESET)\n"
	@uv run pytest
