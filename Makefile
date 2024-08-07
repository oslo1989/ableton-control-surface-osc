create-venv:
	@pyenv virtualenv 3.7.13 ableton-control-surface-osc-venv-3.7.13
	#pyenv activate ableton-control-surface-osc-venv-3.7.13

install-deps:
	@pip install --upgrade pip && pip install -r requirements.txt

launch-ableton:
	@open /Applications/Ableton*12*

kill:
	@pkill -KILL -f "Ableton Live" || echo "Ableton was not running, so just starting it" && sleep .5

tail:
	@tail -n 50 -f ~/Library/Preferences/Ableton/*/Log.txt | grep --line-buffered -i -e AbletonControlSurfaceOSC

tail-all:
	@tail -n 50 -f ~/Library/Preferences/Ableton/*/Log.txt

copy-controller-script:
	@rm -rf ~/Music/Ableton"/User Library/Remote Scripts/fastosc"
	@python copy_libs.py
	@rm -rf ~/Music/Ableton"/User Library/Remote Scripts/fastosc/__pycache__"
	@rm -rf ~/Music/Ableton"/User Library/Remote Scripts/AbletonControlSurfaceOSC"
	@cp -r "AbletonControlSurfaceOSC" ~/Music/Ableton"/User Library/Remote Scripts"
	@rm -rf ~/Music/Ableton"/User Library/Remote Scripts/AbletonControlSurfaceOSC/__pycache__"

lint-fix:
	@ruff AbletonControlSurfaceOSC  --quiet --fix --unsafe-fixes

lint:
	@ruff AbletonControlSurfaceOSC --quiet
	@mypy AbletonControlSurfaceOSC

format:
	@ruff format AbletonControlSurfaceOSC

lint-format: lint-fix format lint

restart: kill copy-controller-script launch-ableton

build: lint-fix lint
