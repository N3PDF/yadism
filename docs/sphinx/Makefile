# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help html view clean cleanall

html:
	sphinx-apidoc -o ./source/modules --module-first ../../src/yadism/
	@rm -f ./source/modules/modules.rst ./source/modules/*/modules.rst}
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

view: html
	$(BROWSER) $(BUILDDIR)/html/index.html

clean:
	rm -rf build
	rm -rf _build

cleanall: clean
	rm -rf $(SOURCEDIR)/modules