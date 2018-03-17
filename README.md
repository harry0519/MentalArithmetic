# MentalArithmetic 小学口算训练统计工具

平时纸质口算使用答题卷, 存在以下问题
* 题目固定.反复练习后, 小孩直接背诵答案顺序, 并未真正训练口算
* 题目数量有限, 没有全覆盖所有可能的题型
* 无法统计单题使用时间, 对答题情况进行精确分析
* 无法根据小孩答题情况, 动态调整出题频率

针对纸质试卷问题, MentalArithmetic工具提供
* 随机出题, 单次测试题目不重复
* 单题用时记录
* 答题完毕后的统计分析
* 长期记录分析(未实现)
* 根据历史答题时间, 动态调整出题频率. 针对性训练不熟练的题(未实现)
* 能力分析. 根据测试题记录, 给出口算速度提高的分析报告, 便于平时进行针对性训练.(未实现)


20以内加减法共20*2*20=800题. 考虑到一些不太需要练习的情况, MentalArithmetic去除了
* 相减<=0 (a<=b)
* 相加的两个数都<=3 (a, b <=3)
* 相加>20的题目 (a+b>20)
剩余题库=371题

# 环境
python 3.5+
https://www.python.org/downloads/

需要的三方库参考requirements.txt
支持windows, linux, macOS

# 运行
默认单次试题数量未60题， 可以通过修改ematch.py文件中QUESTION_NUM 来调整单次试题数量. 建议在20-200题之间.
python emath.py

按enter后开始答题.
答出后马上按enter进入
答题完毕会显示本次答题的时间变化信息及整体, 加法,减法的统计分类信息.
所有历史答题记录会保存在emathis.csv文件中供后续分析
![答题统计图](https://github.com/harry0519/MentalArithmetic/blob/master/Figure_1.png)
# 其他
欢迎发送你小孩的成绩文件(emathis.csv),年龄, 性别, 城市给我:harry0519@gmail.com, 用于进一步的统计分析.
