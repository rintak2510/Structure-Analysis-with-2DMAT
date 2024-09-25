#!/bin/sh

#convolutionのかかった順問題計算結果を出力する
./bulk.exe
./surf.exe
python3 /Users/rin/Datafiles/2DMAT/2DMAT/script/make_Convolution.py
read input
mv convolution.txt ${input}
