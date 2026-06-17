# badsoftware

The Bad Software Company website.

## Blog Posts

Blog posts are written as simple text files in the `posts/` directory and converted to HTML using `build_blog.py`.

### Writing a Blog Post

1. Create a new `.txt` file in the `posts/` directory
2. Add metadata at the top (title, date, slug, excerpt) followed by `---`
3. Write your content as plain text paragraphs (separated by blank lines)
4. Run `python3 build_blog.py` to generate the HTML

Example format:

```
title: My Blog Post Title
date: 2026-06-17
slug: my-post-slug
excerpt: A short description of the post.
---
This is the first paragraph of my blog post.

This is the second paragraph.

And so on...
```

### Building the Blog

To convert text files to HTML blog posts:

```bash
python3 build_blog.py
```

This will:
- Process all `.txt` files in the `posts/` directory
- Generate HTML files in `docs/blog/` 
- Update the blog index page at `docs/blog/index.html`

### Updating Posts

Simply edit the `.txt` file and run `build_blog.py` again to regenerate the HTML.

## Local Development

To preview the site locally:

```bash
python3 -m http.server 8000 --directory docs
```

Then visit http://localhost:8000

