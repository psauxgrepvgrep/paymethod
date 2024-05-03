CGI_DIR = /usr/local/mgr5/cgi/
XML_DIR = /usr/local/mgr5/etc/xml/
EXEC_DIR = /usr/local/mgr5/paymethods/
all: build

build:
	#xml
	cp ./billmgr_mod_testpayment  $(XML_DIR)
	#main exec
	ln -s /root/paymethod/pmtestpayment.py $(EXEC_DIR)
	#cgi
	ln -s /root/paymethod/testpayment.py $(CGI_DIR)

release:
	git push
install:
	apt install python3-pip
	pip install -r requirements.txt 
