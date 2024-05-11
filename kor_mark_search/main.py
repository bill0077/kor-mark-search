from kor_mark_search.index_search import search

while True:
  query = input('query:')
  result = search(query, 'root')
  print(result)