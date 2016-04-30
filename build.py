"""
The Black Hack OGL content Python builder.

This script is Public Domain.
"""
import shutil
import os
from string import Template
from os.path import join, abspath

from cached_property import cached_property
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from shell import shell
import yaml


class Builder(object):

    exceptions = ('.tox', '.git', 'build', 'static', 'templates')

    def __init__(self):
        self.build_path = abspath('build')
        self.languages = []
        self.meta = {}

    @cached_property
    def static_path(self):
        return join(self.build_path, 'static')

    @cached_property
    def version(self):
        return shell('git describe --tags --abbrev=0').output(raw=True).strip()

    @cached_property
    def git_version(self):
        return shell('git describe --tags').output(raw=True).strip()

    @cached_property
    def dir_list(self):
        dir_list = [d for d in os.listdir('.') if d not in self.exceptions]
        dir_list = filter(lambda x: os.path.isdir(x), dir_list)
        return dir_list

    def get_template(self, path):
        "Transform a path into a template"
        with open(path) as fd:
            template_string = fd.read()
        template = Template(template_string)
        return template

    def convert_md_source(self, source):
        "Convert Markdown content into HTML"
        html = markdown.markdown(
            source,
            extensions=[GithubFlavoredMarkdownExtension()]
        )
        return html

    def convert_md(self, filepath):
        "Convert a Markdown file into HTML"
        with open(filepath) as fd:
            source = fd.read()
        return self.convert_md_source(source)

    def mkdir(self, path):
        "Silent make directories"
        if not os.path.isdir(path):
            os.makedirs(path)

    def write_html(self, target_filepath, body, title, static='static'):
        "Write HTML page (body & title) in the target_filepath"
        html = self.main_template.substitute(
            body=body,
            title=title,
            static=static,
            version=self.version,
            git_version=self.git_version,
        )
        with open(target_filepath, 'w') as fd:
            fd.write(html)

    def build_dir(self, directory):
        "Build the directory"
        filepath = join(directory, 'the-black-hack.md')
        if os.path.exists(filepath):
            self.languages.append(directory)
            body = self.convert_md(filepath)
            target_dir = join(self.build_path, directory)
            self.mkdir(target_dir)
            target_filepath = join(target_dir, 'index.html')
            self.write_html(
                target_filepath,
                body,
                directory,
                "../static",
            )

    def update_meta(self, directory):
        "Update meta information dictionary"
        # Search for meta
        filepath = join(directory, 'meta.yaml')
        if os.path.exists(filepath):
            with open(filepath) as fd:
                content = fd.read()
            self.meta[directory] = yaml.load(content)

    def build_homepage_text_list(self):
        "Build the full text list for the homepage"
        # Build text list
        text_list = []
        text_list.append('')
        for language in self.languages:
            label = language
            author = None
            if language in self.meta:
                label = self.meta[language].get('label', label)
                author = self.meta[language].get('author', None)
            item = '* [{label}]({language}/)'.format(
                label=label,
                language=language
            )

            # Add optional author
            if author:
                item = '{}, by {}'.format(item, author)
            text_list.append(item)

        text_list.append('')
        return text_list

    def build_homepage(self):
        "Build the Home page"
        homepage_md = self.get_template('index.md')
        text_list = self.build_homepage_text_list()
        # Build generated body using text_list
        body_md = homepage_md.substitute(text_list='\n'.join(text_list))
        body_html = self.convert_md_source(body_md)
        # Build html page content
        self.write_html(
            join(self.build_path, 'index.html'),
            body_html,
            "Home"
        )

    def build_license(self):
        "Build License page"
        license_html = self.convert_md('LICENSE')
        self.write_html(
            join(self.build_path, 'license.html'),
            license_html,
            "Open Gaming License",
        )

    def build(self):
        "Build main method"
        self.mkdir(self.build_path)
        if os.path.isdir(self.static_path):
            shutil.rmtree(self.static_path)
        shutil.copytree('static', self.static_path)

        self.main_template = self.get_template(join('templates', 'base.html'))

        for directory in self.dir_list:
            self.build_dir(directory)
            self.update_meta(directory)
        self.build_homepage()
        self.build_license()

if __name__ == '__main__':

    builder = Builder()
    builder.build()
