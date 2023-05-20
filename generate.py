import re
import subprocess
from dataclasses import dataclass
from typing import List
from pathlib import Path
import shutil

import markdown

build_dir = Path(__file__).parent / '_build'
if not build_dir.exists():
  build_dir.mkdir()
  shutil.copy('htmlplot.py', build_dir)

def get_lines(input_file: Path):
  with input_file.open() as fp:
    for line in fp:
      yield line.strip()

@dataclass
class Header:
  level: int
  content: str

  @staticmethod
  def from_line(line):
    match = re.match(r'(#+)\s*(.*)', line)
    hashes, content = match.groups()
    return Header(level=len(hashes), content=content)

@dataclass
class Markdown:
  content: str

@dataclass
class Code:
  content: str

def tokenize(lines):
  for line in lines:
    if line == '':
      continue
    elif line.startswith('"""'):
      yield tokenize_markdown(lines)
    else:
      yield tokenize_code_or_header(line, lines)

def tokenize_markdown(lines):
  accumulator = []

  for line in lines:
    if line.startswith('"""'):
      return Markdown('\n'.join(accumulator))
    else:
      accumulator.append(line)

  raise Exception('Expected """')

def tokenize_code_or_header(line, lines):
  accumulator = [line]

  for line in lines:
    if line == '':
      break
    else:
      accumulator.append(line)

  if len(accumulator) == 1:
    return Header.from_line(accumulator[0])
  else:
    return Code('\n'.join(accumulator))

BOILERPLATE = """\
import sys
sys.path.append('..')
import htmlplot

__plot = htmlplot.HtmlPlot(__file__)
"""

def get_code_chunks(tokens):
  def printable(s):
    return s.replace('\n', '\\n')

  yield BOILERPLATE

  first_header = True

  for token in tokens:
    match token:
      case Header(level, content):
        if first_header:
          level += 1
          first_header = False

        prefix = '#' * (4 - level)
        yield f'print("{prefix} {content}\\n")'
      case Markdown(content):
        yield f'print("{printable(content)}\\n")'
      case Code(content):
        yield f'print("```python")'
        yield f'print("{printable(content)}")'
        yield f'print("```\\n")'
        yield f'print("```")'
        yield content.replace('plt.show()', '__plot.save(plt) # plt.show()')
        yield f'print("```\\n")'
        yield '__plot.print_img_elements()'

def generate_python_file(input_file: Path):
  tokens = tokenize(get_lines(input_file))

  python_file = build_dir / input_file.with_suffix('.py')
  with python_file.open('w', encoding='utf8') as fp:
    for chunk in get_code_chunks(tokens):
      fp.write(chunk + '\n')

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
    input = result.stdout.replace(b'\n```\n```\n', b'\n').decode('utf8')
    body = markdown.markdown(input, extensions=['fenced_code'])
    output = (HTML_BOILERPLATE + body  + '\n</body>\n</head>\n</html>').encode('utf8')
  else:
    print(result.stderr.decode('utf8'))
    output = b'```\n' + result.stderr + b'\n```'

  with html_file.open('wb') as fp:
    fp.write(output)

# for token in tokenize(get_lines(Path('gradient-fields-forever.py'))):
#   print(token)

input_file = Path('gradient-fields-forever.py')
python_file = generate_python_file(input_file)
# generate_markdown_file(python_file)
generate_html_file(python_file)
