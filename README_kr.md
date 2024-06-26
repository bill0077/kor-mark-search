# kor_mark_search
`kor_mark_search`는 local 폴더 내부의 한국어 마크다운 문서에서 쿼리를 검색하기 위한 검색 엔진입니다.
자잘한 오타, 한영키 미변환 등도 문제없이 검색이 가능합니다.

root 폴더 내부의 마크다운 문서를 바탕으로 인덱스를 생성하고, 생성된 인덱스로 주어진 쿼리를 검색하는 구조입니다. 인덱스 생성시 비슷한 단어를 하나의 token으로 분류하기 때문에 쿼리나 마크다운 문서에 오탈자가 있어도 검색에 큰 영향이 없습니다 (특수문자는 인덱싱되지 않음).

ex) '컨테이너', '컨테ㅇ너', '커테ㅣㅇ너', 'zjsxpdlsj', 'zjsxpdjs' 모두 '컨테이너` token 하나로 해석됩니다.

# 시작해보기
## 실행 환경 설정
`kor-mark-search`는 외부 패키지가 필요하지 않습니다. `git clone` 이후 main.py를 실행해 빠르게 시작해볼 수 있습니다.

또는 `pip3 install kor-mark-search`로 설치하는 방법도 가능합니다. `import kor-mark-search`로 패키지를 import하고 `kor_mark_search.index_search.search`함수를 사용할 수 있습니다.

minimal example (main.py와 동일):
```python
from kor_mark_search.index_search import search

while True:
  query = input('query:')
  result = search(query, 'YOUR_ROOT_PATH')
  print(result)
```

# kor_mark_search.index_search
## search
실행하면 input으로 검색할 쿼리와 root를 받습니다.
결과값으로 전체 마크다운 파일을 검색 결과에 따라 정렬하여 반환하고, 검색에 사용된 token들과 그 score를 추가로 반환합니다.

초기에는 인덱스를 생성하느라 시간이 걸리지만(전체 문서 길이 n에 대해 매우 완만한 O(n^2) 시간 복잡도) 한번 인덱스를 생성하면 이후에는 기존의 인덱스를 로드해 검색을 진행합니다.
마크다운 파일들을 root(인자로 따로 설정 가능) 폴더에 넣으면 해당 폴더 내부 문서를 기준으로 인덱스를 생성합니다.
쿼리를 인덱스를 기반으로 검색하는 함수입니다. 아래와 같은 매개변수가 있습니다
- `root`: index를 생성할 마크다운들이 있는 폴더입니다. 기본은 'root'입니다.
- `skip_indexing`: index 생성을 하지 않을 폴더의 목록입니다. 기본은 지정되어 있지 않습니다.
- `index_file`: index 파일이 생성되는 경로입니다. 기본은 'index/path_to_root.json'입니다.
- `alpha`: 서로 다른 token들이 같은 group인지 판정하는 기준치입니다. 값이 높을수록 더욱 많은 token이 하나의 group으로 예상합니다.
- `beta`: 한영키가 뒤바뀐채로 입력되었는지 판정하는 기준치입니다. 값이 높을수록 한영키 오타를 높게 예상합니다.
- `min_results`: 최소 min_results 만큼의 마크다운들을 반환합니다. 그 이상의 마크다운은 적합도가 `beta`를 넘어야만 반환됩니다.

# kor_mark_search.index_builder
## load_index
인덱스를 파일로부터 로드해오는 함수입니다.
- `path`: 로드해올 파일의 경로

## build_index
root 폴더의 인덱스를 생성하는 함수입니다.
- `root`: 인덱스를 생성할 최상위 폴더
- `index_file`: 생성한 인덱스를 저장할 파일의 경로
- `skip_indexing`: 인덱스를 생성하지 않을 폴더. 어느 위치에 있든 해당 폴더의 파일은 인덱싱되지 않습니다.
- `alpha`: 위의 `kor_mark_search.index_search.search` 에서 사용된 alpha와 동일

## add_index
기존의 인덱스에 새로운 마크다운을 추가하는 함수입니다. 이미 인덱싱되어있는 마크다운을 다시 `add_index`로 추가하면 해당 마크다운의 인덱스를 덮어씁니다.
- `markdown_path`: 인덱스에 추가할 마크다운의 경로
- `index_file`: 기존 인덱스 파일의 경로
- `alpha`: `build_index`의 alpha와 동일