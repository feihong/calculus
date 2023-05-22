import inspect
from pathlib import Path
from dataclasses import dataclass
import builtins
import contextlib
import textwrap

real_print = builtins.print

@dataclass
class Settings:
  input_file: Path
  counter: int

  def __init__(self, input_file):
    self.input_file = input_file
    self.counter = 1

def init(input_file):
  global settings
  settings = Settings(Path(input_file))

@contextlib.contextmanager
def use_html_print():
  try:
    builtins.print = html_print
    yield
  finally:
    builtins.print = real_print

def html_print(obj, **kwargs):
  if inspect.ismodule(obj) and obj.__name__ == 'matplotlib.pyplot':
    global settings

    suffix = '.' + kwargs.get('format', 'svg')
    img_name = f'{settings.input_file.stem}-{settings.counter}'
    img_file = settings.input_file.with_name(img_name).with_suffix(suffix)
    settings.counter += 1
    plt = obj
    plt.savefig(img_file)
    plt.close()
    real_print(f'<img src="{img_file.name}">')
  elif hasattr(obj, '__html__'):
    real_print(obj.__html__())
  else:
    text = textwrap.indent(str(obj), '    ')
    real_print(text)
    return
