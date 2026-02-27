PROGRAMNAME = pmfind
VERSION = $(shell python -c 'import pmfind; print(pmfind.__version__)')
VENV = venv
MANPAGE = man/$(PROGRAMNAME).1
BIN = $(VENV)/bin/$(PROGRAMNAME)
VENVACTIVATE = $(VENV)/bin/activate
HOMEPAGE = https://github.com/ernstki/terrific-terminal-apps-python
#MAKEFLAGS = --debug --warn-undefined-variables
ME = $(firstword $(MAKEFILE_LIST))

help:  # prints this help
	@bash -c "$$AUTOGEN_HELP_BASH" < $(ME)

all: install man  # make 'install' target, then 'man'

install: $(BIN)  # install pmfind and dependencies into a virtualenv
$(BIN): $(VENVACTIVATE)
	. $(VENVACTIVATE) && \
	pip install -e .[dev]
	# trick Make into believing the console entry point was updated
	touch $(BIN)


.PHONY: man
man: $(MANPAGE)  # build the man page for pmfind

# use `--target=<some/other/dir>` if you don't want the man page generated in a
# `man` subdirectory of the top-level repository directory
#
# see https://github.com/click-contrib/click-man/issues/72 for an explanation
# of the `--man-version` switch, which is currently needed to avoid an error
#
# also see https://github.com/click-contrib/click-man/pull/74 which fixes the
# docstring indentation problem
$(MANPAGE): $(VENVACTIVATE) $(BIN)
	. $(VENVACTIVATE) && \
	click-man --man-version=$(VERSION) $(PROGRAMNAME)

viewman: $(MANPAGE)  # view the generated manpage (requires 'groff')
	groff -Tutf8 -man -rLL=$$(tput cols)n $(MANPAGE) \
	  | less --quit-if-one-screen

venv: $(VENVACTIVATE)  # create a virtualenv
$(VENVACTIVATE):
	python -m venv $(VENV)

uninstall:  # uninstall pmfind
	pip uninstall $(PROGRAMNAME)

clean:  # remove generated files
	-rm -rf build

reallyclean: clean  # same as 'clean' plus remove the virtualenv
	-rm -rf *.egg-info
	-rm -rf $(VENV)


##
##  internals you can safely ignore
##
define AUTOGEN_HELP_BASH
	declare -A targets; declare -a torder
	targetre='^([A-Za-z]+):.* *# *(.*)'
	if [[ $$TERM && $$TERM != dumb && -t 1 ]]; then
		ul=$$'\e[0;4m'; bbold=$$'\e[34;1m'; reset=$$'\e[0m'
	fi
	printf "\n  %sMakefile targets - $(PROGRAMNAME)" "$$ul"
	[[ -n "$(VERSION)" ]] && printf " v$(VERSION)"
	printf "%s\n\n" "$$reset"
	while read -r line; do
		if [[ $$line =~ $$targetre ]]; then
			target=$${BASH_REMATCH[1]}; help=$${BASH_REMATCH[2]}
			torder+=("$$target")
			targets[$$target]=$$help
			if (( $${#target} > max )); then max=$${#target}; fi
		fi
	done
	for t in "$${torder[@]}"; do
		printf "    %smake %-*s%s   %s\n" "$$bbold" $$max "$$t" "$$reset" \
		       "$${targets[$$t]}"
	done
	if [[ -n "$(HOMEPAGE)" ]]; then
		printf "\n  Homepage:\n    $(HOMEPAGE)\n\n"
	else
		printf "\n"
	fi
endef
export AUTOGEN_HELP_BASH
