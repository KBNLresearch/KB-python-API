all: 	install

doc: 	
	rst2html README.rst > README.html

test: testENV testOAI testSRU testALTOtoTXT

testENV:
	python setup.py install

testOAI:
	python ./test/oai_test.py

testSRU:
	python ./test/sru_test.py

testALTOtoTXT:
	python ./test/alto_to_text_test.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf kb.egg-info
	find . -name \*.pyc -exec rm '{}' ';'
	find . -name "__pycache__" -exec rmdir {} \;
	rm -rf env/local/lib/python2.7/site-packages/kb-*
	rm README.html

install:
	python setup.py install
