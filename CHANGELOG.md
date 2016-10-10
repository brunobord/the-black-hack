# Changelog

## 2.3.1 (2016-10-10)

* Added a "language count" on the homepage (#43).
* Build a raw, but readable PDF for every language (#21, #46).
* Contributing docs rewritten and enhanced, added a PR template (#47).
* Small changes to the Portuguese (Brazilian) version, upgraded to v1.1 (#48).

## 2.3.0 (2016-09-16)

* Fix the Italian "Cockatrice" translation (#40).
* Portuguese (Brazilian) translation of *The Black Hack* and *Additional Things* by Fernando Guedes (#41).
* Making sure that "English" will always be at the first place in the list (#42).

## 2.2.0 (2016-09-02)

* Italian translation of *The Black Hack* and *Additional Things* by Fabio Gemesio (#35).
* Updated Japanese translation, fixing typos and errors (#36).
* Little cleanup in `meta.yml` - french and italian (#38).
* Started a small checklist on how to contribute (#37).
* Fixed word-wrap issue with Japanese bestiary table (#39).

## 2.1.0 (2016-08-13)

* tiny typo fix in english "additional things".
* Japanese translation of The Black Hack added - thanks to Toshiya Nakamura (#29).
* New slugification library to handle Japanese - or other non-latin-based languages - (#31).

## 2.0.0 (2016-07-23)

* typo fix in the french text ("exemple" instead of "example").
* Allow to build extra pages ; the `meta.yaml` file must now provide a list of pages to be built (#27 ; was a requirement for #24).
* Additional Things (english) added (#24).
* Additional Things (french) added (#25).

## 1.1.0 (2016-05-14)

* French translation of The Black Hack (#10).
* Spanish translation of The Black Hack (#18).
* More mobile-friendly layout / font size handling (#19).
* Added a `make clean` target to clean the `build/` directory (#22).
* Added a `.htaccess` file to serve `.md` files with the utf-8 encoding (#23).
* Indicate the translation version if mentioned in the `meta.yaml` file (#20).
* Added an anchor in the headers from h1 to h6 (#26).
* Aligned the "converting save" tables to make them prettier (#17).

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
