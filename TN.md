##  git添加/删除远程仓库及github相关：

``` shell
git remote rm origin
git remote add orinin https://github.com/wanggaolang/Blog

echo "# note" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wanggaolang/note.git
git push -u origin master
---

当github与本地master不一致（如github上多了个readme）时，
若让本地与远程相同：git pull
若让远程与本地相同：git push -f


```



一、pull操作
1、将远程指定分支 拉取到 本地指定分支上：

git pull origin <远程分支名>:<本地分支名>
1
2、将远程指定分支 拉取到 本地当前分支上：

git pull origin <远程分支名>
1
3、将与本地当前分支同名的远程分支 拉取到 本地当前分支上(需先关联远程分支，方法见文章末尾)

git pull
1
在克隆远程项目的时候，本地分支会自动与远程仓库建立追踪关系，可以使用默认的origin来替代远程仓库名，
所以，我常用的命令就是 git pull origin <远程仓库名>，操作简单，安全可控。

二、push操作
1、将本地当前分支 推送到 远程指定分支上（注意：pull是远程在前本地在后，push相反）：

git push origin <本地分支名>:<远程分支名>
1
2、将本地当前分支 推送到 与本地当前分支同名的远程分支上（注意：pull是远程在前本地在后，push相反）：

git push origin <本地分支名>
1
3、将本地当前分支 推送到 与本地当前分支同名的远程分支上(需先关联远程分支，方法见文章末尾)

git push
1
同样的，推荐使用第2种方式，git push origin <远程同名分支名>

附：
// 将本地分支与远程同名分支相关联

git push --set-upstream origin <本地分支名>

简写方式：git push -u origin <本地分支名>
``cat .git/config``能看到本地与远程分支的关联关系





## 内存操作的小技巧 

*(int *)ptr的意思是从ptr这个地址开始向上（因为是小端存储）取四个字节出来看成int，注意编译器优化会使两个相邻变量上下字节间发生变化，可以加上```volatile```。大部分机器都是小端存储，变量的首地址是最低的一个字节的地址，取变量时向上取，存储时向低地址存（因为是栈）。



## sqrt是开平方，pow(x,n)是N次方



## 重载<<运算符示例

 ```c++
   ostream & operator<<( ostream & os,const Vector2D & c) //二维向量
   {
       os << "x: "<<c.x <<" y: "<<c.y;
       return os;
   }
 ```



## new和malloc的区别

   1. new可以自动计算所需要大小；malloc则必须要由我们计算字节数。

   2. new操作符内存分配成功时，返回的是对象类型的指针；malloc内存分配成功则是返回void * ，需要通过强制类型转换将void*指针转换成我们需要的类型。

   3. new内存分配失败时，会抛出bac_alloc异常；malloc分配内存失败时返回NULL。

   4. malloc与free是C++/C语言的标准库函数，new/delete是C++的运算符。

   5. 使用new操作符来分配对象内存时会经历三个步骤：

      - 第一步：调用operator new 函数（对于数组是operator new[]）分配一块足够大的，原始的，未命名的内存空间以便存储特定类型的对象。
      - 第二步：编译器运行相应的构造函数以构造对象，并为其传入初值。
      - 第三部：对象构造完成后，返回一个指向该对象的指针。

      使用delete操作符来释放对象内存时会经历两个步骤：

      - 第一步：调用对象的析构函数。
      - 第二步：编译器调用operator delete(或operator delete[])函数释放内存空间。

      总之来说，new/delete会调用对象的构造函数/析构函数以完成对象的构造/析构；而malloc 只管分配内存，并不能对所得的内存进行初始化

      6.使用malloc分配的内存后，如果在使用过程中发现内存不足，可以使用realloc函数进行内存重新分配实现内存的扩充。

      ```c
      void *realloc(void *ptr, size_t size)
          realloc先判断当前的指针所指内存是否有足够的连续空间，如果有，原地扩大可分配的内存地址，并且返回原来的地址指针；如果空间不够，先按照新指定的大小分配空间，将原有数据从头到尾拷贝到新分配的内存区域，而后释放原来的内存区域。
          --ptr   指针指向一个要重新分配内存的内存块，该内存块之前是通过调用 malloc、calloc 或 realloc 进行分配内存的。如果为空指针，则会分配一个新的内存块，且函数返回一个指向它的指针。
      	--size  内存块的新的大小，以字节为单位。如果大小为 0，且 ptr 指向一个已存在的内存块，则 ptr 所指向的内存块会被释放，并返回一个空指针。
      	void *calloc(size_t nitems, size_t size)
          也是申请内存，nitems为元素个数，size为元素大小。与malloc的区别是这个会初始化为0。
      ```



##6. 常见c语言函数

```c
	void *memcpy(void *dest, const void *src, size_t n)
从 src 复制 n 个字符到 dest，不会先清空dest。
	void *memset(void *str, int c, size_t n)
复制字符 c（一个无符号字符）到参数 str 所指向的字符串的前 n 个字符。
	char *strcat(char *dest, const char *src)
把 src 所指向的字符串追加到 dest 所指向的字符串的结尾。
	char *strcpy(char *dest, const char *src)
把 src 所指向的字符串复制到 dest，会先清空dest。
	
	取绝对值：abs(obj)
    a的b次方：pow(a, b)
```



## 红黑树和AVL树

红黑树不追求"完全平衡"，即不像AVL那样要求节点的 `|balFact| <= 1`，它只要求部分达到平衡，但是提出了为节点增加颜色，红黑是用非严格的平衡来换取增删节点时候旋转次数的降低，任何不平衡都会在三次旋转之内解决，而AVL是严格平衡树，因此在增加或者删除节点的时候，根据不同情况，旋转的次数比红黑树要多。

就插入节点导致树失衡的情况，RB-Tree最多两次树旋转来实现复衡rebalance，旋转的量级是O(1)
 ，而AVL的插入和删除节点导致失衡，AVL需要维护从被删除/插入节点到根节点root这条路径上所有节点的平衡，旋转的量级为O(logN)，而RB-Tree最多只需要旋转3次实现复衡，只需O(1)，所以说RB-Tree删除节点的rebalance的效率更高，开销更小！在查找时候AVL更快，但快的有限。



## 同步异步套接字



使用套接字进行数据处理有两种基本模式：同步和异步。　　

**同步模式**：同步模式的特点是在通过Socket进行连接、接收、发送数据时，客户机和服务器在接收到对方响应前会出于阻塞状态，即一直等到收到对方请求进才继续执行下面的语句。可见，同步模式只适用于数据处理不太多的场合。当程序执行的任务很多时，长时间的等待可能会让用户无法忍受。
　　

**异步模式**：异步模式的特点是在通过Socket进行连接、接收、发送操作时，客户机或服务器不会处于阻塞方式，而是利用callback机制进行连接、接收、发送处理，这样就可以在调用发送或接收的方法后直接返回，并继续执行下面的程序。可见，异步套接字特别适用于进行大量数据处理的场合。
　　

使用同步套接字进行编程比较简单，而异步套接字编程则比较复杂



##  GMP库

用于大数运算的c/c++库，在linux下完美支持，windows需要用mingw和msys进行编译，或者用gmp的windows版本mpir，原生支持vs上编译



## clion快捷键设置

Setting	--	Keymap

光标到上一个光标：搜索back 

光标到下一个光标：搜索forward	

## vscode

**快捷键**

查找文件名：command + p

在打开的文件夹中查找一个函数：左侧那个放大镜

回到上一个光标：command + -



**三个配置文件**

//TODO



编译：mac快捷键 command + shift + b





## 进程，线程，协程

进程：计算机程序运行的实体。每个进程都有自己的独立内存空间，上下文切换开销比较大（栈，寄存器，虚拟内存，文件句柄等），相对稳定安全

线程：进程的一个实体，是cpu调度和分派的基本单位。线程只拥有一点在运行中必不可少的资源(如程序计数器,一组寄存器和栈),但是它可与同属一个进程的其他的线程共享进程所拥有的全部资源。线程间通信主要通过共享内存，上下文切换很快，资源开销较少，但相比进程不够稳定容易丢失数据。

协程：



## volatile

volatile关键词影响编译器编译的结果，用volatile声明的变量表示该变量随时可能发生变化，与该变量有关的运算，不再编译优化，以免出错。



## 小知识（一）

1. **ptr--**  会先减再运行
2. 类外定义成员函数不能加上默认参数，如：``Test fun(int a = 1)``会报错，同样static声明的成员在外部定义时候，必须省去static。同时，static成员变量只有跟了const才可以在类里面的初始化列表中进行初始化，其余的都要在类的外部初始化。
3. string.find()和map.find()以及set.find()如果找不到目标，则结果为x.end()



## c++ string的实习

```c++
#include <cstddef>
#include <iosfwd>
#include <iostream>
#include <string.h>
using namespace std;
class String {
private:
    /* data */
    char *data;    //字符串
    size_t length; //长度

public:
    String(const char *str = nullptr); //默认构造函数
    String(const String &str);         //拷贝构造函数
    friend istream &operator>>(istream &is, String &str);
    friend ostream &operator<<(ostream &os, String &str);

    String operator+(const String &str) const; //重载+
    String &operator=(const String &str);      //重载=
    String &operator+=(const String &str);     //重载+=
    bool operator==(const String &str) const;  //重载==
    char &operator[](int n) const;             //重载[]

    size_t size() const;       //获取长度
    const char *c_str() const; //获取C字符串

    ~String();
};

String::String(const char *str) { //通用构造函数
    if (!str) {
        length = 0;
        data = new char[1];
        *data = '\0';
    } else {
        length = strlen(str);
        data = new char[length + 1];
        strcpy(data, str);
    }
}
String::String(const String &str) { //拷贝构造函数
    length = str.size();
    data = new char[length + 1];
    const char *temp = str.c_str();
    strcpy(data, temp);
}

String::~String() {
    delete[] data;
    length = 0;
}

String String::operator+(const String &str) const //重载+
{
    String newString;
    newString.length = length + str.size();
    newString.data = new char[newString.length + 1];
    strcpy(newString.data, data);
    strcat(newString.data, str.data);
    return newString;
}

String &String::operator=(const String &str) //重载+
{
    if (this == &str) {
        return *this;
    }
    delete[] data;
    length = str.size();
    data = new char[length];
    strcpy(data, str.c_str());
    return *this;
}

String &String::operator+=(const String &str) //重载+
{
    length += str.size();
    char *newData = new char[length + 1];
    strcpy(newData, data);
    strcat(newData, str.c_str());
    delete[] data;
    data = newData;
    return *this;
}
inline bool String::operator==(const String &str) const //重载==
{
    if (length != str.size())
        return false;
    return strcmp(data, str.data) ? false : true;
}

inline char &String::operator[](int n) const //重载[]
{
    if (n >= length) {
        return data[length - 1]; //错误处理
    }
    return data[n];
}

inline size_t String::size() const //获取长度
{
    return length;
}
inline auto String::c_str( ) const ->const char * //获取C字符串
{
    return data;
}

istream &operator>>(istream &is, String &str) //输入
{
    char tem[1000]; //简单的申请一块内存
    is >> tem;
    str.length = strlen(tem);
    str.data = new char[str.length + 1];
    strcpy(str.data, tem);
    return is;
}

ostream &operator<<(ostream &os, String &str) //输出
{
    os << str.data;
    return os;
}
int main()
{
    String test("abc");
    cout<<test<<endl;
}
```

## 面向对象三大特性：封装、继承和多态



## socket

假如b进程是异常终止的，发送FIN包是OS代劳的，b进程已经不复存在，**当机器再次收到该socket的消息时，会回应RST（因为拥有该socket的进程已经终止）**。a进程对收到RST的socket调用write时，操作系统会给a进程发送SIGPIPE，默认处理动作是终止进程。即：

> It is okay to write to a socket that has received a FIN, but it is an error to write to a socket that has received an RST

## 浮点数大小	//EQ

float：32位	1位符号位，8位指数位，23位尾数

double：64位	1位符号位，11位指数位，52位尾数



## TCP长连接

长连接：client向server发起连接，server接受client连接，双方建立连接。Client与server完成一次读写之后，它们之间的连接并不会主动关闭，后续的读写操作会继续使用这个连接。

首先说一下TCP/IP详解上讲到的TCP保活功能，保活功能主要为服务器应用提供，服务器应用希望知道客户主机是否崩溃，从而可以代表客户使用资源。如果客户已经消失，使得服务器上保留一个半开放的连接，而服务器又在等待来自客户端的数据，则服务器将应远等待客户端的数据，保活功能就是试图在服务器端检测到这种半开放的连接。

如果一个给定的连接在**两小时**内没有任何的动作，则服务器就向客户发一个探测报文段，客户主机必须处于以下4个状态之一：

1. 客户主机依然正常运行，并从服务器可达。客户的TCP响应正常，而服务器也知道对方是正常的，服务器在两小时后将保活定时器复位。
2. 客户主机已经崩溃，并且关闭或者正在重新启动。在任何一种情况下，客户的TCP都没有响应。服务端将不能收到对探测的响应，并在**75秒**后超时。服务器总共发送**10个**这样的探测 ，每个间隔**75秒**。如果服务器没有收到一个响应，它就认为客户主机已经关闭并终止连接。
3. 客户主机崩溃并已经重新启动。服务器将收到一个对其保活探测的响应，这个响应是一个复位，使得服务器终止这个连接。
4. 客户机正常运行，但是服务器不可达，这种情况与2类似，TCP能发现的就是没有收到探查的响应。

从上面可以看出，TCP保活功能主要为探测长连接的存活状况，不过这里存在一个问题，存活功能的探测周期太长，还有就是它只是探测TCP连接的存活，属于比较斯文的做法，遇到恶意的连接时，保活功能就不够使了。

在长连接的应用场景下，client端一般不会主动关闭它们之间的连接，Client与server之间的连接如果一直不关闭的话，会存在一个问题，随着客户端连接越来越多，server早晚有扛不住的时候，这时候server端需要采取一些策略，如关闭一些长时间没有读写事件发生的连接，这样可以避免一些恶意连接导致server端服务受损；如果条件再允许就可以以客户端机器为颗粒度，限制每个客户端的最大长连接数，这样可以完全避免某个蛋疼的客户端连累后端服务。

在应用层则可以用**心跳包**来进行保持长连接







**1、在函数内定义一个字符数组，用**gets**函数输入字符串的时候，如果输入越界，为什么程序会崩溃？**

答：因为gets无法截断数组越界部分，会将所有输入都写入内存，这样越界部分就可能覆盖其他内容，造成程序崩溃。

 

**2、C++中引用与指针的区别**

答：联系：引用是变量的别名，可以将引用看做操作受限的指针；

区别：

1） 指针是一个实体，而引用仅是个别名；

2）引用只能在定义时必须初始化，指针可以不初始化为空；

3）引用初始化之后其地址就不可改变（即始终作该变量的别名直至销毁，即从一而终。注意：并不表示引用的值不可变，因为只要所指向的变量值改变。引用的值也就改变了），但指针所指地址是不可变的；如下：

int m=23,n=13;

int& a=m;

a=12; //合法，相当于修改m=12

a=n;//合法，相当于修改m=13

**3、C/C++程序的内存分区**

答：其实C和C++的内存分区还是有一定区别的，但此处不作区分：

1）、栈区（stack）— 由编译器自动分配释放 ，存放函数的参数值，局部变量的值等。其 
 操作方式类似于数据结构中的栈。 
 2）、堆区（heap） — 一般由程序员分配释放， 若程序员不释放，程序结束时可能由OS回 
 收 。注意它与数据结构中的堆是两回事，分配方式倒是类似于链表。 
 3）、全局区（静态区）（static）—，全局变量和静态变量的存储是放在一块的，初始化的 
 全局变量和静态变量在一块区域， 未初始化的全局变量和未初始化的静态变量在相邻的另 
 一块区域。 - 程序结束后由系统释放。 
 4）、文字常量区 —常量字符串就是放在这里的。 程序结束后由系统释放 
 5）、程序代码区—存放函数体的二进制代码。 

**栈区与堆区的区别：**

1）堆和栈中的存储内容：栈存局部变量、函数参数等。堆存储使用new、malloc申请的变量等；

2）申请方式：栈内存由系统分配，堆内存由自己申请；

3）申请后系统的响应：栈——只要栈的剩余空间大于所申请空间，系统将为程序提供内存，否则将报异常提示栈溢出。
 堆——首先应该知道操作系统有一个记录空闲内存地址的链表，当系统收到程序的申请时，会遍历该链表，寻找第一个空间大于所申请空间的堆结点，然后将该结点从空闲结点链表 中删除，并将该结点的空间分配给程序；

4）申请大小的限制：Windows下栈的大小一般是2M，堆的容量较大；

5）申请效率的比较：栈由系统自动分配，速度较快。堆使用new、malloc等分配，较慢；

总结：栈区优势在处理效率，堆区优势在于灵活；

**内存模型：自由区、静态区、动态区；**

根据c/c++对象生命周期不同，c/c++的内存模型有三种不同的内存区域，即：自由存储区，动态区、静态区。

自由存储区：局部非静态变量的存储区域，即平常所说的栈；

动态区： 用new ，malloc分配的内存，即平常所说的堆；

静态区：全局变量，静态变量，字符串常量存在的位置；

注：代码虽然占内存，但不属于c/c++内存模型的一部分；



## 虚拟机相关

### 虚拟机网络模式

**NAT**：母机作为一个路由器进行转发，一般可DHCP自动分配IP，注意母机的IP和宿主机可处于不同网段

**桥接模式**：虚拟机的IP与母机同级，相当于让母机产生一个兄弟机



## 网络编程

### 主机字节序和网络字节序的转换问题

**IP的转换**

```
#include <arpa/inet.h>
in_addr_t inet_addr(const char *string);

#include <netdb.h>
#include <sys/socket.h>
hostent *gethostbyname (const char *__name);

inet_ntoa()
inet_
```

## 显示当前时间

```c
void show_now_time()
{
    char nowtime[20];
    time_t rawtime;
    struct tm* ltime;
    time(&rawtime);
    ltime = localtime(&rawtime);
    strftime(nowtime, 20, "%Y-%m-%d %H:%M:%S", ltime);
    cout<<"["<<nowtime<<"] ";
    return;
}
```

## readn和read的区别

read会立即返回，而readn如果当前读取数据非0且小于目标数量，则会继续读取，有可能产生**阻塞**

## wordpress备案信息登记

更详细内容见知乎的技术收藏夹

外观-->主题编辑器-->fotter.php-->末尾加上:

```php
<a href="http://www.beian.miit.gov.cn">渝ICP备18016041号-1 </a>
```



## Linux快捷键

新建终端		在当前窗口为终端情况下：ctrl + shift + n 

回到桌面		ctrl + win + d

## word技巧

```
1.一行装英文+网址装不下，会将网址放下一行，英文稀疏占满一行，将网址分开
选中-->段落-->中文版式-->允许西文在单词中换行
```

## excel技巧 

excel中打回车 alet + 回车

 ## 命名空间

  ：：a表示全局变量a，用于区分局部变量a



## 函数相关

access函数

测试文件是否存在以及文件权限

  





## 对于map

find函数通过查找key返回迭代器，没有查找value返回迭代器的函数，因为可能有多个key对应一个value。



## bind和function

bind里面的\_1、\_2、等\_n指的是合成的新函数的第一、第二、第n个参数放入原函数中的位置

```C++
auto g = bind(f, a, b, _2, c, _1);//意味着新函数的第一个参数放最右边上，第二个参数放_2那儿
g(X, Y);	//等价于f(a, b, Y, c, X);


std::bind绑定一个成员函数
struct Foo {
    void print_sum(int n1, int n2)
    {
        std::cout << n1+n2 << '\n';
    }
    int data = 10;
};
int main() 
{
    Foo foo;
    auto f = std::bind(&Foo::print_sum, &foo, 95, std::placeholders::_1);
    f(5); // 100
}
bind绑定类成员函数时，第一个参数表示对象的成员函数的指针，第二个参数表示对象的地址。
必须显示的指定&Foo::print_sum，因为编译器不会将对象的成员函数隐式转换成函数指针，所以必须在Foo::print_sum前添加&；
使用对象成员函数的指针时，必须要知道该指针属于哪个对象，因此第二个参数为对象的地址 &foo；
```

function在没有auto时可以声明一种类型，或者是一个模板类型

```c++
#include<functional>
function <T> f;  //T是一个可调用对象，可以是函数指针，函数对象或者lambda

作用
在auto不在时，可以和bind联合使用：
int add_3_num(int a, int b, int c){return a + b + c;}
function<int(int, int> add_2_num = bind(add_3_num, _1, _2, 0);
             
也可以做一些有意思的东西，如下面这个TODO c++ primer p512
```



## git

所有的版本控制系统，只能跟踪文本文件的改动

首先用git init 来在当前文件夹创建git的数据库，记录版本相关的东西

在git里有三个区

- 工作区：也就是我们直接改东西的地方，我们能看见的文件等

- 暂存区：记录了一些工作区改变后的文件，如

  git add将工作区改变/新增的文件加入暂存区，git add .会将工作区所有改变记入暂存区中

  git rm将工作区文件删掉，并记录入暂存区

  可理解为提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改

- git仓库（分支）:也就是打游戏的各个存档

  这三个区可以理解为三个同样的仓库，最终的存档需要先改到暂存区（git add XXX），再改到git仓库(git commit)



git status查看状态

git diff可以查看某个文件改变的内容 git diff HEAD -- readme.txt 可以查看工作区和版本库里面最新版本的区别 //QE TODO

git log将显示git仓库中各个版本，就像查看游戏中的所有存档，HEAD指向当前版本

git reset --hard XXX 便能回到XXX版本，XXX可以是sha值（不用写全），

也可以是『HEAD~X』，X是一个数字，表示回到相对当前版本之前第X版本

在回退后再查看git log发现退回来后的已看不到先进版本，

好比从21世纪坐时光机来到了19世纪，想再回去已经回不去了

git relog能够解决这个问题，显示所有的版本

git checkout -- XXX 也就是让工作区该文件回到改变之前，也就是让暂存区版本倒灌进工作区（前提是上一个状态有备案，无论是git commit或git add）

git reset HEAD XXX可以将暂存区回退到和分支一样。举例，有一个bug版本已经在本地写好并提交到暂存区，就可以需要用将暂存区覆盖，再用git checkout -- XXX

让本地分支被远程分支XXX覆盖git fetch    ``git reset --hard origin/XXX``

git rm XXX 删掉暂存区中的文件，如果本地（工作区）文件未删除也会一并被删掉

- 一些显示提示

『Changes to be committed』change需要提交的，也就是改变记录存在暂存区中的

『Changes not staged for commit』更改没有步入（staged）提交（准备）的，也就是改变记录存在工作区的

stage形容了从工作区步入暂存区



```shell
git remote add origin git@github.com:wanggaolang/test_for_git.git
添加后，远程库的名字就是origin，这是Git默认的叫法，也可以改成别的，但是origin这个名字一看就知道是远程库
git push -u origin master
把本地库的内容推送到远程，用git push命令，实际上是把当前分支master推送到远程。

由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。

---
小结
要关联一个远程库，使用命令git remote add origin git@server-name:path/repo-name.git；

关联后，使用命令git push -u origin master第一次推送master分支的所有内容；

此后，每次本地提交后，只要有必要，就可以使用命令git push origin master推送最新修改；
```

git clone git@server-name:path/repo-name.git克隆到本地，会将所有文件保存在仓库名文件夹中，也就是不用自己创建一个文件夹在clone，在主目录clone就行了



- 分支相关

  创建分支`` git branch ``XXX 会将HEAD指向的分支（一般也就是master分支）复制到XXX分支

  删除分支XXX``git branch -d XXX``

  查看所有分支（包括远程的）``git branch -a``，如果不加``- a``就是显示本地的分支，并标明自己在哪

  将远程分支AAA与本地已有分支BBB与关联起来``git branch -u AAA BBB``

  切换分支 ``git switch XXX``切换到XXX分支(或者是``git checkout XXX``)

  可以用``git switch -c XXX``或者``git checkout -b XXX``创建并切入新分支

  在本地创建分支XXX并与远程分支关联``git checkout -b XXX origin/XXX``

  合并当前分支与XXX分支 ``git merge XXX`` 前提当前版本是XXX版本的子集或者相等

  

  如果在XXX分支中进行了改变，切回主分支，不做任何改动就merge，虽然两者内容冲突，但时间线上XXX更新，所以会将XXX的改变改过来，也就是master指针指向XXX

  如果在XXX改了后切到master分支又改东西，即使两者都是添加新东西，在merge时，也会产生冲突，因为产生了两个时间线

  可以用``git log --graph``看到分支合并图

- 百度代码提交审核

  git push origin HEAD:refs/for/master



## 终端shell快捷键

ctrl + y 粘贴”命令行剪切板“

ctrl + u 剪切一行命令，放入”命令行剪切板“



## ssh rsa key

通过``ssh-keygen -t rsa``生成rsa密钥对

在Linux体系存储位置为``~/.ssh``

windows 一般在 /c/Users/{用户名}/.ssh



## markdown(md)一些用法

\`\`将正常的代码放这四个符号间会被凸显，以代码形式显示\`\`

\*\*在这中间的字会加粗\*\*



## 锁

boost::recursive_mutex::scoped_lock guard_lock(_service_map_mutex);



## docker

- 查看ov相关的的容器

  docker ps -a | grep ov

- 启动某个容器

  doeker start {containerID}

- 进入某个容器中

  docker exec -it {containerID} /bin/bash





## photoshop

- ctrl+alt复制图片时总是卡住，结局办法：控制面板-键盘-速度-调到最低