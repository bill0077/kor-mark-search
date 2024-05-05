import os
import yaml

def get_markdown_list(root: str, config: dict) -> list[str]:
  file_list = []
  for path, _, files in os.walk(root):
    path = path.replace('\\', '/')
    curr_dir = path.split('/')[-1]
    if curr_dir in config['skip_indexing']:
      continue
    for file in files:
      file_list.append(path+'/'+file)
  return file_list

def parse_yaml_frontmatter(markdown: str) -> dict[str,str]:
  frontmatter = {}
  remainder = markdown
  if markdown.startswith("---"):
    _, yaml_content, remainder = markdown.split("---", 2)
    frontmatter = yaml.safe_load(yaml_content.strip())
  return frontmatter, remainder

def get_markdown_headings(markdown: str) -> list[str]:
  lines = markdown.split('\n')
  headings = []
  for line in lines:
    if line.startswith('#'):
      heading = line.replace('#', '').strip()
      headings.append(heading)
  return headings