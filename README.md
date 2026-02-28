# Truly Terrific Terminal Apps (in Python)

[Slides](https://ernstki.github.io/terrific-terminal-apps-python) made with
<https://github.com/gnab/remark>.

## Command-line parsing sample code

If you're interested in the command-line parsing examples mentioned in the
slides, see [`sample-code`](sample-code):

* [bare-bones starter script](sample-code/pmfind-explained.py), with comments
* [`pmfind`](sample-code/pmfind) uses [argparse][]
* [`pmfind-docopt.py`](sample-code/pmfind-docopt.py) uses [docopt][]
* [`pmfind-click.py`](sample-code/pmfind-click.py) uses [click][]

Here's a [Click-based example that also creates a man page][setuptools]; see its
[README][streadme] for details.


## Author

Kevin Ernst &lt;[ernstki -at- mail.uc.edu](mailto:ernstki%20-at-%20mail.uc.edu)&gt;


## License

For text content:

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">CC-BY-4.0</a> (do basically whatever you want _except_ claim that you wrote it)

For original code:

[WTFPL][] 2.0 or [ISC][sample-code/LICENSE.txt] at your option.


[argparse]: https://docs.python.org/3/library/argparse.html
[docopt]: https://github.com/docopt/docopt#readme
[click]: https://github.com/pallets/click#readme
[setuptools]: sample-code/pmfind-setuptools
[streadme]: sample-code/pmfind-setuptools#readme
[wtfpl]: https://www.wtfpl.net/about
