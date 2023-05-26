"""
Given a normal Python script, generate another Python script that outputs markdown
"""
import re
from dataclasses import dataclass
from pathlib import Path

def get_lines(input_file: Path):
  with input_file.open() as fp:
    for line in fp:
      yield line.rstrip()

@dataclass
class Header:
  level: int
  content: str

  @staticmethod
  def from_line(line):
    match = re.match(r'(#+)\s*(.*)', line)
    try:
      hashes, content = match.groups()
      return Header(level=len(hashes), content=content)
    except AttributeError:
      raise Exception(f'Failed to parse header line "{line}"')

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

  if len(accumulator) == 1 and accumulator[0].startswith('#'):
    return Header.from_line(accumulator[0])
  else:
    content = '\n'.join(accumulator)
    return Code(content)

def get_code_chunks(tokens):
  def printable(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

  first_header = True

  for token in tokens:
    match token:
      case Header(level, content):
        prefix = '#' * (1 if first_header else level + 1)
        first_header = False
        yield f'print("{prefix} {content}\\n")'
      case Markdown(content):
        yield f'print("{printable(content)}\\n")'
      case Code(content):
        yield f'print("```python")'
        yield f'print("{printable(content)}")'
        yield f'print("```\\n")'
        yield f'print("```")'
        yield replace_plt_show(content)
        yield f'print("```\\n")'

def replace_plt_show(content: str):
  return content.replace(
    'import matplotlib.pyplot as plt',
    'import matplotlib.pyplot as plt\nimport htmlprint\nplt.show = htmlprint.PlotHtmlPrinter(plt, __file__)')

def convert_to(input_file: Path, output_file: Path):
  tokens = tokenize(get_lines(input_file))

  with output_file.open('w', encoding='utf8') as fp:
    for chunk in get_code_chunks(tokens):
      fp.write(chunk + '\n')
