.DEFAULT_GOAL := show-help
.PHONY: show-help create_environment requirements check_environment
PROJECT_NAME := {{ cookiecutter.repo_name }}

SHELL ?= /usr/bin/bash
CONDA_EXE ?= {{ cookiecutter.conda_path }}

## Install macos dependencies
osx-depend: sdl-update gstreamer-update
	@echo "all MacOS dependencies up-to-date"

# Ensure xcode command-line tools are installed (required for gstreamer)
xcode-update: .make.xcode.install

.make.xcode.install: tools/xcode-cli-tools.sh
	./tools/xcode-cli-tools.sh
	touch .make.xcode.install

# Ensure SDL is up to date (required for kivy)
sdl-update: .make.sdl.update

.make.sdl.update: .make.sdl.install
	brew upgrade sdl2 sdl2_image sdl2_ttf sdl2_mixer
	touch .make.sdl.update

sdl-install: .make.sdl.install

.make.sdl.install:
	brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
	touch .make.sdl.install

# Ensure gstreamer is up to date
gstreamer-update: .make.gstreamer.update

.make.gstreamer.update: .make.gstreamer.install
	brew upgrade gstreamer gst-plugins-base gst-plugins-good
	touch .make.gstreamer.update

gstreamer-install: .make.gstreamer.install

.make.gstreamer.install: .make.xcode.install
	brew install gstreamer gst-plugins-base gst-plugins-good
	touch .make.gstreamer.install

## Clean intermediate files. Forces a complete rebuild
clean:
	rm -f .make.*


## Create conda environment used for running this project. Only needed the first time. Use `make requirements` for subsequent updates.
create_environment:
	$(CONDA_EXE) env create -n $(PROJECT_NAME) -f environment.yml

## Delete the virtual environment for this project
delete_environment:
	$(CONDA_EXE) env remove -n $(PROJECT_NAME)

## Install or update Python Dependencies
requirements: check_environment environment.lock.yml
	@echo "$(PROJECT_NAME) environment us up-to-date"

environment.lock.yml: environment.yml
	$(CONDA_EXE) env update -n $(PROJECT_NAME) -f $<
	$(CONDA_EXE) env export -n $(PROJECT_NAME) -f $@

check_environment: osx-depend
ifneq (${CONDA_DEFAULT_ENV}, $(PROJECT_NAME))
	$(error Must activate `$(PROJECT_NAME)` environment before proceeding)
endif

## Build for IOS
ios: osx-depend
	buildozer ios release

## Open XCode project for IOS release
xcode:
	buildozer ios xcode

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
#	* save line in hold space
#	* purge line
#	* Loop:
#		* append newline + line to hold space
#		* go to next line
#		* if line starts with doc comment, strip comment character off and loop
#	* remove target prerequisites
#	* append hold space (+ newline) to line
#	* replace newline plus comments by `---`
#	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>

print-%  : ; @echo $* = $($*)

HELP_VARS := PROJECT_NAME

help-prefix:
	@echo "To get started:"
	@echo "  >>> $$(tput bold)make create_environment$$(tput sgr0)"
	@echo "  >>> $$(tput bold)conda activate $(PROJECT_NAME)$$(tput sgr0)"
	@echo
	@echo "$$(tput bold)Project Variables:$$(tput sgr0)"
	@echo

show-help: help-prefix $(addprefix print-, $(HELP_VARS))
	@echo
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
