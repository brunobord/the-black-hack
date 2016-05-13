# Changelog

## master (unreleased)

* French translation of The Black Hack (#10).
* Spanish translation of The Black Hack (#18).
* More mobile-friendly layout / font size handling (#19).
* Added a `make clean` target to clean the `build/` directory (#22).
* Added a `.htaccess` file to serve `.md` files with the utf-8 encoding (#23).
* Indicate the translation version if mentioned in the `meta.yaml` file (#20).

## 1.0.1 (2016-05-03)

* added the automatic version number on the built HTML page footer (#9).
* small typo fixes in english text.
* Builder refactor (#13).
* Moved link to OGL text out of the "raw" text (#14).
* Page title extracted from the ``meta.yaml`` file (#15).
* Added link to source for the SRD pages and on the homepage (#11).
* Fix display bug with table headers that contain numbers (#16).

## 1.0.0 (2016-04-22)

This is the first version of the *open gaming content* "SRD" of "The Black Hack" roleplaying game. Please refer to the [README](README.md) for more information.

### Main features

* Complete text & tables extracted from "The Black Hack" PDF v1.2 (2016-04-03),
* Included OGL License, accordingly linked from the homepage.
* Python script to build the full website:
  * automatic homepage based on available directories and meta files,
  * HTML pages are styled to (roughly) fit the PDF style,
* Documentation to help eventual contributors.
* Travis builds (for master & pull-requests) ; build badges on the README.

This project website is browsable at [the-black-hack.jehaisleprintemps.net](http://the-black-hack.jehaisleprintemps.net/).

*The name "The Black Hack" is used with kind permission of the author.*
