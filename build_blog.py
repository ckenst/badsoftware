#!/usr/bin/env python3
"""
Build blog posts from text files in posts/ directory.
Converts text files to HTML blog posts and updates the blog index.
"""

import os
import re
from datetime import datetime
from pathlib import Path


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


def generate_html(metadata, content):
    """Generate HTML for a blog post."""
    title = metadata.get('title', 'Untitled')
    date_str = metadata.get('date', '')
    formatted_date = format_date(date_str) if date_str else ''
    excerpt = metadata.get('excerpt', '')
    
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
      <button id="theme-toggle" class="theme-toggle" aria-pressed="false" aria-label="Toggle theme">🌙</button>
    </div>
  </header>

  <main class="container">
    <article class="blog-post">
      <p><a href="/blog/index.html">&larr; Back to blog</a></p>
      <h2>{title}</h2>
      <p class="blog-meta">Published {formatted_date}</p>
      {html_content}
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
        card = f'''      <article class="blog-card">
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
      <button id="theme-toggle" class="theme-toggle" aria-pressed="false" aria-label="Toggle theme">🌙</button>
    </div>
  </header>

  <main class="container">
    <h2>Blog</h2>
    <p>The latest from The Bad Software Company:</p>

    <section class="blog-list" aria-label="Blog posts">
{cards_html}
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 The Bad Software Company</p>
    </div>
  </footer>
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
        
        # Generate HTML
        html = generate_html(metadata, body)
        
        # Write HTML file
        slug = metadata.get('slug', post_file.stem)
        output_file = blog_dir / f"{slug}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  → Generated {output_file}")
        
        # Store post info for index
        posts.append({
            'title': metadata.get('title', 'Untitled'),
            'date': metadata.get('date', ''),
            'slug': slug,
            'excerpt': metadata.get('excerpt', '')
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
