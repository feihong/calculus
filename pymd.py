"""
Given a normal Python script, generate another Python script that outputs markdown
"""
import re
import io
from dataclasses import dataclass
from pathlib import Path
from typing import List

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
  is_fstring: bool
  content: str

@dataclass
class Code:
  lines: List[str]
  finalized: bool

  def __init__(self, lines):
    self.lines = lines
    self.finalized = False
    if self.lines[-1] == '#':
      self.finalized = True
      self.lines.pop()

  def add(self, code):
    self.lines.append('')
    self.lines.extend(code.lines)
    self.finalized = code.finalized

class Tokenizer:
  @staticmethod
  def tokenize(lines):
    last_code = None

    for token in Tokenizer._tokenize(lines):
      match token:
        case Code(_) as code:
          if last_code is None:
            last_code = code
          else:
            last_code.add(code)
            if last_code.finalized:
              yield last_code
              last_code = None
        case _:
          if last_code is not None:
            yield last_code

          yield token
          last_code = None

    if last_code is not None:
      yield last_code

  @staticmethod
  def _tokenize(lines):
    for line in lines:
      if line == '':
        continue
      elif match := re.match(r'^(f?)"""', line):
        yield Tokenizer.markdown(match.group(1) == 'f', lines)
      else:
        yield Tokenizer.code_or_header(line, lines)

  @staticmethod
  def markdown(is_fstring: bool, lines: List[str]):
    sio = io.StringIO()

    for line in lines:
      if line.startswith('"""'):
        return Markdown(is_fstring, sio.getvalue())
      else:
        sio.write(line + '\n')

    raise Exception('Expected """')

  @staticmethod
  def code_or_header(line, lines):
    accumulator = [line]

    for line in lines:
      if line == '':
        break
      else:
        accumulator.append(line)

    if len(accumulator) == 1 and accumulator[0].startswith('#'):
      return Header.from_line(accumulator[0])
    else:
      return Code(accumulator)

def printable(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

def get_code_chunks(tokens):
  first_header = True

  for token in tokens:
    match token:
      case Header(level, content):
        prefix = '#' * (1 if first_header else level + 1)
        first_header = False
        yield f'print("{prefix} {content}\\n")'
      case Markdown(is_fstring, content):
        prefix = 'f' if is_fstring else ''
        yield f'print({prefix}"{printable(content)}\\n")'
      case Code(lines):
        content = '\n'.join(lines)

        yield f'print("```python")'
        yield f'print("{printable(content)}")'
        yield f'print("```\\n")'
        yield f'print("```")'
        yield replace_plt_show(content)
        yield f'print("```\\n")'

def replace_plt_show(content: str):
  return content.replace(
    'import matplotlib.pyplot as plt',
    'import matplotlib.pyplot as plt\nimport mdprint\nplt.show = mdprint.PlotPrinter(plt, __file__)')

def convert_to(input_file: Path, output_file: Path):
  tokens = Tokenizer.tokenize(get_lines(input_file))

  with output_file.open('w', encoding='utf8') as fp:
    for chunk in get_code_chunks(tokens):
      fp.write(chunk + '\n')


if __name__ == '__main__':
  tokens = Tokenizer.tokenize(get_lines(Path('functions/07-discontinuities.py')))
  for token in tokens:
    print(token)
