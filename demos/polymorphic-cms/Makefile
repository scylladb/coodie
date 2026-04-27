COMPOSE  := docker compose -f ../docker-compose.yml
KEYSPACE := cms

.PHONY: db-up db-down seed run clean

db-up:                          ## Start ScyllaDB and create keyspace
	@echo ""
	@echo "  🎭 THE SHAPESHIFTER'S ARCHIVE — Dimension-11"
	@echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  Morph-IX is initializing the content singularity..."
	@echo ""
	$(COMPOSE) up -d
	@echo "  🌀 Waiting for ScyllaDB node to materialize..."
	@until $(COMPOSE) exec scylladb nodetool status 2>/dev/null | grep -q "^UN"; do sleep 2; done
	@echo "  ✓ ScyllaDB is UP — dimensional anchor established"
	@echo "  🔧 Creating keyspace '$(KEYSPACE)' (single table for all content types)..."
	$(COMPOSE) exec scylladb cqlsh -e \
	  "CREATE KEYSPACE IF NOT EXISTS $(KEYSPACE) \
	   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"
	@echo "  ✓ Keyspace ready — the Archive is open"
	@echo ""

db-down:                        ## Stop ScyllaDB
	@echo "  🌀 Collapsing the content singularity... shutting down ScyllaDB"
	$(COMPOSE) down
	@echo "  ✓ Morph-IX has been disconnected"

seed: db-up                     ## Seed sample polymorphic content (depends on db-up)
	@echo "  🎭 Morph-IX is generating polymorphic content..."
	@echo ""
	uv run python seed.py --count 30

run: seed                       ## Install deps, seed, and start the app
	@echo ""
	@echo "  🎭 Launching The Shapeshifter's Archive..."
	@echo "  🖥  http://127.0.0.1:8000 — Dimension-11 portal active"
	@echo "  📰 Articles · 🎬 Videos · 🎙️ Podcasts — one table, one truth"
	@echo ""
	uv run uvicorn main:app --reload

clean: db-down                  ## Stop DB and remove data volumes
	$(COMPOSE) down -v
	@echo "  ✓ All content forms purged — the Archive is reset"
