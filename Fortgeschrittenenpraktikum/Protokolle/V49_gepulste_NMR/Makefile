ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V49_main.pdf

build/V49_main.pdf: Praeambel_prak.tex Theorie.tex Tabellen/* Plots2/* V49_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V49_main.tex

full: Praeambel_prak.tex Theorie.tex V49_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V49_main.tex
		biber build/V49_main.bcf
		lualatex --output-directory=build V49_main.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
