pip install urllib3 requests beautifulsoup4 selenium tqdm

if [ "$(uname)"=="Linux" ]; then
	mkdir -p ~/Install/chrome
	cd ~/Install/chrome/
	sudo apt install unzip -y
	rm chrome-linux64.zip
	rm chromedriver-linux64.zip
	wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chrome-linux64.zip
	wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip
	unzip chrome-linux64.zip
	unzip chromedriver-linux64.zip
	sudo rm /usr/local/bin/chrome*
	cp ./chromedriver-linux64/chromedriver ./chrome-linux64/chromedriver
	sudo ln -s $HOME/Install/chrome/chrome-linux64/chrome* /usr/local/bin/
	sudo chmod +x /usr/local/bin/chromedriver
fi
