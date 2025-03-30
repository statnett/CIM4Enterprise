FIXME = ../../ENTSOE-SHACL/Inst4CIM-KG/rdfs-improved

ttl/Asset.ttl: merge-owl/Asset.merged-owl
	cp $^ temp.rdf
	update.bat --update=$(FIXME)/fix-all.ru --data=temp.rdf --dump |\
	  perl $(FIXME)/fix-namespaces.pl |\
	  cat $(FIXME)/prefixes.ttl - > temp.ttl
	owl.bat write --prefixAlign=right --useCommaByDefault temp.ttl $@
	rm temp.rdf
	#rm temp.ttl
