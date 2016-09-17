import os
from string import Template
from os.path import join, abspath, basename

from cached_property import cached_property
from shell import shell
import yaml


SOURCE_FILE_TEXT = '<p><a href="{source_file}">Link to {source_file_basename}</a></p>'  # noqa


class Builder(object):
    exceptions = (
        'build', 'static', 'templates', 'tests', 'toolbox',
        # Warning: ignoring it to add it on the top position in the list
        'english',
    )

    def __init__(self):
        self.build_path = abspath('build')
        self.languages = []
        self.meta = {}

    def mkdir(self, path):
        "Silent make directories"
        if not os.path.isdir(path):
            os.makedirs(path)

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
        dir_list = filter(lambda x: not x.startswith('.'), dir_list)
        dir_list = ('english',) + tuple(dir_list)
        return dir_list

    def get_template(self, path):
        "Transform a path into a template"
        with open(path) as fd:
            template_string = fd.read()
        template = Template(template_string)
        return template

    def update_meta(self, directory):
        "Update meta information dictionary"
        # Search for meta
        filepath = join(directory, 'meta.yaml')
        if os.path.exists(filepath):
            with open(filepath) as fd:
                content = fd.read()
            self.meta[directory] = yaml.load(content)

    def write_html(self, target_filepath, body, title,
                   prefix='', source_file=''):
        "Write HTML page (body & title) in the target_filepath"
        if source_file:
            source_file_basename = basename(source_file)
            source_file = SOURCE_FILE_TEXT.format(
                source_file=source_file,
                source_file_basename=source_file_basename
            )
        html = self.main_template.substitute(
            body=body,
            title=title,
            static=prefix + 'static',
            license=prefix + 'license.html',
            version=self.version,
            git_version=self.git_version,
            source_file=source_file,
        )
        with open(target_filepath, 'w') as fd:
            fd.write(html)
