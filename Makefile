all: 	install

doc: 	
	rst2html README.rst > README.html

test: install testENV testOAI testSRU testALTOtoTXT

testENV:
	python3 setup.py install

testOAI:
	python3 ./test/oai_test.py

testSRU:
	python3 ./test/sru_test.py

testALTOtoTXT:
	python3 ./test/alto_to_text_test.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf kb.egg-info
	find . -name \*.pyc -exec rm '{}' ';'
	find . -name "__pycache__" -exec rmdir {} \;	
	rm README.html

install:
	python3 setup.py install
