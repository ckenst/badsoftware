import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import build_blog


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


EXPECTED_NAVIGATION = (
    ('/testopsy.html', 'TestOpsy'),
    ('/advisory.html', 'Advisory'),
    ('/implementation.html', 'Implementation'),
    ('/case-studies/index.html', 'Case Studies'),
    ('/blog/index.html', 'Insights'),
    ('/about.html', 'About'),
    ('/contact.html', 'Discuss a TestOpsy'),
)


class SiteBuildTests(unittest.TestCase):
    def assert_has_primary_navigation(self, html):
        for href, label in EXPECTED_NAVIGATION:
            with self.subTest(href=href):
                self.assertRegex(
                    html,
                    rf'href="{re.escape(href)}"[^>]*>{re.escape(label)}</a>',
                )

        self.assertNotIn('href="/services.html">Services</a>', html)
        self.assertNotIn('href="/blog/index.html">Blog</a>', html)
        self.assertNotIn('href="/contact.html">Contact Us</a>', html)

    def test_build_generates_case_studies_and_insights_with_new_navigation(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            workspace = Path(temp_directory)
            shutil.copytree(REPOSITORY_ROOT / 'posts', workspace / 'posts')
            shutil.copytree(REPOSITORY_ROOT / 'case-studies', workspace / 'case-studies')
            (workspace / 'docs').mkdir()

            previous_directory = Path.cwd()
            try:
                os.chdir(workspace)
                build_blog.main()
            finally:
                os.chdir(previous_directory)

            index_html = (workspace / 'docs/case-studies/index.html').read_text()
            detail_html = (
                workspace
                / 'docs/case-studies/mailinator-developer-experience.html'
            ).read_text()
            blog_html = (workspace / 'docs/blog/index.html').read_text()
            sitemap = (workspace / 'docs/sitemap.xml').read_text()

            self.assertIn('Mailinator', index_html)
            self.assertIn(
                '/case-studies/mailinator-developer-experience.html',
                index_html,
            )
            self.assertIn('Project snapshot', detail_html)
            self.assertIn('Ruby', detail_html)
            self.assertIn('64.5%', detail_html)
            self.assertIn('<title>Insights — The Bad Software Company</title>', blog_html)
            self.assertIn('<h2>Insights</h2>', blog_html)
            self.assertIn('Articles, research, talks, and company news', blog_html)
            self.assert_has_primary_navigation(blog_html)
            self.assert_has_primary_navigation(detail_html)
            for page in ('testopsy', 'advisory', 'implementation'):
                self.assertTrue((workspace / f'docs/{page}.html.md').exists())
                self.assertIn(
                    f'https://badsoftware.com/{page}.html',
                    sitemap,
                )

    def test_static_pages_use_new_primary_navigation(self):
        for relative_path in (
            'docs/index.html',
            'docs/about.html',
            'docs/services.html',
            'docs/testopsy.html',
            'docs/advisory.html',
            'docs/implementation.html',
            'docs/contact.html',
        ):
            with self.subTest(path=relative_path):
                html = (REPOSITORY_ROOT / relative_path).read_text()
                self.assert_has_primary_navigation(html)

    def test_homepage_connects_assessment_to_implementation(self):
        html = (REPOSITORY_ROOT / 'docs/index.html').read_text()

        self.assertIn('Start with a TestOpsy', html)
        self.assertIn('Each service stands on its own', html)
        self.assertIn('href="/testopsy.html"', html)
        self.assertIn('href="/advisory.html"', html)
        self.assertIn('href="/implementation.html"', html)
        self.assertIn(
            'href="/case-studies/mailinator-developer-experience.html"',
            html,
        )

    def test_testopsy_page_explains_what_happens_after_the_assessment(self):
        html = (REPOSITORY_ROOT / 'docs/testopsy.html').read_text()

        self.assertIn('What happens after a TestOpsy?', html)
        self.assertIn('href="/advisory.html"', html)
        self.assertIn('href="/implementation.html"', html)

    def test_contact_page_offers_the_fit_call_from_issue_18(self):
        html = (REPOSITORY_ROOT / 'docs/contact.html').read_text()

        self.assertIn('<h2>Discuss a TestOpsy</h2>', html)
        self.assertIn('Request a free 30-minute fit call', html)
        self.assertIn('whether a TestOpsy is appropriate', html)
        self.assertNotIn('Book a free 30-minute fit call', html)

    def test_implementation_is_available_as_a_standalone_service(self):
        html = (REPOSITORY_ROOT / 'docs/implementation.html').read_text()

        self.assertIn('Implementation is a standalone service', html)


if __name__ == '__main__':
    unittest.main()
