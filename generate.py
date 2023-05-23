import sys
import subprocess
from pathlib import Path

import markdown

import pymd
import mdcleaner

build_dir = Path(__file__).parent / '_build'
if not build_dir.exists():
  build_dir.mkdir()

def generate_python_file(input_file: Path):
  python_file = build_dir / input_file.with_suffix('.py')
  pymd.convert_to(input_file, python_file)
  return python_file


HTML_BOILERPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Note</title>
</head>
<body>
"""

def generate_html_file(input_file: Path):
  python_file = generate_python_file(input_file)
  html_file = python_file.with_suffix('.html')

  env = {'PYTHONPATH': Path(__file__).parent}
  result = subprocess.run([sys.executable, python_file], env=env, capture_output=True)
  if result.returncode == 0:
    input = mdcleaner.clean(result.stdout.decode('utf8'))
    body = markdown.markdown(input, extensions=['fenced_code'])
    output = (HTML_BOILERPLATE + body  + '\n</body>\n</head>\n</html>').encode('utf8')
  else:
    print(result.stderr.decode('utf8'))
    output = b'```\n' + result.stderr + b'\n```'

  with html_file.open('wb') as fp:
    fp.write(output)

input_file = Path('01-functions.py')
generate_html_file(input_file)
