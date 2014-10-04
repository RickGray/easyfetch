MultiSearch
===========

MultiSearch是一款集合各种搜索引擎来进行 ``Hacking Search`` 以获取搜索结果信息的辅助工具。

借助 ``MultiSearch``，可以通过 ``Google Hacking`` 等查询手段获取你想要的信息并进行相应的后续处理。

ScreenShots
----

![][img1]


Installation
----
将此项目克隆至本地：
    
    git clone https://github.com/rickgray/MultiSearch MultiSearch

Usage
----

通过 ``Hacking Search`` 搜索 ``inurl:.asp?id=``

    python multisearch.py -s 'inurl:.asp?id=' -b baidu -l 200 -o urls.txt


[img1]:http://rickgray.github.io/Mixed/images/MultiSearch/shot1.jpeg