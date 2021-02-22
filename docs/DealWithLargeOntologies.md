# Dealing with huge ontologies in your import chain

Dealing with very large ontologies, such as the Protein Ontology (PR), NCBI Taxonomy (NCBITaxon), Gene Ontology (GO) and the CHEBI Ontology is a big challenge when developing ontologies, especially if we want to import and re-use terms from them. There are two major problems:
1. It currently takes about 12–16 GB of memory to process PR and NCBITaxon – memory that many of us do not have available.
2. The files are so large, pulling them over the internet can lead to failures, timeouts and other problems. 

There are a few strategies we can employ to deal with the problem of memory consumption:
1. We try to reduce the memory footprint of the import as much as possible. In other words: we try to not do the fancy stuff ODK does by default when extracting a module, and keep it simple.
2. We manage the import manually ourselves (no import)

To deal with file size, we:
1. Instead of importing the whole thing, we import curated subsets.
2. If available, we use gzipped (compressed) versions.

All four strategies will be discussed in the following. We will then look a bit 

## Overwrite ODK default: less fancy, custom modules

The default recipe for creating a module looks something like this:

```
imports/%_import.owl: mirror/%.owl imports/%_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) query  -i $< --update ../sparql/preprocess-module.ru \
		extract -T imports/$*_terms_combined.txt --force true --copy-ontology-annotations true --individuals exclude --method BOT \
		query --update ../sparql/inject-subset-declaration.ru --update ../sparql/postprocess-module.ru \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/%_import.owl
```
(Note: This snippet was copied here on 10 February 2021 and may be out of date by the time you read this.)

As you can see, a lot of stuff is going on here: first we run some preprocessing (which is really costly in ROBOT, as we need to load the ontology into Jena, and then back into the OWL API – so basically the ontology is loaded three times in total), then extract a module, then run more SPARQL queries etc, etc. Costly. For small ontologies, this is fine. All of these processes are important to mitigate some of the shortcomings of module extraction techniques, but even if they could be sorted in ROBOT, it may still not be enough.

So what we can do now is this. In your `ont.Makefile` (for example, `go.Makefile`, NOT `Makefile`), located in `src/ontology`, you can add a snippet like this:

```
imports/pr_import.owl: mirror/pr.owl imports/pr_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/pr_terms_combined.txt --force true --method BOT \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/pr_import.owl
```

Note that all the `%` variables and uses of `$*` are replaced by the ontology ID in question. Adding this to your `ont.Makefile` will overwrite the default ODK behaviour in favour of this new recipe.

_The ODK supports this reduced module out of the box. To activate it, do this:_

```
import_group:
  products: 
    - id: pr
      use_gzipped: TRUE
      is_large: TRUE
```

This will (a) ensure that PR is pulled from a gzipped location (you _have_ to check whether it exists though. It must correspond to the PURL, followed by the extension `.gz`, for example `http://purl.obolibrary.org/obo/pr.owl.gz`) and (b) that it is considered large, so the default handling of large imports is activated for `pr`, and you don't need to paste anything into `ont.Makefile`.

If you prefer to do it yourself, in the following sections you can find a few snippets that work for three large ontologies. Just copy and paste them into `ont.Makefile`, and adjust them however you wish.

### Protein Ontology (PR)

```
imports/pr_import.owl: mirror/pr.owl imports/pr_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/pr_terms_combined.txt --force true --method BOT \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/pr_import.owl
```

### NCBI Taxonomy (NCBITaxon)

```
imports/ncbitaxon_import.owl: mirror/ncbitaxon.owl imports/ncbitaxon_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/ncbitaxon_terms_combined.txt --force true --method BOT \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/ncbitaxon_import.owl
```

### CHEBI

```
imports/chebi_import.owl: mirror/chebi.owl imports/chebi_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/chebi_terms_combined.txt --force true --method BOT \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/chebi_import.owl
```

Feel free to use an even cheaper approach, even one that does not use ROBOT, as long as it produces the target of the goal (e.g. `imports/chebi_import.owl`).

## Use slims when they are available

For some ontologies, you can find slims that are _much_ smaller than full ontology. For example, NCBITaxon maintains a slim for OBO here: http://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.obo, which is just 3 MB (!) compared to the 1 or 2 GB of the full version. Many ontologies maintain such slims, and if not, probably should. (I would really like to see an OBO slim for Protein Ontology!)

You can also add your favourite taxa to the NCBITaxon slim by simply making a pull request on here: https://github.com/obophenotype/ncbitaxon/blob/master/subsets/taxon-subset-ids.txt

You can use those slims simply like this:

```
import_group:
  products: 
    - id: ncbitaxon
      mirror_from: http://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.obo
```

## Manage imports manually

This is a real hack – and we want to strongly discourage it – but sometimes, importing an ontology just to import a single term is total overkill. What we do in these cases is to maintain a simple template to "import" minimal information. I can't stress enough that we want to avoid this, as such information will necessarily go out of date, but here is a pattern you can use to handle it in a sensible way:

Add this to your `src/ontology/ont-odk.yaml`:

```
import_group:
  products: 
    - id: my_ncbitaxon
```

Then add this to `src/ontology/ont.Makefile`:

```
mirror/my_ncbitaxon.owl:
	echo "No mirror for $@"

imports/my_ncbitaxon_import.owl: imports/my_ncbitaxon_import.tsv
	if [ $(IMP) = true ]; then $(ROBOT) template --template $< \
  --ontology-iri "$(ONTBASE)/$@" --output $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: imports/my_ncbitaxon_import.owl
```

Now you can manage your import manually in the template, and the ODK will not include your manually-curated import in your base release. But again, avoid this pattern for anything except the most trivial case (e.g. you need one term from a huge ontology).


## File is too large: Network timeouts and long runtimes

Remember that ontologies are text files. While this makes them easy to read in your browser, it also makes them huge: from 500 MB (CHEBI) to 2 GB (NCBITaxon), which is an enormous amount.

Thankfully, ROBOT can automatically read gzipped ontologies without the need of unpacking. To avoid long runtimes and network timeouts, we can do the following two things (with the new ODK 1.2.26):

```
import_group:
  products: 
    - id: pr
      use_gzipped: TRUE
```
This will try to append `.gz` to the default download location (http://purl.obolibrary.org/obo/pr.owl &rarr; http://purl.obolibrary.org/obo/pr.owl.gz). Note that you must make sure that this file actually exists. It does for CHEBI and the Protein Ontology, but not for many others.

If the file exists, but is located elsewhere, you can do this:

```
import_group:
  products: 
    - id: pr
      mirror_from: http://purl.obolibrary.org/obo/pr.owl.gz
```

You can put any URL in `mirror_from` (including non-OBO ones!)
