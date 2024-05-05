import math

from index_builder import IndexBuilder
from string_group import StringGroup, get_levenshtein_distance
from unicode_converter import kor_unicode_to_char, reverse_kor_eng

def evaluate_token(token: str, index: list[dict[str,StringGroup|str]]) -> dict[str,float]:
  #print(token)
  score_table = {}
  match_list = []
  for sub_index in index:
    string_set = sub_index['string_set']
    min_distance = math.inf
    min_group = None
    for str_grp in string_set:
      avg_distance = get_levenshtein_distance(StringGroup(token), str_grp) / len(token)
      if avg_distance < min_distance:
        min_distance = avg_distance
        min_group = str_grp

    # evaluate score for each sub-index
    #score = len(min_group.group) / (0.1+min_distance)**2
    #score = math.log1p(len(min_group.group)) / (0.1+min_distance)**2
    score =  (2 ** (-15*min_distance)) * math.log1p(len(min_group.group))
    score_table[sub_index['path']] = score
    match_list.append((score, min_group.centroid))
    #print(min_group.centroid, score)

  #print()
  match = sorted(match_list)[-1]
  return score_table, match

def evaluate_query(query: str, index: list[dict[str,StringGroup|str]], config: dict) -> dict[str, float]:
  # initialize score table
  score_table = {}
  match_list = []
  for sub_index in index:
    score_table[sub_index['path']] = 0

  tokens = query.split()
  for token in tokens:
    token = ''.join(list(map(kor_unicode_to_char, token))) # convert kor unicode to each characters
    token = token.lower()
    token_score_table, match = evaluate_token(token, index)
    if match[0] < config['beta']: # consider korean/english toggle key
      tkn_scr_tbl, mch = evaluate_token(reverse_kor_eng(token), index)
      if mch[0] > match[0]:
        match = mch
        token_score_table = tkn_scr_tbl

    for path, score in token_score_table.items():
      score_table[path] += score
    match_list.append(match)

  return score_table, match_list

def search(query: str, root: str, config: dict):
  index = IndexBuilder.load_index(config['index_file'])
  if index == []:
    IndexBuilder.build_index(root, config)
    index = IndexBuilder.load_index(config['index_file'])

  score_table, match_list = evaluate_query(query, index, config)
  score_list = sorted(score_table, key=lambda k: score_table[k], reverse=True)
  return score_list, match_list