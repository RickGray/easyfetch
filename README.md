MultiSearch
===========

MultiSearch是一款集合各搜索引擎来进行综合搜索以获取搜索结果信息（url, host, ip等）的辅助工具。
同时也可以在自己的工程中直接使用各搜索引擎的模块，来获取信息进行处理加工。

借助 ``MultiSearch``，可以通过 ``Google Hacking`` 等查询手段获取你想要的信息并进行相应的后续处理；还可以查询域名信息，从大量搜索引擎的结果中整合出所有的子域名或者其他信息。

Installation
----
将此项目克隆至本地：

    git clone https://github.com/rickgray/MultiSearch MultiSearch

Usage
----

通过 ``Hacking Search`` 搜索 ``inurl:.asp?id=``

    python multisearch.py -s 'inurl:.asp?id=' -b baidu -l 200 -o urls.txt
