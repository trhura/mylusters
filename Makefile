all: clean
	for file in *.py; do \
		python $$file; \
	done
	echo "Done"

clean:
	rm -rf *.csv
