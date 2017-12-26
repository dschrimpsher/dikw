import rdflib
from rdflib import Literal, Namespace
from rdflib.namespace import FOAF, RDF

data = rdflib.Graph()
information = rdflib.Graph()

result = data.parse("airline-customers-data.rdf", format="xml")

dataNS = Namespace("http://cablelabs.com/data/")
data.bind("foaf", FOAF)
data.bind("data", dataNS)

informationNS = Namespace("http://cablelabs.com/information/")
information.bind("information", informationNS)
information.bind("foaf", FOAF)

sumX = 0.0
sumW = 0.0
count = 0
# weights = [181.6,
#            197.1,
#            210.4,
#            173.3,
#            215.0,
#            163.9,
#            207.2,
#            215.3,
#            169.7,
#            208.8,
#            193.1,
#            175.1,
#            187.5,
#            190.8,
#            156.9,
#            217.6,
#            175.2,
#            233.6,
#            180.7,
#            185.9,
#            252.5,
#            168.3,
#            208.8,
#            204.3,
#            132.8,
#            214.6,
#            200.3,
#            157.5,
#            265.7,
#            190.3,
#            163.1]

for s, p, o in data.triples((None, dataNS.height, None)):
    # data.add((s, RDF.type, FOAF.person))
    # data.add((s, dataNS.weight, Literal(weights[count])))
    # print "%s is %s inches tall" % (s, o)
    sumX += float(o)
    count += 1

average = sumX / count
variance = 0.0

for s, p, o in data.triples((None, dataNS.height, None)):
    variance += (float(o) - average) ** 2

variance = variance / count
stddev = variance ** 0.5

count = 0
for s, p, o in data.triples((None, dataNS.weight, None)):
    # data.add((s, RDF.type, FOAF.person))
    # data.add((s, dataNS.weight, Literal(weights[count])))
    # print "%s is %s inches tall" % (s, o)
    sumW += float(o)
    count += 1

averageW = sumW / count
varianceW = 0.0

for s, p, o in data.triples((None, dataNS.weight, None)):
    varianceW += (float(o) - averageW) ** 2

varianceW = varianceW / count
stddevW= varianceW ** 0.5

information.add((informationNS.meanHeight, RDF.type, informationNS.statistic))
information.add((informationNS.meanHeight, informationNS.mean, Literal(average)))
information.add((informationNS.meanHeight, informationNS.stdDev, Literal(stddev)))

information.add((informationNS.meanWeight, RDF.type, informationNS.statistic))
information.add((informationNS.meanWeight, informationNS.mean, Literal(averageW)))
information.add((informationNS.meanWeight, informationNS.stdDev, Literal(stddevW)))

# canned information
information.add((informationNS.seats, RDF.type, informationNS.range))
information.add((informationNS.seats, informationNS.minimum, Literal(200)))
information.add((informationNS.seats, informationNS.maximum, Literal(240)))

# Serialize the store as RDF/XML file
information.serialize("airline-seats.rdf", format="pretty-xml", max_depth=3)
# data.serialize("airline-customers-data.rdf", format="pretty-xml", max_depth=3)
