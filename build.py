"""
The Black Hack OGL content Python builder.

This script is Public Domain.
"""
import shutil
import os
from string import Template
from os.path import join

import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import yaml
from shell import shell


if __name__ == '__main__':

    version = shell('git describe --tags --abbrev=0').output(raw=True).strip()
    git_version = shell('git describe --tags').output(raw=True).strip()

    build_path = 'build'
    static_path = join(build_path, 'static')
    with open(join('templates', 'base.html')) as fd:
        template_string = fd.read()
    template = Template(template_string)

    exceptions = ['.tox', '.git', 'build', 'static', 'templates']
    dir_list = [d for d in os.listdir('.') if d not in exceptions]
    dir_list = filter(lambda x: os.path.isdir(x), dir_list)

    if not os.path.isdir(build_path):
        os.makedirs(build_path)
    if os.path.isdir(static_path):
        shutil.rmtree(static_path)
    shutil.copytree('static', static_path)

    languages = []
    meta = {}

    for directory in dir_list:
        filepath = join(directory, 'the-black-hack.md')
        if os.path.exists(filepath):
            languages.append(directory)
            with open(filepath) as fd:
                source = fd.read()
            body = markdown.markdown(
                source,
                extensions=[GithubFlavoredMarkdownExtension()]
            )
            html = template.substitute(
                body=body,
                title=directory,
                static='../static',
                version=version,
                git_version=git_version,
            )
            target_dir = join(build_path, directory)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            target_filepath = join(target_dir, 'index.html')
            with open(target_filepath, 'w') as fd:
                fd.write(html)
        # Search for meta
        filepath = join(directory, 'meta.yaml')
        if os.path.exists(filepath):
            with open(filepath) as fd:
                content = fd.read()
            meta[directory] = yaml.load(content)

    # Homepage
    with open(join('index.md')) as fd:
        template_string = fd.read()
    homepage_md = Template(template_string)

    # Build text list
    text_list = []
    text_list.append('')
    for language in languages:
        label = language
        author = None
        if language in meta:
            label = meta[language].get('label', label)
            author = meta[language].get('author', None)
        item = '* [{label}]({language}/)'.format(
            label=label,
            language=language
        )

        # Add optional author
        if author:
            item = '{}, by {}'.format(item, author)
        text_list.append(item)

    text_list.append('')
    # Build generated body using text_list
    body_md = homepage_md.substitute(text_list='\n'.join(text_list))
    body_html = markdown.markdown(
        body_md,
        extensions=[GithubFlavoredMarkdownExtension()]
    )
    # Build html page content
    html = template.substitute(
        body=body_html,
        title="Home",
        static='static',
        version=version,
        git_version=git_version,
    )
    with open(join(build_path, 'index.html'), 'w') as fd:
        fd.write(html)

    # Build License page
    with open('LICENSE') as fd:
        license_md = fd.read()
    license_html = markdown.markdown(
        license_md,
        extensions=[GithubFlavoredMarkdownExtension()]
    )
    # Build html page content
    html = template.substitute(
        body=license_html,
        title="Open Gaming License",
        static='static',
        version=version,
        git_version=git_version,
    )
    with open(join(build_path, 'license.html'), 'w') as fd:
        fd.write(html)
