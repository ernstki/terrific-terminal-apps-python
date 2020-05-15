class: center, middle

.squeezed[
# Truly Terrific
## Terminal Applications
### (in Python)
]

<!--small>"User-friendly" and "command line application"<br>
aren't necessarily mutually exclusive.</small-->

<small>[bit.ly/tttapy](https://bit.ly/tttapy) &bull; [bit.ly/tttapyc](https://bit.ly/tttapyc)</small>

.footnote[
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />
Text licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
]

---
## What's about to happen

* philosophizing

--
* figure out what makes a good <abbr title="comand-line interface">CLI</abbr>

--
    * using _science!_
--
* some dos and don'ts

--
* practical demonstration
    * argparse
    * Click
    * docopt
--
* [next-level stuff](#nextlevel)

---
## All on the same page?

* "Unix"
  * Mac is a Unix (actually more so than Linux)
* "pipe"
* `$PATH`
* experience with argparse, docopt, and Click?
* ever written a command-line utility to scratch an itch?

---

## Unix philosophy

Credited [Doug McIlroy](https://en.wikipedia.org/wiki/Douglas_McIlroy) (who came up with Unix pipelines<sup>1</sup>), the Unix philsophy is summed up:

--

* Write programs that do one thing and do it well.
--

* Write programs to work together.
--

* Write programs to handle text streams
--
, because that is a universal interface.

--

Other Unix strengths:

* documentation is excellent, and has a standard format
* program options have a standard format<sup>2</sup>

.footnote[
<sup>1</sup> <https://en.wikipedia.org/wiki/Unix_philosophy>

<sup>2</sup> codified in [IEEE Std 1003](https://en.wikipedia.org/wiki/POSIX)
]

---
background-image: url(img/POSIX.jpg)
background-color: black

.footnote[
.white[
[docopt intro video](https://www.youtube.com/watch?v=pXhcPJK5cMc) by Vladimir Keleshev]
]

---
## Pipe-and-filter programming

Every Unix program has **one input stream**<sup>0</sup>
--
, **two output streams** (one for normal output<sup>1</sup>, the other for errors or "exceptional" output<sup>2</sup>)
--
, and returns an **integer status** upon termination.<sup>3</sup>

.footnote[
<sup>0</sup> filehandle 0, _a.k.a._ standard input or **stdin**

<sup>1</sup> filehandle 1, _a.k.a._ standard output or **stdout**

<sup>2</sup> filehandle 2, _a.k.a._ standard error or **stderr**

<sup>3</sup> usually referred to in the manuals as the "exit code"
]

--

Because plain text is used for inter-process communication:

--

* commands are composable

--
    * simply chain outputs to inputs w/ a pipe (`|`)
--
* possible to build pipelines in steps and examine output

---
exclude: true
## Serious strengths of the Unix toolkit (cont'd)

Manual pages<sup>[1]</sup>

* have a well-defined structure that is (or becomes) familiar
    * use a shallow hierarchy (hardly ever see sub-subsections)
    * section titles follow a familiar convention<sup>[2]</sup> `NAME`,
      `SYNOPSIS`, `DESCRIPTION`…
* they get to the point
    * `SYNOPSIS` is usually all you need to use a program you've never used
      before
* they have an _extremely_ limited set of formatting capabilities, and
  **this is a feature**

.footnote[
[1]: courtesy <https://github.com/rtomayko/ronn#background>
[2]: it's actually [a standard](https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_xcu_chap01.html#tag_23_01_05)
]

---
## Unix pipeline example

Print [Python end-of-support dates](https://www.python.org/downloads) as
a formatted table:

```
curl -sL https://www.python.org/downloads \
  | xidel - -s -e '//(span[@class="release-version"],
                      span[@class="release-end"])' \
  | paste - - \
  | grep -E '^(Python|3)' \
  | column -s $'\t' -t \
  | sed '1s/$/\n------------------------------/'
```

Result:

```
Python version  End of support
------------------------------
3.8             2024-10
3.7             2023-06-27
3.6             2021-12-23
3.5             2020-09-13
```

---
## Example of a manual page

.manpage[
```
LS(1)                   BSD General Commands Manual                      LS(1)

NAME
     ls -- list directory contents

SYNOPSIS
     ls [-ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1] [file ...]

DESCRIPTION
     For each operand that names a file of a type other than directory, ls
     displays its name as well as any requested, associated information.  For
     each operand that names a file of type directory, ls displays the names
     of files contained within that directory, as well as any requested, asso-
     ciated information.

     The following options are available:

     -@      Display extended attribute keys and sizes in long (-l) output.

     -1      (The numeric digit ``one''.)  Force output to be one entry per
             line.  This is the default when output is not to a terminal.
     ⋮
```
]

---
## Not all roses

* "one thing well" sometimes leads to specialied mini-languages you need to
  learn
--

  * _e.g._ `sed` and `awk` and regular expressions
--

* it takes time to become enculturated
  * why are the commands so short?
  * what are these funny symbols (`>/dev/null 2>&1`)?
  * what does `man(1)` mean? isn't that sexist?
--

* terseness and cleverness were assets when programming 1960s mainframes
--

    * but sometimes it borders on cryptic
--
* input assumed to come from stdin when no arguments
--

    * can lead unfamiliar users to think a program is frozen
    * _e.g._, `awk` when you forget the file argument

---
## The science of being terrific

From "Ten recommendations for creating usable bioinformatics command line software"<sup>1</sup>

.footnote[
<sup>1</sup> Torsten Seemann; <https://doi.org/10.1186/2047-217X-2-15>
]

--

* _(If possible)_ print something if no parameters are supplied

--
* Have a `-h` or `--help` switch

--
* Have a `-v` or `--version` switch

--
* Do not use stdout for messages and errors
  * stdout is for data, or other user-requested output
--

* Always raise an error if something goes wrong
  * I would add: **and return non-zero*

---
## The science of being terrific (cont'd)

* Validate your parameters
  * make sure integers are integers, input files are readable
  * and **return non-zero** exit code if not

--
* Don't hard-code any paths
  * no "magic numbers," as my boss would say
--

* Don't pollute the `$PATH`
  * don't name script same as/similar to other common utilities
  * use subcommands (like `git`) if necessary
--

* Check that your dependencies are installed
  * and **return non-zero** exit code if not
  * don't wait until your `subprocess.Popen` causes a traceback
--

* Don't distribute bare JAR (_Java ARchive_) files
  * for Python: include a `setup.py` with an [`entry_points`][ep] setting

[ep]: https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation

---
layout: true
## Being terrific

---
exclude:true
Terrific terminal applications:

* have a `-h` / `--help` option
    * limit to one screenful (~24 lines), if possible
* have other options and commands that make sense and sound like English
  * _e.g._, `-i` for input file, `-o` for output file
  * `port echo installed`, `apt-get update`
* send error messages and other "exceptional" output to standard error
<!--  * `<rant>`the output of `cmd help` is not an error!`</rant>` -->

---
Also nice to have:

* link to your issue tracker in `--help`
* include a `--help-all` or `--manual` for detailed usage
* give each subcommand has its own help (_e.g._, `git commit --help`)
* an easy installation method
  * `curl` an installation script (ehhhhhhhh…)
  * a package in PyPI, so users can `pip install`
  * `make install PREFIX=$HOME/.local/bin`
* tests
  * Expect or DejaGnu are probably good options
  * Click has support for common Python test frameworks

---
Icing on the command-line cupcake:

* programmable completion
    * Click provides facilities for this
    * or you can [write your own][manual]
    * look at [these examples][bashcompletion]
* a user config file
    * _e.g._, `mysql` command line client
* defaults configurable with environment variables
    * _e.g._, `LESS` environment variable for `less`

[manual]: https://www.gnu.org/software/bash/manual/html_node/A-Programmable-Completion-Example.html#A-Programmable-Completion-Example
[bashcompletion]: https://github.com/scop/bash-completion

---
Over-9000-Super-Saiyan stuff:

* an interactive shell
    * MacPorts `port`, `mysql`, `python`
* a front-end that communicates with a persistent daemon
    * _e.g._, `clamscan`, `spamassassin`, Heroku and AWS clients

---
layout:true

---
## Please do

* limit `--help` to a screenful (or less)
* print `--help` to standard output
    * you'll know if you're printing to standard error

<!-- * messages to stderr, yes, except in this case
    * I went _years_ before I learned `|&`
    * otherwise: `cmd help 2&gt;&1 | less` is required -->

---
## Please do (cont'd)

* act like a built-in program; not
  ```bash
  python your-big-long-script-name.py
  ```
  * use a `#!/usr/bin/env` shebang on Linux/Unix
  * or file association with `%PATHEXT%` in
    Windows<span style="color:red">\*</span>
  * short, memorable, names with personality are ideal
      * `awk`, `grep`, `jq`, `curl`, `ack`
* provide an auto-confirm option
  * `--yes`, for example, to confirm overwriting a file

.footnote[
<span style="color:red">\*</span>See this SO thread: ["Set up Python on Windows to not type “python” in cmd"](https://stackoverflow.com/questions/11472843/set-up-python-on-windows-to-not-type-python-in-cmd)
]

---
name: nextlevel
## Next-level stuff

* making installation easy
  * PyPI, `curl | bash`, or `make install`
* a manual page so that `man yourcommand` works
  * but you don't have to learn [roff][], because there's
   [ronn](https://github.com/rtomayko/ronn)
* executable packages
    ```bash
    # e.g.,
    python -m mymodule
    ```
  * just add a `__main__.py` in the package directory
  * this can alleviate `PATH` variable woes for users who don't want to mess
    with that
  * example: `python3 -m http.server` (so memorable!)

[roff]: https://linux.die.net/man/7/roff

---
name: demo
## Practical demo

[`pmfind`][pmfind]: fetch headlines of research papers from
<abbr title="National Center for Biotechnology Information">NCBI</abbr>'s
[PubMed][pm] index.

--

Yes, there is an [API][entrez].

--

However scraping the headline and URL from the web page is a one-liner in
[XPath][xpath], and I didn't want to be unwrapping mountains of JSON for
a simple example.

[pmfind]: https://github.com/ernstki/terrific-terminal-apps-python/blob/master/pmfind
[pm]: https://pubmed.ncbi.nlm.nih.gov/
[entrez]: https://www.ncbi.nlm.nih.gov/books/NBK25500/
[xpath]: https://www.w3.org/TR/xpath/all/

---
name: clipboard
## Tips for working with the clipboard

macOS has `pbcopy` and `pbpaste`.

On Linux, you can create these substitutes:

```bash
sudo your-package-manager install xclip

# add to your ~/.bashrc
alias pbcopy='xclip -i -sel clip'
alias pbpaste='xclip -o -sel clip'
```

Windows PowerShell has [`Set-Clipboard`][sc] and [`Get-Clipboard`][gc] cmdlets:

```cmd
MyProgram | Get-Clipboard
```

[sc]: https://ss64.com/ps/set-clipboard.html
[gc]: https://ss64.com/ps/get-clipboard.html

---
## Tips for working with the clipboard (cont'd)

[pyperclip][pyper] seems to be a good cross-platform library for
reading/writing the clipboard from Python programs.

…but, does your Python command-line program _need_ to do that, if there is already a facility for that built in to the OS (macOS)?

Remember, One Thing Well.

[pyper]: https://pypi.org/project/pyperclip/

---
name: powershell
## Windows: PowerShell and CMD.EXE

In spite of this having been mostly "Unixy," this is PLENTY applicable for
Windows people as well.

There's a `CLIP.EXE` that comes with Windows, so this works<span style="color:red">\*</span>

```dos
your-program | clip
```

Only in the copy-to-clipboard direction, though. If you need to send clipboard text _to_ your program, do this instead<span style="color:red">\*\*</span>

```dos
powershell -command get-clipboard | your-program-that-reads-stdin
```

.footnote[
<span style="color:red">\*</span> Is that too much typing for you? Create a [DOSKEY macro](https://superuser.com/a/1134468/73744)!

<span style="color:red">\*\*</span>I _think_ this works in the copy-to-clipboard, too?
]

<!--
```dos
doskey pastelong=powershell^ -command get-clipboard^ ^|^ howlong
```

in a file called something like `macros.doskey` and load that up every time you
run a new Command Prompt with an "AutoRun" registry key as detailed
-->

---
## Using Windows' PowerShell

PowerShell plays just fine with Unix-style programs that read text streams as
input and yield text streams as output.

```powershell
get-clipboard | your-program-that-reads-stdin
```

If you want a shortcut for that, you can create a
[PowerShell function](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions)<span style="color:red">\*</span>

```powershell
function pastelong { get-clipboard | your-program }
```

PowerShell functions behave about the same as Unix shell functions in that you
can pipe data into them.

.footnote[
<span style="color:red">\*</span> and add that to a
[PowerShell profile](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles),
which will load up every time you run PowerShell.
]

---
# See also

* [UNIX: Making Computers Easier To Use](https://www.youtube.com/watch?v=XvDZLjaCJuw) — AT&T Archives film from 1982, Bell Laboratories
    * see [this gist](https://gist.github.com/ernstki/1432b3ea843410a4826ce9cb1584d7b5) for a step-by-step recreation of the spellchecker and talking calculator in Bash and Python
* [The Unix Chainsaw][3] by Gary Bernhardt
* PyCon UK 2012: [Create *beautiful* command-line interfaces with Python][1] (by the author of [docopt][2])
* [jlevy/the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line)
* Internet your pipes and pipe the Internet with [`curl`](https://curl.haxx.se)
    * just look at the protocol support!

[1]: https://www.youtube.com/watch?v=pXhcPJK5cMc
[2]: https://github.com/docopt/docopt
[3]: https://www.youtube.com/watch?v=sCZJblyT_XM

---
# .rainbow[BONUS ROUND!]

Tools for working with Internet data sources:

* [`xmlstarlet`](http://xmlstar.sourceforge.net)
    ```bash
    alias xml='xmlstarlet'  # much more convenient
    ```
* [`xidel`](http://www.videlibri.de/xidel.html)<span style="color:red">\*</span>
    ```bash
    curl -s "$URL" | xidel - -e '//p[contains(.,"MD5")]'
    ```
* [`pup`](https://github.com/ericchiang/pup)
    * see [issue #123](https://github.com/ericchiang/pup/issues/123) if it crashes on startup

.footnote[
<span style="color:red">\*</span> my personal favorite, does what it says on the tin, no fuss
]

---
# .rainbow[BONUS ROUND, PART DEUX!]

* [`hxselect`](https://www.w3.org/Tools/HTML-XML-utils/) - "HTML and XML select"
* [`jq`](https://stedolan.github.io/jq/) - a command-line JSON processor
  * [helpful cheatsheet](https://gist.github.com/olih/f7437fb6962fb3ee9fe95bda8d2c8fa4)

The URL _is_ the interface:
* <http://cheat.sh>
  ```bash
  curl -s cheat.sh/python/loops | less -R
  ```
* <http://wttr.in>
  ```bash
  curl -s wttr.in/honolulu | less -R
  ```

---
# References

1. ["Ten recommendations for creating usable bioinformatics command line software"][1] by Torsten Seemann
2. ["Ten Essential Development Practices"][2] by Damian Conway
3. [argparse][3] - from the Python standard library
  * [official tutorial][4]
4. [Click][5] - by [Armin Ronacher](https://github.com/mitsuhiko), and others
  * [API documentation][6]
5. [docopt][6] - by [Vladimir Keleshev](https://github.com/keleshev), and others
  * [try it in a browser][7]

[1]: https://www.perl.com/pub/2005/07/14/bestpractices.html/
[2]: https://doi.org/10.1186/2047-217X-2-15
[3]: https://docs.python.org/3/library/argparse.html
[4]: https://docs.python.org/3/howto/argparse.html
[5]: https://palletsprojects.com/p/click/
[6]: http://docopt.org/
[7]: http://try.docopt.org/

---
class: center, middle

# THANKS

for your kind attention!

.footnote[
these slides are available at<br><https://bit.ly/tttapy>
]

---
class: center, middle

<small>here's a cute kitten</small>

![a cute kitten](img/kitten.jpg)

