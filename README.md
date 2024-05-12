# kor_mark_search
`kor_mark_search` is a search engine for retrieving queries from Korean markdown documents inside the local folder.
You can search for small typos and Korean-English keys without any problems.

It generates an index based on the markdown document inside the root folder and searches for a given query with the generated index. Similar words are classified as one token group when the index is generated, so the search is not significantly affected even if there are typos in the query or markdown document (special characters are not indexed).

ex) '컨테이너', '컨테ㅇ너', '커테ㅣㅇ너', 'zjsxpdlsj', 'zjsxpdjs' are all interpreted as one 컨테이너` token.

# Get started
## Environment settings
`kor-mark-search` does not require an external package. You can start quickly by running main.py after `git clone`.

Alternatively, you can install it with `pip3 install kor-mark-search`. You can import the package with `import kor-mark-search` and use the `kor_mark_search.index_search.search` function.

minimal example (same as main.py):
```python
from kor_mark_search.index_search import search

while True:
query = input('query:')
result = search(query, 'YOUR_ROOT_PATH')
print(result)
```

# kor_mark_search.index_search
## search
When executed, it receives the query and root to be retrieved as input.
As a result, the entire markdown file is sorted according to the search result and returned, and additional tokens and their scores used in the search are returned.

Initially, it takes time to generate an index (a very gentle O(n^2) time complexity for the entire document length n), but once you generate an index, you can then load the existing index to proceed with the search.
When you place markdown files in the root folder, you create an index based on the documents inside that folder.
A function that searches a query based on an index. It has the following parameters
- `root`: A folder with markdowns to create an index. The default is 'root'.
- `skip_indexing`: List of folders that do not want to create an index. Default is not specified.
- `index_file`: The path from which the index file is created. The default is 'index/path_to_root.json'.
- `alpha`: A criterion for determining whether tokens are the same group. The higher the value, the more tokens expect to be a group.
- `beta`: A criterion for determining whether a Korean/English key is entered in reverse. The higher the value, the higher the Korean/English key typo is expected.
- `min_results`: Returns a minimum of min_results markdowns. Any more markdown is returned only when the fit exceeds 'beta'.

# kor_mark_search.index_builder
## load_index
A function that loads indexes from a file.
- `path`: the path of the file to be loaded

## build_index
A function that generates the index of the root folder.
- `root`: Top folder to generate index
- `index_file`: the path of the file to store the generated index
- `skip_indexing`: the folder in which you will not create an index. Files in that folder will not be indexed wherever it is.
- `alpha`: same as alpha used in `kor_mark_search.index_search.search` above

## add_index
A function that adds a new markdown to an existing index. Adding an already indexed markdown back to `add_index` overwrites the index of that markdown.
- `markdown_path`: the path of the markdown to be added to the index
- `index_file`: Path to an existing index file
- `alpha`: the same as alpha in `build_index`