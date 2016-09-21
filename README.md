# The Black Hack

This project publishes the "raw text" of the Roleplaying game "The Black Hack", by David Black. As specified in the [License](LICENSE) document, the text and tables are *open game content*.

It means that anyone can use this *open game content* and make derivative works without asking for permission, as long as this derivative fits the [Open Gaming License terms](http://www.opengamingfoundation.org/ogl.html).

[![GitHub tag](https://img.shields.io/github/tag/brunobord/the-black-hack.svg?maxAge=2592000)]() [![Travis](https://img.shields.io/travis/brunobord/the-black-hack.svg?maxAge=2592000)]()

The name "The Black Hack" is used here with kind permission of the author.

See the [License](LICENSE) for more details.


## Contribute

The main document describing the [guidelines on how to contribute is readable here](.github/CONTRIBUTING.md). Please read it carefully in order to make sure your contribution will be easily reviewed and accepted.

### Requirements

You must have [Python language](https://www.python.org/) available on your system, and either a way to create a virtualenv with a recent version of [tox](http://tox.readthedocs.io/en/latest/) or a recent version of tox available system-wide.

To build the HTML pages, you can run on of the following commands:

```
make html
tox -e html
```

The build pages are in the ``build/`` directory. This may help you if you try to fix or translate into a new language.

You'll probably won't have to, but if you want to build PDF files, you'll need to install [wkhtmltopdf](http://wkhtmltopdf.org/) on your system. And you may run ``tox -e pdf`` to build PDF files.

If you want to target a specific language, you can run:

```
tox -e pdf -- french
```

----

## References

* [David Black G+ Profile](https://plus.google.com/112905476698977529502),
* [David Black blog](http://dngnsndrgns.blogspot.fr/),
* [Square Hex](http://squarehex.myshopify.com/),
* The (very successful) [Kickstarter campaign](https://www.kickstarter.com/projects/1730454032/the-black-hack),
* [The Black Hack G+ Community](https://plus.google.com/communities/107832933727516137622),
* [The Open Gaming License](http://www.opengamingfoundation.org/ogl.html).
