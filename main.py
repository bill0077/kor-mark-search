from index_search import search
from config import get_config

while True:
  config = get_config()
  query = input('query:')
  result = search(query, config['root'], config)
  print(result)