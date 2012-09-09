all: pdf html

pdf: elektroninen_keittokirja.pdf

elektroninen_keittokirja.pdf: elektroninen_keittokirja.rst
	rst2pdf elektroninen_keittokirja.rst

html: elektroninen_keittokirja.html

elektroninen_keittokirja.html: elektroninen_keittokirja.rst
	rst2html elektroninen_keittokirja.rst >elektroninen_keittokirja.html

dbdoc:
	(mkdir -p dbdoc && cd dbdoc && postgresql_autodoc -s rohmotti && dot -Tpng < jonne.dot >rohmotti.png)

clean:
	rm -f elektroninen_keittokirja.pdf elektroninen_keittokirja.html

distclean: clean
	rm -f *~
