"""Management command to sync coodie models to Cassandra/ScyllaDB."""

from __future__ import annotations

import os
import sys

from django.core.management.base import BaseCommand

# Ensure the project root is importable so ``cassandra_models`` resolves.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


class Command(BaseCommand):
    """Synchronize coodie Cassandra tables for TaskEvent and TaskCounter."""

    help = "Create or update Cassandra tables for coodie models"

    def handle(self, *args: object, **options: object) -> None:
        from cassandra_models import TaskCounter, TaskEvent
        from django.conf import settings

        from coodie.sync import init_coodie

        hosts = settings.SCYLLA_HOSTS
        keyspace = settings.SCYLLA_KEYSPACE

        self.stdout.write(f"  📡 Connecting to ScyllaDB ({', '.join(hosts)})...")
        init_coodie(hosts=hosts, keyspace=keyspace)

        self.stdout.write("  🔧 Syncing TaskEvent table...")
        TaskEvent.sync_table()
        self.stdout.write(self.style.SUCCESS("  ✓ TaskEvent synced"))

        self.stdout.write("  🔧 Syncing TaskCounter table...")
        TaskCounter.sync_table()
        self.stdout.write(self.style.SUCCESS("  ✓ TaskCounter synced"))

        self.stdout.write(self.style.SUCCESS("\n  ✓ All Cassandra tables are ready."))
