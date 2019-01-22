@echo off 
for /r ..\src %%i in (*.pyc) do @echo %%i & del %%i