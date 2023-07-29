INPUT_FORMATS = {
    "bib": "bibtex",
    "md": "markdown",
    "creole": "creole",
    "csljson": "csljson",
    "csv": "csv",
    "xml": "docbook",
    "docx": "docx",
    "dokuwiki": "dokuwiki",
    "epub": "epub",
    "fb2": "fb2",
    "haddock": "haddock",
    "html": "html",
    "ipynb": "ipynb",
    "jats": "jats",
    "jira": "jira",
    "json": "json",
    "tex": "latex",
    "man": "man",
    "mediawiki": "mediawiki",
    "muse": "muse",
    "native": "native",
    "odt": "odt",
    "opml": "opml",
    "org": "org",
    "rst": "rst",
    "rtf": "rtf",
    "t2t": "t2t",
    "textile": "textile",
    "tikiwiki": "tikiwiki",
    "twiki": "twiki",
    "vimwiki": "vimwiki"
}
INPUT_FORMATS_CHOICES = [(key, value) for key, value in INPUT_FORMATS.items()]

OUTPUT_FORMATS = {
    "bib": "bibtex",
    "md": "markdown_strict",
    "creole": "creole",
    "csljson": "csljson",
    "csv": "csv",
    "xml": "docbook",
    "docx": "docx",
    "dokuwiki": "dokuwiki",
    "epub": "epub",
    "fb2": "fb2",
    "haddock": "haddock",
    "html": "html",
    "ipynb": "ipynb",
    "jats": "jats",
    "jira": "jira",
    "json": "json",
    "tex": "latex",
    "man": "man",
    "mediawiki": "mediawiki",
    "muse": "muse",
    "native": "native",
    "odt": "odt",
    "opml": "opml",
    "org": "org",
    "rst": "rst",
    "rtf": "rtf",
    "t2t": "t2t",
    "textile": "textile",
    "tikiwiki": "tikiwiki",
    "twiki": "twiki",
    "vimwiki": "vimwiki",
    "asciidoc": "asciidoc",
    "asciidoctor": "asciidoctor",
    "beamer": "beamer",
    "context": "context",
    "docbook": "docbook",
    "docbook4": "docbook4",
    "docbook5": "docbook5",
    "dzslides": "dzslides",
    "epub2": "epub2",
    "epub3": "epub3",
    "icml": "icml",
    "jats_archiving": "jats_archiving",
    "jats_articleauthoring": "jats_articleauthoring",
    "jats_publishing": "jats_publishing",
    "markua": "markua",
    "ms": "ms",
    "odt": "opendocument",
    "pdf": "pdf",
    "txt": "plain",
    "pptx": "pptx",
    "revealjs": "revealjs",
    "s5": "s5",
    "slideous": "slideous",
    "slidy": "slidy",
    "tei": "tei",
    "texinfo": "texinfo",
    "xwiki": "xwiki",
    "zimwiki": "zimwiki"
}
OUTPUT_FORMATS_CHOICES = [(key, value) for key, value in OUTPUT_FORMATS.items()]