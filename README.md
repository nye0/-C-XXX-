怎么批量检索C末端为KDEL序列的所有蛋白？

1.	工具：
a.	blastp
b.	python
2.	步骤：
a.	检索包含KDEL氨基酸序列的全部蛋白。
i.	在Enter accession number(s), gi(s), or FASTA sequence(s)中输入“KDEL”
ii.	在organism 中输入：Homo sapiens (taxid:9606)
iii.	Algorithm部分使用：PSI-BLAST (Position-Specific Iterated BLAST)
1.	QuickBLASTP及BlastP对长序列效果较好，我们的序列仅含4个氨基酸，不适用
2.	PHI-BLAST及DELTA-BLAST也可以尝试
iv.	Algorithm parameters: 可调节Max target sequences选项以获得更多结果。
v.	其余参数均使用默认
vi.	设置完成后点击“BLAST”开始计算（用时3-5分钟）
vii.	结果显示后，点击“Download All”，选择XML格式保存结果到本地。
b.	选择KDEL氨基酸序列的位于c末端的蛋白
i.	运行脚本：c-end.py（）
ii.	例：
./ C-end.py    /path/to/xml /result/path/xlsx (结果需保存为xlsx格式)
iii.	注意：
1.	c-end.py中第一行需修改为本机python可执行程序的路径
2.	本机python需安装pandas及xml 库

