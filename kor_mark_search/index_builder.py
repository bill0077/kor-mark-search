import re
import time
import sys
import json

from kor_mark_search.markdown_utils import get_markdown_list
from kor_mark_search.string_group import StringGroup, get_levenshtein_distance

class IndexBuilder:
  '''Class for building index'''

  @staticmethod
  def load_index(path: str) -> list[dict[str,StringGroup|str]]:
    '''Load index from given path. 
    If load fails, return empty index'''
    index = []
    try:
      with open(path, 'r', encoding='utf8') as index_file:
        index_json = json.load(index_file)
        for sub_index in index_json:
          string_set = []
          for str_grp in sub_index['string_set']:
            string_set.append(StringGroup(str_grp['centroid'],
                                          str_grp['centrality'],
                                          str_grp['distribution'],
                                          str_grp['group']))
          index.append({'path': sub_index['path'], 'string_set': string_set})
    except Exception as e:
      print('failed to load index:', e)
    return index
  
  @staticmethod
  def build_index(root: str, index_file: str, skip_indexing: list[str], alpha: float) -> None:
    '''Creates an index file for root folder at index_file.'''
    start = time.time()
    print(f'start building index for \'{root}\':')
    for md_path in get_markdown_list(root, skip_indexing):
      IndexBuilder.add_index(md_path, index_file, alpha)
    print(f'index builded: takes total {time.time()-start:.2f}s')

  @staticmethod
  def add_index(markdown_path: str, index_file: str, alpha: float) -> None:
    '''Add one markdown to the index file. 
    If the same markdown already exists, it will be overwritten. 
    Group tokens that are differences below aplha'''
    start = time.time()

    string_set: list[StringGroup] = []
    markdown = ''
    with open(markdown_path, 'rt', encoding='utf8') as md_file:
      markdown = md_file.read()

    # Tokenize markdown based on special characters 
    tokens = re.split('[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣|_|-]', markdown)
    token_len_sum = 0
    token_count = 0
    for i, token in enumerate(tokens):
      sys.stdout.write(f'\rindexing \'{markdown_path}\': {i/len(tokens)*100:.2f}%')
      sys.stdout.flush()
      token = token.lower() # do not consider casing
      if len(token) == 0:
        continue
      token_len_sum += len(token)
      token_count += 1

      # Group each token based on levenshtein distance.
      for string_group in string_set:
        distance = get_levenshtein_distance(StringGroup(token), string_group)
        if distance / len(token) < alpha:
          string_group.add_group(token)
          break
      else:
        string_set.append(StringGroup(token))
    
    # Make a new index for a given markdown
    new_index = {'path': markdown_path,
                 'string_set': [{
                 'centroid': str_grp.centroid,
                 'centrality': str_grp.centrality,
                 'distribution': str_grp.distribution,
                 'group': str_grp.group
                 } for str_grp in string_set
                 ]}

    # Add new index part to existing index file
    index_json = []
    try:
      with open(index_file, 'r') as json_file:
        index_json = json.load(json_file)
    except:
      pass

    for i in range(len(index_json)):
      if index_json[i]['path'] == markdown_path:
        index_json[i] = new_index
        break
    else:
      index_json.append(new_index)

    # Save index to file
    with open(index_file, 'w') as json_file:
      json.dump(index_json, json_file)
    
    print(f'\rindexing \'{markdown_path}\': 100% ({token_count} tokens of average length {token_len_sum/token_count:.2f}, {len(string_set)} groups found, {time.time()-start:.2f}s)')