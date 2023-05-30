import sys
import subprocess
import os
from pathlib import Path

import markdown

import pymd
import mdcleaner

build_dir = Path.cwd() / '_build'

def generate_python_file(input_file: Path):
  python_file = build_dir / input_file.relative_to(Path.cwd())
  if not python_file.parent.exists():
    python_file.parent.mkdir(parents=True)
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
  <style>
  table {
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #bbb;
    padding: 0.5em;
  }
  td {
    text-align: right;
  }
  </style>
  <script>
  MathJax = {
    loader: {
      load: ['input/asciimath', 'output/chtml', 'ui/menu']
    },
    tex: {
      inlineMath: [['$', '$']]
    },
    asciimath: {
      delimiters: [['◊', '◊']]
    },
    svg: {
      fontCache: 'global'
    }
  };
  </script>
  <script type="text/javascript" id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
  </script>
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
    body = markdown.markdown(input, extensions=['fenced_code', 'tables'])
    output = (HTML_BOILERPLATE + body  + '\n</body>\n</head>\n</html>').encode('utf8')
    error = result.stderr.decode('utf8')
    if error != '':
      print('Errors:')
      print(error)
  else:
    print(result.stderr.decode('utf8'))
    output = b'```\n' + result.stderr + b'\n```'

  with html_file.open('wb') as fp:
    fp.write(output)

  return html_file

if __name__ == '__main__':
  input_file = Path(sys.argv[1]).absolute()
  print(f'Processing {input_file}')
  if input_file.suffix != '.py':
    sys.exit(1)
  html_file = generate_html_file(input_file)
  print(f'Generated {html_file}')
