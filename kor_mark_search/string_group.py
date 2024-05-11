from kor_mark_search.unicode_converter import decompose_kor_unicode

class StringGroup:

  def __init__(self, 
               string: str, 
               centrality: list[float]=None, 
               distribution: list[dict[str,int]]=None, 
               group: list[str]=None):
    de_string = decompose_kor_unicode(string)
    self.centroid = de_string
    self.centrality = [1 for _ in range(len(de_string))]
    self.distribution = [{ch: 1} for ch in de_string]
    self.group = [string]

    if distribution and centrality and group:
      self.centrality = centrality
      self.distribution = distribution
      self.group = group

  def add_group(self, string: str) -> None:
    '''Add new string to string group. 
    The centroid of that group, centrality, distribution is also updated'''
    # update group
    self.group.append(string)
    string = decompose_kor_unicode(string)
    
    # update distribution
    for i in range(len(string)):
      ch = string[i]
      if i >= len(self.distribution):
        self.distribution.append({ch: 1})
      elif ch in self.distribution[i]:
        self.distribution[i][ch] += 1
      else:
        self.distribution[i][ch] = 1

    # update centroid and centrality
    self.centroid = ''
    for i in range(len(self.distribution)):
      dist_i = self.distribution[i]
      max_char = max(dist_i, key=dist_i.get)
      num_max_char = dist_i[max_char]
      #num_blank = len(self.group) - sum(dist_i.values())
      if num_max_char < 0.5 * len(self.group):
        self.centrality = self.centrality[:i+1]
        break
      self.centroid += max_char
      if i >= len(self.centrality):
        self.centrality.append(num_max_char / len(self.group))
      else:
        self.centrality[i] = num_max_char / len(self.group)

  def get_elems(self) -> list[str]:
    '''Returns the elements of the string group sorted in order of greatest number.
    Copies are removed'''
    count = {}
    for group in self.group:
      count[group] = count.get(group, 0) + 1
    sorted_elems = sorted(count, key=lambda x: count[x], reverse=True)
    unique_elems = list(dict.fromkeys(sorted_elems))
    return unique_elems

def get_levenshtein_distance(str1: StringGroup, str2: StringGroup) -> float:
  '''Calculate the distance between given strings.
  Not only centroid but also centrality is considered'''
  dp = [[0 for _ in range(len(str2.centroid)+1)] for _ in range(len(str1.centroid)+1)]
  for i in range(1, len(str1.centroid)+1):
    dp[i][0] = dp[i-1][0] + str1.centrality[i-1]
  for j in range(1, len(str2.centroid)+1):
    dp[0][j] = dp[0][j-1] + str2.centrality[j-1]

  for i in range(1, len(str1.centroid)+1):
    for j in range(1, len(str2.centroid)+1):
      sub_cost = (1-(1-str1.centrality[i-1])*(1-str2.centrality[j-1]) 
                  if str1.centroid[i-1][0] != str2.centroid[j-1][0] 
                  else 0)
      # substitution costs littler bigger than adding or removing
      dp_min = min(dp[i-1][j-1]+sub_cost, 
                  dp[i-1][j]+str1.centrality[i-1]*0.9,
                  dp[i][j-1]+str2.centrality[j-1]*0.9)
      dp[i][j] = dp_min

  return dp[-1][-1]