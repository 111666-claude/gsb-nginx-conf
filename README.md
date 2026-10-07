# nginx-conf

解析 nginx 风格配置：块嵌套、指令继承、同级重复指令的取值、include 展开，以及按块路径查找。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m nginxconf --sample=nested
python3 -m nginxconf --sample=inherit
python3 -m nginxconf --sample=last
python3 -m nginxconf --sample=include
python3 -m nginxconf --sample=work
```

## 口径

- **块**：`名字 参数... {` 开一个块，`}` 结束；块可以嵌套。
- **指令**：`键 值;`；同名指令在同一层出现多次时取最后一条。
- **继承**：内层块看不到的指令向外层找，最内层优先。
- **include**：`include 路径;` 在该位置展开另一份配置。
- **查找**：按块路径与键查找走索引。

## 不变量

- 块路径的每一段都对应真实嵌套。
- 取到的值来自最内层最后一条同名指令。
- `scanned` 不随查找次数平方级放大：八百次查找的 `scanned` 不超过 6000。

## 输出契约

`lookup(root, path, key)` 返回取值或空串。场景打印一行 JSON。
`--sample=work` 打印 `{"lookups": N, "scanned": N}`。
