# graphviz
https://graphviz.org/
在线： https://dreampuf.github.io/GraphvizOnline/

## 基础指向
```
digraph demo{
    A->B[dir=both];
    B->C[dir=none];
    C->D[dir=back];
    D->A[dir=forward];
}
```
```viz
digraph demo{
    A->B[dir=both];
    B->C[dir=none];
    C->D[dir=back];
    D->A[dir=forward];
}
```