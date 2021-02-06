import $ivy.`net.sourceforge.owlapi:owlapi-distribution:4.5.16`
import $ivy.`com.outr::scribe-slf4j:2.7.12`
import org.semanticweb.owlapi.apibinding.OWLManager
import org.semanticweb.owlapi.model._
import org.semanticweb.owlapi.vocab.OWLFacet
import java.io.File
import scala.collection
import scala.collection.mutable
import scala.jdk.CollectionConverters._
@main
def main(id_range_file: os.Path) = {
    val o = OWLManager.createOWLOntologyManager().loadOntology(IRI.create(id_range_file.toIO))
    val allMyFacets = mutable.ListBuffer.empty[MyFacet]
    for (dt <- o.getDatatypesInSignature().asScala) {
        val defs = o.getAxioms(dt)
        for (ax <- defs.asScala) { 
            val range = ax.getDataRange()
            val f = new MyFacet() 
            f.id = dt.toString()
            range.accept(new OWLDataRangeVisitor() {
                override
                def visit(owlDatatype: OWLDatatype) = ()
                override
                def visit(owlDataOneOf: OWLDataOneOf) =  ()
                override
                def visit(owlDataComplementOf: OWLDataComplementOf) =  ()
                override
                def visit(owlDataIntersectionOf: OWLDataIntersectionOf) = ()
                override
                def visit(owlDataUnionOf: OWLDataUnionOf) = ()
                override
                def visit(owlDatatypeRestriction: OWLDatatypeRestriction) = {
                    for (fr <- owlDatatypeRestriction.getFacetRestrictions().asScala) {
                        var i = fr.getFacetValue().parseInteger()
                        if(fr.getFacet().equals(OWLFacet.MIN_INCLUSIVE)) {
                            f.min = i
                        } else if(fr.getFacet().equals(OWLFacet.MAX_INCLUSIVE)) {
                            f.max = i
                        } else if(fr.getFacet().equals(OWLFacet.MIN_EXCLUSIVE)) {
                            i += 1
                            f.min = i
                        } else if(fr.getFacet().equals(OWLFacet.MAX_EXCLUSIVE)) {
                            i -= 1
                            f.max = i
                        } else {
                            log("Unknown range restriction: "+fr)
                        }
                    }
                }
            })
            log("Testing range: "+f)
            testFacetViolation(f,allMyFacets)
            allMyFacets.append(f)
        }
    }
}
def testFacetViolation(f: MyFacet , allMyFacets: collection.Seq[MyFacet]) = {
    for (f_p <- allMyFacets) {
        if (((f.min <= f_p.max) && (f_p.min <= f.max))) {
            throw new IllegalStateException(f + " overlaps with " + f_p + "!")
        }
    }
}
def log(o: Object) = {
    println(o.toString())
}
class MyFacet {
    var min: Int = _
    var max: Int = _
    var id: String = _
    override
    def toString(): String = {
        return "Facet{" + id + "}[min:" + min + " max:" + max + "]"
    }
}