filename="main.py"

MacOS:
	pyinstaller --onefile main.py --hidden-import=PyQt5.sip --windowed
	mv dist/main.app  dist/minecraft-mac.app
	cp -r .inits dist/minecraft-mac.app/Contents/MacOS/

Linux:
	echo "not finish"

clean_tmp:
	rm -rf build dist __pycache__ main.spec

clean:
	rm -rf .config .Download .inits/default_* .DS_Store .inits/.DS_Store .inits/img/.DS_Store .inits/languages/.DS_Store
	echo "" > .inits/default_loc
	echo "" > .inits/default_lang