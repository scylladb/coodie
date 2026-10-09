"""Minimal FastAPI app for the schema-migrations demo.

This app assumes all five migrations have already been applied via
``coodie migrate``.  It provides two read-only endpoints for querying the
migrated schema — one for featured products and one for product reviews.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI
from models import Product, Review

from coodie.aio import init_coodie


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to ScyllaDB on startup."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "migrations_demo")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    yield


app = FastAPI(
    title="Schema Migrations Demo",
    description="Minimal API to explore the migrated catalog schema.",
    lifespan=lifespan,
)


@app.get("/products/featured")
async def featured_products():
    """Return all products where ``featured = true`` (uses migration 002 index)."""
    rows = await Product.find(featured=True).all()
    return [r.model_dump(mode="json") for r in rows]


@app.get("/products/{product_id}/reviews")
async def product_reviews(product_id: UUID):
    """Return reviews for a product, newest first (uses clustering order)."""
    rows = await Review.find(product_id=product_id).order_by("-created_at").all()
    return [r.model_dump(mode="json") for r in rows]


@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "ok"}
