@echo off
CHCP 65001
echo 开始复制配置文件
copy %~dp0LuaTool.lua C:\Users\%USERNAME%
copy %~dp0PathConfig.lua C:\Users\%USERNAME%
echo 配置文件复制结束
pause