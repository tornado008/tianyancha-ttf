最近学习爬虫，发现天眼查字库会进行替换，于是就学着如何获取正确的数据

配置:

  安装依赖
    pip install -r requirements.txt

    centos7.X 安装 tesseract-ocr

    （1）依赖安装:
        yum install -y automake autoconf libtool gcc gcc-c++
        yum install autoconf automake libtool
        yum install libjpeg-devel libpng-devel libtiff-devel zlib-devel

    （2）安装leptonica

        wget http://www.leptonica.org/source/leptonica-1.72.tar.gz
        tar xvzf leptonica-1.72.tar.gz
        cd leptonica-1.72/
        ./configure
        make && make install

    （3）安装tesseract-ocr

        wget https://github.com/tesseract-ocr/tesseract/archive/3.04.zip
        unzip 3.04.zip
        cd tesseract-3.04/
        ./configure
        make && make install
        sudo ldconfig

     （4）在 /user/local/share/tessdata 下放置 chi_sim.traineddata

        下载地址: https://github.com/tesseract-ocr/tessdata

运行:
    python3 ttf.py （数字替换）
    python3 font.py （所有字体替换）

其他:
    现阶段 ttf.py实现了 数字的正确获取, font.py 实现将所有被替换字体合并成一张图片。
    下阶段，将图片字体转成字符串, 匹配成对应的json, 思路：机器学习或者使用公有云提供的ocr通用字体识别，例如:
    https://cloud.tencent.com/act/event/ci_demo.html上进行测试, 测试识别率很好, 而且有免费额度。
