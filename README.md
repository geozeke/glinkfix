![GitHub](https://img.shields.io/github/license/geozeke/glinkfix)
![PyPI](https://img.shields.io/pypi/v/glinkfix)
![PyPI - Status](https://img.shields.io/pypi/status/glinkfix)
![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/glinkfix)
![GitHub issues](https://img.shields.io/github/issues/geozeke/glinkfix)
![PyPI - Downloads](https://img.shields.io/pypi/dm/glinkfix)
![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/glinkfix)
![Lines of code](https://img.shields.io/tokei/lines/github/geozeke/glinkfix)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/glinkfix)

<br>

<img src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc" width="120"/>

# Google Drive Link Fixer

## Installation

The Google Drive Link Fixer is lightweight, pure Python, with no third-party dependencies.

```
pip3 install glinkfix  
```

## Purpose / Usage

When you share files with Google Drive, the sharing link you get is only good for accessing the content through a web browser. If you want to use a Google Drive sharing link to embed an image in a document (e.g. in a markdown or html file), or you want to directly download a file pointed-to by a Google Drive sharing link using something like `curl` or `wget` in linux, the link needs to be adjusted ("fixed") for these purposes.

It's not especially hard to repackage the link, but it's a pain. You have to copy the link to a text editor, carve it up manually, and reassemble it. If you've got a lot of links to deal with, it starts to get very tedious. This tool is designed to remove the tedium.

*Note: The animated gifs below are actually hosted on Google Drive, and the corrected links are embedded into this README file.*

<hr>

Start by getting a link to a file on Google Drive. Make sure it's set up for public access (*Anyone with the link*):

![](https://drive.google.com/uc?export=view&id=1BJ5cR04cSzHa4xMIPApjLXv0IHPDu9U2)

<hr>

Now run `glinkfix` and paste the link into the terminal. Copy the "fixed" version and use is as required.

![](https://drive.google.com/uc?export=view&id=1wrrGh-cm_Hf7hH5WN_aCO-wwxIsrk6j5)

<hr>

To display the help menu, run: `glinkfix -h`

```
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

* There is a 40MB size limit for a single file when using Google Drive sharing links directly for viewing or downloading. Individual files larger than 40MB will not render/download properly. This limit is a function of how Google Drive works and is not related to `glinkfix`.
* When creating a download link for use with `curl`, make sure to use `curl`'s `-L` option to allow for redirects.
* `glinkfix` supports links that use Google's [resource key](https://support.google.com/a/answer/10685032) security feature.


## Version History

* 1.0.6 (2022-01-17)
	* Code cleanup.<br><br>
* 1.0.5 (2021-12-23)
	* Code linting.
	* Documentation cleaup.<br><br>
* 1.0.4 (2021-12-19)
	* Initial release<br>
