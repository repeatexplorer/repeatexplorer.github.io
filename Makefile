# Build and check the site. `make check` is what CI runs and what must pass
# before any commit; run it locally so CI is a confirmation, not a discovery.

HUGO_VERSION := $(shell cat .hugo-version)

.PHONY: help serve build check check-cutover clean redirects validate links mixed version

help:
	@echo "make serve     live preview at http://localhost:1313 (drafts shown)"
	@echo "make build     build the site into public/"
	@echo "make check     everything CI runs: build, schemas, redirects, links"
	@echo "make check-cutover  stricter: every old URL must resolve (phase 4)"
	@echo "make clean     remove public/ and Hugo caches"

version:
	@hugo version | grep -q "v$(HUGO_VERSION)" || \
	  { echo "hugo $(HUGO_VERSION) expected (.hugo-version), got: $$(hugo version)"; exit 1; }

serve: redirects
	hugo server -D --disableFastRender

redirects:
	@python scripts/build_redirects.py

build: version redirects
	hugo --panicOnWarning --printPathWarnings

validate:
	@python scripts/validate_data.py

links:
	@lychee --offline --no-progress --include-fragments public/

mixed:
	@python scripts/check_mixed_content.py

check: build validate
	@python scripts/check_redirects.py
	@$(MAKE) --no-print-directory mixed
	@$(MAKE) --no-print-directory links
	@echo "all checks passed"

# Cut-over gate (phase 4): every old URL must resolve, no exceptions.
check-cutover: check
	@python scripts/check_redirects.py --strict
	@echo "cut-over checks passed"

clean:
	rm -rf public resources .hugo_build.lock
