# This makefile is purely for running tests on the complete ontology-starter-kit package on travis;
# users should not need to use this

test: test1 test2

test1:
	 ./seed-my-ontology-repo.pl -c -d pato -t my-ontology1 myont

test2:
	 ./seed-my-ontology-repo.pl -c -d pato -d ro -t my-ontology2 myont

test3:
	 ./seed-my-ontology-repo.pl -c -d pato -d cl -d ro -t my-ontology3 myont
