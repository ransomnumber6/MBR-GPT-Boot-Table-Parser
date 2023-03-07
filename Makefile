all: setup
	cp boot_info.py boot_info && chmod +x boot_info && ./boot_info

setup:
	sudo apt install pip
	pip install -r requirements.txt