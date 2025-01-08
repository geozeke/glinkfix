![GitHub][github]
![PyPI][pypi]
![PyPI - Status][pypi-stats]
![GitHub last commit][github-commit]
![GitHub issues][github-issues]
![PyPI - Downloads][pypi-downloads]
![GitHub repo size][github-size]
![PyPI - Python Version][pypi-version]

<br>

# glinkfix

<br>

<img src="https://lh3.googleusercontent.com/d/1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc"
alt="Dinobox logo" width="120"/>

## Google Drive Link Fixer

## Notes (please read)

1. It's turning into an arms race. Google keeps changing how links are
   handled on their servers, which often breaks tools like *glinkfix*.
   Direct downloading and embedding G-Drive links is definitely an
   unsupported "off the books" feature as far as Google is concerned. As
   of Jan 2024, Google made a significant change, which definitely broke
   some links created with this tool. This update (Apr 2024) works, *for
   now*, but if Google changes again, things may break.

2. Viewing links that point to animated GIFs may just show up as static
   images.

3. In the v2 update, in addition to displaying the fixed link on the
   screen, *glinkfix* will also attempt to copy the fixed link to the
   clipboard. Copying to the clipboard only works for Desktop-based
   operating systems (not Server installs). Even without automatic
   copying, link fixing will still work and the results will be
   displayed on the screen, regardless of where you run it (Server or
   Desktop). *glinkfix* uses the [pyperclip][def9] library, and
   automatic copying to the clipboard should work seamlessly on
   Windows/Mac. If you're running Linux and links are not automatically
   copied to the clipboard, [refer to this note][def8] from the
   pyperclip developer.

## To Developers

If you're just using *glinkfix*, then carry on!

If you're a developer looking to fork this repository and modify
*glinkfix*, there are two important considerations:

1. *glinkfix* requires [uv][def11] for dependency management. It is well
   behaved and extremely fast. If you're a Python developer, you should
   check it out. Visit the [uv site][def11] and install it using
   the instructions for your operating system.

2. I've included a file called `global-gitignore.txt` which is a copy of
   the `.gitignore` I placed in my home directory and configured
   globally for all my development projects. The `global-gitignore.txt`
   file reflects my development setup (for example, using tools like
   VSCode), but yours may be different. Just cherry-pick any necessary
   elements from `global-gitignore.txt` for your own use.

   *Details on gitignore files are available on [GitHub][def2].*

## Installation

The preferred way to install *glinkfix* is with [pipx][def3]:

```shell
pipx install glinkfix
```

Alternatively, you can create a separate virtual environment and install
it the traditional way:

```shell
pip3 install glinkfix
```

If you just need a quick one-time link fix, and don't want to commit to
a full installation, use:

```shell
pipx run glinkfix -h
```

and follow the directions to run it again with the option you want.

## Purpose / Usage

When you share files with Google Drive, the sharing link you get is only
good for accessing the content through a web browser. If you want to use
a Google Drive sharing link to embed an image in a document (e.g. in a
Markdown or HTML file), or you want to directly download a file
pointed to by a Google Drive sharing link using something like `curl` or
`wget` in Linux, the link needs to be adjusted ("fixed") for these
purposes.

It's not especially hard to repackage the link, but it's a pain. You
have to copy the link to a text editor, carve it up manually, and
reassemble it. If you've got a lot of links to deal with, it starts to
get very tedious. This tool is designed to remove the tedium.

*Note: The images below are actually hosted on Google Drive, and the
"fixed" links are embedded into this README file.*

---

Start by getting a sharing link to a file on Google Drive. Make sure
it's set up for public access (*Anyone with the link*):

<img src="https://lh3.googleusercontent.com/d/1aHqCi_R6S9T9OI8kYLj-bH-Rd1eEgiWd"
alt="Getting Link" width="450"/>

---

<img src="https://lh3.googleusercontent.com/d/1DM7C91o8K32B95YkVPUv9rVga6lJdYzA"
alt="Getting Link" width="450"/>

Now run *glinkfix* and paste the link into the terminal. Copy the
"fixed" version and use it as required.

---

To display the help menu, run: `glinkfix -h`

```text
usage: glinkfix [-h] [-d]

This program takes a Google Drive sharing link for a file and repackages
it into a link that can be downloaded directly (e.g. using curl) or
embedded in a document to be viewed (e.g. an image in a Markdown
document). Note: there is a size limit of 40MB for a single file when
using Google Drive links in this manner.

optional arguments:
  -h, --help      show this help message and exit
  -d, --download  The default behavior for glinkfix is to repackage a
                  Google Drive link to make it suitable for embedding in
                  a website. Use this option if you want to repackage a
                  Google Drive link for direct downloading (e.g.
                  downloading using curl).
```

## Usage Notes

* There is a 40MB size limit for a single file when using Google Drive
  sharing links directly for viewing or downloading. Individual files
  larger than 40MB will not render/download properly. This limit is a
  function of how Google Drive works and is not related to *glinkfix*.
* When creating a download link for use with `curl`, make sure to use
  `curl`'s `-L` option to allow for redirects.
* *glinkfix* supports links that use Google's [resource key][def6]
 security feature.

### License

This project is licensed under the MIT License. See the [LICENSE][def5]
file for details.

### Acknowledgements

This project uses the [pyperclip library][def4] which is licensed under
the BSD 3 Clause License. The full license text can be found in the
[LICENSE-BSD-3-CLAUSE][def10] file.

[def2]: https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files
[def3]: https://pipx.pypa.io/stable/
[def4]: https://github.com/asweigart/pyperclip
[def5]: ./LICENSE
[def6]: https://support.google.com/a/answer/10685032
[def8]: https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error
[def9]: https://pypi.org/project/pyperclip/
[def10]: ./LICENSE-BSD-3-CLAUSE
[def11]: https://docs.astral.sh/uv/
[github]: https://img.shields.io/github/license/geozeke/glinkfix
[pypi]: https://img.shields.io/pypi/v/glinkfix
[pypi-stats]: https://img.shields.io/pypi/status/glinkfix
[github-commit]: https://img.shields.io/github/last-commit/geozeke/glinkfix
[github-issues]: https://img.shields.io/github/issues/geozeke/glinkfix
[pypi-downloads]: https://img.shields.io/pypi/dm/glinkfix
[github-size]: https://img.shields.io/github/repo-size/geozeke/glinkfix
[pypi-version]: https://img.shields.io/pypi/pyversions/glinkfix
