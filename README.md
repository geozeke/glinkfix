![GitHub](https://img.shields.io/github/license/geozeke/glinkfix)
![PyPI](https://img.shields.io/pypi/v/glinkfix)
![PyPI - Status](https://img.shields.io/pypi/status/glinkfix)
![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/glinkfix)
![GitHub issues](https://img.shields.io/github/issues/geozeke/glinkfix)
![PyPI - Downloads](https://img.shields.io/pypi/dm/glinkfix)
![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/glinkfix)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/glinkfix)

<br>

<img src="https://lh3.googleusercontent.com/d/1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc"
alt="Dinobox logo" width="120"/>

# Google Drive Link Fixer

## A note to developers

If you're just using glinkfix, then carry on!

If you're a developer looking to fork this repository and modify glinkfix,
there are two important considerations:

1. glinkfix requires [poetry](https://python-poetry.org/) for dependency
   management. Poetry is well behaved and if you're a Python developer you
   should check it out. It installs itself in a virtual environment, uninstalls
   cleanly and easily, and doesn't require `sudo` for installation. Visit the
   [poetry site](https://python-poetry.org/) and install it using the
   instructions for your operating system.

   *Note: When you install poetry, pay careful attention to the message printed
   by the poetry installer. It provides details on how to modify `$PATH` to
   access the poetry runtime.*

2. I've included a file called `global-gitignore.txt` which is a copy of the
   `.gitignore` I placed in my home directory and configured globally for all
   my development projects. The `global-gitignore.txt` file reflects my
   development setup (for example using tools like vscode), but yours may be
   different. Just cherry-pick any necessary elements from
   `global-gitignore.txt` for your own use.

   *Details on gitignore files are available on
   [GitHub](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files).*

## Installation

The Google Drive Link Fixer is lightweight, pure Python, with no third-party
dependencies. You could install it within a virtual environment using pip3:

```text
pip3 install glinkfix  
```

or

You could install it using [pipx](https://pipx.pypa.io/stable/):

```text
pipx install glinkfix
```

If you just need a quick one-time link fix, and don't want to commit to
a full installation, use:

```text
pipx run glinkfix -h
```

and follow the directions to run it again with the option you want.

## Purpose / Usage

When you share files with Google Drive, the sharing link you get is only good
for accessing the content through a web browser. If you want to use a Google
Drive sharing link to embed an image in a document (e.g. in a markdown or html
file), or you want to directly download a file pointed-to by a Google Drive
sharing link using something like `curl` or `wget` in linux, the link needs to
be adjusted ("fixed") for these purposes.

It's not especially hard to repackage the link, but it's a pain. You have to
copy the link to a text editor, carve it up manually, and reassemble it. If
you've got a lot of links to deal with it starts to get very tedious. This tool
is designed to remove the tedium.

*Note: The animated gifs below are actually hosted on Google Drive and the
"fixed" links are embedded into this README file.*

---

Start by getting a sharing link to a file on Google Drive. Make sure it's set
up for public access (*Anyone with the link*):

![Retrieving Google Link](https://drive.google.com/uc?export=view&id=1BJ5cR04cSzHa4xMIPApjLXv0IHPDu9U2)

---

Now run `glinkfix` and paste the link into the terminal. Copy the "fixed"
version and use is as required.

![Using Google Link](https://drive.google.com/uc?export=view&id=1wrrGh-cm_Hf7hH5WN_aCO-wwxIsrk6j5)

---

To display the help menu, run: `glinkfix -h`

```text
usage: glinkfix [-h] (-v | -d)

This program takes a Google Drive sharing link for a file and repackages it into a link
that can be downloaded directly (e.g. using curl) or embedded in a document to be viewed
(e.g. an image in a markdown document). Note: there is a size limit of 40MB for a single
file when using Google Drive links in this manner.

optional arguments:
  -h, --help      show this help message and exit
  -v, --view      repackage the link for viewing (e.g. as an embedded link in a markdown
                  document).
  -d, --download  repackage the link for downloading (e.g. downloading using curl).
```

## Usage Notes

* There is a 40MB size limit for a single file when using Google Drive sharing
  links directly for viewing or downloading. Individual files larger than 40MB
  will not render/download properly. This limit is a function of how Google
  Drive works and is not related to `glinkfix`.
* When creating a download link for use with `curl` make sure to use `curl`'s
  `-L` option to allow for redirects.
* `glinkfix` supports links that use Google's [resource
  key](https://support.google.com/a/answer/10685032) security feature.

## Version History

* 1.2.1 (2024-01-24)
  * Version re-baseline and documentation corrections. No functional
    changes in the 1.2.x release cycle.
    <br><br>
* 1.2.0 (2024-01-23)
  * Updated installation options to include [pipx](https://pipx.pypa.io/stable/).
  <br><br>
* 1.0.16 (2023-12-31)
  * Cleaned up packaging for better [PEP
  561](https://peps.python.org/pep-0561/) compliance.
  * Dropped support for Python <=3.7
  <br><br>
* 1.0.15 (2023-06-23)
  * Migrated code formatter to *black*.
  <br><br>
* 1.0.14 (2023-04-19)
  * Documentation cleanup.
  <br><br>
* 1.0.13 (2022-11-03)
  * Google made a breaking change to the format for sharing links (not that
    they checked with me first 😊). This patch updates glinkfix to support the
    change.
  <br><br>
* 1.0.12 (2022-10-22)
  * Regression bug fixes.
  <br><br>
* 1.0.11 (2022-10-21)
  * Migrated dependency/build management to [poetry](https://python-poetry.org/).
  <br><br>
* 1.0.9 (2022-10-13)
  * Fixed a bug when IDs or resource keys contain underscore characters (`_`)
  * Additional test case for bug fix.
  * Moved task runner to make.
  * Build local virtual environment for development.
  * Code refactoring and linting.
  <br><br>
* 1.0.8 (2022-07-23)
  * Implemented code coverage for testing infrastructure.
  * Code refactoring and linting.
  <br><br>
* 1.0.7 (2022-07-15)
  * Fixed handling of URLs with resource keys.
  * Code cleanup and refactoring.
  * Implemented custom exception handling.
  * Implemented testing infrastructure.<br><br>
* 1.0.6 (2022-01-17)
  * Code cleanup.<br><br>
* 1.0.5 (2021-12-23)
  * Code linting.
  * Documentation cleanup.<br><br>
* 1.0.4 (2021-12-19)
  * Initial release<br>
