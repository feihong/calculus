import subprocess
from pathlib import Path
import shutil

import markdown

import pymd

build_dir = Path(__file__).parent / '_build'
if not build_dir.exists():
  build_dir.mkdir()
  shutil.copy('htmlviz.py', build_dir)

def generate_python_file(input_file: Path):
  python_file = build_dir / input_file.with_suffix('.py')
  pymd.convert_to(input_file, python_file)
  return python_file

def generate_markdown_file(python_file: Path):
  markdown_file = python_file.with_suffix('.md')

  result = subprocess.run(['python', python_file], capture_output=True)
  if result.returncode == 0:
    # replace empty output blocks with whitespace
    output = result.stdout.replace(b'\n```\n```\n', b'\n')
  else:
    print(result.stderr.decode('utf8'))
    output = b'```\n' + result.stderr + b'\n```'

  with markdown_file.open('wb') as fp:
    fp.write(output)

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

def generate_html_file(python_file: Path):
  html_file = python_file.with_suffix('.html')

  result = subprocess.run(['python', python_file], capture_output=True)
  if result.returncode == 0:
    # replace empty output blocks with whitespace
    input = result.stdout.decode('utf8').replace('\n```\n```\n', '\n')
    body = markdown.markdown(input, extensions=['fenced_code'])
    output = (HTML_BOILERPLATE + body  + '\n</body>\n</head>\n</html>').encode('utf8')
  else:
    print(result.stderr.decode('utf8'))
    output = b'```\n' + result.stderr + b'\n```'

  with html_file.open('wb') as fp:
    fp.write(output)

# for token in tokenize(get_lines(Path('gradient-fields-forever.py'))):
#   print(token)

input_file = Path('01-functions.py')
python_file = generate_python_file(input_file)
# generate_markdown_file(python_file)
generate_html_file(python_file)
