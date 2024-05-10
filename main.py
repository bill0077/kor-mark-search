from index_search import search

while True:
  query = input('query:')
  result = search(query, 'root')
  print(result)