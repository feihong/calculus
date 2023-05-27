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
  content: str

@dataclass
class Code:
  lines: List[str]

  def add(self, lines):
    self.lines.append('')
    self.lines.extend(lines)

class Tokenizer:
  last_block = None

  @staticmethod
  def tokenize(lines):
    for line in lines:
      if line == '':
        continue
      elif line.startswith('"""'):
        yield Tokenizer.markdown(lines)
      else:
        result = Tokenizer.code_or_header(line, lines)
        if result is not None:
          yield result

  @staticmethod
  def markdown(lines):
    sio = io.StringIO()

    for line in lines:
      if line.startswith('"""'):
        Tokenizer.last_block = Markdown(sio.getvalue())
        return Tokenizer.last_block
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
      Tokenizer.last_block = Header.from_line(accumulator[0])
      return Tokenizer.last_block
    else:
      if isinstance(Tokenizer.last_block, Code):
        Tokenizer.last_block.add(accumulator)
        return None
      else:
        Tokenizer.last_block = Code(accumulator)
        return Tokenizer.last_block

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
    'import matplotlib.pyplot as plt\nimport htmlprint\nplt.show = htmlprint.PlotHtmlPrinter(plt, __file__)')

def convert_to(input_file: Path, output_file: Path):
  tokens = Tokenizer.tokenize(get_lines(input_file))

  with output_file.open('w', encoding='utf8') as fp:
    for chunk in get_code_chunks(list(tokens)):
      fp.write(chunk + '\n')
