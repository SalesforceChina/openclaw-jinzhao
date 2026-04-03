     #js\_row\_immersive\_stream\_wrap { max-width: 667px; margin: 0 auto; } #js\_row\_immersive\_stream\_wrap .wx\_follow\_avatar\_pic { display: block; margin: 0 auto; } #page-content, #js\_article\_bottom\_bar, .\_\_page\_content\_\_ { max-width: 667px; margin: 0 auto; } img { max-width: 100%; } .sns\_opr\_btn::before { width: 16px; height: 16px; margin-right: 3px; }

![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/O1HUibMqqHXdxibrOKsIkRaZoEp6wciaDcIK86Ecns36YMav3uGdrYHzibBbaL1MBu8Y2ggA6EzSRgXQ2NibHJGSae5ibWKVXYNSTiauIhFBzBic27o/0?wx_fmt=jpeg)

装好OpenClaw，第二件必干的是这件事！（第6讲，干货收藏）
================================

原创 58沈剑 58沈剑 [架构师之路](javascript:void\(0\);)

在小说阅读器中沉浸阅读

《OpenClaw100讲》

6. OpenClaw，初始化

  

昨天聊了《[装好OpenClaw，首件要干的事（第5讲）](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651980712&idx=1&sn=3dee11313dd93a78aac4ab91aee98613&scene=21#wechat_redirect)》，最重要的是安全设置。

  

为了让龙虾更好，更个性化的为我们服务，第二件要干的事情是什么呢？

人格的初始化！

  

什么是人格初始化？

告诉OpenClaw，我是谁，你是谁，我们之间的关系，要为我做什么，以及怎么做。

  

更具体的，就是完成以下几个文件的初始化：

1. USER.md：告诉OpenClaw，我是谁，我希望龙虾帮我完成哪些工作，例如：帮我做公众号运营；

2. IDENTITY.md ：告诉OpenClaw，你是谁，例如：妩媚的运营小姐姐；

3\. SOUL.md：告诉OpoenClaw，你的核心人格；

4\. AGENTS.md：你怎么帮我完成相关的工作。

  

其中，AGENTS.md文件最为重要，OpenClaw每次第一时间会读取这个文件，昨天文章中提到的安全准则，就是放到这个文件里的。

  

如何完成人格初始化？

和OpenClaw聊天呀。

  

首先，通过聊天，是让她认识我是谁，以及我想让她帮我干什么。

  

向我提问，以便加强对我的认识。

![](https://mmbiz.qpic.cn/mmbiz_png/O1HUibMqqHXdfBZwyTTpGtARXxzZ9btiaOVh5utN36G7XhA2POuMCctMX82c3ibjK5YnhvEg5OQsexaib3dx6NDVYCt6hrMHL3QbWnVMYqdLicJU/640?wx_fmt=png&from=appmsg)

OpenClaw哐哐哐问了我很多问题。

  

关于我是谁，你去网上搜一下不就知道了吗？

画外音：我真不知道，自己在她面前显摆什么。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXfDoLcLibc9KAF22Aeb4tMeRaASZfnu5wXib7IrP4Z3AGy8Vwe8AE2ibyCC2Fxvho4WLuiabLWUmlV02enYGYjYYUeIiacfteHAT6Sw/640?wx_fmt=png&from=appmsg)

OpenClaw到网上一顿搜，识别出来我的基础履历。

  

看了下更新后的USER.md：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXfe8xDct3oysGrHrfibXtzlollJ3QZ13fDR3GEeDjibncnINN3bviaJkuPNblibG2CBeNNiag19VLRqWfKsgW4BnrUWQzFWpzLbn1TE/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXfKfR4qmXCxC4k29nNacPziahbFmFDPLfLUxy46GQ28PtLQ0lTq9QsPhbMNvZtc3gMDCNicarNfNnpGVBfz5SnHdw6XShb1CHu7o/640?wx_fmt=png&from=appmsg)

还真是这么回事，虽然网上有些内容也不准。

  

接着，通过聊天，告诉她，她是谁。

  

她向我提了四个问题：

1\. 她的角色定位；

2\. 她的口头禅；

3\. 她的专业偏好；

4\. 她喜欢的Emoji；

![](https://mmbiz.qpic.cn/mmbiz_png/O1HUibMqqHXedOJ2qmHSAEcWJf4aIv9K2eOjGAPZ9Bq0r1TnB2vbUJibH7sa2EIoWVKL4YAEm4ulI1XNLMcfhjV5gfxH9gZSFF0VH0sibRX59g/640?wx_fmt=png&from=appmsg)

  

我对她问的四个问题进行了回答：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXdg0wYB3eGmHFhTQLDrib4CPo5MUiaJjCmyrhz1ywz0HtK38OcricMsNMUGRzrjybouEtnpxvGbIUU5SiajnjNibR1TevVOpAc2xiaJw/640?wx_fmt=png&from=appmsg)

整个过程中，还触发了之前修订的安全规范。修改核心文件之前，进行了备份。

  

看了下更新后的IDENTITY.md：

![](https://mmbiz.qpic.cn/mmbiz_png/O1HUibMqqHXeOEutvQMKqx0SvRyPRog6WyQj4CAQcj4Y8UhBXTff1X4WqUvLMCkPaUjSmCJiaqQo1PticyE5Q7iaaNCic6fbRvHQVkmpgUib5Wces/640?wx_fmt=png&from=appmsg)

  

第三，通过聊天，是让她的内在，要恪守什么。

![](https://mmbiz.qpic.cn/mmbiz_png/O1HUibMqqHXdyuWc8Ig4icy03ibgGYTtoyK96yzQGl86GxvJA3Jicf2uBFWsj0QSBjJQ4m7PZAwNkqPLeuj3UHLTIWm7VHO3JwOB8BlUtBBShN4/640?wx_fmt=png&from=appmsg)

  

最后，通过聊天，让她知道，怎么完成相关的任务（重要）。

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXeAjHvPemibnEUvfp2Me7EJ29Q3ic94jkFe7jb0WN5AknJKE3f3IF8ZWUDs3BpgkMtX0hJLLZT7Umr30kLrRKZC7icf1vgelgEHPQ/640?wx_fmt=png&from=appmsg)

这里面要聊的内容比较多，比较久，需要耐心进行沟通。

  

看了下更新后的AGENTS.md：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXcdqtfXBA2HXOicJIVOrlgvHNR6Ugibr1847ExZmZk0SAOW7KnKa7ibBIHuoPwsDzwA4asZ1k1CrzuPY0svcfRnrNUvfFvxhX34FY/640?wx_fmt=png&from=appmsg)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/O1HUibMqqHXct9oCicRzV9vsmViaMBicQfaK4r4JTIadxKpUXb1FkVibTlMxLe1YtFYPfELWvOeE8GhaJiaAjLvpq85jiaMsD0NbVVcDLGNoia7H0Cw/640?wx_fmt=png&from=appmsg)

  

![](https://mmbiz.qpic.cn/mmbiz_png/O1HUibMqqHXfrClBPyO9CuPCiaicuZUibotSYaEU6Udia9ibnzEaCwFOJayxhcYmeVZczOXickVibhzpo0kialt1KfVtC9WIrbSlnu7iaXRhd8icSdyq7k/640?wx_fmt=png&from=appmsg)

内容较多，我就不一一展开了，但可以看到，我是十分强调安全的。

  

有了这些沟通，更新了这一系列MD文件，OpenClaw才能知道我是谁，她是谁，她是什么样的人，以及如何更好的辅助我。

  

最后，和OpenClaw相处这么多天，我的一些经验是：

1. 把她当人看，而不是工具；

2. 不要手动修改任何文件，全部通过沟通完成（重要）；

3. 让她主动问我们问题（重要）；

4\. 不要指望从一开始她就按照我们的指令行事，OpenClaw需要耐心的调教，随着时间的推移，她才会越来越懂我们；

  

以上，装好OpenClaw后的第二件事，你做了吗？

  

希望大家有收获！

  

相关文章：

[装好OpenClaw，首件要干的是这件事！（5）](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651980712&idx=1&sn=3dee11313dd93a78aac4ab91aee98613&scene=21#wechat_redirect)

[我用OpenClaw，5分钟写出一个skill（3）](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651980646&idx=1&sn=6802aa2dee88a0ebfd5a6606c1cf3c92&scene=21#wechat_redirect)

[我用OpenClaw，5分钟写出一个程序（2）](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651980623&idx=1&sn=20fd90016f2b31cb32b7f4f69f98b2b5&scene=21#wechat_redirect)

  

OpenClaw一起学习，加我星球，来我直播：

下一讲，你想听什么？评论里告诉我！

OpenClaw100讲，欢迎围观！

[阅读原文](javascript:;)