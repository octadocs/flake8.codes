.PHONY: lint
lint:
	git diff origin/master | flakehell lint --diff

.PHONY: test
test: lint
	@echo "No tests at this time."
