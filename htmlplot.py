"""
Save plots to file and output their corresponding img elements
"""
from pathlib import Path

class HtmlPlot:
  def __init__(self, input_file):
    self.input_file = Path(input_file)
    self.counter = 1
    self.image_files = []

  def save(self, plt):
    img_file = self.input_file.with_name(self.input_file.stem + f'-{self.counter}').with_suffix('.svg')
    self.counter += 1
    plt.savefig(img_file)
    plt.close()
    self.image_files.append(img_file)

  def print_img_elements(self):
    if len(self.image_files):
      for image_file in self.image_files:
        print(f'<img src="{image_file.name}"> <!-- {image_file.stat().st_size} -->\n')

      self.image_files = []
