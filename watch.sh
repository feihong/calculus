fswatch -0 --exclude ".*" --include "\\.py$" functions | xargs -0 -n 1 -I {} python generate.py {}
