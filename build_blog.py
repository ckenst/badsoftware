#!/usr/bin/env python3
"""Build the static blog, case studies, and machine-readable site indexes."""

import re
import xml.etree.ElementTree as ET
from html import escape
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from xml.dom import minidom


SITE_URL = 'https://badsoftware.com'
SLUG_PATTERN = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
MARKDOWN_ESCAPE_CHARS = '\\`[]<>()'
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
STATIC_PAGES = [
    {
        'path': 'index.html',
        'title': 'Home',
        'description': (
            'The Bad Software Company is a boutique systems-engineering advisory '
            'firm focused on quality, AI, Developer Relations, and practical '
            'product engineering.'
        ),
        'content': [
            "Software so bad, it's good.",
            (
                'We help teams understand why software, AI systems, and '
                'engineering organizations fail—and what to do next.'
            ),
            'Why Bad Software?',
            (
                'Most teams know when quality is slipping. Releases get slower. '
                'Bugs escape. Tests become noisy. AI-generated code adds speed, '
                'but also uncertainty. Confidence drops.'
            ),
            'The hard part is knowing why.',
            (
                'The Bad Software Company helps teams investigate the technical, '
                'organizational, and human systems behind software failure—so '
                'they can make better decisions, improve reliability, and build '
                'software they can trust.'
            ),
            (
                'Consulting includes quality, AI, and Developer Relations work: '
                'product strategy, architecture reviews, training, speaking, and '
                'honest feedback.'
            ),
            (
                'TestOpsy offers pragmatic testing strategies, test infrastructure, '
                'observability, and chaos testing to keep systems reliable.'
            ),
            'Design and build work includes full-stack development and rapid iteration.',
            'Founder-led by Chris Kenst',
            (
                'The Bad Software Company is founded by Chris Kenst '
                '(https://kenst.com), a software quality leader, writer, '
                'open-source contributor, and former President of the Association '
                'for Software Testing (https://associationforsoftwaretesting.org). '
                'Chris writes about software engineering, AI, systems thinking, '
                'and quality at Kenst.com (https://kenst.com), and created '
                'TestingConferences.org (https://testingconferences.org) to help '
                'the software community discover conferences and learning '
                'opportunities.'
            ),
        ],
    },
    {
        'path': 'about.html',
        'title': 'About',
        'description': (
            'Learn how The Bad Software Company helps organizations understand '
            'why software, AI systems, and engineering organizations fail to meet '
            'expectations.'
        ),
        'content': [
            'The Bad Software Company is a boutique systems-engineering advisory firm.',
            (
                'The Bad Software Company helps organizations understand why '
                'software, AI systems, and engineering organizations fail to meet '
                'expectations.'
            ),
            (
                'We investigate the hidden assumptions, failure modes, organizational '
                'dynamics, and system behaviors that create unreliable products and '
                'false confidence.'
            ),
            (
                'Through analysis, research, and advisory services, we help teams '
                'move beyond symptoms to address the underlying causes of bad software.'
            ),
            'Our goal is simple: help organizations build software they can trust.',
        ],
    },
    {
        'path': 'services.html',
        'title': 'Services',
        'description': (
            'Consulting, training, speaking, TestOpsy quality investigations, '
            'and full-stack design and build work.'
        ),
        'content': [
            'The Bad Software Company is a boutique systems-engineering advisory firm.',
            (
                'Consulting, training, and speaking help teams make better decisions '
                'about software quality, AI-assisted development, developer relations, '
                'and engineering systems.'
            ),
            (
                'Engagements include advisory work, product and architecture reviews, '
                'hands-on workshops, team training, conference talks, and executive '
                'briefings.'
            ),
            'A TestOpsy is a forensic examination of a software project\'s quality DNA.',
            (
                'A TestOpsy investigates the systems, processes, architecture, tooling, '
                'and feedback loops that shape software quality.'
            ),
            (
                'The three pillars of a TestOpsy are failure mode analysis, cause of '
                'failure investigation, and quality observability.'
            ),
            (
                'Deliverables include current-state quality assessment, risk and '
                'failure mode analysis, findings report with prioritized recommendations, '
                'executive summary, and follow-up review session.'
            ),
            (
                'Design and build work helps teams move from idea to working software '
                'with practical product design, full-stack implementation, and fast '
                'feedback loops.'
            ),
        ],
    },
    {
        'path': 'contact.html',
        'title': 'Contact',
        'description': 'Contact The Bad Software Company about advisory or build work.',
        'content': [
            'Contact The Bad Software Company at hello@badsoftware.com.',
        ],
    },
]


def navigation_html():
    """Return the shared primary navigation."""
    return '''      <nav>
        <a href="/index.html">Home</a>
        <a href="/about.html">About</a>
        <a href="/services.html">Services</a>
        <a href="/case-studies/index.html">Case Studies</a>
        <a href="/blog/index.html">Blog</a>
        <a href="/contact.html">Contact Us</a>
      </nav>'''


def site_header_html():
    """Return the shared site header used by generated pages."""
    return f'''  <header class="site-header">
    <div class="container">
      <h1 class="logo"><a href="/index.html" aria-label="The Bad Software Company home"><img class="logo-light" src="/assets/logos/light_background.png" alt="The Bad Software Company"><img class="logo-dark" src="/assets/logos/dark_background.png" alt="The Bad Software Company"></a></h1>
{navigation_html()}
    </div>
  </header>'''


def absolute_url(path):
    """Build a canonical absolute URL for a generated site path."""
    return f"{SITE_URL}/{path.lstrip('/')}"


def markdown_path(path):
    """Return the generated Markdown mirror path for an HTML page path."""
    return f'{path}.md'


def validate_slug(slug, post_file):
    """Validate that a post slug is safe as both a filename and URL path segment."""
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            f"{post_file}: invalid slug {slug!r}. Use lowercase letters, "
            "numbers, and single hyphens only."
        )


def markdown_inline(text):
    """Escape text for Markdown inline contexts and collapse metadata newlines."""
    normalized = ' '.join(str(text).split())
    return ''.join(
        f'\\{char}' if char in MARKDOWN_ESCAPE_CHARS else char
        for char in normalized
    )


def markdown_text(text):
    """Escape text while preserving existing paragraph and line breaks."""
    escaped_lines = []
    for line in str(text).splitlines():
        escaped = ''.join(
            f'\\{char}' if char in MARKDOWN_ESCAPE_CHARS else char
            for char in line
        )
        stripped = escaped.lstrip()
        leading_spaces = len(escaped) - len(stripped)
        if stripped.startswith(('#', '-', '+', '*', '>')):
            escaped = f'{escaped[:leading_spaces]}\\{stripped}'
        if re.match(r'^\d+\.', stripped):
            stripped = stripped.replace('.', r'\.', 1)
            escaped = f'{escaped[:leading_spaces]}{stripped}'
        escaped_lines.append(escaped)

    return '\n'.join(escaped_lines)


def first_paragraph(text):
    """Return the first non-empty paragraph from plain text."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs[0] if paragraphs else ''


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


def parse_case_study(content, source_file):
    """Extract case-study metadata from its Markdown source."""
    lines = content.splitlines()
    if not lines or not lines[0].startswith('# '):
        raise ValueError(f"{source_file}: case study must start with an H1 title")

    title = lines[0][2:].strip()
    summary = next((line.strip() for line in lines[1:] if line.strip()), '')
    slug = source_file.stem
    validate_slug(slug, source_file)

    return {
        'title': title,
        'summary': summary,
        'slug': slug,
        'body': content.strip(),
    }


def render_markdown_inline(text):
    """Render the small inline Markdown subset used by case studies."""
    rendered = escape(text, quote=False)
    rendered = re.sub(
        r'\[([^\]]+)\]\((https?://[^)]+)\)',
        lambda match: (
            f'<a href="{escape(match.group(2), quote=True)}" '
            f'target="_blank" rel="noopener">{match.group(1)}</a>'
        ),
        rendered,
    )
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', rendered)


def is_table_separator(line):
    """Return whether a Markdown table row is the header separator."""
    cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
    return bool(cells) and all(re.fullmatch(r':?-{3,}:?', cell) for cell in cells)


def render_case_study_markdown(content):
    """Render the block Markdown subset used by case-study source files."""
    lines = content.splitlines()
    rendered = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue

        heading = re.match(r'^(#{1,3})\s+(.+)$', line)
        if heading:
            level = len(heading.group(1))
            rendered.append(
                f'<h{level}>{render_markdown_inline(heading.group(2))}</h{level}>'
            )
            index += 1
            continue

        if (
            line.startswith('|')
            and index + 1 < len(lines)
            and is_table_separator(lines[index + 1])
        ):
            headers = [
                cell.strip() for cell in line.strip('|').split('|')
            ]
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip().startswith('|'):
                rows.append([
                    cell.strip()
                    for cell in lines[index].strip().strip('|').split('|')
                ])
                index += 1

            header_html = ''.join(
                f'<th scope="col">{render_markdown_inline(cell)}</th>'
                for cell in headers
            )
            rows_html = ''.join(
                '<tr>' + ''.join(
                    f'<td>{render_markdown_inline(cell)}</td>' for cell in row
                ) + '</tr>'
                for row in rows
            )
            rendered.append(
                '<div class="case-study-table-wrap"><table class="case-study-table">'
                f'<thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody>'
                '</table></div>'
            )
            continue

        unordered = line.startswith('- ')
        ordered = bool(re.match(r'^\d+\.\s+', line))
        if unordered or ordered:
            tag = 'ul' if unordered else 'ol'
            items = []
            pattern = r'^-\s+' if unordered else r'^\d+\.\s+'
            while index < len(lines):
                candidate = lines[index].strip()
                if not re.match(pattern, candidate):
                    break
                items.append(re.sub(pattern, '', candidate))
                index += 1
            items_html = ''.join(
                f'<li>{render_markdown_inline(item)}</li>' for item in items
            )
            rendered.append(f'<{tag}>{items_html}</{tag}>')
            continue

        paragraph_lines = [line]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if (
                not candidate
                or re.match(r'^#{1,3}\s+', candidate)
                or candidate.startswith('|')
                or candidate.startswith('- ')
                or re.match(r'^\d+\.\s+', candidate)
            ):
                break
            paragraph_lines.append(candidate)
            index += 1
        rendered.append(
            f'<p>{render_markdown_inline(" ".join(paragraph_lines))}</p>'
        )

    return '\n        '.join(rendered)


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
          <img class="author-avatar" src="/assets/chris-kenst.png" alt="Chris Kenst">
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
    title_html = escape(title, quote=False)
    excerpt_html = escape(excerpt, quote=True)
    tags = parse_tags(metadata)
    tags_html = tag_links(tags)
    footer_html = post_footer(title, slug)
    
    # Convert plain text paragraphs to HTML paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    html_content = '\n      '.join(f'<p>{escape(p, quote=False)}</p>' for p in paragraphs)
    
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{excerpt_html}">
  <title>{title_html} — The Bad Software Company Blog</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js" defer></script>
</head>
<body>
{site_header_html()}

  <main class="container">
    <article class="blog-post">
      <p><a href="/blog/index.html">&larr; Back to blog</a></p>
      <h2>{title_html}</h2>
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
        post_url = f"/blog/{quote(post['slug'])}.html"
        card = f'''      <article class="blog-card" data-tags="{escape(data_tags)}">
        <h3><a href="{post_url}">{escape(post['title'], quote=False)}</a></h3>
        <p class="blog-meta">{formatted_date}</p>
        <p>{escape(post['excerpt'], quote=False)}</p>
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
{site_header_html()}

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


def generate_case_study_html(case_study):
    """Generate a public HTML page for one case study."""
    title = escape(case_study['title'], quote=False)
    summary = escape(case_study['summary'], quote=True)
    rendered_body = render_case_study_markdown(case_study['body'])

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{summary}">
  <title>{title} — The Bad Software Company Case Studies</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js" defer></script>
</head>
<body>
{site_header_html()}

  <main class="container">
    <article class="case-study-detail">
      <p><a href="/case-studies/index.html">&larr; Back to case studies</a></p>
      {rendered_body}
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


def generate_case_studies_index(case_studies):
    """Generate the public case-studies index."""
    cards = []
    for case_study in case_studies:
        cards.append(f'''      <article class="case-study-card">
        <h3><a href="/case-studies/{quote(case_study['slug'])}.html">{escape(case_study['title'], quote=False)}</a></h3>
        <p>{escape(case_study['summary'], quote=False)}</p>
        <a class="section-link" href="/case-studies/{quote(case_study['slug'])}.html">Read the case study</a>
      </article>''')

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Case studies from The Bad Software Company.">
  <title>Case Studies — The Bad Software Company</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js" defer></script>
</head>
<body>
{site_header_html()}

  <main class="container">
    <h2>Case Studies</h2>
    <p>How investigation, engineering, and measurement improve real software systems.</p>
    <section class="case-study-list" aria-label="Case studies">
{chr(10).join(cards)}
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


def markdown_header(title, source_path, description=None):
    """Generate common metadata for Markdown mirrors."""
    lines = [
        f'# {markdown_inline(title)}',
        f'Source: {absolute_url(source_path)}',
    ]

    if description:
        lines.append(f'Summary: {markdown_inline(description)}')

    return lines


def generate_static_markdown(page):
    """Generate a Markdown mirror for a static page."""
    lines = markdown_header(
        f"The Bad Software Company - {page['title']}",
        page['path'],
        page['description'],
    )
    lines.extend(markdown_text(content) for content in page.get('content', []))
    return '\n\n'.join(lines).strip() + '\n'


def generate_blog_index_markdown(posts):
    """Generate a Markdown mirror for the blog index."""
    lines = markdown_header(
        'The Bad Software Company - Blog',
        'blog/index.html',
        'Articles from The Bad Software Company.',
    )
    lines.append('## Posts')

    for post in sorted(posts, key=lambda p: p['date'], reverse=True):
        formatted_date = format_date(post['date']) if post['date'] else 'Undated'
        post_markdown_path = markdown_path(f"blog/{post['slug']}.html")
        lines.append(
            f"- [{markdown_inline(post['title'])}]({absolute_url(post_markdown_path)}): "
            f"{markdown_inline(post['excerpt'])} Published {formatted_date}."
        )

    return '\n\n'.join(lines).strip() + '\n'


def generate_post_markdown(post):
    """Generate a Markdown mirror for a blog post."""
    title = post['title']
    source_path = f"blog/{post['slug']}.html"
    lines = markdown_header(
        f"The Bad Software Company Blog - {title}",
        source_path,
        post['excerpt'],
    )
    lines.extend([
        f"Published: {format_date(post['date']) if post['date'] else 'Undated'}",
    ])

    if post.get('tags'):
        lines.append(
            f"Tags: {', '.join(markdown_inline(tag) for tag in post['tags'])}"
        )

    lines.append(markdown_text(post['body']))
    return '\n\n'.join(lines).strip() + '\n'


def generate_case_studies_index_markdown(case_studies):
    """Generate a Markdown mirror for the case-studies index."""
    lines = markdown_header(
        'The Bad Software Company - Case Studies',
        'case-studies/index.html',
        'Case studies from The Bad Software Company.',
    )
    lines.append('## Case Studies')
    for case_study in case_studies:
        case_path = markdown_path(
            f"case-studies/{case_study['slug']}.html"
        )
        lines.append(
            f"- [{markdown_inline(case_study['title'])}]({absolute_url(case_path)}): "
            f"{markdown_inline(case_study['summary'])}"
        )
    return '\n\n'.join(lines).strip() + '\n'


def generate_case_study_markdown(case_study):
    """Generate a canonical Markdown mirror for one case study."""
    lines = markdown_header(
        f"The Bad Software Company Case Study - {case_study['title']}",
        f"case-studies/{case_study['slug']}.html",
        case_study['summary'],
    )
    lines.append(case_study['body'])
    return '\n\n'.join(lines).strip() + '\n'


def generate_markdown_mirrors(posts, case_studies):
    """Generate Markdown mirrors next to the published HTML pages."""
    for page in STATIC_PAGES:
        output_file = Path('docs') / markdown_path(page['path'])
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(generate_static_markdown(page))
        print(f"Generated {output_file}")

    blog_index_file = Path('docs') / markdown_path('blog/index.html')
    with open(blog_index_file, 'w', encoding='utf-8') as f:
        f.write(generate_blog_index_markdown(posts))
    print(f"Generated {blog_index_file}")

    for post in posts:
        post_file = Path('docs') / markdown_path(f"blog/{post['slug']}.html")
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(generate_post_markdown(post))
        print(f"Generated {post_file}")

    case_studies_dir = Path('docs/case-studies')
    case_studies_dir.mkdir(parents=True, exist_ok=True)
    case_index_file = Path('docs') / markdown_path('case-studies/index.html')
    with open(case_index_file, 'w', encoding='utf-8') as f:
        f.write(generate_case_studies_index_markdown(case_studies))
    print(f"Generated {case_index_file}")

    for case_study in case_studies:
        case_file = Path('docs') / markdown_path(
            f"case-studies/{case_study['slug']}.html"
        )
        with open(case_file, 'w', encoding='utf-8') as f:
            f.write(generate_case_study_markdown(case_study))
        print(f"Generated {case_file}")


def sitemap_entry(parent, path, lastmod=None):
    """Add a URL entry to the sitemap."""
    url = ET.SubElement(parent, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = absolute_url(path)

    if lastmod:
        lastmod_element = ET.SubElement(url, 'lastmod')
        lastmod_element.text = lastmod


def generate_sitemap(posts, case_studies):
    """Generate XML sitemap content for the static site and blog posts."""
    urlset = ET.Element(
        'urlset',
        xmlns='http://www.sitemaps.org/schemas/sitemap/0.9',
    )

    latest_post_date = max((post['date'] for post in posts), default=None)
    for page in STATIC_PAGES:
        sitemap_entry(urlset, page['path'])
        sitemap_entry(urlset, markdown_path(page['path']))

    sitemap_entry(urlset, 'blog/index.html', latest_post_date)
    sitemap_entry(urlset, markdown_path('blog/index.html'), latest_post_date)
    sitemap_entry(urlset, 'case-studies/index.html')
    sitemap_entry(urlset, markdown_path('case-studies/index.html'))
    sitemap_entry(urlset, 'llms.txt')
    sitemap_entry(urlset, 'llms-full.txt')

    for post in sorted(posts, key=lambda p: p['date'], reverse=True):
        sitemap_entry(urlset, f"blog/{post['slug']}.html", post['date'])
        sitemap_entry(
            urlset,
            markdown_path(f"blog/{post['slug']}.html"),
            post['date'],
        )

    for case_study in case_studies:
        source_path = f"case-studies/{case_study['slug']}.html"
        sitemap_entry(urlset, source_path)
        sitemap_entry(urlset, markdown_path(source_path))

    rough_xml = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent='  ')
    return '\n'.join(line for line in pretty_xml.splitlines() if line.strip()) + '\n'


def generate_llms_txt(posts, case_studies):
    """Generate an llms.txt overview for AI agents and other text consumers."""
    lines = [
        '# The Bad Software Company',
        '',
        (
            '> Boutique systems-engineering advisory firm helping organizations '
            'understand and improve software quality, AI-assisted development, '
            'Developer Relations, and practical product delivery.'
        ),
        '',
        'This file points agents to Markdown-friendly mirrors of the primary '
        'public pages and blog posts for badsoftware.com. Each mirror includes '
        'its canonical HTML source URL.',
        '',
        '## Core Pages',
    ]

    for page in STATIC_PAGES:
        page_markdown_path = markdown_path(page['path'])
        lines.append(
            f"- [{markdown_inline(page['title'])}]({absolute_url(page_markdown_path)}): "
            f"{markdown_inline(page['description'])}"
        )

    lines.extend([
        f"- [Blog]({absolute_url(markdown_path('blog/index.html'))}): Articles from The Bad Software Company.",
        '',
        '## Case Studies',
    ])

    for case_study in case_studies:
        case_path = markdown_path(
            f"case-studies/{case_study['slug']}.html"
        )
        lines.append(
            f"- [{markdown_inline(case_study['title'])}]({absolute_url(case_path)}): "
            f"{markdown_inline(case_study['summary'])}"
        )

    lines.extend([
        '',
        '## Blog Posts',
    ])

    for post in sorted(posts, key=lambda p: p['date'], reverse=True):
        formatted_date = format_date(post['date']) if post['date'] else 'Undated'
        excerpt = post['excerpt'].rstrip('.')
        post_path = markdown_path(f"blog/{post['slug']}.html")
        lines.append(
            f"- [{markdown_inline(post['title'])}]({absolute_url(post_path)}): "
            f"{markdown_inline(excerpt)}. Published {formatted_date}."
        )

    lines.extend([
        '',
        '## Machine-Readable Indexes',
        '- [XML sitemap](https://badsoftware.com/sitemap.xml): Canonical URL list for crawlers.',
        '- [Full LLM context](https://badsoftware.com/llms-full.txt): Expanded text context for agents.',
    ])

    return '\n'.join(lines) + '\n'


def generate_llms_full_txt(posts, case_studies):
    """Generate a fuller single-file context bundle for AI agents."""
    lines = [
        '# The Bad Software Company',
        '',
        (
            'The Bad Software Company is a boutique systems-engineering advisory '
            'firm helping organizations understand and improve software quality, '
            'AI-assisted development, Developer Relations, and practical product '
            'delivery.'
        ),
        '',
        'Canonical site: https://badsoftware.com/',
        'Sitemap: https://badsoftware.com/sitemap.xml',
        'LLMS index: https://badsoftware.com/llms.txt',
        '',
        '## Core Pages',
    ]

    for page in STATIC_PAGES:
        lines.extend([
            '',
            f"### {markdown_inline(page['title'])}",
            f"Source: {absolute_url(page['path'])}",
            f"Markdown: {absolute_url(markdown_path(page['path']))}",
            '',
            markdown_text(page['description']),
            '',
            '\n\n'.join(markdown_text(content) for content in page.get('content', [])),
        ])

    lines.extend(['', '## Case Studies'])

    for case_study in case_studies:
        source_path = f"case-studies/{case_study['slug']}.html"
        lines.extend([
            '',
            f"### {markdown_inline(case_study['title'])}",
            f"Source: {absolute_url(source_path)}",
            f"Markdown: {absolute_url(markdown_path(source_path))}",
            '',
            case_study['body'],
        ])

    lines.extend(['', '## Blog Posts'])

    for post in sorted(posts, key=lambda p: p['date'], reverse=True):
        post_source_path = f"blog/{post['slug']}.html"
        post_markdown_path = markdown_path(post_source_path)
        lines.extend([
            '',
            f"### {markdown_inline(post['title'])}",
            f"Source: {absolute_url(post_source_path)}",
            f"Markdown: {absolute_url(post_markdown_path)}",
            f"Published: {format_date(post['date']) if post['date'] else 'Undated'}",
        ])

        if post.get('tags'):
            lines.append(
                f"Tags: {', '.join(markdown_inline(tag) for tag in post['tags'])}"
            )

        body_lines = ['', markdown_text(post['body'])]
        if post['excerpt'].strip() != first_paragraph(post['body']):
            body_lines = ['', markdown_text(post['excerpt']), *body_lines]

        lines.extend([
            *body_lines,
        ])

    return '\n'.join(lines).strip() + '\n'


def main():
    """Build public blog and case-study pages."""
    posts_dir = Path('posts')
    blog_dir = Path('docs/blog')
    case_studies_source_dir = Path('case-studies')
    case_studies_output_dir = Path('docs/case-studies')
    
    if not posts_dir.exists():
        print("Error: posts/ directory not found")
        return
    
    blog_dir.mkdir(parents=True, exist_ok=True)
    case_studies_output_dir.mkdir(parents=True, exist_ok=True)
    
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
        validate_slug(slug, post_file)
        
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
            'tags': parse_tags(metadata),
            'body': body,
        })
    
    # Generate index page
    if posts:
        index_html = generate_index(posts)
        index_file = blog_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"\nGenerated blog index with {len(posts)} post(s)")

    case_studies = []
    for case_study_file in sorted(case_studies_source_dir.glob('*.md')):
        print(f"Processing {case_study_file.name}...")
        case_study = parse_case_study(
            case_study_file.read_text(encoding='utf-8'),
            case_study_file,
        )
        case_studies.append(case_study)

        output_file = case_studies_output_dir / f"{case_study['slug']}.html"
        output_file.write_text(
            generate_case_study_html(case_study),
            encoding='utf-8',
        )
        print(f"  → Generated {output_file}")

    case_studies_index_file = case_studies_output_dir / 'index.html'
    case_studies_index_file.write_text(
        generate_case_studies_index(case_studies),
        encoding='utf-8',
    )
    print(f"Generated case studies index with {len(case_studies)} case study/studies")

    sitemap_file = Path('docs/sitemap.xml')
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write(generate_sitemap(posts, case_studies))
    print(f"Generated {sitemap_file}")

    llms_file = Path('docs/llms.txt')
    with open(llms_file, 'w', encoding='utf-8') as f:
        f.write(generate_llms_txt(posts, case_studies))
    print(f"Generated {llms_file}")

    llms_full_file = Path('docs/llms-full.txt')
    with open(llms_full_file, 'w', encoding='utf-8') as f:
        f.write(generate_llms_full_txt(posts, case_studies))
    print(f"Generated {llms_full_file}")

    generate_markdown_mirrors(posts, case_studies)
    
    print("\nBuild complete!")


if __name__ == '__main__':
    main()
