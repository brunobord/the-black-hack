from toolbox.pdf import pdf_filename_parse as parse
from toolbox.pdf import TBH, AT


def test_parser():
    assert parse('meuh') is None
    assert parse('the-black-hack-english-v1.2.pdf') == (TBH, 'english', '1.2')
    assert parse('the-black-hack-brazilian-portuguese-v1.1.pdf') \
        == (TBH, 'brazilian-portuguese', '1.1')

    assert parse('additional-things-english-v1.2.pdf') \
        == (AT, 'english', '1.2')
    assert parse('additional-things-brazilian-portuguese-v1.1.pdf') \
        == (AT, 'brazilian-portuguese', '1.1')
