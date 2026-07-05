#!/usr/bin/env python3
"""
Build blog posts from text files in posts/ directory.
Converts text files to HTML blog posts and updates the blog index.
"""

import os
import re
from html import escape
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


SITE_URL = 'https://badsoftware.com'
AUTHOR_NAME = 'Chris Kenst'
AUTHOR_BIO_HTML = (
    'Chris Kenst studies why software succeeds—and why it fails. He is the founder '
    'of The Bad Software Company, author of '
    '<a href="https://kenst.com" target="_blank" rel="noopener">Kenst.com</a>, '
    'creator of '
    '<a href="https://testingconferences.org" target="_blank" rel="noopener">'
    'TestingConferences.org</a>, an open-source contributor, and former President '
    'of the '
    '<a href="https://associationforsoftwaretesting.org" target="_blank" '
    'rel="noopener">Association for Software Testing</a>.'
)


def parse_post(content):
    """Parse a blog post text file into metadata and content."""
    parts = content.split('---', 1)
    if len(parts) != 2:
        raise ValueError("Post must have metadata separated by '---'")
    
    metadata_text, body = parts
    metadata = {}
    
    for line in metadata_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    return metadata, body.strip()


def format_date(date_str):
    """Convert YYYY-MM-DD to 'Month DD, YYYY' format."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%B %d, %Y')


def parse_tags(metadata):
    """Parse comma-separated tags from post metadata."""
    tags = metadata.get('tags', '')
    return [tag.strip() for tag in tags.split(',') if tag.strip()]


def tag_links(tags):
    """Generate linked tags for blog posts."""
    if not tags:
        return ''

    links = [
        f'<a class="blog-tag" href="/blog/index.html?tag={quote(tag)}">{escape(tag)}</a>'
        for tag in tags
    ]
    return f'<p class="blog-tags">Tags: {", ".join(links)}</p>'


def post_footer(title, slug):
    """Generate social share links and author callout for a blog post."""
    post_url = f'{SITE_URL}/blog/{slug}.html'
    encoded_title = quote(title)
    encoded_url = quote(post_url, safe='')
    x_share_url = f'https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}'
    linkedin_share_url = f'https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}'

    return f'''      <footer class="blog-post-footer">
        <section class="blog-share" aria-label="Share this article">
          <h3>Share this article</h3>
          <div class="blog-share-links">
            <a class="blog-share-link" href="{x_share_url}" target="_blank" rel="noopener" aria-label="Share on X">X</a>
            <a class="blog-share-link" href="{linkedin_share_url}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">in</a>
          </div>
        </section>

        <section class="author-card" aria-label="Written by">
          <div class="author-avatar" aria-hidden="true">CK</div>
          <div>
            <p class="author-label">Written by</p>
            <h3>{escape(AUTHOR_NAME)}</h3>
            <p>{AUTHOR_BIO_HTML}</p>
          </div>
        </section>
      </footer>'''


def generate_html(metadata, content, slug):
    """Generate HTML for a blog post."""
    title = metadata.get('title', 'Untitled')
    date_str = metadata.get('date', '')
    formatted_date = format_date(date_str) if date_str else ''
    excerpt = metadata.get('excerpt', '')
    tags = parse_tags(metadata)
    tags_html = tag_links(tags)
    footer_html = post_footer(title, slug)
    
    # Convert plain text paragraphs to HTML paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    html_content = '\n      '.join(f'<p>{p}</p>' for p in paragraphs)
    
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{excerpt}">
  <title>{title} — The Bad Software Company Blog</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js" defer></script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <h1 class="logo"><a href="/index.html" aria-label="The Bad Software Company home"><img class="logo-light" src="/assets/logos/light_background.png" alt="The Bad Software Company"><img class="logo-dark" src="/assets/logos/dark_background.png" alt="The Bad Software Company"></a></h1>
      <nav>
        <a href="/index.html">Home</a>
        <a href="/about.html">About</a>
        <a href="/services.html">Services</a>
        <a href="/blog/index.html">Blog</a>
        <a href="/contact.html">Contact Us</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <article class="blog-post">
      <p><a href="/blog/index.html">&larr; Back to blog</a></p>
      <h2>{title}</h2>
      <p class="blog-meta">Published {formatted_date}</p>
      {tags_html}
      {html_content}
{footer_html}
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 The Bad Software Company</p>
    </div>
  </footer>
</body>
</html>
'''


def generate_index(posts):
    """Generate the blog index HTML."""
    # Sort posts by date (newest first)
    sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)
    
    # Generate blog cards
    cards = []
    for post in sorted_posts:
        formatted_date = format_date(post['date'])
        tags = post.get('tags', [])
        data_tags = '|'.join(tag.lower() for tag in tags)
        card = f'''      <article class="blog-card" data-tags="{escape(data_tags)}">
        <h3><a href="/blog/{post['slug']}.html">{post['title']}</a></h3>
        <p class="blog-meta">{formatted_date}</p>
        <p>{post['excerpt']}</p>
      </article>'''
        cards.append(card)
    
    cards_html = '\n'.join(cards)
    
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Blog — The Bad Software Company</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js" defer></script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <h1 class="logo"><a href="/index.html" aria-label="The Bad Software Company home"><img class="logo-light" src="/assets/logos/light_background.png" alt="The Bad Software Company"><img class="logo-dark" src="/assets/logos/dark_background.png" alt="The Bad Software Company"></a></h1>
      <nav>
        <a href="/index.html">Home</a>
        <a href="/about.html">About</a>
        <a href="/services.html">Services</a>
        <a href="/blog/index.html">Blog</a>
        <a href="/contact.html">Contact Us</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h2>Blog</h2>
    <p id="blog-intro">The latest from The Bad Software Company:</p>

    <section class="blog-list" aria-label="Blog posts">
{cards_html}
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 The Bad Software Company</p>
    </div>
  </footer>
  <script>
    const selectedTag = new URLSearchParams(window.location.search).get('tag');
    if (selectedTag) {{
      const normalizedTag = selectedTag.toLowerCase();
      const cards = document.querySelectorAll('.blog-card');
      let visibleCount = 0;

      cards.forEach((card) => {{
        const tags = (card.dataset.tags || '').split('|');
        const isVisible = tags.includes(normalizedTag);
        card.hidden = !isVisible;
        if (isVisible) visibleCount += 1;
      }});

      const intro = document.getElementById('blog-intro');
      intro.textContent = visibleCount === 1
        ? `1 article tagged "${{selectedTag}}":`
        : `${{visibleCount}} articles tagged "${{selectedTag}}":`;
    }}
  </script>
</body>
</html>
'''


def main():
    """Build all blog posts from text files."""
    posts_dir = Path('posts')
    blog_dir = Path('docs/blog')
    
    if not posts_dir.exists():
        print("Error: posts/ directory not found")
        return
    
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all text files in posts/
    posts = []
    for post_file in sorted(posts_dir.glob('*.txt')):
        # Skip template file
        if post_file.name == 'template.txt':
            continue
            
        print(f"Processing {post_file.name}...")
        
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata, body = parse_post(content)
        
        slug = metadata.get('slug', post_file.stem)
        
        # Generate HTML
        html = generate_html(metadata, body, slug)
        
        # Write HTML file
        output_file = blog_dir / f"{slug}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  → Generated {output_file}")
        
        # Store post info for index
        posts.append({
            'title': metadata.get('title', 'Untitled'),
            'date': metadata.get('date', ''),
            'slug': slug,
            'excerpt': metadata.get('excerpt', ''),
            'tags': parse_tags(metadata)
        })
    
    # Generate index page
    if posts:
        index_html = generate_index(posts)
        index_file = blog_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"\nGenerated blog index with {len(posts)} post(s)")
    
    print("\nBuild complete!")


if __name__ == '__main__':
    main()
