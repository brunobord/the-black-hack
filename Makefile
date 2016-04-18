help:
	@echo "Build 'The Black Hack' HTML files using the following command:"
	@echo ""
	@echo "  make html"
	@echo ""

html:
	tox -e build
