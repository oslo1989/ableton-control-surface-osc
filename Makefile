launch12:
	@open /Applications/Ableton*12*

kill:
	@pkill -KILL -f "Ableton Live" || echo "Ableton was not running, so just starting it" && sleep .5

tail:
	@tail -n 50 -f ~/Library/Preferences/Ableton/*/Log.txt | grep --line-buffered -i -e AbletonControlSurfaceOSC

tail-all:
	@tail -n 50 -f ~/Library/Preferences/Ableton/*/Log.txt

copy-controller-script:
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

install-deps:
	@pip install -r requirements.txt

restart-12: kill copy-controller-script launch12

restart: restart-12

build: lint-fix lint