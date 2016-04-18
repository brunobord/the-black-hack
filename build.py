import shutil
import os
from string import Template
from os.path import join
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

if __name__ == '__main__':

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
            )
            target_dir = join(build_path, directory)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            target_filepath = join(target_dir, 'index.html')
            with open(target_filepath, 'w') as fd:
                fd.write(html)

    body = []
    body.append('<h1>The Black Hack available texts</h1>')
    body.append('<ul>')
    for language in languages:
        body.append(
            '<a href="{language}/">{language}</a>'.format(
                language=language
            )
        )
    body.append('</ul>')
    html = template.substitute(
        body='\n'.join(body),
        title="Home",
    )
    with open(join(build_path, 'index.html'), 'w') as fd:
        fd.write(html)
