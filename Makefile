help:
	@echo "Build 'The Black Hack' HTML files using the following command:"
	@echo ""
	@echo "  make html: build HTML pages."
	@echo "  make clean: delete the 'build' directory"
	@echo ""

html:
	tox -e build

clean:
	rm -Rf build/
