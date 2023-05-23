"""
Clean markdown content:
- Remove empty output blocks
- Indent plain text output
- Extract html blocks out of output blocks
"""
from typing import Iterable

def clean(md: str):
  lines = iter(line.rstrip() for line in md.splitlines())
  chunks = get_transformed_lines(lines)
  return '\n'.join(chunks)

def get_transformed_lines(lines: Iterable[str]):
  inside_code_block = False
  inside_output_block = False
  inside_html_block = False

  for line in lines:
    if line == '```python':
      inside_code_block = True
      yield line
    elif line == '```' and inside_code_block:
      inside_code_block = False
      yield line
    elif line == '```':
      inside_output_block = not inside_output_block
    elif line == '<html>' and inside_output_block:
      inside_html_block = True
    elif line == '</html>' and inside_output_block:
      inside_html_block = False
    elif inside_output_block and not inside_html_block:
      yield '    ' + line
    else:
      yield line
