from ..core import slugify


def test_slugify_english():
    assert slugify('hello', '-') == 'hello'
    assert slugify('hello world', '-') == 'hello-world'


def test_slugify_french():
    assert slugify("De quoi s'agit-il ?", '-') == 'de-quoi-s-agit-il'


def test_slugify_castellano():
    assert slugify("¿Qué es esto?", '-') == 'que-es-esto'


def test_slugify_japanese():
    assert slugify("これは何？", '-') == 'korehahe'


def test_slugify_portuguese():
    assert slugify("O que é isso?", '-') == 'o-que-e-isso'


def test_slugify_converting_saves():
    assert slugify('Converting Saves', '-') == 'converting-saves'
    assert slugify('Conversion des jets de sauvegarde', '-') == 'conversion-des-jets-de-sauvegarde'  # noqa
    assert slugify('Convirtiendo tiradas de salvación', '-') == 'convirtiendo-tiradas-de-salvacion'  # noqa
    assert slugify('セーブの変換', '-') == 'sebunobian-huan'
    assert slugify('Convertendo jogadas de proteção', '-') == 'convertendo-jogadas-de-protecao'  # noqa
