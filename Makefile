help: ## Show this help
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "}; \
	       /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: clean
clean: ## Delete dependencies and other files
	find . -type d -name "__pycache__" -exec rm -rfv {} + > /dev/null
	find . -type d -name ".venv" -exec rm -rfv {} + > /dev/null

.PHONY: install
install: ## Install all dependencies for local development
	@uv sync --locked --all-groups

define update_python_deps
	@ echo Updating $(1)
	@ cd $(1) &&\
	poetry update
endef