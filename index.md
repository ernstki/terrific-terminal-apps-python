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
class: center

.white[
## ALSO KNOWN AS
]

.footnote[
.white[[docopt intro video](https://www.youtube.com/watch?v=pXhcPJK5cMc) by Vladimir Keleshev]
]

---
## Pipe-and-filter programming

Every Unix program:

* has **one input stream**<sup>0</sup>
--

  * **default source is user's keyboard**
--

  * could also be a file (via direction operator: `< filename`)
--

  * or the output of another program (via a pipe: `prog1 | prog2`)
--

* has **two output streams**
--

  * one for "normal," expected output<sup>1</sup> <!-- this is possibly transformed intput data, hence the "filter" in "pipe-and-filte -->
--

  * the other for errors or "exceptional" output<sup>2</sup>
--

  * **default destination is user's screen** (for both)
--

      * but can be redirected _independently_ with `> filename` or `| otherprogram`


.footnote[
<sup>0</sup> file descriptor 0, _a.k.a._ standard input or **stdin**

<sup>1</sup> file descriptor 1, _a.k.a._ standard output or **stdout**

<sup>2</sup> file descriptor 2, _a.k.a._ standard error or **stderr**
]

---
## Pipe-and-filter programming (cont'd)


Every Unix program also returns an **integer status** upon
termination.<sup>1</sup>


```bash
# short circuit" Boolean operators
do-this || handle-failure

# and the value of $? can be used for error handling
if [ $? -eq 128 ]; then echo "Communications failure" >&2; fi
```

.footnote[
<sup>1</sup> usually referred to in the manuals as the "exit code"
]

--

Because plain text is used for inter-process communication:

--

* commands are composable (with redirections &amp; pipes)

--
* …and it's possible to build and inspect pipelines step-wise

---
exclude: true
## Serious strengths of the Unix toolkit (cont'd)

Manual pages<sup>1</sup>

* have a well-defined structure that is (or becomes) familiar
    * use a shallow hierarchy (hardly ever see sub-subsections)
    * section titles follow a familiar convention<sup>2</sup> `NAME`,
      `SYNOPSIS`, `DESCRIPTION`…
* they get to the point
    * `SYNOPSIS` is usually all you need to use a program you've never used
      before
* they have an _extremely_ limited set of formatting capabilities, and
  **this is a feature**

.footnote[
<sup>1</sup> courtesy <https://github.com/rtomayko/ronn#background>
<sup>2</sup> it's actually [a standard](https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_xcu_chap01.html#tag_23_01_05)
]

---
## Unix pipeline example

Print [Python end-of-support dates](https://www.python.org/downloads) as
a formatted table:

```bash
curl -sL https://www.python.org/downloads \
  | xidel - -s -e '//(span[@class="release-version"],
                      span[@class="release-end"])' \
  | paste - - \
  | grep -E '^(Python|3)' \
  | column -s $'\t' -t \
  | sed '1s/$/\n------------------------------/'  # GNU sed only*

# result:
# 
# Python version  End of support
# ------------------------------
# 3.8             2024-10
# 3.7             2023-06-27
# 3.6             2021-12-23
# 3.5             2020-09-13
```

.footnote[
<span style="color:red">\*</span> On Mac, `sudo port install gsed` or use [Homebrew](https://brew.sh) to get GNU sed
]

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

--
  * screw this up and users end up with data + errors intermingled
  * **standard out is for data**, or other user-requested output
--

  * **standard error is for errors** and other "exceptional" messages
---
## The science of being terrific (cont'd)

* Always raise an error if something goes wrong
  * I would add, critically: **and return a non-zero exit code**
--

* Validate your parameters
  * make sure integers are integers, input files are readable
  * and **return non-zero** exit code if not

--
* Don't hard-code any paths
  * no "magic numbers," as my boss would say
--

* Don't pollute the `$PATH`
  * don't name your script same as/similar to other common utilities
  * use subcommands (like `git`) if necessary

---
## The science of being terrific (cont'd)

* Check that your dependencies are installed
  * and **return non-zero** exit code if not
  * don't wait until your `subprocess.Popen` causes a traceback
--

* Don't distribute bare JAR (_Java ARchive_) files
  * _i.e._, give users _something they can run_

--

<small>Some well-known bioinformatics software is distributed as <tt>.jar</tt>
files, and they expect their users (who probably _aren't_ Java people) to:

```bash
java -weirdJVMoptionsxX500 -c /path/to/classes -jar jarfile.jar
```

--

<small>Please, think of the users. Just write a wrapper script to do that for
them.</small>

---
## Being terrific: act like a built-in

There is no reason to make users do this (even on Windows)

```bash
python your-big-long-script-name.py
```

--

On macOS, Linux, and other Unices:

* add a [shebang][] line like `#!/usr/bin/env python3`
--

* mark the script executable with `chmod a+x scriptname`
--

* put the script somewhere in your `$PATH` (_e.g._, `~/bin`)

--

<small>You could go even farther and **leave off the .py** — no one needs to
know or care that your program is written in Python, because it will be
literally indistinguable from any other installed programs at this
point.</small>

[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)

---
name: windows-install
## Act like a built-in (Windows edition)

For Windows users, include pointers in your README for

--
* modifying their `PATH` variable

--
* setting up file assocations or `%PATHEXT%`<sup>1</sup> so they can run your Python script as a program, even without the `.py`

--

Rumor has it, these days even Windows supports Unix's `#!/path/to/interpreter`
"shebangs" to some extent, which seems weird<sup>2</sup> but could be good for your users.

--

<small>Python's setuptools can actually help automate all this; see
[this slide](#easy-to-install).</small>

.footnote[
<sup>1</sup> see this SO thread: ["Set up Python on Windows to not type “python” in cmd"](https://stackoverflow.com/questions/11472843/set-up-python-on-windows-to-not-type-python-in-cmd)

<sup>2</sup> not all that weird, given their 1990s motto of ["embrace, extend, and extinguish"](https://en.wikipedia.org/wiki/Microsoft_POSIX_subsystem)
]

---
## Being terrific: act like a built-in (cont'd)

Take a page out of Unix's book:

--
* use short but memorable, names, with _personality_
  * _e.g._, `awk`, `grep`, `jq`, `curl`, `ack`
--

* avoid mixed case names

--

<small>You may have a really clever acronym for your project that you're proud
of, but your users will appreciate it if your actual program name is **short,
sweet, and easy to type.**</small>

--

<small> Don't make them try to remember if it's `MEGAtool`, `MegaTool`, or `megaTOOL`. Just `megatool` is fine.<span style="color:red">\*</span></small> 

.footnote[
<span style="color:red">\*</span>Someone will inevitably change their mind about the capitalization anyway; see: [bedtools][].
]

[bedtools]: https://bedtools.readthedocs.io/en/latest/

---
name: easy-to-install
## Being terrific: make it easy to install

Publish to PyPI, so users can just `pip install megatool`

--

* (another reason to stick with lower-case)
--

* use setuptools' [`entry_points`][ep] to install your script as an executable in the users' `PATH`
--

* this patches over many of the rough spots [on Windows](#windows-install)

--

If you're not thrilled by learning [all the setuptools/PyPI stuff][pypitut]:

--

* `curl $INSTALLSCRIPT | bash`
--

  * not everyone's thrilled by _this_ either
--

* include a good old-fashioned Makefile
  * with a `make install` recipe that allows a user-defined `PREFIX`

[ep]: https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
[pypitut]: https://pythonhosted.org/an_example_pypi_project/setuptools.html

---
## Being terrific: be kind to your user<span style="color:red">\*</span>

.footnote[
<span style="color:red">\*</span> (even if your user is yourself)

<span style="color:red">\*\*</span> you would have to _try_ to do this wrong with Python; default for `print()` is stdout
]

* print `--help` to **standard out**, not standard error<span style="color:red">\*\*</span>

--
  * .rant[wanting to see the help is not an error!]
--

  * link to your issue tracker in `--help`
--

  * limit `--help` output to about a screenful, so `| less` isn't needed
--

* send error messages and other "exceptional" output to standard error
  * _e.g._, `print("OH NOES! It broked.", file=sys.stderr)`

--
* try to make your options and operations read like English
  * _e.g._, `-i` for input file, `-o` for output file

--
  * good examples: `port echo installed`, `apt-get update`


---
## Being terrific: also nice to have

* include a `--help-all` for detailed usage
  * whatever doesn't fit on one screen in `--help`
--

  * …but is still useful enough the user shouldn't have to go to the full
    documentation on the project web site or whatever
--
* consider baking _all_ of your documentation into the tool itself
--

  * `go` does this, _e.g._, `go help get`
--

  * some tools have a `--manual` option (_e.g._, Perl tools using [Pod::Usage][pu])
--

* give each subcommand its own help
  * how Git does it: `git subcommand --help` opens `man git-subcommand`

---
## Being terrific: also nice to have (cont'd)

* tests (so you can tell if contributors break your code)
  * Click has [built-in support][clicktest] for automated tests
  * [Expect][] or [DejaGnu][] are interesting (if old-school) options

[pu]: https://perldoc.perl.org/Pod/Usage.html
[clicktest]: https://click.palletsprojects.com/en/7.x/testing/
[expect]: https://blog.robertelder.org/don-libes-expect-unix-automation-tool/
[dejagnu]: https://www.gnu.org/software/dejagnu/
---
## Being terrific: icing on the CLI cupcake

* programmable completion
    * Click provides [facilities][cc] for this (Bash only, I think)
    * or you can [write your own][manual]
    * look at [these examples][bashcompletion]
* a user config file where they can specify default behavior
    * _e.g._, `mysql` command line client
* defaults configurable with environment variables
    * _e.g._, `LESS` environment variable for `less`

[cc]: https://click.palletsprojects.com/en/7.x/bashcomplete/
[manual]: https://www.gnu.org/software/bash/manual/html_node/A-Programmable-Completion-Example.html#A-Programmable-Completion-Example
[bashcompletion]: https://github.com/scop/bash-completion

---
## Over-9000-Super-Saiyan stuff

* an interactive shell
    * MacPorts' `port` command, `mysql`, `python`
* a front-end that communicates with a persistent daemon
    * _e.g._, `clamscan`, `spamassassin`, Heroku and AWS clients

Your Friday-after-lunch, scratch-an-itch project probably isn't going to benefit
from an interactive shell or
<abbr title="Interprocess Communcation">IPC</abbr> with a long-running daemon.

<small>However, there _are_ Readline bindings and introspection / autocompletion
libraries for Python ([jedi](https://github.com/davidhalter/jedi) is one that
comes to mind), so an interactive shell might not be as far off as you
think.</small>

---
name: nextlevel
## Next-level stuff

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

### [`pmfind`][pmfind]

Scrapes the titles and URLs of research papers matching user-provided search terms from <abbr title="National Center for Biotechnology Information">NCBI</abbr>'s
[PubMed][pm] index.

Only the first page of results, though.

--

<small>Yes, as a matter of fact, there _is_ an [API][entrez].</small>

--

<small>Scraping the headline and URL from the web page is a one-liner in
[XPath][xpath], and I didn't want to be unwrapping mountains of JSON for
a simple demo.</small>

[pmfind]: https://github.com/ernstki/terrific-terminal-apps-python/blob/master/pmfind
[pm]: https://pubmed.ncbi.nlm.nih.gov/
[entrez]: https://www.ncbi.nlm.nih.gov/books/NBK25500/
[xpath]: https://www.w3.org/TR/xpath/all/

---
## `pmfind`: next steps

* allow reading from an input file (`--i` / `--input`)
* allow specifying an alternate delimiter (`-s` / `--sep`)
* `setup.py` with an `entry_point`
  * so that an executable is automatically created in the user's `PATH`
--

* profit!

---
class: center, middle

# BONUS SLIDES

---
name: clipboard
## Piping to/from the clipboard

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
## Piping to/from the clipboard (cont'd)

[pyperclip][pyper] seems to be a good cross-platform library for
reading/writing the clipboard from Python programs.

…but, does your Python command-line program _need_ to do that, if there is already a facility for that built in to the OS (macOS)?

Remember, One Thing Well.

[pyper]: https://pypi.org/project/pyperclip/

---
name: powershell
## Windows: PowerShell and CMD.EXE

In spite of the early "Unixy" pipe-and-filter discussion, the concepts are
PLENTY applicable for Windows people as well.

`CLIP.EXE` comes with Windows, so this works<span style="color:red">\*</span>

```dos
your-program | clip
```

Only in the copy-to-clipboard direction, though. If you need to send clipboard text _to_ your program, do this instead<span style="color:red">\*\*</span>

```dos
powershell -command get-clipboard | your-program-that-reads-stdin
```

.footnote[
<span style="color:red">\*</span> Is that too much typing for you? Create a [DOSKEY macro](https://superuser.com/a/1134468/73744)!

<span style="color:red">\*\*</span>I _think_ this works in the copy <em>to</em> clipboard direction, too?
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
  * really informative, and (to a Unix nerd, anyway) doesn't feel dated
  * see [this gist](https://gist.github.com/ernstki/1432b3ea843410a4826ce9cb1584d7b5) for a step-by-step recreation of the spellchecker and talking calculator in modern shell script and Python
* [The Unix Chainsaw][chainsaw] by Gary Bernhardt
  * very revelatory talk about using Unix pipes and functions to their fullest potential, to encapsulate complexity
* [Create *beautiful* command-line interfaces with Python][pycon2012]
  * from PyCon 2012, by the author of [docopt][]
* [jlevy/the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line)
* Internet your pipes and pipe the Internet with [`curl`](https://curl.haxx.se)
    * just look at the protocol support!

[pycon2012]: https://www.youtube.com/watch?v=pXhcPJK5cMc
[docopt]: https://github.com/docopt/docopt
[chainsaw]: https://www.youtube.com/watch?v=sCZJblyT_XM

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

1. ["Ten recommendations for creating usable bioinformatics command line software"][tenrec] by Torsten Seemann
2. ["Ten Essential Development Practices"][dc] by Damian Conway
3. [argparse][] - from the Python standard library
  * [official tutorial][aptut]
4. [Click][] - by [Armin Ronacher](https://github.com/mitsuhiko), and others
  * [API documentation][clickdoc]
5. [docopt][] - by [Vladimir Keleshev](https://github.com/keleshev), and others
  * [try it in a browser][trydocopt]

[tenrec]: https://doi.org/10.1186/2047-217X-2-15
[dc]: https://www.perl.com/pub/2005/07/14/bestpractices.html/
[argparse]: https://docs.python.org/3/library/argparse.html
[aptut]: https://docs.python.org/3/howto/argparse.html
[click]: https://palletsprojects.com/p/click/
[clickdoc]: https://click.palletsprojects.com/en/7.x/
[trydocopt]: http://try.docopt.org/

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

