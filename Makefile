all: dist/ports.tar.bz2 dist/ports.tar.bz2.rmd160

dist:
	mkdir -p dist

dist/ports.tar.bz2: dist
	find . -name '*~' -delete && \
	mkdir dist/ports && \
	cp -R sysutils dist/ports/ && \
	cd dist && tar -cjvf ports.tar.bz2 ports && \
	rm -rf ports

dist/ports.tar.bz2.rmd160:
	openssl dgst -ripemd160 -sign privkey.pem -out dist/ports.tar.bz2.rmd160 dist/ports.tar.bz2.rmd160

clean:
	rm -rf dist

release:
	rsync -avz dist/* zerokspot.com:/srv/www/h10n.me/www/htdocs/macports-ports/ && \
	rsync -avz pubkey.* zerokspot.com:/srv/www/h10n.me/www/htdocs/macports-ports/

check_updates:
	@cd _scripts && $(MAKE) $@

.PHONY: all clean release check_updates
