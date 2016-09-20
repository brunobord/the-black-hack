help:
	@echo "Build 'The Black Hack' HTML files using the following command:"
	@echo ""
	@echo "  make clean: delete the 'build' directory"
	@echo "  make html: build HTML pages."
	@echo "  make softbuild: build HTML+synchronize PDFs (no rebuild)."
	@echo "  make fullbuild: Build the HTML+PDF files for every language"
	@echo ""

clean:
	rm -Rf build/

html:
	tox -e html

softbuild: html
	tox -e pdf -- none

fullbuild:
	tox -e html,pdf
