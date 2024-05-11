import os

def get_markdown_list(root: str, skip_indexing: list[str]) -> list[str]:
  '''Returns a list of all files excluding skip_indexing in the given root folder.'''
  file_list = []
  for path, _, files in os.walk(root):
    path = path.replace('\\', '/')
    curr_dir = path.split('/')[-1]
    if curr_dir in skip_indexing:
      continue
    for file in files:
      file_list.append(path+'/'+file)
  return file_list