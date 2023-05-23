dev:
	fswatch -0 --include "*.py" functions | xargs -0 -n 1 -I {} python generate.py {}

server:
	python server.py

clean:
	rm _build/*
