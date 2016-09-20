from collections import namedtuple
import os
from os.path import join, abspath
import shutil
import re

from shell import shell

from .core import Builder, cd, convert_md_source

TBH = 'TBH'
AT = 'AT'
RE_PDF_TBH = re.compile(r'the-black-hack-([\w-]+)-v(\d+(?:\.\d+)+).pdf')
RE_PDF_AT = re.compile(r'additional-things-([\w-]+)-v(\d+(?:\.\d+)+).pdf')
Download = namedtuple(
    'Download',
    [('filetype'), 'filename', 'version', 'label', 'language']
)


def pdf_filename_parse(filename):
    """
    Parse filename and return the language and version.
    """
    matches = RE_PDF_TBH.match(filename)
    if matches:
        return (TBH,) + matches.groups()
    matches = RE_PDF_AT.match(filename)
    if matches:
        return (AT,) + matches.groups()
    return None


class PDFBuilder(Builder):
    __version__ = '0.0.1'

    def get_tbh_page(self, directory):
        meta_dir = self.meta[directory]
        for page in meta_dir['pages']:
            if 'filename' not in page \
                    or page['filename'] == 'the-black-hack.md':
                return page
        raise Exception(
            "Missing meta.yaml or not a source directory: {}".format(directory)
        )

    def get_additional_things(self, directory):
        meta_dir = self.meta[directory]
        for page in meta_dir['pages']:
            if page.get('filename', None) == 'additional-things.md':
                return page
        return None

    def write_pdf(self, curdir, source, target, label, version):
        print("Building PDF: {} - v{}".format(label, version,))
        command = 'wkhtmltopdf {} --user-style-sheet {} {}'.format(
            source,
            self.user_css_path,
            target,
        )
        with cd(curdir):
            shell(command)

    def build_dir(self, directory):
        # Building TBH PDF
        curdir = join(
            self.build_path,
            directory,
        )
        page = self.get_tbh_page(directory)
        version = page['version']
        filename = 'the-black-hack-{}-v{}.pdf'.format(directory, version)
        source = 'index.html'
        target = join(self.download_source, filename)
        self.write_pdf(
            curdir,
            source,
            target,
            self.meta[directory]['label'],
            version,
        )

        # Building optional "Additional Things"
        page = self.get_additional_things(directory)
        if page:
            version = page['version']
            filename = 'additional-things-{}-v{}.pdf'.format(
                directory, version)
            source = 'additional-things.html'
            target = join(self.download_source, filename)
            self.write_pdf(
                curdir,
                source,
                target,
                'Additional Things {}'.format(directory),
                version
            )

    def generate_body(self, file_list):
        body_md = [
            '# Downloads',
            'Here you will find auto-generated PDFs corresponding to '
            'the different source texts.',
            'These PDFs were generated using the v{} of the PDF builder'.format(self.__version__)
        ]
        for language in self.dir_list:
            language_label = self.meta[language]['label']
            body_md.append('## {}'.format(language_label))
            language_dl = filter(lambda x: x.language == language, file_list)
            language_dl = map(
                lambda x: '* [{} (v{})]({})'.format(
                    x.label,
                    x.version,
                    join('static', 'pdfs', x.filename)
                ),
                language_dl
            )
            language_dl = '\n'.join(language_dl)
            body_md.append(language_dl)

        body_md = '\n\n'.join(body_md)
        return convert_md_source(body_md)

    def write_html_page(self):
        file_list = []
        for filename in os.listdir(self.target_pdf_path):
            filetype, language, version = pdf_filename_parse(filename)
            if filetype == TBH:
                label = self.get_tbh_page(language)['label']
            else:
                label = self.get_additional_things(language)['label']
            file_list.append(
                Download(
                    filetype=filetype,
                    language=language,
                    version=version,
                    filename=filename,
                    label=label,
                )
            )
        body = self.generate_body(file_list)
        self.write_html(
            join(self.build_path, 'downloads.html'),
            body, 'Download page'
        )

    def build(self, target, sync=True):
        """
        PDF main Builder method.
        Either the target is "all" or is the name of a language to rebuild.
        """
        static_source = abspath('static')
        self.download_source = join(static_source, 'pdfs')
        self.target_pdf_path = join(self.static_path, 'pdfs')
        self.user_css_path = abspath('wkhtmltopdf.css')

        # Directories to build
        directories = self.dir_list
        if target == 'none':
            directories = []
        elif target != 'all':
            directories = filter(lambda x: x == target, directories)

        # Build meta anyway
        for directory in self.dir_list:
            self.update_meta(directory)

        for directory in directories:
            self.build_dir(directory)

        if sync:
            # Sync pdfs in the build directory
            self.mkdir(self.target_pdf_path)
            for filename in os.listdir(self.download_source):
                shutil.copy(
                    join(self.download_source, filename),
                    join(self.target_pdf_path, filename),
                )

        self.write_html_page()
