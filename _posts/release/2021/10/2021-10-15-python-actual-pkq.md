---
layout: post
category: python
title: 
tagline: by 潮汐
tags:用 Python 给小表弟画皮卡丘！
  - Python技巧
  - 编程
---

今天是周六，祝大家周末愉快，昨天晚上小表弟来家里玩，给他看了皮卡丘动画片，突发奇想给他用 Python 画一个皮卡丘，也让他提前感受 Python 技术的强大与好玩之处，于是就有了今天的文章。


### Python 画皮卡丘1

```python
import turtle as t

def face(x, y):
    """画脸"""
    t.begin_fill()
    t.penup()
    # 将海龟移动到指定的坐标
    t.goto(x, y)
    t.pendown()
    # 设置海龟的方向
    t.setheading(40)

    t.circle(-150, 69)
    t.fillcolor("#FBD624")
    # 将海龟移动到指定的坐标

    t.penup()
    t.goto(53.14, 113.29)
    t.pendown()

    t.setheading(300)
    t.circle(-150, 30)
    t.setheading(295)
    t.circle(-140, 20)
    print(t.position())
    t.forward(5)
    t.setheading(260)
    t.circle(-80, 70)
    print(t.position())
    t.penup()
    t.goto(-74.43, -79.09)
    t.pendown()

    t.penup()
    # 将海龟移动到指定的坐标
    t.goto(-144, 103)
    t.pendown()
    t.setheading(242)
    t.circle(110, 35)
    t.right(10)
    t.forward(10)
    t.setheading(250)
    t.circle(80, 115)
    print(t.position())

    t.penup()
    t.goto(-74.43, -79.09)
    t.pendown()
    t.setheading(10)
    t.penup()
    t.goto(-144, 103)

    t.pendown()
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.end_fill()

    # 下巴
    t.penup()
    t.goto(-50, -82.09)
    t.pendown()
    t.pencolor("#DDA120")
    t.fillcolor("#DDA120")
    t.begin_fill()
    t.setheading(-12)
    t.circle(120, 25)
    t.setheading(-145)
    t.forward(30)
    t.setheading(180)
    t.circle(-20, 20)
    t.setheading(143)
    t.forward(30)
    t.end_fill()
    # penup()
    # # 将海龟移动到指定的坐标
    # goto(0, 0)
    # pendown()


def eye():
    """画眼睛"""
    # 左眼
    t.color("black", "black")
    t.penup()
    t.goto(-110, 27)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(24)
    t.end_fill()
    # 左眼仁
    t.color("white", "white")
    t.penup()
    t.goto(-105, 51)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(10)
    t.end_fill()
    # 右眼
    t.color("black", "black")
    t.penup()
    t.goto(25, 40)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(24)
    t.end_fill()
    # 右眼仁
    t.color("white", "white")
    t.penup()
    t.goto(17, 62)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(10)
    t.end_fill()


def cheek():
    """画脸颊"""
    # 右边
    t.color("#9E4406", "#FE2C21")
    t.penup()
    t.goto(-130, -50)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(27)
    t.end_fill()

    # 左边
    t.color("#9E4406", "#FE2C21")
    t.penup()
    t.goto(53, -20)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(27)
    t.end_fill()


def nose():
    """画鼻子"""
    t.color("black", "black")
    t.penup()
    t.goto(-40, 38)
    t.pendown()
    t.begin_fill()
    t.circle(7, steps=3)
    t.end_fill()


def mouth():
    """画嘴"""
    t.color("black", "#F35590")
    # 嘴唇
    t.penup()
    t.goto(-10, 22)
    t.pendown()
    t.begin_fill()
    t.setheading(260)
    t.forward(60)
    t.circle(-11, 150)
    t.forward(55)
    print(t.position())
    t.penup()
    t.goto(-38.46, 21.97)
    t.pendown()
    t.end_fill()

    # 舌头
    t.color("#6A070D", "#6A070D")
    t.begin_fill()
    t.penup()
    t.goto(-10.00, 22.00)
    t.pendown()
    t.penup()
    t.goto(-14.29, -1.7)
    t.pendown()
    t.penup()
    t.goto(-52, -5)
    t.pendown()
    t.penup()
    t.goto(-60.40, 12.74)
    t.pendown()
    t.penup()
    t.goto(-38.46, 21.97)
    t.pendown()
    t.penup()
    t.goto(-10.00, 22.00)
    t.pendown()

    t.end_fill()

    t.color("black", "#FFD624")

    t.penup()
    t.goto(-78, 15)
    t.pendown()
    t.begin_fill()
    t.setheading(-25)
    for i in range(2):
        t.setheading(-25)
        t.circle(35, 70)

    t.end_fill()
    t.color("#AB1945", "#AB1945")
    t.penup()
    t.goto(-52, -5)
    t.pendown()
    t.begin_fill()
    t.setheading(40)
    t.circle(-33, 70)
    t.goto(-16, -1.7)
    t.penup()
    t.goto(-18, -17)
    t.pendown()
    t.setheading(155)
    t.circle(25, 70)
    t.end_fill()


def ear():
    """画耳朵"""
    # 左耳
    t.color("black", "#FFD624")
    t.penup()
    t.goto(-145, 93)
    t.pendown()
    t.begin_fill()
    t.setheading(165)
    t.circle(-248, 50)
    t.right(120)
    t.circle(-248, 50)
    t.end_fill()
    t.color("black", "black")
    t.penup()
    t.goto(-240, 143)
    t.pendown()
    t.begin_fill()
    t.setheading(107)
    t.circle(-170, 25)
    t.left(80)
    t.circle(229, 15)
    t.left(120)
    t.circle(300, 15)
    t.end_fill()

    # 右耳
    t.color("black", "#FFD624")
    t.penup()
    t.goto(30, 136)
    t.pendown()
    t.begin_fill()
    t.setheading(64)
    t.circle(-248, 50)

    t.right(120)
    t.circle(-248, 50)
    t.end_fill()
    t.color("black", "black")
    t.penup()
    t.goto(160, 200)
    t.pendown()
    t.begin_fill()
    t.setheading(52)
    t.circle(170, 25)
    t.left(116)
    t.circle(229, 15)
    t.left(71)
    t.circle(-300, 15)
    t.end_fill()

def setting():
  """设置参数"""
  t.pensize(2)
   # 隐藏海龟
  t.hideturtle()
  t.speed(10)


def main():
    """主函数"""
    setting()
    face(-132, 115)
    eye()
    cheek()
    nose()
    mouth()
    ear()
    t.done()


if __name__ == '__main__':
    main()

```

输出效果如下：
![](https://files.mdnice.com/user/6478/c73211ca-035d-40ba-b842-303f63af7b6c.png)


### Python 画皮卡丘2

```python
import turtle

def getPosition(x,y):
    turtle.setx(x)
    turtle.sety(y)
    print(x,y)

class Pikachu:
    def __init__(self):
         self.t = turtle.Turtle()
         t = self.t
         t.pensize(3) # 画笔大小
         t.speed(9) #画笔速度
         t.ondrag(getPosition)

    def onTrace_goto(self,x,y):
        self.t.penup()
        self.t.goto(x,y)
        self.t.pendown()

    def leftEye(self,x,y):
        self.onTrace_goto(x,y)
        t = self.t
        t.seth(0)
        t.fillcolor('#333333')
        t.begin_fill()
        t.circle(22)
        t.end_fill()

        self.onTrace_goto(x,y+10)
        t.fillcolor('#000000')
        t.begin_fill()
        t.circle(10)
        t.end_fill()

        self.onTrace_goto(x+6,y+22)
        t.fillcolor('#ffffff')
        t.begin_fill()
        t.circle(10)
        t.end_fill()

    def rightEye(self,x,y):
        self.onTrace_goto(x,y)
        t = self.t
        t.seth(0)
        t.fillcolor('#333333')
        t.begin_fill()
        t.circle(22)
        t.end_fill()

        self.onTrace_goto(x,y+10)
        t.fillcolor('#000000')
        t.begin_fill()
        t.circle(10)
        t.end_fill()

        self.onTrace_goto(x-6,y+22)
        t.fillcolor('#ffffff')
        t.begin_fill()
        t.circle(10)
        t.end_fill()


    def mouth(self,x,y):
        self.onTrace_goto(x,y)
        t = self.t
        t.fillcolor('#88141D')
        t.begin_fill()
        # 下嘴唇
        l1 = []
        l2 = []
        t.seth(190)
        a = 0.7
        for i in range(28):
            a +=0.1
            t.right(3)
            t.fd(a)
            l1.append(t.position())

        self.onTrace_goto(x,y)
        t.seth(10)
        a = 0.7
        for i in range(28):
            a +=0.1
            t.left(3)
            t.fd(a)
            l2.append(t.position())

        #上嘴唇

        t.seth(10)
        t.circle(50,15)
        t.left(180)
        t.circle(-50,15)

        t.circle(-50,40)
        t.seth(233)
        t.circle(-50,55)
        t.left(180)
        t.circle(50,12.1)
        t.end_fill()


        # 舌头
        self.onTrace_goto(17,54)
        t.fillcolor('#DD716F')
        t.begin_fill()
        t.seth(145)
        t.circle(40,86)
        t.penup()
        for pos in reversed(l1[:20]):
            t.goto(pos[0],pos[1]+1.5)
        for pos in l2[:20]:
            t.goto(pos[0],pos[1]+1.5)
        t.pendown()
        t.end_fill()

        # 鼻子
        self.onTrace_goto(-17,94)
        t.seth(8)
        t.fd(4)
        t.back(8)


    # 红脸颊

    def leftCheck(self,x,y):
        turtle.tracer(False)
        t = self.t
        self.onTrace_goto(x,y)
        t.seth(60)
        t.fillcolor('#DD4D28')
        t.begin_fill()
        a = 2.3
        for i in range(120):
            if 0 <= i <30 or 60 <= i <90:
                a -= 0.05
                t.lt(3)
                t.fd(a)
            else:
                a += 0.05
                t.lt(3)
                t.fd(a)
        t.end_fill()
        turtle.tracer(True)

    def rightCheck(self,x,y):
        t = self.t
        turtle.tracer(False)
        self.onTrace_goto(x,y)
        t.seth(60)
        t.fillcolor('#DD4D28')
        t.begin_fill()
        a = 2.3
        for i in range(120):
            if 0<= i<30 or 60 <= i< 90:
                a -= 0.05
                t.lt(3)
                t.fd(a)
            else:
                a += 0.05
                t.lt(3)
                t.fd(a)

        t.end_fill()
        turtle.tracer(True)




    def colorLeftEar(self,x,y):
        t = self.t
        self.onTrace_goto(x,y)
        t.fillcolor('#000000')
        t.begin_fill()
        t.seth(330)
        t.circle(100,35)
        t.seth(219)
        t.circle(-300,19)
        t.seth(110)
        t.circle(-30,50)
        t.circle(-300,10)
        t.end_fill()

    def colorRightEar(self,x,y):
        t = self.t
        self.onTrace_goto(x,y)
        t.fillcolor('#000000')
        t.begin_fill()
        t.seth(300)
        t.circle(-100,30)
        t.seth(35)
        t.circle(300,15)
        t.circle(30,50)
        t.seth(190)
        t.circle(300,17)
        t.end_fill()

    def body(self):

        t = self.t
        t.fillcolor('#F6D02F')
        # 右脸轮廓
        t.penup()
        t.circle(130,40)
        t.pendown()
        t.circle(100,105)
        t.left(180)
        t.circle(-100,5)

        # 右耳朵
        t.seth(20)
        t.circle(300,30)
        t.circle(30,50)
        t.seth(190)
        t.circle(300,36)

        # 上轮廓
        t.seth(150)
        t.circle(150,70)


        #左耳朵
        t.seth(200)
        t.circle(300,40)
        t.circle(30,50)
        t.seth(20)
        t.circle(300,35)

        # 左脸轮廓
        t.seth(240)
        t.circle(105,95)
        t.left(180)
        t.circle(-105,5)

        #左手
        t.seth(210)
        t.circle(500,18)
        t.seth(200)
        t.fd(10)
        t.seth(280)
        t.fd(7)
        t.seth(210)
        t.seth(300)
        t.circle(10,80)
        t.seth(220)
        t.seth(10)
        t.seth(300)
        t.circle(10,80)
        t.seth(240)
        t.fd(12)
        t.seth(0)
        t.fd(13)
        t.seth(240)
        t.circle(10,70)
        t.seth(10)
        t.circle(10,70)
        t.seth(10)
        t.circle(300,18)


        t.seth(75)
        t.circle(500,8)
        t.left(180)
        t.circle(-500,15)
        t.seth(250)
        t.circle(100,65)

        # 左脚
        t.seth(320)
        t.circle(100,5)
        t.left(180)
        t.circle(-100,5)
        t.seth(220)
        t.circle(200,20)
        t.circle(20,70)

        t.seth(60)
        t.circle(-100,20)
        t.left(180)
        t.circle(100,20)
        t.seth(300)
        t.circle(10,70)

        t.seth(60)
        t.circle(-100,20)
        t.left(180)
        t.circle(100,20)
        t.seth(10)
        t.circle(100,60)

        # 横向
        t.seth(180)
        t.circle(-100,10)
        t.left(180)
        t.circle(100,10)
        t.seth(5)
        t.circle(100,10)
        t.circle(-100,40)
        t.circle(100,35)
        t.left(180)
        t.circle(-100,10)

        # 右脚
        t.seth(290)
        t.circle(100,55)
        t.circle(10,50)

        t.seth(120)
        t.circle(100,20)
        t.left(180)
        t.circle(-100,20)

        t.seth(0)
        t.circle(10,50)

        t.seth(110)
        t.circle(110,20)
        t.left(180)
        t.circle(-100,20)

        t.seth(30)
        t.circle(20,50)

        t.seth(100)
        t.circle(100,40)

        # 右侧身体轮廓
        t.seth(200)
        t.circle(-100,5)
        t.left(180)
        t.circle(100,5)
        t.left(30)
        t.circle(100,75)
        t.right(15)
        t.circle(-300,21)
        t.left(180)
        t.circle(300,3)

        # 右手
        t.seth(43)
        t.circle(200,60)

        t.right(10)
        t.fd(10)

        t.circle(5,160)
        t.seth(90)
        t.circle(5,160)
        t.seth(90)

        t.fd(10)
        t.seth(90)
        t.circle(5,180)
        t.fd(10)

        t.left(180)
        t.left(20)
        t.fd(10)
        t.circle(5,170)
        t.fd(10)
        t.seth(240)
        t.circle(50,30)

        t.end_fill()
        self.onTrace_goto(130,125)
        t.seth(-20)
        t.fd(5)
        t.circle(-5,160)
        t.fd(5)


        # 手指纹
        self.onTrace_goto(166,130)
        t.seth(-90)
        t.fd(3)
        t.circle(-4,180)
        t.fd(3)
        t.seth(-90)
        t.fd(3)
        t.circle(-4,180)
        t.fd(3)

        # 尾巴
        self.onTrace_goto(168,134)
        t.fillcolor('#F6D02F')
        t.begin_fill()
        t.seth(40)
        t.fd(200)
        t.seth(-80)
        t.fd(150)
        t.seth(210)
        t.fd(150)
        t.left(90)
        t.fd(100)
        t.right(95)
        t.fd(100)
        t.left(110)
        t.fd(70)
        t.right(110)
        t.fd(80)
        t.left(110)
        t.fd(30)
        t.right(110)
        t.fd(32)


        t.right(106)
        t.circle(100,25)
        t.right(15)
        t.circle(-300,2)

        t.seth(30)
        t.fd(40)
        t.left(100)
        t.fd(70)
        t.right(100)
        t.fd(80)
        t.left(100)
        t.fd(46)
        t.seth(66)
        t.circle(200,38)
        t.right(10)
        t.end_fill()


        # 尾巴花纹
        t.fillcolor('#923E24')
        self.onTrace_goto(126.82,-156.84)
        t.begin_fill()
        t.seth(30)
        t.fd(40)
        t.left(100)
        t.fd(40)
        t.pencolor('#923e24')
        t.seth(-30)
        t.fd(30)
        t.left(140)
        t.fd(20)
        t.left(150)
        t.fd(20)
        t.right(150)
        t.fd(20)
        t.left(130)
        t.fd(18)
        t.pencolor('#000000')
        t.seth(-45)
        t.fd(67)
        t.right(110)
        t.fd(30)
        t.left(110)
        t.fd(32)
        t.right(106)
        t.circle(100,25)
        t.right(15)
        t.circle(-300,2)
        t.end_fill()



        # 帽子、眼睛、嘴巴、脸颊
        self.cap(-134.07,147.81)
        self.mouth(-5,25)
        self.leftCheck(-126,32)
        self.rightCheck(107,63)
        self.colorLeftEar(-250,100)
        self.colorRightEar(150,270)
        self.leftEye(-85,90)
        self.rightEye(50,110)
        t.hideturtle()

    def cap(self,x,y):
        self.onTrace_goto(x,y)
        t = self.t
        t.fillcolor('#CD0000')
        t.begin_fill()
        t.seth(200)
        t.circle(400,7)
        t.left(180)
        t.circle(-400,30)
        t.circle(30,60)
        t.fd(60)
        t.circle(30,45)
        t.fd(60)
        t.left(5)
        t.circle(30,70)
        t.right(20)
        t.circle(200,70)
        t.circle(30,60)
        t.fd(70)
        t.right(35)
        t.fd(50)
        t.right(35)
        t.fd(50)
        t.circle(8,100)
        t.end_fill()
        self.onTrace_goto(-168.47,185.52)
        t.seth(36)
        t.circle(-270,54)
        t.left(180)
        t.circle(270,27)
        t.circle(-80,98)

        t.fillcolor('#444444')
        t.begin_fill()
        t.left(180)
        t.circle(80,197)
        t.left(58)
        t.circle(200,45)
        t.end_fill()

        self.onTrace_goto(-58,270)
        t.pencolor('#228B22')
        t.dot(35)

        self.onTrace_goto(-30,280)
        t.fillcolor('#228B22')
        t.begin_fill()
        t.seth(100)
        t.circle(30,180)
        t.seth(190)
        t.fd(15)
        t.seth(100)
        t.circle(-45,180)
        t.right(90)
        t.fd(15)
        t.end_fill()
        t.fillcolor('#228B22')


    def start(self):
        self.body()

def main():
    print(" Painting the Pikachu....")
    turtle.screensize(800,600)
    turtle.title("Pickachu")
    pickachu = Pikachu()
    pickachu.start()

    turtle.mainloop() # running


if __name__ =='__main__':
    main()
```
输出效果如下：
![](https://files.mdnice.com/user/6478/52f7de3b-9b28-4f2e-aaad-5f1e2505462e.png)

### 总结
希望小表弟以后能成为一个优秀的新生代农民工，愿他健康茁壮成长。大家感兴趣的可以一试。

### 参考

[https://www.cnblogs.com/zeroing0/p/13703631.html](https://www.cnblogs.com/zeroing0/p/13703631.html)
[https://www.jb51.net/article/174748.htm](https://www.jb51.net/article/174748.htm)


