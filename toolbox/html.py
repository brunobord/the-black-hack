import os
from os.path import join
import shutil

from .core import Builder, convert_md_source


HTACCESS = """
# Serving .md files as UTF-8.
AddType 'text/plain; charset=UTF-8' md
""".strip()
DEFAULT_PAGE = {}


class HTMLBuilder(Builder):

    def convert_md(self, filepath):
        "Convert a Markdown file into HTML"
        with open(filepath) as fd:
            source = fd.read()
        return convert_md_source(source)

    def build_homepage_text_list(self):
        "Build the full text list for the homepage"
        # Build text list
        text_list = []
        text_list.append('')
        for language in self.languages:
            label = language
            meta_language = self.meta.get(language, {})
            label = meta_language.get('label', label)
            text_list.append('### {}'.format(label))
            for page in meta_language.get('pages', [DEFAULT_PAGE]):
                item = self.get_item_homepage(language, page)
                text_list.append(item)

        text_list.append('')
        return text_list

    def build_homepage(self):
        "Build the Home page"
        homepage_md = self.get_template('index.md')
        text_list = self.build_homepage_text_list()
        # Build generated body using text_list
        body_md = homepage_md.substitute(
            text_list='\n'.join(text_list),
            language_count=len(self.languages),
        )
        body_html = convert_md_source(body_md)
        # Build html page content
        self.write_html(
            join(self.build_path, 'index.html'),
            body=body_html,
            title="Home",
        )

    def page_update(self, language, page):
        """
        Update the page dict, to be shared by the individual pages & homepage.
        """
        page['language'] = language
        if 'filename' not in page:
            page['filename'] = 'the-black-hack.md'

        basefile, _ = os.path.splitext(page['filename'])
        if page['filename'] == 'the-black-hack.md':
            page['target_filename'] = 'index'
        else:
            page['target_filename'] = basefile
        page['raw_filename'] = basefile

    def get_page_title(self, directory):
        "Extract page title form meta information"
        if directory in self.meta:
            meta = self.meta[directory]
            if 'label' in meta:
                return meta.get('label', None)

    def page_build(self, directory, page):
        "Build individual page."
        title = self.get_page_title(directory) or directory
        source_filepath = join(directory, page['filename'])
        body = self.convert_md(source_filepath)
        target_dir = join(self.build_path, directory)
        target_filename = page['target_filename']
        self.mkdir(target_dir)
        target_filepath = join(target_dir, '{}.html'.format(target_filename))
        self.write_html(
            target_filepath,
            body=body,
            title=title,
            prefix="../",
            source_file=page['filename'],
        )
        # Copy source to the target_dir
        shutil.copyfile(source_filepath, join(target_dir, page['filename']))

    def get_item_homepage(self, language, page):
        label = page.get('label', page['raw_filename'])
        if page['target_filename'] != 'index':
            target = '{}.html'.format(page['target_filename'])
        else:
            target = ''
        item = '* [{label}]({language}/{target})'.format(
            label=label,
            language=language,
            target=target,
        )

        # Add optional author
        author = page.get('author', None)
        if author:
            item = '{}, by {}'.format(item, author)

        # Add optional version
        version = page.get('version', None)
        if version:
            item = '{} (v{})'.format(item, version)

        # Add link to source
        item = '{item} ([source]({language}/{filename}))'.format(
            item=item,
            language=language,
            filename=page['filename'],
        )

        return item

    def build_license(self):
        "Build License page"
        license_html = self.convert_md('LICENSE')
        self.write_html(
            join(self.build_path, 'license.html'),
            body=license_html,
            title="Open Gaming License",
        )

    def build_dir(self, directory):
        "Build the directory"
        mandatory_file = join(directory, 'the-black-hack.md')
        if os.path.exists(mandatory_file):
            self.languages.append(directory)
            meta_language = self.meta.get(directory, {})
            for page in meta_language.get('pages', [DEFAULT_PAGE]):
                self.page_update(directory, page)
                self.page_build(directory, page)

    def build(self):
        "Build main method"
        self.mkdir(self.build_path)
        if os.path.isdir(self.static_path):
            shutil.rmtree(self.static_path)
        shutil.copytree('static', self.static_path)
        # Write an .htaccess file
        with open(join(self.build_path, '.htaccess'), 'w') as fd:
            fd.write(HTACCESS)

        for directory in self.dir_list:
            self.update_meta(directory)
            self.build_dir(directory)
        self.build_homepage()
        self.build_license()
