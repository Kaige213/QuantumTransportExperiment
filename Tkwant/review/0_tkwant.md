<center>
    <b>描述要准确，能用图、表达式、代码，就不要用文字 ---- 鲁迅 </b>  &#160; &#160; &#160;&#160; &#160;&#160; &#160;  <img src="../figures/0/1.png" style="zoom:90%;" />
</center>




# Tkwant学习笔记

[2021.1.28]

最近看文献，遇到tkwant，觉得很有意思，想知道tkwant是如何将含时输运转换为数学问题，并用程序实现数值解。但网站上的示例只展示了如何使用tkwant，关键的计算过程，以及如何获取各个物理量都没有仔细讲解。只能根据他们的论文，结合源码，来理解tkwant。



**说明：**

- 1-6小节是自己写的代码重复tkwant对1维系统的计算，用来理解tkwant的算法；
- 第7小节是以Fabry_Perot_interferometer为例，总结一些命令的含义，以及如何查看tkwant中的关键量；
- 第8小节是总结如何使用tkwant的log功能
- 程序源码在我的[github](https://github.com/Kaige213/QuantumTransportExperiment/tree/master/Tkwant)中（用jupyter notebook打开）



**目录：**

1. [波函数在无限深势阱中的演化](http://www.yxkblog.com/StudyNotes/tkwant/1_波函数在无限深势阱中的演化.html)
2. [波函数在平直空间的演化（吸收势的使用）](http://www.yxkblog.com/StudyNotes/tkwant/2_波函数在平直空间的演化（吸收势的使用）.html)
3. [定态散射](http://www.yxkblog.com/StudyNotes/tkwant/3_定态散射.html)
4. [散射态的时域演化](http://www.yxkblog.com/StudyNotes/tkwant/4_散射态的时域演化.html)
5. [多体态的演化](http://www.yxkblog.com/StudyNotes/tkwant/5_多体态的演化.html)
6. [Fabry_Perot_interferometer](http://www.yxkblog.com/StudyNotes/tkwant/6_Fabry_Perot_interferometer.html)
7. [tkwants使用总结](http://www.yxkblog.com/StudyNotes/tkwant/7_tkwants使用总结.html)
8. [其他](http://www.yxkblog.com/StudyNotes/tkwant/8_其他.html)

