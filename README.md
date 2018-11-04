# PageRank 

dict-dict 형식의 inbound graph 에 대한 pagerank 계산

```python
pr = pagerank(
    G_inbound,    # inbound graph. doesn't care key type.
    bias=None,    # bias for personalized pagerank
    df=0.15,      # damping factor
    max_iter=50,
    converge_error=0.001,
    verbose=0
)
```