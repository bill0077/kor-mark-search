def get_config() -> dict:
  return {
    'root': 'post-contents',
    'skip_indexing': ['media'],
    'index_file': 'index/index.json',
    'alpha': 0.2,
    'beta': 0.005
  }