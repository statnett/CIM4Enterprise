RDF = $(wildcard ../rdf/*.rdf)
TTL = $(patsubst ../rdf/%.rdf,%.ttl,$(RDF))
FIXME = ../../../ENTSOE-SHACL/Inst4CIM-KG/rdfs-improved

all: $(TTL) asset-terms-in-telemark-120.md asset-terms-in-nordic-telemark.md

%.ttl: ../rdf/%.rdf
	update.bat --update=$(FIXME)/fix-all.ru --data=$^ --dump |\
	  perl $(FIXME)/fix-namespaces.pl |\
	  cat $(FIXME)/prefixes.ttl - > temp.ttl
	owl.bat write --prefixAlign=right --useCommaByDefault temp.ttl $@
	rm temp.ttl

asset-terms-in-telemark-120.md: ../../asset-terms-in-telemark-120.pl
	perl $^ > $@

asset-terms-in-nordic-telemark.md: ../../asset-terms-in-nordic-telemark.pl
	perl $^ > $@
