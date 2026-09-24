import os
import shutil
import tempfile
import unittest
from pathlib import Path

import build_blog


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CaseStudyBuildTests(unittest.TestCase):
    def test_build_generates_case_study_pages_with_navigation(self):
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

            self.assertIn('Mailinator', index_html)
            self.assertIn(
                '/case-studies/mailinator-developer-experience.html',
                index_html,
            )
            self.assertIn('Project snapshot', detail_html)
            self.assertIn('Ruby', detail_html)
            self.assertIn('64.5%', detail_html)
            self.assertIn('/case-studies/index.html">Case Studies</a>', blog_html)
            self.assertIn('/case-studies/index.html">Case Studies</a>', detail_html)

    def test_static_page_navigation_links_to_case_studies(self):
        for relative_path in (
            'docs/index.html',
            'docs/about.html',
            'docs/services.html',
            'docs/contact.html',
        ):
            with self.subTest(path=relative_path):
                html = (REPOSITORY_ROOT / relative_path).read_text()
                self.assertIn(
                    '/case-studies/index.html">Case Studies</a>',
                    html,
                )


if __name__ == '__main__':
    unittest.main()
