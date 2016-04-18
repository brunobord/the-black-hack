import shutil
import os
from os.path import join
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

if __name__ == '__main__':

    build_path = 'build'
    static_path = join(build_path, 'static')

    exceptions = ['.tox', '.git', 'build', 'static']
    dir_list = [d for d in os.listdir('.') if d not in exceptions]
    dir_list = filter(lambda x: os.path.isdir(x), dir_list)

    if not os.path.isdir(build_path):
        os.makedirs(build_path)
    if os.path.isdir(static_path):
        shutil.rmtree(static_path)
    shutil.copytree('static', static_path)

    for directory in dir_list:
        filepath = join(directory, 'the-black-hack.md')
        if os.path.exists(filepath):
            with open(filepath) as fd:
                source = fd.read()
            html = markdown.markdown(
                source,
                extensions=[GithubFlavoredMarkdownExtension()]
            )
            target_dir = join(build_path, directory)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            target_filepath = join(target_dir, 'index.html')
            with open(target_filepath, 'w') as fd:
                fd.write(html)
