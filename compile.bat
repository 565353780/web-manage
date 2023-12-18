rd /q /s build
rd /q /s dist
del run.spec
del run_thread.spec
pyinstaller -F run.py
pyinstaller -F run_thread.py
