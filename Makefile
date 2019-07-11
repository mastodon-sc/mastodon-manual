all: trackmate 

trackmate:
	./convert_to_tex.py MastodonManual.wtex MastodonManual.tex
	pdflatex MastodonManual.tex
	./convert_to_wiki.py MastodonManual.wtex MastodonManual.txt

clean:
	rm *.aux *.log *.out *.toc
	rm MastodonManual.pdf MastodonManual.tex MastodonManual.txt

