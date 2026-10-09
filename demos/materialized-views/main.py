"""FastAPI Materialized Views demo showcasing coodie's MaterializedView."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Product, ProductByBrand, ProductByCategory
from pydantic import BaseModel

from coodie.aio import init_coodie
from coodie.exceptions import DocumentNotFound, MultipleDocumentsFound

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB, sync base table and materialized views."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "viewdemo")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await Product.sync_table()
    await ProductByCategory.sync_view()
    await ProductByBrand.sync_view()
    yield


app = FastAPI(
    title="The Oracle's Mirror — Materialized Views",
    version="0.1.0",
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# Exception handlers
# ------------------------------------------------------------------


@app.exception_handler(DocumentNotFound)
async def not_found_handler(request, exc):
    raise HTTPException(status_code=404, detail=str(exc))


@app.exception_handler(MultipleDocumentsFound)
async def multiple_found_handler(request, exc):
    raise HTTPException(status_code=409, detail=str(exc))


class ProductCreate(BaseModel):
    """Fields for creating a product."""

    name: str
    category: str
    brand: str
    price: float
    description: str | None = None


# ------------------------------------------------------------------
# Base table routes (read/write)
# ------------------------------------------------------------------


@app.get("/products", response_model=list[Product])
async def list_products() -> list[Product]:
    return await Product.find().all()


@app.post("/products", response_model=Product, status_code=201)
async def create_product(body: ProductCreate) -> Product:
    product = Product(**body.model_dump())
    await product.save()
    return product


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: UUID) -> Product:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: UUID) -> None:
    product = await Product.find_one(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await product.delete()


# ------------------------------------------------------------------
# Materialized view routes (read-only)
# ------------------------------------------------------------------


@app.get("/views/by-category", response_model=list[ProductByCategory])
async def list_by_category(
    category: str = Query(..., description="Category to filter by"),
) -> list[ProductByCategory]:
    """Query the products_by_category materialized view."""
    return await ProductByCategory.find(category=category).all()


@app.get("/views/by-brand", response_model=list[ProductByBrand])
async def list_by_brand(
    brand: str = Query(..., description="Brand to filter by"),
) -> list[ProductByBrand]:
    """Query the products_by_brand materialized view."""
    return await ProductByBrand.find(brand=brand).all()


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui/products", response_class=HTMLResponse)
async def ui_list_products(request: Request) -> HTMLResponse:
    products = await Product.find().all()
    return templates.TemplateResponse(
        "partials/product_list.html",
        {"request": request, "products": products},
    )


@app.post("/ui/products", response_class=HTMLResponse)
async def ui_create_product(
    request: Request,
    name: str = Form(),
    category: str = Form(),
    brand: str = Form(),
    price: float = Form(),
    description: str = Form(default=""),
) -> HTMLResponse:
    product = Product(
        name=name,
        category=category,
        brand=brand,
        price=price,
        description=description or None,
    )
    await product.save()
    products = await Product.find().all()
    return templates.TemplateResponse(
        "partials/product_list.html",
        {"request": request, "products": products},
    )


@app.delete("/ui/products/{product_id}", response_class=HTMLResponse)
async def ui_delete_product(request: Request, product_id: UUID) -> HTMLResponse:
    product = await Product.find_one(id=product_id)
    if product:
        await product.delete()
    products = await Product.find().all()
    return templates.TemplateResponse(
        "partials/product_list.html",
        {"request": request, "products": products},
    )


@app.get("/ui/views/by-category", response_class=HTMLResponse)
async def ui_view_by_category(
    request: Request,
    category: str = Query(default=""),
) -> HTMLResponse:
    """Query the products_by_category materialized view via HTMX."""
    results: list[ProductByCategory] = []
    if category:
        results = await ProductByCategory.find(category=category).all()
    return templates.TemplateResponse(
        "partials/view_results.html",
        {"request": request, "results": results, "view_name": "products_by_category", "filter_value": category},
    )


@app.get("/ui/views/by-brand", response_class=HTMLResponse)
async def ui_view_by_brand(
    request: Request,
    brand: str = Query(default=""),
) -> HTMLResponse:
    """Query the products_by_brand materialized view via HTMX."""
    results: list[ProductByBrand] = []
    if brand:
        results = await ProductByBrand.find(brand=brand).all()
    return templates.TemplateResponse(
        "partials/view_results.html",
        {"request": request, "results": results, "view_name": "products_by_brand", "filter_value": brand},
    )
