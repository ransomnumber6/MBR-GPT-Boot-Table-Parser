all:
	sudo apt install pip
	pip install pyinstaller
	pip install -r requirements.txt
	pyinstaller boot_info.py --onefile
	mv -f dist/* .
	chmod +x boot_info