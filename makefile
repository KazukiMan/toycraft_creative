# Python auto Package system
# copyright by KazukiAmakawa and TesMeow
# Kazuki Amakawa's Github: https://www.github.com/KazukiMan
# Kazuki Amakawa's Mail: KazukiAmakawa@gmail.com
# TesMeow's Github: https://www.github.com/TesMeow

filename="main.py"

MacOS:
	pyinstaller --onefile main.py --hidden-import=PyQt5.sip --windowed 
	mv dist/main.app  dist/minecraft-mac.app
	cp -r .inits dist/minecraft-mac.app/Contents/MacOS/
	open ./dist
	open /Applications/

Linux:
	echo "not finish"

Windows:
	pyinstaller --onefile main.py --hidden-import=PyQt5.sip --windowed 

clean:
	rm -rf .config .Download .DS_Store .inits/.DS_Store .inits/img/.DS_Store .inits/languages/.DS_Store build dist __pycache__ main.spec