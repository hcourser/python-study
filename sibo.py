sinhx = (e^x - e^(-x)) /2
cosh x = (e^x + e^(-x)) /2
tanh x = sinh x/ cosh x = (e^x - e^(-x)) / (e^x + e^(-x))
coth x = cosh x/ sinh x = (e^x + e^(-x)) / (e^x - e^(-x))
sech x = 1/coshx
csc x = 1/sinhx
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BASE_COLORS as bc
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
e = np.e
color_ls = list(bc.keys())
hyperbDic = {
"sinh": lambda x: (e ** x - e **(-x))/2,
"cosh": lambda x: (e ** x + e **(-x)) /2,
"tanh": lambda x: (e ** x - e **(-x))/ (e ** x + e **(-x)),
"coth": lambda x: (e ** x + e **(-x))/ (e ** x - e **(-x)),
"sech": lambda x: 2/(e ** x + e ** (-x)),
"csch": lambda x: 2/(e ** x - e ** (-x)),
}
def hyperbolic(x, fun_name):
return hyperbDic[fun_name](x)
print(hyperbolic(2,"sinh"))
x = np.arange(-10,10, 0.5)
print(hyperbolic(x,'sinh'))
ls = ['sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch']
plt.figure()
for i in range(len(ls)) :
y = hyperbolic(x, ls[i])
plt.subplot(2,len(ls) // 2,i+1)
plt.plot(x, y, '-'+color_ls[i])
plt.title(ls[i])
plt.grid()
plt.suptitle("双曲函数")
plt.show()