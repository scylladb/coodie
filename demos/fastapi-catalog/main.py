"""FastAPI Product Catalog demo showcasing coodie's async API."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Product, Review
from pydantic import BaseModel

from coodie.aio import init_coodie
from coodie.exceptions import DocumentNotFound, MultipleDocumentsFound

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync tables."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "catalog")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await Product.sync_table()
    await Review.sync_table()
    yield


app = FastAPI(title="Product Catalog", version="0.1.0", lifespan=lifespan)


# ------------------------------------------------------------------
# Exception handlers
# ------------------------------------------------------------------


@app.exception_handler(DocumentNotFound)
async def not_found_handler(request, exc):
    raise HTTPException(status_code=404, detail=str(exc))


@app.exception_handler(MultipleDocumentsFound)
async def multiple_found_handler(request, exc):
    raise HTTPException(status_code=409, detail=str(exc))


class ProductUpdate(BaseModel):
    """Fields that may be updated on a Product."""

    name: str | None = None
    brand: str | None = None
    category: str | None = None
    price: float | None = None
    description: str | None = None
    tags: list[str] | None = None


# ------------------------------------------------------------------
# Product routes
# ------------------------------------------------------------------


@app.get("/products", response_model=list[Product])
async def list_products(
    category: str | None = Query(default=None),
    brand: str | None = Query(default=None),
) -> list[Product]:
    qs = Product.find()
    if category:
        qs = qs.filter(category=category)
    if brand:
        qs = qs.filter(brand=brand)
    if category or brand:
        qs = qs.allow_filtering()
    return await qs.all()


@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: Product) -> Product:
    await product.save()
    return product


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: UUID) -> Product:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: UUID, updates: ProductUpdate) -> Product:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    await product.save()
    return product


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: UUID) -> None:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await product.delete()


# ------------------------------------------------------------------
# Review routes
# ------------------------------------------------------------------


@app.get("/products/{product_id}/reviews", response_model=list[Review])
async def list_reviews(
    product_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[Review]:
    return await Review.find(product_id=product_id).order_by("-created_at").limit(limit).all()


@app.post("/products/{product_id}/reviews", response_model=Review, status_code=201)
async def create_review(product_id: UUID, review: Review) -> Review:
    review.product_id = product_id
    await review.save()
    return review


@app.delete("/products/{product_id}/reviews/{ts}", status_code=204)
async def delete_review(product_id: UUID, ts: datetime) -> None:
    review = await Review.find_one(product_id=product_id, created_at=ts)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    await review.delete()


# ------------------------------------------------------------------
# HTMX UI routes (server-rendered HTML fragments)
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui/products", response_class=HTMLResponse)
async def ui_list_products(
    request: Request,
    category: str | None = Query(default=None),
    brand: str | None = Query(default=None),
) -> HTMLResponse:
    qs = Product.find()
    if category:
        qs = qs.filter(category=category)
    if brand:
        qs = qs.filter(brand=brand)
    if category or brand:
        qs = qs.allow_filtering()
    products = await qs.all()
    return templates.TemplateResponse("partials/product_list.html", {"request": request, "products": products})


@app.post("/ui/products", response_class=HTMLResponse)
async def ui_create_product(
    request: Request,
    name: str = Form(),
    brand: str = Form(),
    category: str = Form(),
    price: float = Form(),
    tags: str = Form(default=""),
    description: str = Form(default=""),
) -> HTMLResponse:
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    product = Product(
        name=name,
        brand=brand,
        category=category,
        price=price,
        tags=tag_list,
        description=description or None,
    )
    await product.save()
    products = await Product.find().all()
    return templates.TemplateResponse("partials/product_list.html", {"request": request, "products": products})


@app.delete("/ui/products/{product_id}", response_class=HTMLResponse)
async def ui_delete_product(request: Request, product_id: UUID) -> HTMLResponse:
    product = await Product.find_one(id=product_id)
    if product:
        await product.delete()
    products = await Product.find().all()
    return templates.TemplateResponse("partials/product_list.html", {"request": request, "products": products})


@app.get("/ui/products/{product_id}", response_class=HTMLResponse)
async def ui_product_detail(request: Request, product_id: UUID) -> HTMLResponse:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("partials/product_detail.html", {"request": request, "product": product})


@app.get("/ui/products/{product_id}/reviews", response_class=HTMLResponse)
async def ui_list_reviews(request: Request, product_id: UUID) -> HTMLResponse:
    reviews = await Review.find(product_id=product_id).order_by("-created_at").limit(50).all()
    return templates.TemplateResponse("partials/review_list.html", {"request": request, "reviews": reviews})


@app.post("/ui/products/{product_id}/reviews", response_class=HTMLResponse)
async def ui_create_review(
    request: Request,
    product_id: UUID,
    author: str = Form(),
    rating: int = Form(),
    content: str = Form(default=""),
) -> HTMLResponse:
    review = Review(
        product_id=product_id,
        author=author,
        rating=rating,
        content=content or None,
    )
    await review.save()
    reviews = await Review.find(product_id=product_id).order_by("-created_at").limit(50).all()
    return templates.TemplateResponse("partials/review_list.html", {"request": request, "reviews": reviews})


@app.delete("/ui/products/{product_id}/reviews/{ts}", response_class=HTMLResponse)
async def ui_delete_review(request: Request, product_id: UUID, ts: datetime) -> HTMLResponse:
    review = await Review.find_one(product_id=product_id, created_at=ts)
    if review:
        await review.delete()
    reviews = await Review.find(product_id=product_id).order_by("-created_at").limit(50).all()
    return templates.TemplateResponse("partials/review_list.html", {"request": request, "reviews": reviews})
