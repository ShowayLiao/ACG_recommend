# ACG_recommend
一个基于bungumi的收视记录，利用Gemini强大的能力，根据喜好推荐动画的prompt。
# Quick Start
1. `main`程序是一个自动爬取bungumi看过记录的脚本，需要修改`main`函数入口处你的用户名，就可以进行爬取。缺少`request`库，就`pip`装上。
2. 爬取后会有一个json文件和一个txt文件，把json文件拖入gem的知识库里，把`prompt.md`的指令输入到指令区即可。
