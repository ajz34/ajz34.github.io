---
title: "Lapack，Slatec Fortran 运行库安装"
comments: True
permalink: /post/Lapack-etc-Installation/
categories: [Linux 安装配置]
excerpt: "介绍三个常见数学库的安装，以及介绍可能会产生的报错信息。"
keywords: Lapack, Blas, Slatec, Fortran Library, Ubuntu, Installation, 运行库, 安装
---

{% include toc %}

# 缘起

尽管安装这些包并不是什么难事，但是对于新上手 Linux 系统的我来说，因为有了 `apt-get` 这么一个方便的工具，于是 Lapack 或者 Blas 运行库几乎不用费脑筋就可以安装好；但是 Slatec 库的安装则是费了一番脑筋。而且安装过程始终记不住；曾经也几乎没有通过 `Make` 安装过 Lapack 运行库—— 而 `apt-get` 则应该是类 Debian 专有的安装软件包方法，不适用于所有系统；于是想留下这份笔记，以备以后重新安装系统的不时之需。

# Lapack，Slatec 简介

### Lapack，Blas

![Lapack](/images/Posts/2016-09-18-Lapack-Front.jpg)

[Lapack](http://www.netlib.org/lapack/) 全名 Linear Algebra PACKage，专门用于解决 **稠密** 或 **对称**、**带状** 矩阵（而不适合解决稀疏矩阵）线性代数问题，例如求解特征向量、特征值、进行矩阵分解等。一般来说，Lapack 运行库通常包含 Blas，因为几乎所有实用的 Lapack 子程序都要调用 Blas 库。

[Blas](http://www.netlib.org/blas/) 全名 Basic Linear Algebra Subprograms，是大多数矩阵或向量的基本操作运行库，它包含向量内积、求模，矩阵数乘、相乘、转置等操作。这些子程序的功能并不难以实现；事实上一般的程序员为实现这些功能，应该能写出比较高效的相应代码。

Lapack、Blas 的真正意义应该不在于它们的运行效率有多快（尽管它们在一般情况下运行效率确实很快），而是在于它们已经是非稀疏向量、矩阵运算的事实标准。有许多运行库都基于 Lapack、Blas 的标准和框架构建，并且专门针对特定的编译器、处理器进行优化；故可以在实际应用的时候，不需要对代码作太多改动即可获得很好的加速效果。

Blas 库的框架事实上再千禧年之前就已经确定了，并且几乎没有更新。曾经 Blas 开发者通过 Blas 后续开发的标准（[BLAS Technical Forum Standard](http://www.netlib.org/blas/blast-forum/)），但这个标准应该没有在现在的 Lapack 中使用。这个标准最重要的期望之一是将稀疏矩阵的计算纳入 Blas 中。现有的库中，[MKL](https://software.intel.com/en-us/intel-mkl) 可能是支持新 Blas 标准最好的运行库。

Lapack、Blas 完全支持 Fortran 90、C 语言的应用。由于一般编译器在编译 FORTRAN 77 文件时对 Fortran 90 以上标准的容忍程度很高，故这些运行库一般也可以用于通常的 Fortran 77 编译。实际使用这些运行库的时候，可以先在 Cheat-Sheet（[Lapack](http://www.netlib.org/lapack/lapackqref.ps)，[Blas](http://www.netlib.org/blas/blasqr.pdf)）上找到所需要的子程序，然后通过 manpage 来了解详细情况。

### Slatec

[Slatec](http://www.netlib.org/slatec/) 是 FORTRAN 77 特殊函数库，它将在我自己尝试编写的 SCF 程序里有所建树。在使用函数的时候，可以先到 [toc](http://www.netlib.org/slatec/toc) 目录下搜索关键词，然后通过对应关键词找到子程序名称；最后用过 manpage 了解该子程序应当如何调用参数。

# 安装过程

详细的安装过程与调试指南在运行库主网站上都有所链接，这里只提供非常简单的安装过程。

## 系统配置

* 系统：Ubuntu 16.04.1 LTS
* Lapack 版本：3.6.1
* Slatec 版本：4.1

## 准备文件

### 下载文件

Lapack 可以容易地通过 [Lapack网站](http://www.netlib.org/lapack/) 找到，其中 3.6.1 版本可以在此 [下载](http://www.netlib.org/lapack/lapack-3.6.1.tgz)；Slatec 的文件准备稍繁琐一些，我们至少需要下载 [slatec_src.tgz](http://www.netlib.org/slatec/slatec_src.tgz) 和 [slatec4linux.tgz](http://www.netlib.org/slatec/slatec4linux.tgz) 。

> :warning: 注意
>
> 在 Internet Explorer 浏览器上下载的 `tgz` 文件包的后缀名可能是 `gz`；若这种情况出现，请先将后缀名改为 `tgz` 再解压缩。

> :pencil: 建议
>
> 如果你使用的 Linux 系统是不带图形界面的，那么你可以考虑在命令行界面使用 `wget` 命令下载文件，例如下载 Lapack 运行库：
>
>```shell
$ wget http://www.netlib.org/lapack/lapack-3.6.1.tgz
```

### 解压缩

`tar` 文件的解压缩命令是 `tar -xzf` ；若要在解压过程中查看所被解压的文件列表，则使用 `tar -xvzf` 命令；相应地，压缩的命令为 `tar -czf` 。

现在进入下载文件所在目录，操作如下命令：

```shell
$ tar -xzf lapack-3.6.1.tgz
$ mkdir slatec
$ tar -xzf slatec4linux.tgz -C slatec/
$ tar -xzf slatec_src.tgz -C slatec/
$ mv slatec/src/* slatec/
```

### Lapack、Blas Static Library安装

> :pencil: 提醒
>
> 下述的过程只适合静态（static）运行库的构建，若要使用更为方便的动态（dynamic）库的构建，还是任然需要使用 `apt-get` 安装至少 `liblapack-dev` ，该过程会连带安装 Blas；安装 `liblapack-doc-man` 、 `liblapack-doc` 则可以运行 manpage。在 Ubuntu 16.04 LTS 默认软件库中，Lapack 的版本已经很新了（3.6.0）。
>
> 关于动态 Blas 库，其安装比较方便，可以参考 [GNU](https://gcc.gnu.org/wiki/GfortranBuild) 比较过时的文章。

在 Lapack-3.6.1 目录下，首先需要创建 `make.inc` 配置文件；该文件的模板可以参照该目录下的 `make.inc.example` 文件，也可以通过复制 `./INSTALL` 目录下的配置文件的文本到 `make.inc` 实现。一般来说，如果使用 `gfortran` 编译程序且没有特殊的编译要求的话，直接照搬 `make.inc.example` 的内容即可：

```shell
$ mv make.inc.example make.inc
```

同时需要更改安装根目录下的 `Makefile` 文件以安装所有需要的库。我们必须要安装的库为 `blaslib` 和 `lapacklib`，而默认安装的库是 `lapacklib` 和 `tmglib` ，故我们需要更改 `Makefile` 文件的第 11 或 12 行。如果只需要安装 `blaslib` 和 `lapacklib` ，则可以运行：

```shell
$ sed -i '11s/apacklib tmglib/lblaslib lapacklib/g' Makefile
```

若不进行这一步而又没有事先安装 `linrefblas.a` （即 Blas 库） 于安装根目录，则会出现下述错误信息：

```
gfortran  -O2 -frecursive -c sblat1.f -o sblat1.o
gfortran  sblat1.o  \
        ../../librefblas.a  -o ../xblat1s
gfortran: error: ../../librefblas.a: No such file or directory
Makeblat1:47: recipe for target '../xblat1s' failed
make[1]: *** [../xblat1s] Error 1
```

这一步结束后就可以安装 Lapack、Blas 运行库了：

```shell
$ make
```

生成安装包后，手动将安装包输出至系统的运行库文件夹中，该步骤需要管理员权限：

```shell
$ sudo cp *.a /usr/local/lib/
```

> :pencil: 建议
>
> 上述安装方法应不会成功生成测试信息文件，同时会返回错误信息：
>
>```
make[1]: *** No rule to make target '../libtmglib.a', needed by 'xlintsts'.  Stop.
Makefile:45: recipe for target 'lapack_testing' failed
make: *** [lapack_testing] Error 2
```
>
> 解决方案就是无视之，因为我们其实已经成功将我们需要的库文件 `*.a` 生成了。当然如果我们期望得到测试结果，我们需要安装所有运行库，在这之中可能出现的问题请看下面的 *注意* 部分。

> :warning: 注意
>
> 在我的安装过程中可能会遇到两个问题。其一为编译 `variants` 库出现问题。如果你对根目录下的 `Makefile` 的改变是将 11 行注释掉而将 12 行取消注释，安装所有库，则会遇到该问题。这很有可能是因为库中的目录设置出现问题，屏幕将会输出：
>
>```
ar cr LIB/cholrl.a cholesky/RL/cpotrf.o cholesky/RL/dpotrf.o cholesky/RL/spotrf.o cholesky/RL/zpotrf.o
ar: LIB/cholrl.a: No such file or directory
Makefile:38: recipe for target 'cholrl' failed
make[1]: *** [cholrl] Error 1
```
>
>为解决该问题，可以在安装根目录下运行下述命令：
>
>```shell
$ sed -i '1,$s/$(VARIANTSDIR)\///g' SRC/VARIANTS/Makefile
```
>
> 另一个错误是在测试时遇到堆栈问题，由于堆栈达到系统容许上线，故被迫在测试双精度复数子程序计算时退出：
>
>```
NEP: Testing Nonsymmetric Eigenvalue Problem routines
./xeigtstz < nep.in > znep.out 2>&1
Makefile:453: recipe for target 'znep.out' failed
make[1]: *** [znep.out] Error 139
```
>
> 这种情况下应当运行下述命令(参考 [StackOverflow](https://stackoverflow.com/questions/36059694/install-clapack-3-2-1-in-fedora-23/36296489#36296489?newreg=5b4e4d5e6e794c449c92e011b65e1946) 解答)：
>
>```shell
$ ulimit -s unlimited
```
>
> 若遇到权限错误，请先运行 `su root` 登陆超级用户再运行上述命令。

最后可以通过一个测试程序 [lapack_prb.f](https://people.sc.fsu.edu/~jburkardt/f77_src/lapack_examples/lapack_prb.f) 来检查安装是否成功；下述指令要求安装包与测试程序在同一文件夹下：

```shell
$ gfortran lapack_prb.f liblapack.a librefblas.a
```

> :warning: 提醒
>
> 在编译调用库的时候，尽量按照后者被前者调用的顺序输入命令，否则会可能出现编译错误。

### Slatec

Slatec 库的安装相对容易一些。不过注意 Slatec 默认的编译环境是 `f77` ，在部分系统该程序指代的是 `fort77` 而非 `gfortran` ，需要手动调整编译环境：

```shell
$ sed -i '1s/^/FC= gfortran \n/' static/makefile
$ sed -i '1s/^/FC= gfortran \n/' dynamic/makefile
$ make
$ sudo make install
```

> :warning: 注意
>
> 安装过程中很有可能遇到没有 `/usr/local/man/man1` 的错误：
>
> ```shell
mv: target '/usr/local/man/man1' is not a directory
makefile:228: recipe for target 'install' failed
make: *** [install] Error 1
```
>
> 那么我们需要新建该文件夹。

这种方法安装 Slatec 是同时安装了动态与静态库，故调用的时候可以比较方便地在被编译程序后加上 `-lslatec` 即可。由于它有时会调用 Lapack，故我们在编译时应该将 `-lslatec` 放在 Lapack 库的前面。

> :pencil: 提醒
>
> 安装 Slatec 后将会把 Blas 的 manpage 覆盖掉；所以如果平时需要看原始的 Blas manpage，则应该输入类似于 `man double_blas_level2` 以查看被调用函数。
