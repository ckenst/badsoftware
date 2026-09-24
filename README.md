# badsoftware

The Bad Software Company website.

## Site Content

The static site is published from `docs/` and generated with `build_blog.py`.

## Case Studies

Case studies are written as Markdown files in the `case-studies/` directory. Each file must begin with an H1 title followed by a one-paragraph summary.

Run `python3 build_blog.py` to generate:

- The Case Studies index at `docs/case-studies/index.html`
- One public HTML page and Markdown mirror per case study
- Case study entries in the sitemap and LLM indexes

The case study renderer supports headings, paragraphs, ordered and unordered lists, tables, bold text, and external links.

## Insight Articles

Insight articles are written as simple text files in the `posts/` directory and converted to HTML using `build_blog.py`.

### Writing an Insight Article

1. Create a new `.txt` file in the `posts/` directory
2. Add metadata at the top (title, date, slug, excerpt, tags) followed by `---`
3. Write your content as plain text paragraphs (separated by blank lines)
4. Run `python3 build_blog.py` to generate the HTML

Example format:

```
title: My Insight Article Title
date: 2026-06-17
slug: my-post-slug
excerpt: A short description of the post.
tags: Tag One, Tag Two
---
This is the first paragraph of my blog post.

This is the second paragraph.

And so on...
```

### Building the Site

To convert text files to HTML blog posts:

```bash
python3 build_blog.py
```

This will:
- Process all `.txt` files in the `posts/` directory
- Process all `.md` files in the `case-studies/` directory
- Generate HTML files in `docs/blog/` 
- Update the blog index page at `docs/blog/index.html`
- Generate the Case Studies index and detail pages in `docs/case-studies/`
- Generate the crawler sitemap at `docs/sitemap.xml`
- Generate the agent-friendly site index at `docs/llms.txt`
- Generate the expanded agent context file at `docs/llms-full.txt`
- Generate Markdown mirrors for published pages and posts as `.html.md` files

### Updating Posts

Simply edit the `.txt` file and run `build_blog.py` again to regenerate the HTML.

## Local Development

To preview the site locally:

```bash
python3 -m http.server 8000 --directory docs
```

Then visit http://localhost:8000

### Theme Testing

The site follows the computer's light/dark appearance setting by default. To test a specific theme locally, add one of these query parameters:

- `http://localhost:8000/?theme=light`
- `http://localhost:8000/?theme=dark`
- `http://localhost:8000/?theme=system`
