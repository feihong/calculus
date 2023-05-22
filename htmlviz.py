"""
Save plots to file and output their corresponding img elements
"""
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Settings:
  input_file: Path
  plt: object
  counter: int

settings = None

def init(input_file, plt):
  global settings
  settings = Settings(Path(input_file), plt, 1)

def show(format='svg'):
  global settings
  img_file = settings.input_file.with_name(settings.input_file.stem + f'-{settings.counter}').with_suffix('.' + format)
  settings.counter += 1
  settings.plt.savefig(img_file)
  settings.plt.close()
  print(f'<img src="{img_file.name}">')
