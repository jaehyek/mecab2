MeCab2 : MeCab  Windows 64 module for MeCab 0.996
===================================

## 소개

MeCab2은 [MeCab-ko](https://bitbucket.org/eunjeon/mecab-ko)에서 제공하는 은전한닢 프로젝트을 Windows 64bit에 맞게 재구성 및 수정해서 작성한 module 이다.

## libmecab 설치

먼저 본 repository을 받아서 풀고,  "mecab.sln"을 실행시킨다 ( VS2015 혹은 VS2017이 설치됐다고 가정.)

solution이 열린 상태에서 상단 Bar의  64bit, Releae을 선택하고 각 프로젝트를 선택 및 빌드을 완성한다. 
원래의 소스 대비 변경한 부분을 아래와 같다.


    변경1 : feature_index.cpp
    변경전)
    case 't':  os_ << (size_t)path->rnode->char_type;     break;
    변경후)
    case 't':  os_ << path->rnode->char_type;     break;

    변경2 : writer.cpp
    변경전)
    case 'L': *os << lattice->size(); break;
    변경후)
    case 'L': *os << (char)lattice->size(); break;

    변경3 : thread.h
    변경전)
    #define YieldProcessor() __asm { rep nop }
    변경후)
    //#define YieldProcessor() __asm { rep nop }
    
그리고 libmecab 프로젝트 설정시,  전처리기 정의는  다음과 같이

    _CRT_SECURE_NO_DEPRECATE
    MECAB_USE_THREAD
    DLL_EXPORT
    HAVE_GETENV
    HAVE_WINDOWS_H
    DIC_VERSION=102
    VERSION="0.996/ko-0.9.0"
    PACKAGE="\"mecab\""
    MECAB_DEFAULT_RC="c:\\Program Files\\mecab\\etc\\mecabrc"

또한 파일 mecabrc의 내용에는 다음과 같다.

    dicdir=C:\Program Files\mecab\dic
    
즉 libmecab.dll은 default dic dir을 가지고 compile된다. 필요시 이 부분을 수정한다.

## dic-ko 설치

먼저  은전한닢 프로젝트에서 mecab-ko-dic-2.0.1-20150920.tar.gz을 받거나, 다음 명령을 수행해서 다운 받고 압축을 푼다.

    curl -LO https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz
    tar -zxvf mecab-ko-dic-2.0.1-20150920.tar.gz
    cd mecab-ko-dic-2.0.1-20150920

다음은  사전을 만들기 위해 앞에서 만든 mecab_dict_index.exe 으로 다음과 같이 실행한다.

    cmd) mecab_dict_index.exe -d . -o . -f UTF-8 -t UTF-8

생성된 다음의 파일들을  위에서 정의한 dicdir에 copy한다. 

    char.bin, matrix.bin, model.bin, sys.dic, unk.dic, dicrc


## mecab python module 설치

본 repository의 mecab-python-0.996 에서 다음의 명령을 수행한다. 
단 VS2015(혹은 VS2017) tool의 64bit cmd을 관리자 권한으로 열어서 실행한다.

    cmd) python setup.py build 
    cmd) python setup.py install
    
주의할 것은  setup.py 내용중 필요한 부분을 자신에 맞게 수정한다.  본 repository에 있는 것을 보면 

    from distutils.core import setup,Extension,os
    import string
    
    def cmd1(str):
        return os.popen(str).readlines()[0][:-1]
    
    def cmd2(str):
        return cmd1(str).split()
    
    setup(name = "mecab-python",
    	version = "0.996/ko-0.9.0",
    	py_modules=["MeCab"],
    	ext_modules = [
    		Extension("_MeCab",
    			["MeCab_wrap.cxx",],
    			include_dirs=["C:\\project_c++\\mecab2\\libmecab"],
    			library_dirs=["C:\\project_c++\\mecab2\\x64\\Release"],
    			libraries=["libmecab"])
    			])

추가로 주의 할 점은 libmecab.dll이 자동적으로 C:\python3\Lib\site-packages에 copy가 되지 않으므로
직접 copy한다. 
            

## 사용법

본 repository의 mecab-python-0.996 에 있는 test.py를  실행 해 본다. 

> python test.py

이상없어 실행된다면 성공한 것이다. 

