---
title: "重装 Ubuntu 16.04 的笔记"
categories: [Linux]
permalink: /note/ReInstall_Ubuntu1604/
excerpt: "用来重装 Ubuntu 16.04 的笔记，包括我经常用的安装包、经常需要执行的命令、以及需要进行手动操作的事项。"
---

{% include toc %}

# 软件包安装

## `apt` 安装部分

### 需要添加的 PPA 源

```
sudo add-apt-repository ppa:webupd8team/atom
sudo add-apt-repository ppa:notepadqq-team/notepadqq
```

### 基本软件

> vim chromium-browser fcitx wine-development terminator evolution net-tools

其中 `net-tools` 是避免 expressvpn 在高版本 Ubuntu 中会出现的无法链接 vpn 服务器的软件。

### 文本处理软件

> atom notepadqq emacs perl-tk jabref

其中 `perl-tk` 是安装 TeX Live 时可以用于图形化安装与图形化查看宏的必需软件。

### 科学计算与程序软件

> gfortran libopenblas-dev libopenmpi-dev openmpi-bin tcsh make g++ libatlas3-base subversion git-svn

### 媒体与娱乐软件

> vlc clementine redeclipse

### 博客需要的软件

> ruby-dev libffi-dev zlib1g-dev

上面的后两个软件包是避免在用 `bundle` 安装 `ffi` 与 `nokogiri` 时会产生的依赖关系报错。

在进入 Jekyll 静态博客环境之前，需要先执行下面的命令：
```
sudo gem install bundler
```
随后执行
```
bundle install
```

### 需要手动安装的软件

* [expressvpn](https://download.expressvpn.xyz/clients/linux/expressvpn_1.2.0_amd64.deb)：VPN 工具，[主页网站地址](https://www.expressvpn.com)
* texstudio：TeX 文本编辑器，[主页网站地址](http://texstudio.sourceforge.net/)
* [sogoupinyin](http://cdn2.ime.sogou.com/dl/index/1491565850/sogoupinyin_2.1.0.0086_amd64.deb)：搜狗输入法，[主页网站地址](http://pinyin.sogou.com/linux/?r=pinyin)
* [netease-cloud-music](http://s1.music.126.net/download/pc/netease-cloud-music_1.0.0-2_amd64_ubuntu16.04.deb)：网易云音乐，[主页网站地址](http://music.163.com/#/download)

# 指令部分

### 安装字体

```
mkdir -p $/HOME/.font
cp -r $(FontDir) $HOME/.font
sudo fc-cache -fv
```

### 安装 PGI 编译器

[PGI 2017](http://www.pgroup.com/support/download_community.php?file=pgi-community-linux-x64) 是可以获得免费副本的软件。在安装该软件后需要在 `.bashrc` 中加入
```
PATH=$PATH:/opt/pgi/linux86-64/2017/bin
```
并生成下述软链接：
```
sudo ln -s /usr/lib/x86_64-linux-gnu/ /usr/lib64
```

<!--### 安装 Gaussian 09

需要在 `.bashrc` 中加入下述语句：
```
## gaussian 09 C01 Source start
export g09root=$(your destination of g09root)
export GAUSS_EXEDIR=$g09root/g09
export GAUSS_SCRDIR=$HOME/Tmp/g09chk
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$g09root/g09
export PATH=$g09root/g09:$PATH
source $g09root/g09/bsd/g09.profile
export PATH=$g09root/g09-Mod:$PATH
## gaussian 09 C01 Source end

```
并执行
```
mkdir -p $HOME/Tmp/g09chk
ln -s /usr/lib/atlas-base/libatlas.so.3 $g09root/g09/libatlas-corei764sse3.a
ln -s /usr/lib/atlas-base/libf77blas.so.3 $g09root/g09/libf77blas-corei764sse3.a
```
-->

### 安装 NWCHEM 6.6 (27746)

首先在 tcsh 下设置环境：
```
setenv NWCHEM_TOP /usr/local/share/ajzapps/nwchem-6.6
setenv NWCHEM_TARGET LINUX64
setenv USE_MPI y
setenv USE_PYTHONCONFIG n
setenv BLASOPT "-lopenblas -lpthread -lrt"
setenv BLAS_SIZE 4
setenv USE_64TO32 y
setenv PATH /usr/local/share/ajzapps/nwchem-6.6/bin/LINUX64:$PATH
```
随后依次在 `src` 文件夹下执行
```
make nwchem_config NWCHEM_MODULES="all rimp2_grad"
make 64_to_32
make
```

### 配置文件

* [terminator](/assets/files/2017-10-06-Reinstall_Ubuntu1604/config) 配置文件，安装到 `$HOME/.config/terminatior` 中
* [.vimrc](/assets/files/2017-10-06-Reinstall_Ubuntu1604/vimrc) 配置文件，安装到 `$HOME` 中
* [.bashrc](/assets/files/2017-10-06-Reinstall_Ubuntu1604/vimrc) 配置文件，安装到 `$HOME` 中
* [.tcshrc](/assets/files/2017-10-06-Reinstall_Ubuntu1604/vimrc) 配置文件，安装到 `$HOME` 中
