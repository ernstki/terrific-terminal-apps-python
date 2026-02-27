How to install man pages with setuptools
========================================

Make sure you have some recent (≥3.8) version of Python installed, and pip. On
Debian/Ubuntu systems, this is accomplished with:

    sudo apt install python3 python3-pip

Then:

    make viewman

You can see the raw source of the generated man page [here](man/pmfind.1). The
typesettings language used here is [roff][]. If you've used LaTex, Markdown,
reStructuredText, or anything in that vein, you already get the concept.

While not impossible to learn the basics in an afternoon, I suspect that few
people write roff by hand anymore. _See below._


Implementation notes
--------------------

As mentioned [here][stman] in the setuptools documentation

> It is common for developers to attempt using `data_files` for manpages.
> Please note however that depending on the installation directory, this will
> not work out of the box - often the final user is required to change the
> [`MANPATH` environment variable][manpath].

Thus, the Python Packaging Authority "[DISCOURAGES][data_files]" the use of
this keyword because it's an "advanced feature."

However, if you use pip, [pipx][], or newer tools like `uv` on a
reasonably-equipped, modern Linux system, you **don't have to worry about any
of this**. Everything Just Works™, since:

* `~/.local/bin` is in the default user search path for most modern Linuxes
    * (and this is where `pip install --user` installs to)
* and man-db is configured to add a `MANPATH` entry for each `PATH` entry by
  default
    * (as long as your `MANPATH` variable either starts or ends with a colon,
      or has `::` somewhere in the middle)

…thus `~/.local/man` and `~/.local/share/man` are added to `MANPATH`
automatically.

On other platforms, it's not too hard to update `MANPATH` in your login
scripts:

    # in your ~/.profile, if you have one, or ~/.bash_profile for Bash
    export MANPATH=$MANPATH:$HOME/.local/man:$HOME/.local/share/man

Read [man(1)][man1] and [manpath(5)][manpath5] (if it exists on your
platform) for more details.


See also
--------

* [ronn][] written in Ruby

* Perls' [pod2man][] utility, which is probably the most mature solution out
  there, and you probably already have it on your computer anyway
  ([for now][], Mac users)

The Ranger project, while written in Python, writes [its man pages][] with
[POD][] and then [converts them][] using `pod2man` as a packaging step.


References
----------

* https://github.com/pypa/pipx/pull/1047, which implemented support for man pages in [`pipx`][]
    * [ranger's `setup.py`][rangersetup]
    * [visidata's `setup.py`][vdsetup]
* setuptools [`data_files` keyword][data_files]
* "[Should there be a new standard for installing arbitrary data
  files?][discourse]" - _discuss.python.org_
    * specifically [post #63][63]

[roff]: https://en.wikipedia.org/wiki/Roff_(software)
[stman]: https://setuptools.pypa.io/en/latest/references/keywords.html#manpages
[manpath]: https://man7.org/linux/man-pages/man5/manpath.5.html
[man1]: https://www.man7.org/linux/man-pages/man1/man.1.html
[manpath5]: https://man7.org/linux/man-pages/man5/manpath.5.html
[ronn]: https://github.com/rtomayko/ronn
[pod2man]: https://perldoc.perl.org/pod2man
[its man pages]: https://github.com/ranger/ranger/tree/master/doc
[pod]: https://perldoc.perl.org/perlpod
[converts them]: https://github.com/ranger/ranger/blob/126d3ee487b5c291c49d5ef25176fbe8207d71e3/Makefile#L138
[for now]: https://www.macobserver.com/columns-opinions/macos-catalina-deprecates-unix-scripting-languages/
[pipx]: https://pipx.pypa.io
[rangersetup]: https://github.com/ranger/ranger/blob/126d3ee487b5c291c49d5ef25176fbe8207d71e3/setup.py#L101
[vdsetup]: https://github.com/saulpw/visidata/blob/55c00790d1eaefbf8a81cc0f19db173180c8426c/setup.py#L73
[data_files]: https://setuptools.pypa.io/en/latest/references/keywords.html#keyword-data-files
[discourse]: https://discuss.python.org/t/should-there-be-a-new-standard-for-installing-arbitrary-data-files/7853
[63]: https://discuss.python.org/t/should-there-be-a-new-standard-for-installing-arbitrary-data-files/7853/63
