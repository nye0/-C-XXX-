# **怎样批量检索C末端为XXXX序列的所有蛋白？**

## 工具：
- [blastp](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome)
- Python Package: *pandas*,*xml*

## 步骤：
 ### 1. 检索包含KDEL氨基酸序列的全部蛋白。
- 在Enter accession number(s), gi(s), or FASTA sequence(s)中输入“XXXX”
- 在organism 中输入：Homo sapiens (taxid:9606)
- Algorithm部分使用：PSI-BLAST (Position-Specific Iterated BLAST)
- Algorithm parameters: 可调节Max target sequences选项以获得更多结果。
- 其余参数均使用默认,设置完成后点击“BLAST”开始计算（用时3-5分钟）
- 结果显示后，点击“Download All”，选择XML格式保存结果到本地。
 ### 2. 选择KDEL氨基酸序列的位于c末端的蛋白
- 运行脚本： [c-end.py](https://github.com/nye0/SearchProtein-C-teminal-End-with-XXX/blob/master/C-end.py)

```
./ C-end.py    /path/to/xml /result/path/xlsx (结果需保存为xlsx格式)
```
-	**注意**：
  - c-end.py中第一行需修改为本机python可执行程序的路径
  - 本机python需安装pandas及xml 库


