

- [元组](#元组)
  - [拆包](#拆包)
    - [用法](#用法)
    - [场景](#场景)
  - [交换](#交换)
- [列表](#列表)
  - [移除元素](#移除元素)
  - [检查是否存在](#检查是否存在)
  - [连接和联合列表](#连接和联合列表)
- [字典](#字典)
  - [特性](#特性)
  - [字典构造生成](#字典构造生成)
  - [合并字典](#合并字典)
  - [默认值](#默认值)
- [集合](#集合)
  - [操作](#操作)
  - [构造](#构造)
- [生成器](#生成器)
  - [生成器表达式](#生成器表达式)
  - [itertools模块](#itertools模块)
- [列表、集合和字典的推导式](#列表集合和字典的推导式)
  - [基本推导式](#基本推导式)
  - [嵌套推导式](#嵌套推导式)
- [re模块](#re模块)
- [匿名函数(Lambda)](#匿名函数lambda)


# 元组
## 拆包
### 用法
```
tup = (3,4,(5,6))
```
1. 常规
```
a,b,c = tup
```
***注：左边的数量要与右边相等***

2. 技巧
```
a,b,*_ = tup
```
用[*_]指代之后所有的元素，避开了数量一致的要求，只关心需要的前几个


### 场景
1. 遍历元组或列表组成的序列
```
seq = [(1,2,3),(4,5,6),(7,8,9)]
for a,b,c in sql:
    print('a={0},b={1},c={2}'.format(a,b,c))
```
2. 从函数返回多个值
```
待续
```
## 交换
```
a,b = 1,2
a,b = b,a
```
# 列表
## 移除元素
1. pop
```
list.pop(position)
```
***移除position位置的元素***

2. remove
```
list.remove(element)
```
***移除第一个等于element的元素***

**想想看，各自起到什么效果？**
## 检查是否存在
```
'dwarf' in a_list
'dwarf' not in a_list
```
***与字典、集合相比，用in/not in检查列表是非常缓慢的。这是因为python对列表进行了线性逐个扫描，而在字典和集合中是基于哈希表同时检查***
## 连接和联合列表
```
1. [1,2,3]+[4,5,6]
2. x=[1,2,3]
   x.extend([4,5,6])
```
***通过+号连接是一种高代价操作，因为有了创建和复制动作。而extend将元素直接添加，所以extend实现速度更快***

# 字典
## 特性
1. 键可以是任何不可变（immutable）数据类型（不可变数据类型：数字，字符串、元组）（也就是说key不能为列表和字典类型）
   可以通过hash()函数对一个键进行检查是否可以哈希化来确定它是否可以作为Key.
2. 字典的Key不可重复
3. 字典中每一项的顺序是任意的
## 字典构造生成
用两个序列来构造一个字典

我们可能会这样写
```
mapping = {}
for key,value in zip(key_list,value_list):
    mapping[key]=value
```

但实际上这样写更好
```
mapping = dict(zip(key_list,value_list))
```
## 合并字典
```
dl = {'a':1,'b':2}
dl.update({'c',5})
```

## 默认值
先看一段代码：
```
words = ['apple','bat','bar','atom','book']
by_letter = {}
for word in words:
    letter = word[0]
    if letter not in by_letter:
        by_letter[letter] = [word]
    else:
        by_letter[letter].append(word)
```
输出
```
by_letter
{'a': ['apple', 'atom'], 'b': ['bat', 'bar', 'book']}
```
这段代码是对words进行依据首字母分类，而python中的setdefault方法可以简化创建新字典时找不到还未分析的首字母为KEY的处理：
```
for word in words:
    by_letter.setdefault(word[0],[]).append(word)
```
一把搞定，setdefault(key,default)函数会去分析key是否存在，如果不存在，则创建一个{key,default}键值对，并返回那个default键值指针。如果存在，直接返回找到的值指针。

***然鹅***

有更好的
```
from collections import defaultdict
by_letter2=defaultdict(list)
for word in words:
    by_letter2[word[0]].append(word)
```
输出
```
by_letter2
defaultdict(list, {'a': ['apple', 'atom'], 'b': ['bat', 'bar', 'book']})
```

# 集合
集合是一种无序且***元素唯一***的容器。
看上去也很像一个只有***Key***没有值的字典。
所以集合的元素必须是不可变的。
## 操作
|函数|替代方法|描述|
|----|----|----|
|a.add(x)|N/A|将元素x加入集合a|
|a.clear()|N/A|将集合重置为空，清空所有元素|
|a.remove(x)|N/A|从集合a移除某个指定元素，如果不存在，抛出KeyError异常|
|a.pop()|N/A|***随机***移除任意一个元素，如果集合是空的抛出KeyError异常|
|-|-|-|
|a.unicon(b)|a\|b|并集。a和b的所有***不同***元素|
|a.update(b)|a\|=b|将a的内容设置为a和b的并集|
|a.intersection(b)|a&b|交集。a、b中同时包含的元素|
|a.intersection_update(b)|a&=b|将a的内容设置为a和b的交集|
|a.difference(b)|a-b|在a不在b的元素|
|a.difference_update(b)|a-=b|将a的内容设置为在a不在b的元素|
|a.symmetric_difference(b)|a^b|所有在a或b中，但不是同时在a和b中的元素|
|a.symmetric_difference_update(b)|a^=b|将a的内容设置为如上|
|a.issubset(b)|N/A|如果a包含于b，返回True|
|a.isdisjoint(b)|N/A|a，b没有交集则返回True|
## 构造
```
my_data=[1,2,3,3,4]
my_set=set(my_date)

输出：
my_set
{1,2,3,4}
```
# 生成器
普通函数执行并一次性返回完整结果，而**生成器**则***惰性***地返回一个多结果序列，***在每一个元素产生之后暂停，直到下一个请求。***

如需创建一个生成器，只需要在函数中将返回关键字***return***替换为***yield***关键字：
```
def squares(n=10):
    print('Generating squares from 1 to {0}'.format(n**2))
    for i in range(1,n+1):
        yield i**2
```
当你实际调用生成器时，代码并不会立即执行：
```
gen=squares()
gen
<generator object squares at 0x89798797>
```
直到你请求生成器中的元素时，它才会执行它的代码：
```
for x in gen:
    print(x)


```
## 生成器表达式
生成器表达式和列表推导式很类似，只需要将推导式的方括号替换为小括号就可以了：
```
gen=(x**2 for x in range(10))
```
这个代码与上面那个使用squares函数的gen是等价的！
## itertools模块
标准库里有个生成器集合，很有用。



# 列表、集合和字典的推导式
它允许过滤一个容器的元素，用一种简明的表达式转换传递给过滤器的元素，从而生成一个新的列表。

## 基本推导式
1. 列表推导式
```
[expr for val in collection if condition]
```
等价于下面
```
result=[]
for val in collection:
    if condiction:
        result.append(expr)
```
2. 集合推导式
只是方括号变成了大括号而已
```
{expr for val in collection if condition}
```
3. 字典推导式
字典的expr需要一对Key:Value
```
{key-expr:value-expr for value in collection if condition}
```
## 嵌套推导式
有如下形式的嵌套推导式：
```
some_tuples = [(1,2,3),(4,5,6),(7,8,9)]
flattened = [x for tup in some_tuples for x in tup if x>2]

输出：
flattened
[3, 4, 5, 6, 7, 8, 9]
```
其实，它的原本形式是：
```
flattened = []
for tup in some_tuples:
    for x in tup:
        if x>2:
            flattened.append(x)
```
注意它的对应关系！

还有一个头晕的嵌套列表推导式：
```
some_tuples = [(1,2,3),(4,5,6),(7,8,9)]
[[x for x in tup] for tup in some_tuples]

输出：
[[1,2,3],[4,5,6],[7,8,9]]
```
# re模块
re模块是python独有的匹配字符串的模块，该模块中提供的很多功能是基于正则表达式实现的，而正则表达式是对字符串进行模糊匹配，提取自己需要的字符串部分，他对所有的语言都通用。注意：

1. re模块是python独有的
2. 正则表达式所有编程语言都可以使用
3. re模块、正则表达式是对字符串进行操作

因为，re模块中的方法大都借助于正则表达式，故必须先学习正则表达式。

# 匿名函数(Lambda)
tips:Lambda表达式基于数学中的λ演算得名。

匿名函数是一种通过***单个语句***生成函数的方式，其结果是返回值。

匿名函数使用**lambda**关键字定义，该关键字仅表达**“我们声明一个匿名函数”**的意思：
```
def short_function(x):
    return x*2

等价：

equiv_anon=lambda x:x*2
```
