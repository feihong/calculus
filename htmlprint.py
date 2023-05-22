from types import ModuleType
from pathlib import Path

class PlotHtmlPrinter:
  def __init__(self, plt_module: ModuleType, input_file: str):
    self.input_file = Path(input_file)
    self.plt = plt_module
    self.counter = 1

  def __call__(self, format='svg'):
    suffix = '.' + format
    img_name = f'{self.input_file.stem}-{self.counter}'
    img_file = self.input_file.with_name(img_name).with_suffix(suffix)
    self.counter += 1
    self.plt.savefig(img_file)
    self.plt.close()
    print('<html>')
    print(f'<img src="{img_file.name}">')
    print('</html>')
