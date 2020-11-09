## 笔记规范

- 要求易懂且简洁
- 标题：一级用##，二级用数字+英文点（用空格后在typora上会自动向下拼加），三级用黑点，四级用数字+英文点，五级用二级黑点
- 可选参数用英文中括号（[]）括起来，必要参数用大括号（{}）括起来。如果括号是真正需要显示的，则在里面再加一个`{}`，在该大括号中添加描述性语言。如: `[{外面的中括号是必要的}]`
- 在一大段论述或者一个一级标题内容结束后有个回车
- 同一行内容间隔4空格
- 有疑问的地方用QE标记，如果紧急在前面加三个$$$



## 常用规范

- 在linux体系机器，临时文件放/test_for_all，提示文件放~/README

- 代码注释

  维护代码时，在原来代码上基于新需求增加或修改代码，要备注来自第几个新需求，备注方法为`//{新需求的顺序id}`

  ​	如第一个需求注释为`//+++01`
  
  如果只是对原来代码做一些改动，如打印调试信息，注释为`//@@@`
  
  如果是很重要的地方`//$$$`    正在view的地方`//$$$$`
  



## typora相关

- 页内跳转
  1. 如果想调到指定标题名去，可用[任意内容]\(#标题名，注意带左边的#号\)
  2. 如果想跳到任意文本处：1）要先在该文本处加上”锚点“，\<a name=锚点名>指定文本（也可以空白）\</a>    2）[任意内容]\(#锚点名，注意带左边的#号\)

##  git相关及github相关

**概念**

注意所有的版本控制系统，只能跟踪文本文件的改动

首先用`git init `来在当前文件夹创建git的数据库，记录版本相关的东西

将整个git分为4个仓库，在数据同步后可以理解为四个相同的文件夹：

- 工作区：主机上看见的文件夹

- 暂存区：提交一个版本是个严肃的事，先放暂存区，确认了再提交到更上层

- git本地仓库：也就是打游戏的各个存档
- git远程仓库：远程版``git本地仓库``，为了方便联网和多人操作

而多一个分支，表明多了一份`git本地仓库`，不会影响工作区和暂存区。举个例子：在当前分支工作区有未到暂存区的文件a，暂存区有未到git本地仓库的文件b，新建分支并切换到新分支，用`git status`查看与在老分支结果一样



一些初始操作：

``` shell
git init    //在当前文件夹建设git数据库，之后对当前文件夹及其子文件夹提交到比工作区更上层的仓库后，再变化工作区相关文件，就能够知道其变化
//添加远程仓库有以下两种方式，添加后，远程库的名字就是origin，这是Git默认的叫法，也可以改成别的，但是origin这个名字一看就知道是远程库
git remote add orinin https://github.com/wanggaolang/test.git		//https方式添加远程仓库
git remote add orinin git@{server_name,如“github.com”}:wanggaolang/test.git  //ssh方式添加远程仓库
git remote set-url orinin {以上两种方式的远程仓库}    //以覆盖的放式添加远程仓库orinin，也就是说若orinin有则被覆盖
git remote rm origin    //删掉远程仓库

git push -u origin master    //在远程仓库创建master分支，并将当前分支git本地仓库上传上去
git push -f    //强制让远程关联分支的git远程仓库被本地覆盖
ssh -T git@github.com    //测试与github联通性
```



**各个仓库的常规流动**

1. 查看前三个仓库间的未提交状况:`git status`
2. 

- pull操作

1. 将远程指定分支拉取到本地指定分支上    `git pull origin {远程分支名}[:{本地分支名}，如果不要就是拉取到本地当前分支]`

2. 将与本地当前分支同名的远程分支 拉取到 本地当前分支上(需先关联远程分支，方法见文章末尾)    `git pull`

- push操作
  1、将指定分支推送到远程指定分支    ``git push origin {本地分支名}:{远程分支名}``

  2、将指定本地分支推送到同名远程分支    ``git push origin {本地分支名}``

  3、将本地当前分支 推送到 与远程同名分支上(需先关联远程分支，方法见文章末尾)    ``git push``

同样的，推荐使用第2种方式，git push origin <远程同名分支名>QE

``cat .git/config``看到本地与远程分支的关联关系

---

**仓库间之间和仓库内部版本的回滚**

- 从`git本地仓库`回滚某次提交（commit）到`工作区`

  `git reset --hard {某次commit}`    该命令使工作区回滚到指定的一次commit，这个参数可以是sha值（不用写全），

  也可以是:`HEAD~{数字}`，表示回到相对当前版本之前上多少个版本

  ？git reset HEAD {文件名}

  git log将显示git仓库中各个版本，就像查看游戏中的所有存档，HEAD指向当前版本

  在回退后再查看git log发现退回来后的已看不到先进版本，好比从21世纪坐时光机来到了19世纪，想再回去已经回不去了

  `git reflog`能够解决这个问题，显示所有的版本

- 暂存区回滚到工作区:    `git checkout -- {文件名，用.表示所有。注意文件名前有空格} `

git reset HEAD XXX可以将暂存区回退到和git仓库当前版本一样。举例，有一个bug版本已经在本地写好并提交到暂存区，就可以需要用将暂存区覆盖，再用git checkout -- XXX

让本地分支被远程分支XXX覆盖   `git reset --hard origin/XXX`    QE 描述有问题样

git rm XXX 删掉暂存区中的文件，如果本地（工作区）文件未删除也会一并被删掉

- 如何查看`git status`的提示

『Changes to be committed』change需要提交的，也就是改变记录存在暂存区中的

『Changes not staged for commit』更改没有步入（staged）提交（准备）的，也就是改变记录存在工作区的stage形容了从工作区步入暂存区

  在键入`git commit -m {消息}`后想修改消息通过`git commit --amend`命令

git clone git@server-name:path/repo-name.git克隆到本地，会将所有文件保存在仓库名文件夹中，也就是不用自己创建一个文件夹在clone，在主目录clone就行了。这种clone会把git数据库克隆过来，所以会让本地有所有远程分支

git fetch QE

- 在使用git提交代码的时，`git commit -m "内容"` 如果内容编写错误：

  使用`git commit --amend` 对上次提交的内容进行修改

**分支相关**



分支的作用：1）多人同时操作同一仓库，为了防止混乱，要让每个人有自己的`git本地仓库`，而多一个分支就多一个`git本地仓库`。    2）当有一个新需求需要更改代码，而更改过程中可能要回到没改变之前的样子用于调试修复其他功能模块。这时候可以将新功能commit到新分支，再切换回来修复其他功能模块。当新需求完成后在master分支merge该分支，处理冲突并commit就行了。这时在master分支只会多出一个merge的log版本。

如果在XXX分支中进行了改变并commit，切回主分支，不做任何改动就merge，虽然两者内容冲突，但时间线上XXX更新，所以会将XXX的改变改过来，也就是master指针指向XXX

如果在XXX改了后切到master分支又改东西，即使两者都是添加新东西，在merge时，也会产生冲突，因为产生了两个时间线



1、创建分支``git branch {新分支名}``    新分支复刻当前分支，并且HEAD指针，也就是当前工作区指向的分支仍为原来分支

2、切换分支``git checkout {分支名}``

3、创建并切入新分支``git checkout -b {分支名}``

4、创建分支并与远程分支关联``git checkout -b {新建分支} origin/{远程分支}``    这时新建分支内容就是关联分支内容

​	新建分支并与当前分支某个commit关联`git checkout -b {新分支名} {commit_id}`

5、删除分支``git branch -d {要删分支}``

6、查看所以分支``git branch -a``    不加``- a``为显示本地分支

？将远程分支与本地已有分支BBB与关联起来``git branch -u AAA BBB``

8、添加远程分支：git push origin {本地分支}:{远程分支}

9、删除远程分支：git push origin {空格}:{远程分支}		or		 git push origin --delete {远程分支}

10、在当前分支合并（并入）指定分支：git merge {指定分之名}   如果有冲突需要解决冲突再add，commit。若无冲突会自动commit



合并当前分支与XXX分支 ``git merge XXX`` 前提当前版本是XXX版本的子集或者相等

可以用``git log --graph``看到分支合并图

- 杂项

  `git diff [多个参数]`    

  ​	概念：git diff a b意味着相较于b来说，a增加了啥，减少了啥

  ​	只显示不同文件名：--name-only

  ​	比较当前工作区与暂存区区别:`git diff`
  
  ​	比较俩commit区别:`git diff {第1个commit的sha值} {第2个commit的sha值}`
  
  ​	比较本地git仓库和远端区别:`git diff origin`
  
  ​	解决`git diff`中文文件名乱码问题：
  
  ```shell
  $ git config --global core.quotepath false          # 显示 status 编码
  $ git config --global gui.encoding utf-8            # 图形界面编码
  $ git config --global i18n.commit.encoding utf-8    # 提交信息编码
  $ git config --global i18n.logoutputencoding utf-8  # 输出 log 编码
  ```
  
  `暂存git stash`
  
  将包括未追踪文件一同暂存进栈：git stash -u
  
  出栈：git stash pop
  
  

## 内存操作的小技巧 

*(int *)ptr的意思是从ptr这个地址开始向上（因为是小端存储）取四个字节出来看成int，注意编译器优化会使两个相邻变量上下字节间发生变化，可以加上```volatile```。大部分机器都是小端存储，变量的首地址是最低的一个字节的地址，取变量时向上取，存储时向低地址存（因为是栈）。



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



## 常见c语言函数

```c
	void *memcpy(void *dest, const void *src, size_t n)
从 src 复制 n 个字符到 dest，不会先清空dest。
	void *memset(void *str, int c, size_t n)
复制字符 c（一个无符号字符）到参数 str 所指向的字符串的前 n 个字符。
	char *strcat(char *dest, const char *src)
把 src 所指向的字符串追加到 dest 所指向的字符串的结尾。
	char *strcpy(char *dest, const char *src)
把 src 所指向的字符串复制到 dest，会先清空dest。
	
	取绝对值：abs(obj)和fabs(obj),前者是整数，后者是浮点数。都需要导入<math.h>
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

## vscode相关

**快捷键**

快捷键设置：`ctrl+k+s`

查找文件名：command + p

在打开的文件夹中查找一个函数：左侧那个放大镜

回到上一个光标：mac：`command + -`    windows：`alt + ←`

批量向左、向右缩进：``ctrl + [``   、 ``ctrl + ]``

批量保存文件：（改了键位的）windows：`ctrl + alt + s`    mac：`command + option + s`

打开终端:    `control + ~`    或者 查看-终端

到大括号的尾端/首部:    `Ctrl + Shift+\`

删除光标行：`ctrl+shift+k`

**三个配置文件**

//TODO



编译：mac快捷键 command + shift + b

解决ubuntu中vscode字体间距过大问题：安装适配`firacode`字体

1. 更新可用软件包列表: `sudo apt update`;
2. 通过安装/升级软件来更新系统: `sudo apt upgrade`;
3. 安装字体管理器: `sudo apt install font-manage`;
4. 安装`firacode`字体: `sudo apt install fonts-firacode`;
5. 在首选项-设置-字体中将`Fira Code`放最前边，重启vscode;

解决 \#ifdef 的地方可能变灰问题：文件-首选项-设置-搜索dimInactiveRegions    取消勾选





## 进程，线程，协程

进程：计算机程序运行的实体。每个进程都有自己的独立内存空间，上下文切换开销比较大（栈，寄存器，虚拟内存，文件句柄等），相对稳定安全

线程：进程的一个实体，是cpu调度和分派的基本单位。线程只拥有一点在运行中必不可少的资源(如程序计数器,一组寄存器和栈),但是它可与同属一个进程的其他的线程共享进程所拥有的全部资源。线程间通信主要通过共享内存，上下文切换很快，资源开销较少，但相比进程不够稳定容易丢失数据。

协程：



## c++相关

1. 在有派生类时各构造函数和析构函数调用顺序

   构造函数顺序：基类构造函数、对象成员构造函数、派生类本身的构造函数 

   析构函数顺序：派生类本身的析构函数、对象成员析构函数、基类析构函数（与构造顺序正好相反）
   
2. lambda表达式

   - [{捕获列表}]\({参数列表})->{返回值}{{函数体}}    举例: `auto add_1 = [](int a)->int {return a+1;};`
   
   - 该表达式一般定义在函数内部，也就是函数中定义函数
   - 捕获列表用于传入lambda所在函数的非static变量，对于其他变量或者函数，只要lambda所在函数能调用它便能使用。捕获列表默认为const值传递而非地址传递。如[v_1, v_2]在内部改变他们值并不会改变lambda所在函数里他们的值。地址传递需要在其前面加上&，如[&v_1, &v_2]。如果传入值很多可以隐式传递，编译器会根据函数体内部的调用情况推断传入了哪些值。[=]为值传递，[&]为地址传递，如果两者皆有，则第一个参数必须为&或=，表示默认传递方式，在其后面跟上另外的参数，如[=, &v_2, &v_3]
   
   - 可以省略掉参数列表和返回值，如: `auto get_1 = []{return 1;};`

3. 格式化：#include \<iomanip\>  std::fixed << std::setprecision(8) << _double    前者表示以非科学计数法打印，后者表示显示８位小数

4. 类模板的成员函数在类外定义以及类模板的函数特例化

   ```c++
   //类模板，但是在类外定义成员函数的时候，需要使用函数模板 
   #include <iostream>  
   using namespace std ;  
   template <class T>  
   class Base  
   {  
   public :
       T a ;
       Base(T b)    {  a = b ;    }
       T getA(){ return a ;} //类内定义
       void setA(T c);
   };
   
   template <class T>   void  Base<T>::setA(T c)//模板成员函数在类外的定义
   {
       a = c ;
   }
   
   template<> void Base<int>::setA(int value)//模板成员函数的特例化
   {
       a = value*2;
   }
   ```

   



## 设计模式

1. 观察者模式

   ​	场景为有一个通知者和多个观察者，在通知者发生或发现某种变化时，挨个通知每个观察者。实现上说白了就是在通知者内部保存一个可调用对象的list，设置一个通知函数来依次调用每个可调用对象，该list可以动态增加减少。当然在通知者内部也可以是一个对象队列，通知函数为调用每个对象的update函数。反正核心就是有可调用对象的队列在通知者里面。由于计算机语言的限制，大部分语言实现上该可调用对象list的每一个都是有同样的参数列表和返回值，不然无法将一堆不同的可调用对象放在同一个list里面。

   ​	注意在多线程中如果一个线程往list添加可调用对象，一个线程负责在发生事件调用通知函数（也许这个事件只发生一次，所以希望在调用通知程序前所有可调用对象已加入），就可能涉及竞争问题。好的做法是把增加操作和调用通知程序放在同一个线程中



## 小知识（一）

1. chrome快捷键：历史记录    ``ctrl + y``

2. 类外定义成员函数不能加上默认参数，如：``Test fun(int a = 1)``会报错，同样static声明的成员在外部定义时候，必须省去static。同时，static成员变量只有跟了const才可以在类里面的初始化列表中进行初始化，其余的都要在类的外部初始化

3. string.find()和map.find()以及set.find()如果找不到目标，则结果为x.end()

4. volatile关键词影响编译器编译的结果，用volatile声明的变量表示该变量随时可能发生变化，与该变量有关的运算，不再编译优化，以免出错

5. 在linux中，默认c++的include位置为`/usr/include`

6. `LD_LIBRARY_PATH`是Linux环境变量名，该环境变量主要用于指定查找共享库（动态链接库）时除了默认路径之外的其他路径

   一般的用法为`export LD_LIBRARY_PATH={新添加地址}:$LD_LIBRARY_PATH`，放冒号左边表示先搜索。这是临时性的，退出shell再进就没了
   
   动态链接库默认导入路径在linux中查看配置`/etc/ld.so.conf`，可以将路径写入配置，再用`ldconfig`载入，永久生效。
   
7. scp 从本地复制到远程    `scp [-r] {本地文件/夹} {remote_username@remote_ip:文件/夹} `

8. 在同一文件夹下多个文件中查找某个关键字：

   1）通过`cat ./* | grep {查找内容}`确认文件中是否有这个关键字

   ​	通过`find . -type f -name "*" | xargs grep {查找内容}`找到这个文件//todo 查看原理

   2）find {文件夹，如果是当前文件夹可以省略} -type f -name "*.c" | xargs grep {查找的关键字}

   - type f 意思是只找文件
   
   - name "\*.c"  表示只找C语言写的代码，从而避免去查binary；也可以不写，表示找所有文件
   
9. 查看linux发行版本：`cat /etc/issue`
   
10. linux命令行`2>&1`    标准错误重定向到标准输出

11. 罗技鼠标驱动软件：官网－下载－Logitech G HUB

12. 查看当前目录下，每个文件夹大小：du -h --max-depth=1

13. 用md5sum计算文件的消息摘要

14. 

    



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

## 浮点数大小	//QE

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



## Linux相关/终端相关/terminal相关

- Ubuntu启动终端：`Ctrl + Alt + T`

- 终端和shell的区别：类似编辑器和编译器，编辑器展示给程序员看，编译器用来真正的编译

- 配置shell-bash：增加或在原文注释改动为以下内容

  ```shell
  if [ "$color_prompt" = yes ]; then
  	#这些注释掉的就是原文
      #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
      PS1='${debian_chroot:+($debian_chroot)}\w\$ '
  else
      #PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
      PS1='${debian_chroot:+($debian_chroot)}\w\$ '
  fi
  unset color_prompt force_color_prompt
  
  # If this is an xterm set the title to user@host:dir
  case "$TERM" in
  xterm*|rxvt*)
      #PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS3"
      #w展示全路径，W展示最后一截路径；\u@\h表示：用户名@电脑型号名
      #\e[32;32m是绿色，\e[0m表示后边自己的输入变为默认色
      PS1="\[\e[32;32m\]\w\[\e[0m\]\$"
      ;;
  *)
      ;;
  esac
  ```

  

- 配置终端

  **Iterm2 **

  Iterm2 + oh-my-zsh，注意需要配置Meslo 字体，否则会乱码
  
  Iterm2的配色可以好好看一下，目前用的**Solarized Dark Higher Contrast**配色
  
  为了让多用户都使用同样的配置，要将`~/.zshrc`复制到每个用户下
  
  通过历史记录自动补全`pip install powerline-status`
  
  插件配置（位于~/.zshrc）：`plugins=(git zsh-autosuggestions extract zsh-syntax-highlighting z)`
  
  Iterm2快捷键：
  
  ```bash
  command + ，设置
  command + enter 进入与返回全屏模式
  command + t 新建标签
  command + w 关闭标签
  command + 数字 command + 左右方向键    切换标签
  command + enter 切换全屏
  command + f 查找
  command + d 水平分屏
  command + shift + d 垂直分屏
  command + option + 方向键 command + [ 或 command + ]    切换屏幕
  command + ; 查看历史命令
  command + shift + h 查看剪贴板历史
  ctrl + u    清除当前行
  ctrl + l    清屏
  ctrl + a    到行首
  ctrl + e    到行尾
  ctrl + f/b  前进后退
  ctrl + p    上一条命令
  ctrl + r    搜索命令历史
  ```
  
  
  
  **terminator**
  
  1. sudo apt-get install terminator
  
  2. 启动terminator，在里边`vim .config/terminator/config`
  
     ```shell
     [global_config]
       title_font = Ubuntu Mono 11[keybindings]
     [layouts]
       [[default]]
         [[[child1]]]
           parent = window0
           type = Terminal
         [[[window0]]]
           parent = ""
           type = Window
     [plugins]
     [profiles]
       [[default]]
         background_color = "#002b36"
         background_darkness = 0.91
         background_image = None
         background_type = transparent
         font = Ubuntu Mono 11
         foreground_color = "#e0f0f1"
         use_system_font = False
         show_titlebar = False
     ```
  
     
3. 通过dconfig-editor将terminator设置为默认终端（自己搜）
4. 修改`.bashrc`：https://blog.csdn.net/zhangkzz/article/details/90524066

  


- 快捷键

  新建终端		在当前窗口为终端情况下：ctrl + shift + n 

  回到桌面		ctrl + win + d
  
  
  
- 命令

  创建多级目录/文件夹    ``mkdir -p {路径}``
  
  查找文件``find / -name {文件名，可配合通配符} 2>/dev/null``
  
  
  
- 权限

  chmod只是改变文件的读写、执行权限，更底层的属性控制是由chattr来改变的QE lsattr

  让文件不可删除`chattr +i {file/folder}`  

  

- 命令别名

  将一个长命令起一个别名，变为短命令    `alias {新命令}="{老命令}"`

  查看有哪些起了别名的命令    `alias`

  

- 一些疑难问题

  1. Ubuntu下`alt + tab`出现两个窗口

     原因：系统启动了两个不同的程序切换程序

     办法：安装Compiz，然后关掉“应用程序切换条”

     ```shell
     sudo apt-get install compiz-plugins
     sudo apt-get install compizconfig-settings-manager
     ```

     

  

- mac相关
  
  1. **Homebrew**：是Mac OS 不可或缺的套件管理器。可以通过它安装软件，比如wget
  
     进入其目录    `cd "$(brew --repo)"`
  
     换源:
  
     ```shell
     //设置homebrew本身源：
     cd "$(brew --repo)" && git remote set-url origin git://mirrors.ustc.edu.cn/brew.git
     
     //设置并更新formula源
     cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core" && git remote set-url origin git://mirrors.ustc.edu.cn/homebrew-core.git
     
     //使用中科大的bottles源：
     echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
     
     ```
  
     homebrew会将下载的软件统一安装在/usr/local/Cellar目录中
  
  2. 配置iterm2的配色为**`Solarized Dark Higher Contrast`**，在./etc下有一个版本可以用，最好在[这](https://iterm2colorschemes.com/)弄最新的
  
  3. 在当前窗口是终端时新建一个终端``command + t``
  
  4. 在finder根目录中`command + shift + .`显示隐藏文件
  
  5. 录屏：QuickTime player
  
  



## word技巧

```
1.一行装英文+网址装不下，会将网址放下一行，英文稀疏占满一行，将网址分开
选中-->段落-->中文版式-->允许西文在单词中换行
```

## excel技巧 

excel中打回车 alet + 回车

 ## 命名空间

  ::a表示全局变量a，用于区分局部变量a



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



## 终端shell相关

ctrl + u 剪切一行命令，放入”命令行剪切板“

ctrl + y 粘贴”命令行剪切板“

查看当前文件夹文件数量（子文件夹算1文件）    `ls | wc -w`

`| awk '{print $1}'`    （注意是单引号）将每一行中以空格为分割符的第一个字段打印出来

`| xargs`    将多行合并到一行，以空格分割

查看某个端口的tcp状态：`netstat -antop | grep {portID}`

改变当前用户默认shell：`chsh`

shell配色：PS1

\[\e[F;Bm\] （F表示字体颜色，B表示背景颜色，具体如下）

| 字体代码 |       背景代码 |       颜色/作用        |
| -------- | -------------: | :--------------------: |
| 30       |             40 |          黑色          |
| 31       |             41 |          红色          |
| 32       |             42 |          绿色          |
| 33       |             43 |          黄色          |
| 34       |             44 |          蓝色          |
| 35       |             45 |         紫红色         |
| 36       |             46 |         青蓝色         |
| 37       |             47 |          白色          |
|          |              1 |          高亮          |
|          |              2 |          低亮          |
|          |              3 |          斜体          |
|          |              4 |         下划线         |
|          |              5 |          闪烁          |
|          |              7 | 和字体颜色一样的背景色 |
|          | 与字体代码相同 |       默认背景？       |

注意最后要用\[\e[0m\\]结尾，如这种（用typora源码模式看）：PS1="\[\e[32;32m\][\[\e[33;33m\]cp_3_05\[\e[32;32m\]:\w]\$ \[\e[0m\]"



## shell编程/shell脚本编程

1. $0 是shell脚本本身名字，$1是shell脚本第一个参数，以此类推。注意c语言的int main(int argc, char *argv[])与此类似，argv[0]是程序本身名字，然后就是参数，argc是包含程序本身名的参数数量(>=1)

   ![image-20201103165334785](./etc/pic/image-20201103165334785.png)



## vim相关

- 快捷键模式

  全选:    `ggVG`    一行行选择`V`，一个个光标单位选择`v`

  将选择的复制`y`，粘贴`p`

  - 光标移动
    1. 到行尾:`$`    到下一行行尾:`2$`    到从当前行算起第n行行尾:`n$`
    
    2. 到行首:`0`
    
  - 撤销：命令模式下按u    撤销的撤销：ctrl + r
  
  - 查看关键字出现次数：%s/{关键字}//gn  
  
    
  

## ssh rsa key

通过`ssh-keygen -t rsa`生成rsa密钥对

在Linux体系存储位置为`~/.ssh`

windows 一般在 /c/Users/{用户名}/.ssh



## markdown(md)一些用法

1. \`将正常的代码放这四个符号间会被凸显，以代码形式显示\`，左右两个这种引号也行
2. *\*在这中间的字会加粗\*\*
3. 在typora中数字+英文点+空格会让后续自动增加序号，如果要将两段序号（如123、12）合为一个（12345），进入typora编辑模式，将中间的空格之类的清除就行
4. []右边放()会产生隐藏链接，点击中括号内容便转到链接



## 锁

boost::recursive_mutex::scoped_lock guard_lock(_service_map_mutex);



## docker相关

 **docker概念**

镜像就是模板类；容器是对应模板的具象化（对象）






- 查看镜像    ``docker image ls``或者`docker images`

- 查看ov相关的的容器，前面显示所有容器    ``docker ps -a | grep ov``

- 启动某个容器    ``doeker start {containerID}``

- 进入某个容器中    ``docker exec -it {containerID} /bin/bash``

- 主机和容器间文件的拷贝

  主机拷贝文件到容器    `docker cp {主机路径} {容器hash，如96f7f14e99ab}:{容器路径，末尾有/}`
  
  将容器文件拷贝到主机，如:    `docker cp 96f7f14e99ab:/www /tmp/`
  
- 删除容器：`docker rm {containerID}`

- 复制容器

  - 保存镜像

    docker save ID > xxx.tar

    docker load < xxx.tar

  - 保存容器

    docker export ID >xxx.tar

    docker import xxx.tar containr:v1

    然后再docker run -it containr:v1 bash

- 容器内部查看容器ID:




## photoshop相关

- ctrl+alt复制图片时总是卡住，解决办法：

  方法1：控制面板-键盘-速度-调到最低（不打管用）

  方法2：任务管理器--关闭ps进程下的一些怀疑对象，卡住画面恢复



## protobuf相关/pb相关

1、限定修饰符包含 required\optional\repeated 

Required: 表示是一个必须字段，必须相对于发送方，在发送消息之前必须设置该字段的值，对于接收方，必须能够识别该字段的意思。发送之前没有设置required字段或者无法识别required字段都会引发编解码异常，导致消息被丢弃。

Optional：表示是一个可选字段，可选对于发送方，在发送消息时，可以有选择性的设置或者不设置该字段的值。对于接收方，如果能够识别可选字段就进行相应的处理，如果无法识别，则忽略该字段，消息中的其它字段正常处理。---因为optional字段的特性，很多接口在升级版本中都把后来添加的字段都统一的设置为optional字段，这样老的版本无需升级程序也可以正常的与新的软件进行通信，只不过新的字段无法识别而已，因为并不是每个节点都需要新的功能，因此可以做到按需升级和平滑过渡。

Repeated：表示该字段可以包含0~N个元素。其特性和optional一样，但是每一次可以包含多个值。可以看作是在传递一个数组的值。N 表示打包的字节并不是固定。而是根据数据的大小或者长度。对于结构体的repeated字段，会生成

``{结构体对象名}.{repeated对象名}_size()``，函数返回int。如果想取出某个index对应的单位:   

 `{结构体对象名}.{repeated对象名}({index})`

2、可以将message理解为一个结构体，每个结构体有一定的 required\optional\repeated，对于某结构体的可选字段（Optional），会生成`{结构体对象名}.has_{Optional成员名字}`，函数返回bool；

对于Required和Optional成员，如果存在，可以通过{message，对象承接的名字}.{成员名字}()来获取

而对于Repeated成员，需要通过{message，对象承接的名字}.{成员名字}(index，int类型)



## 压缩/解压文件

```shell
tar
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件

这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。

-z：有gzip属性的
-j：有bz2属性的
-Z：有compress属性的
-v：显示所有过程
-O：将文件解开到标准输出

下面的参数-f是必须的

-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

# tar -cf all.tar *.jpg
这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。

# tar -rf all.tar *.gif
这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。

# tar -uf all.tar logo.gif
这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。

# tar -tf all.tar
这条命令是列出all.tar包中所有文件，-t是列出文件的意思

# tar -xf all.tar
这条命令是解出all.tar包中所有文件，-x是解开的意思

压缩
tar –cvf jpg.tar *.jpg //将目录里所有jpg文件打包成tar.jpg
tar zcf jpg.tar.gz *.jpg   //将所有jpg后缀文件压缩为一个gz压缩包
tar zcf cg.tgz ./*    //将所有文件压缩为tgz文件（参数可以记为“政策房”，将零散的村落打包压缩在一起）
tar –cjf jpg.tar.bz2 *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用bzip2压缩，生成一个bzip2压缩过的包，命名为jpg.tar.bz2
tar –cZf jpg.tar.Z *.jpg   //将目录里所有jpg文件打包成jpg.tar后，并且将其用compress压缩，生成一个umcompress压缩过的包，命名为jpg.tar.Z
rar a jpg.rar *.jpg //rar格式的压缩，需要先下载rar for linux
zip jpg.zip *.jpg //zip格式的压缩，需要先下载zip for linux

解压
tar –xvf file.tar //解压 tar包
tar -xzvf file.tar.gz -C ~/test_for_all //将tar.gz或者tar.tgz解压到指定目录
tar -xjvf file.tar.bz2   //解压 tar.bz2
tar –xZvf file.tar.Z   //解压tar.Z
unrar e file.rar //解压rar
unzip file.zip //解压zip

总结
加压解压都可以加v参数看中间过程
1、*.tar 用 tar –xvf 解压
2、*.gz 用 gzip -d或者gunzip 解压
3、*.tar.gz和*.tgz 用 tar –xzf 解压（参数几位“香樟房”，散开的叶子这么多，也就是解压缩）
4、*.bz2 用 bzip2 -d或者用bunzip2 解压
5、*.tar.bz2用tar –xjf 解压
6、*.Z 用 uncompress 解压
7、*.tar.Z 用tar –xZf 解压
8、*.rar 用 unrar e解压
9、*.zip 用 unzip 解压
```



## python相关

- 常规

  1. 教程看的

  2. python中所有都可看做对象，如变量，函数，类，类的对象

  3. 一句话起http服务    ``python2 -m SimpleHTTPServer [端口，默认8000]``    or

     `python3 -m http.server [端口，默认8000]`


  4. 在同时安装了python2和python3时使用pip安装第三方库会产生歧义，要指定具体哪个python的pip安装可以用一下方法`{python版本:python2或python3} -m pip install {第三方库名}`
  5. 在Python的string前面加上‘r’， 是为了告诉编译器这个string是个raw string，不要转意backslash '\' 。 例如，\n 在raw string中，是两个字符，\和n， 而不会转意为换行符。由于正则表达式和 \ 会有冲突，因此，当一个字符串使用了正则表达式后，最好在前面加上'r'



- **语法**

  1. 单引号和双引号效果一样，三引号里可以放前两者，让他们显示出来

  2. 格式化

     ```python
     age = 20
     name = 'Swaroop'
     print('{0} was {1} years old when he wrote this book'.format(name, age))
     
     # 对于浮点数 '0.333' 保留小数点(.)后三位
      print('{0:.3f}'.format(1.0/3))
     # 使用下划线填充文本，并保持文字处于中间位置
     # 使用 (^) 定义 '___hello___'字符串长度为 11
     print('{0:_^11}'.format('hello'))
     # 基于关键词输出 'Swaroop wrote A Byte of Python'  并去除最后的换行
     print('{name} wrote {book}'.format(name='Swaroop', book='A Byte of Python'), end = '')
     
     ```

  3. 转义字符，与c类似，核心的有：``\t``    ``\n``    ``\"``    注意单纯的\会将上下两行代码拼接

  4. 整除`//`    且`and`    或`or`    非`not`

  5. 可以在while后面接else

  6. **imoport 模块**

     将模块理解为一个.py的文件，每次导入该文件都是原地执行了一次该文件

     可以通过`__name__ == '__main__'`的值判断对当前文件的执行是真正的运行这个文件还是被当模块导入时顺带执行

     通过`from {模块名} import {变量名}`语句可以在当前文件直接使用变量，而不用使用`{模块名}.{变量名}`

  7. dir({模块/对象名})

     返回该模块/对象内部的对象，也就是变量，函数，类，类的对象等等

  8. del {对象名}

     可理解为调用了该对象析构函数，后续不能使用该对象

  9. 类

     @classmethod和@staticmethod一个是类方法，一个叫静态方法。其实都可以理解为c++的类静态函数。这两者的区别是前者第一个参数声明为cls，意为类本身，实际调用不需要带上它。

     从c++的角度来看，直接声明和定义在类里面的成员变量是static变量（也叫类变量），声明和定义在`__init__(self[,其余可选参数])`内部的形如`self.{成员变量名}`是对象变量

     - 静态变量（类变量）和成员变量

       直接在类里面声明的是静态变量，注意每次调用都用`{类名}.{成员名}`来指定调用，而对象成员

  


​     

- 多线程

  1. 多线程相关QE

  2. 线程池

     [不错的讲解](http://c.biancheng.net/view/2627.html)



## expect脚本

if {$value eq "abc"} {XXX}    注意大括号的左括号左边要有空格，右括号右边要有空格

中途退出    `exit`

spawn

echo  QE

expect脚本自动ssh登陆，当终端窗口发生变化时，默认expect不会将终端窗口大小改变的信号传送到远程的服务器上，因此在使用上会出现很不方便的地方，比如vim打开文件时出现串行，要是含有中文的文件可能根本无法编辑。解决办法是在脚本中添加: 

```shell
#!/usr/bin/env expect 
#trap sigwinch spawned
trap {
 set rows [stty rows]
 set cols [stty columns]
 stty rows $rows columns $cols < $spawn_out(slave,name)
} WINCH
```

`set timeout 1`设置超时时间，目前知道的作用是来计时`expect`的

`expect "*bash-baidu-ssl*" {send "ssh $host \r"}` 如果匹配到对应字符，则发送ssh数据。在timeout时间后还没匹配到这些字符，自动跳过



## 厨房/厨艺

**油焖大虾**

- 准备
    葱姜蒜
    汁：酱油，糖，料酒，胡椒粉，配至半碗
    虾去虾线，减掉腿、触须以及嘴角，并在背部切一刀
- 实操
    放油放虾，多炒下炸酥脆炒出虾油，放入葱姜蒜，翻炒下放入汁，再大火收汁



**大盘鸡**

- 准备

  卤料包相关材料    胖子鱼佐料    葱姜蒜    干辣椒    花椒    料酒

  鸡肉宰成块，放入料酒

  土豆，青椒

- 实操

  放油炒鸡肉，多炒下把油炒干，然后放入花椒、辣椒、鱼佐料、姜翻炒下，放入卤料材料翻炒加水

  然后加入生抽老抽，盐。在鸡肉好的差不多的时候加入土豆，注意水淹没土豆，煮好就行

**火锅**

- 准备

  火锅底料，卤料包（很重要），火锅香油

  各类菜（如黄瓜、莴笋、土豆、藕片、



**海鲜蘸料**

- 准备

  醋(总酸3.5)，酱油，老姜

- 实操

  老姜切碎泡在醋里1小时，吃的时候在放入酱油

## json相关

jsoncpp是cpp处理json的库，可以直接在github上拉取，然后找到amalgamate.py文件，执行`python amalgamate.py`命令，会在`dist`目录下生成两个头文件和一个源文件`json-forwards.h` 、`json.h`和`jsoncpp.cpp`。之后就直接`include "jsoncpp.cpp"`便可以使用了。

因为每次使用json会先声明一个json对象，如果不考虑重复使用对象，则每一个大括号就是一个对象，而`”key“:{XXX}`这种值为一个大括号的又是一个新的对象，可以用`json["key"] = obj`来复制；而`”key“:[{XXX}]`也是一个对象，对于这种，可以用json["key"].append(obj)来插值。也就是说对于json的对象，在有key时其value是对象还是数组，取决于用等号还是append函数。

- 清空Json对象中的数组    `root["array"].resize(0);`
- 删除Json对象    `root.removeMember("key");`
- 产生value为null的对象：` root["abc"];`    //root["abc"] = null
- 判断json对象是否为空：`bool Json::Value::isNull () const`

## 时间戳相关

在cpp上返回返回1970年01月01日00时00分00秒起至现在的总秒数。

可以通过函数返回值或者传入指针获取时间戳：`extern time_t time(time_t *__timer)`

```c++
#include <iostream>
#include <time.h>
using namespace std;
 
int main()
{
    time_t myt=time(NULL);
    cout<<"sizeof(time_t) is: "<<sizeof(time_t)<<endl;
    cout<<"myt is :"<<myt<<endl;
 
    time_t t;
    time(&t);
    cout<<"t is:"<<t<<endl;
}
```



获取当前时间

```c++
#include <time.h>
#include <stdio.h>
int main(){
    char *wday[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
    time_t timep;
    struct tm *p;
    time(&timep);
    p = localtime(&timep); //取得当地时间
    printf ("%d/%d/%d ", (1900+p->tm_year), (1+p->tm_mon), p->tm_mday);
    printf("%s %d:%d:%d\n", wday[p->tm_wday], p->tm_hour, p->tm_min, p->tm_sec);
}

//其中localtime把time_t转换为了下方的结构体
struct tm {
   int tm_sec;         /* 秒，范围从 0 到 59*/
   int tm_min;         /* 分，范围从 0 到 59*/
   int tm_hour;        /* 小时，范围从 0 到 23*/
   int tm_mday;        /* 一月中的第几天，范围从 1 到 31*/
   int tm_mon;         /* 月份，范围从 0 到 11*/
   int tm_year;        /* 自 1900 起的年数 */
   int tm_wday;        /* 一周中的第几天，范围从 0 到 6*/
   int tm_yday;        /* 一年中的第几天，范围从 0 到 365*/
   int tm_isdst;       /* 夏令时*/    
};
```



## 文件操作相关

cpp中的fstream

```c++
	#include<fstream>
	std::ofstream fout;
    fout.open("./test", std::ios::in | std::ios::ate);
    if (fout.is_open()) {
        fout << "json.toStyledString();";
        fout.close();
    }
```

open函数有下列的打开方式，默认的打开方式是`ios_base::in | ios_base::out`

ios::in	为输入(读)而打开文件
ios::out	为输出(写)而打开文件
ios::ate	初始位置：文件尾
ios::app	所有输出附加在文件末尾
ios::trunc	如果文件已存在则先删除该文件
ios::binary	二进制方式



## gdb相关

1. 开始    gdb {程序名}
2. 输入参数    set args {参数}
3. 下断点     b {断点，如launch_service.cpp:127}
4. 打印参数    p {参数}