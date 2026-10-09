"""Flask Blog demo showcasing coodie's sync API."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from datetime import datetime
from pathlib import Path
from uuid import UUID

from flask import Flask, abort, redirect, render_template, request, url_for
from models import Comment, Post

from coodie.sync import init_coodie

BASE_DIR = Path(__file__).resolve().parent


def create_app() -> Flask:
    """Application factory — initializes coodie and registers routes."""
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "blog")

    with app.app_context():
        init_coodie(hosts=hosts, keyspace=keyspace)
        Post.sync_table()
        Comment.sync_table()

    # ------------------------------------------------------------------
    # Page routes
    # ------------------------------------------------------------------

    @app.get("/")
    def index():
        """Homepage — list all posts."""
        posts = Post.find().all()
        return render_template("index.html", posts=posts)

    @app.get("/posts/<uuid:post_id>")
    def post_detail(post_id: UUID):
        """View a single post with its comments."""
        post = Post.find_one(id=post_id)
        if post is None:
            abort(404)
        comments = Comment.find(post_id=post_id).order_by("-created_at").limit(50).all()
        return render_template("post_detail.html", post=post, comments=comments)

    @app.get("/new")
    def new_post_form():
        """Show the create-post form."""
        return render_template("new_post.html")

    @app.post("/posts")
    def create_post():
        """Handle post creation from the form."""
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        category = request.form.get("category", "").strip()
        content = request.form.get("content", "").strip()
        tags_raw = request.form.get("tags", "").strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

        if not title or not author or not category:
            abort(400)

        post = Post(
            title=title,
            author=author,
            category=category,
            content=content or None,
            tags=tags,
        )
        post.save()
        return redirect(url_for("post_detail", post_id=post.id))

    @app.post("/posts/<uuid:post_id>/comments")
    def create_comment(post_id: UUID):
        """Add a comment to a post."""
        post = Post.find_one(id=post_id)
        if post is None:
            abort(404)

        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()
        if not author or not content:
            abort(400)

        comment = Comment(
            post_id=post_id,
            author=author,
            content=content,
        )
        comment.save()
        return redirect(url_for("post_detail", post_id=post_id))

    @app.post("/posts/<uuid:post_id>/delete")
    def delete_post(post_id: UUID):
        """Delete a post and redirect to the homepage."""
        post = Post.find_one(id=post_id)
        if post is not None:
            # Delete associated comments
            for comment in Comment.find(post_id=post_id).all():
                comment.delete()
            post.delete()
        return redirect(url_for("index"))

    @app.post("/posts/<uuid:post_id>/comments/<ts>/delete")
    def delete_comment(post_id: UUID, ts: str):
        """Delete a comment and redirect back to the post."""
        created_at = datetime.fromisoformat(ts)
        comment = Comment.find_one(post_id=post_id, created_at=created_at)
        if comment is not None:
            comment.delete()
        return redirect(url_for("post_detail", post_id=post_id))

    # ------------------------------------------------------------------
    # JSON API routes
    # ------------------------------------------------------------------

    @app.get("/api/posts")
    def api_list_posts():
        """List posts as JSON (with optional filters)."""
        category = request.args.get("category")
        author = request.args.get("author")
        qs = Post.find()
        if category:
            qs = qs.filter(category=category)
        if author:
            qs = qs.filter(author=author)
        if category or author:
            qs = qs.allow_filtering()
        posts = qs.all()
        return [p.model_dump(mode="json") for p in posts]

    @app.get("/api/posts/<uuid:post_id>")
    def api_get_post(post_id: UUID):
        """Get a single post as JSON."""
        post = Post.find_one(id=post_id)
        if post is None:
            abort(404)
        return post.model_dump(mode="json")

    @app.post("/api/posts")
    def api_create_post():
        """Create a post from JSON body."""
        data = request.get_json(force=True)
        post = Post(**data)
        post.save()
        return post.model_dump(mode="json"), 201

    @app.delete("/api/posts/<uuid:post_id>")
    def api_delete_post(post_id: UUID):
        """Delete a post via API."""
        post = Post.find_one(id=post_id)
        if post is None:
            abort(404)
        post.delete()
        return "", 204

    @app.get("/api/posts/<uuid:post_id>/comments")
    def api_list_comments(post_id: UUID):
        """List comments for a post as JSON."""
        comments = Comment.find(post_id=post_id).order_by("-created_at").limit(50).all()
        return [c.model_dump(mode="json") for c in comments]

    @app.post("/api/posts/<uuid:post_id>/comments")
    def api_create_comment(post_id: UUID):
        """Create a comment from JSON body."""
        data = request.get_json(force=True)
        comment = Comment(post_id=post_id, **data)
        comment.save()
        return comment.model_dump(mode="json"), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
