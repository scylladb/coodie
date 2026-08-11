COMPOSE  := docker compose -f ../docker-compose.yml
KEYSPACE := argus

.PHONY: db-up db-down seed clean test

db-up:                          ## Start ScyllaDB and create keyspace
	@echo ""
	@echo "  🐙 THE PANOPTICON PROTOCOL — Dimension-13"
	@echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  ARGUS-PRIME is awakening..."
	@echo ""
	$(COMPOSE) up -d
	@echo "  🌀 Waiting for ScyllaDB node to materialise..."
	@until $(COMPOSE) exec scylladb nodetool status 2>/dev/null | grep -q "^UN"; do sleep 2; done
	@echo "  ✓ ScyllaDB is UP — surveillance network established"
	@echo "  🔧 Creating keyspace '$(KEYSPACE)' for the Panopticon..."
	$(COMPOSE) exec scylladb cqlsh -e \
	  "CREATE KEYSPACE IF NOT EXISTS $(KEYSPACE) \
	   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"
	@echo "  ✓ Keyspace ready — ARGUS-PRIME's data store is online"
	@echo ""

db-down:                        ## Stop ScyllaDB
	@echo "  🌀 Shutting down surveillance network..."
	$(COMPOSE) down
	@echo "  ✓ ARGUS-PRIME has been disconnected"

seed: db-up                     ## Seed test tracker data (interactive walkthrough)
	@echo "  🐙 Activating the Panopticon Protocol..."
	@echo "  (run with NO_INTERACTIVE=1 to skip pauses)"
	@echo ""
	@if [ "$$NO_INTERACTIVE" = "1" ]; then \
	    uv run python seed.py --no-interactive; \
	else \
	    uv run python seed.py --interactive; \
	fi

clean: db-down                  ## Stop DB and remove data volumes
	$(COMPOSE) down -v
	@echo "  ✓ All surveillance data purged — Panopticon dismantled"

test:                           ## Run smoke test (requires ScyllaDB running)
	uv run python smoke_test.py
