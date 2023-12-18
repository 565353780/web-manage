rm -rf build
rm -rf dist
rm run.spec
rm run_thread.spec
pyinstaller -F run.py
pyinstaller -F run_thread.py
