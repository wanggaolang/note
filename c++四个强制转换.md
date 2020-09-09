# c++四个强制转换
 
**static_cast**

　　任何具有明确定义的类型转换，只要不包含``底层const``，都可以使用static_cast。例如，通过将一个运算对象强制转换成double类型就能表达式浮点数除法：

```c++
//进行强制类型转换以便执行浮点数处罚
double slope = static_cast<double>(j)/i;
```

　　当需要把一个较大的算术类型赋值给较小的类型时，static_cast非常有用。此时，强制类型转换告诉程序的读者和编译器：我们知道并且不在乎潜在的精度损失。一般来说，如果编译器发现一个较大的算术类型试图赋值给较小的类型，就会给出警告信息；但是当我们执行了显式的类型转换后，警告信息就会被关闭了。

　　static_cast对于编译器无法自动执行的类型转换也非常有用。例如我们可以使用static_cast找回存在于void*指针中的值：

```c++
void *p=&d;//正确：任何非常量对象的地址都能存入void*
//正确：将void*转换回初始的指针类型
double *dp=static_cast<double*>(p);
```

　　当我们把指针存放在void*中，并且使用static_cast将其强制转换回原来的类型时，应该确保指针转换后所得的类型就是指针所指的类型。类型一旦不符，将产生未定义的后果。



-----



**const_cast**

　　const_cast只能改变运算对象的``底层const``

```c++
const char *pc;
char *p=const_cast<char*>(pc);//正确：但通过p写值是未定义的后果
```

对于将常量对象转换成非常量对象的行为，我们一般称其为“去掉const性质”。一旦我们去掉了某个对象的const性质，编译器就不再阻止我们对该对象进行写操作了。如果对象本身不是一个常量，使用强制类型转换获得写权限是合法的行为。**然而如果对象是一个常量，在使用const_cast执行写操作就会产生未定义的后果**。

　　只有const_cast能改变表达式的常量属性，使用其他形式的命名强制类型转换改变表达式的常量都将引发编译器错误。同样的，也不能用const_cast改变表达式的类型：

```c++
const char *cp;
//错误：static_cast不能转换掉const性质
char *q=static_cast<char*>(cp);
static_cast<string>(cp);//正确：字符串字面值转换成string类型
const_cast<string>(cp);//错误：const_cast只改变常量属性
```

　　const_cast常常用于有函数重载的上下文中。

------



**reinterpret_cast**

　　reinterpret_cast通常为运算对象的位模式提供较低层次上的重新解释。举个例子，假设有如下的转换：

```c++
int *ip;
char *pc=reinterpret_cast<char*>(ip);
```

我们必须牢记pc所指的真实对象是一个int而非字符，如果把pc当成普通的字符指针使用就可能在运行时发生错误。例如：

```c++
string str(pc);
```

可能导致异常的运行时行为。

　　使用reinterpret_cast是非常危险的，用pc初始化str的例子很好地证明了这一点。其中的关键问题是类型改变了，但编译器没有给出任何警告或者错误的提示信息，当我们用一个int的地址初始化pc时，由于显式地声称这种转换合法，所以编译器不会犯傻呢个任何警告或者错误信息。接下来再使用pc时就会认定它的值是char*类型，编译器没法知道它实际存放的是指向int的指针。最终的结果就是，在上面的例子中虽然用pc初始化str没什么实际意义，甚至还可能引发更糟糕的后果，但仅从语法上而言这种操作无可指摘。查找这类问题的原因非常困难，如果将ip强制转换成pc的语法和用pc初始化string对象的语句分属不同文件就更是如此。

>注：reinterpret_cast本质上依赖于机器。要想安全地使用reinterpret_cast必须对涉及的类型和编译器实现转换的过程都非常了解。



---

**dynamic_cast**

```c++
dynamic_cast<type*>(e)
dynamic_cast<type&>(e)
dynamic_cast<type&&>(e)
```

　　type必须是一个类类型，在第一种形式中，type必须是一个有效的指针，在第二种形式中，type必须是一个左值，在第三种形式中，type必须是一个右值。在上面所有形式中，e的类型必须符合以下三个条件中的任何一个：e的类型是是目标类型type的公有派生类、e的类型是目标type的共有基类或者e的类型就是目标type的的类型。如果一条dynamic_cast语句的转换目标是指针类型并且失败了，则结果为0。如果转换目标是引用类型并且失败了，则dynamic_cast运算符将抛出一个std::bad_cast异常(该异常定义在typeinfo标准库头文件中)。e也可以是一个空指针，结果是所需类型的空指针。

dynamic_cast主要用于类层次间的上行转换和下行转换，还可以用于类之间的交叉转换（cross cast）。

在类层次间进行上行转换时，dynamic_cast和static_cast的效果是一样的；

> 在进行下行转换时，dynamic_cast具有类型检查的功能，比static_cast更安全。dynamic_cast是唯一无法由旧式语法执行的动作，也是唯一可能耗费重大运行成本的转型动作。



（1）指针类型

举例，Base为包含至少一个虚函数的基类，Derived是Base的共有派生类，如果有一个指向Base的指针bp，我们可以在运行时将它转换成指向Derived的指针，代码如下：

```c++
if(Derived *dp = dynamic_cast<Derived *>(bp)){
  //使用dp指向的Derived对象  
}
else{
  //使用bp指向的Base对象  
}
```

值得注意的是，在上述代码中，if语句中定义了dp，这样做的好处是可以在一个操作中同时完成类型转换和条件检查两项任务。



（2）引用类型

因为不存在所谓空引用，所以引用类型的dynamic_cast转换与指针类型不同，在引用转换失败时，会抛出std::bad_cast异常，该异常定义在头文件typeinfo中。

```c++
void f(const Base &b){
 try{
   const Derived &d = dynamic_cast<const Base &>(b);  
   //使用b引用的Derived对象
 }
 catch(std::bad_cast){
   //处理类型转换失败的情况
 }
}
```



**建议：避免强制类型转换**

　　强制类型转换干扰了正常的类型检查，因此我们强烈建议程序员避免使用强制类型转换。这个建议对于reinterpret_cast尤其适用，因为此类型转换总是充满了风险。在有重载函数的上下文中使用const_cast无可厚非；但是在其他情况下使用const_cast也就意味着程序存在某种设计缺陷。其他强制类型转换，比如static_cast和dynamic_cast，都不应该频繁使用。每次书写了一条强制类型转换语句，都应该反复斟酌能否以其他方式实现相同的目标。就算是在无法避免，也应该尽量限制类型类型转换值的作用于，并且记录对相关类型的所有假设，这样可以减少错误发生的机会。
