## A simple interpreter

学习 programming language ，然后试图实现一个解释器。
我选择了语法比较简单的类似 scheme 语言的语法，这样我可以比较容易的产生 AST，从而将更多地精力放在后端的处理上。

最终这个语言会被加入各种特性，因为是为了学习研究而建立的 repo，所以不会考虑诸如加入某种特性是否合理之类的问题。

业余时间开发这个项目，有待完善。

使用语法如下：

```scheme
(+ 3 2)

(define test
    (lambda (x y)
        (* 2 x y)))

(test 5 6)
```

