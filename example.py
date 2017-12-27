import rdflib
from rdflib import Literal, Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD

data = rdflib.Graph()
information = rdflib.Graph()
knowledge = rdflib.Graph()

result = data.parse("airline-customers-data.rdf", format="xml")

dataNS = Namespace("http://cablelabs.com/data/")
data.bind("foaf", FOAF)
data.bind("data", dataNS)

informationNS = Namespace("http://cablelabs.com/information/")
information.bind("information", informationNS)
information.bind("foaf", FOAF)

knowledgeNS = Namespace("http://cablelabs.com/knowledge/")
knowledge.bind("knowledge", knowledgeNS)
knowledge.bind("foaf", FOAF)

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

information.add((informationNS.statistic, RDF.type, RDFS.Class))
information.add((informationNS.mean, RDF.type, RDF.Property))
information.add((informationNS.mean, RDFS.domain, informationNS.statistic))
information.add((informationNS.mean, RDFS.range, XSD.float))

information.add((informationNS.stdDev, RDF.type, RDF.Property))
information.add((informationNS.stdDev, RDFS.domain, informationNS.statistic))
information.add((informationNS.stdDev, RDFS.range, XSD.float))

information.add((informationNS.meanHeight, RDF.type, informationNS.statistic))
information.add((informationNS.meanHeight, informationNS.mean, Literal(average, datatype=XSD.float)))
information.add((informationNS.meanHeight, informationNS.stdDev, Literal(stddev, datatype=XSD.float)))

information.add((informationNS.meanWeight, RDF.type, informationNS.statistic))
information.add((informationNS.meanWeight, informationNS.mean, Literal(averageW, datatype=XSD.float)))
information.add((informationNS.meanWeight, informationNS.stdDev, Literal(stddevW, datatype=XSD.float)))

# canned information
information.add((informationNS.aircraft, RDF.type, RDFS.Class))

information.add((informationNS.maxLandingWeight, RDF.type, RDF.Property))
information.add((informationNS.maxLandingWeight, RDFS.domain, informationNS.aircraft))
information.add((informationNS.maxLandingWeight, RDFS.range, XSD.integer))

information.add((informationNS.breakEvenLoadFactor, RDF.type, RDF.Property))
information.add((informationNS.breakEvenLoadFactor, RDFS.domain, informationNS.aircraft))
information.add((informationNS.breakEvenLoadFactor, RDFS.range, XSD.integer))

information.add((informationNS.length, RDF.type, RDF.Property))
information.add((informationNS.length, RDFS.domain, informationNS.aircraft))
information.add((informationNS.length, RDFS.range, XSD.integer))

information.add((informationNS.aircraftType, RDF.type, RDF.Property))
information.add((informationNS.aircraftType, RDFS.domain, informationNS.aircraft))
information.add((informationNS.aircraftType, RDFS.range, XSD.string))

information.add((informationNS.e737, RDF.type, informationNS.aircraft))
information.add((informationNS.e737, informationNS.maxLandingWeight, Literal(52700, datatype=XSD.integer)))
information.add((informationNS.e737, informationNS.breakEvenLoadFactor, Literal(120, datatype=XSD.integer)))
information.add((informationNS.e737, informationNS.aircraftType, Literal('E737-800', datatype=XSD.string)))
information.add((informationNS.e737, informationNS.length, Literal(129, datatype=XSD.integer)))


minimumPassengers = int(information.value(informationNS.e737, informationNS.breakEvenLoadFactor))
passengerWeightMean = float(information.value(informationNS.meanWeight, informationNS.mean))
passengerWeightStdDev = float(information.value(informationNS.meanWeight, informationNS.stdDev))

length = int(information.value(informationNS.e737, informationNS.length))

knowledge.add((knowledgeNS.designDecision, RDF.type, RDFS.Class))
knowledge.add((knowledgeNS.legRoom, RDF.type, knowledgeNS.designDecision))

knowledge.add((knowledgeNS.maxLegRoom, RDF.type, RDF.Property))
knowledge.add((knowledgeNS.maxLegRoom, RDFS.domain, knowledgeNS.designDecision))
knowledge.add((knowledgeNS.maxLegRoom, RDFS.range, XSD.float))

knowledge.add((knowledgeNS.minLegRoom, RDF.type, RDF.Property))
knowledge.add((knowledgeNS.minLegRoom, RDFS.domain, knowledgeNS.designDecision))
knowledge.add((knowledgeNS.minLegRoom, RDFS.range, XSD.float))

chairSize = 2  # feet
maxLegRoom = length / (minimumPassengers / 6) - chairSize # 6 seats wide

knowledge.add((knowledgeNS.legRoom, knowledgeNS.maxLegRoom, Literal(maxLegRoom, datatype=XSD.integer)))

maxLandingWeight = int(information.value(informationNS.e737, informationNS.maxLandingWeight))
baggage = 25.0
maxPassengers = int(maxLandingWeight / (baggage + passengerWeightMean))

print maxLandingWeight
print passengerWeightMean
print maxPassengers

minLegRoom = length / (maxPassengers / 6) - chairSize # 6 seats wide

knowledge.add((knowledgeNS.legRoom, knowledgeNS.minLegRoom, Literal(minLegRoom, datatype=XSD.integer)))


# Serialize the store as RDF/XML file
information.serialize("airline-seats.rdf", format="pretty-xml", max_depth=3)
knowledge.serialize("airline-design-decisions.rdf", format="pretty-xml", max_depth=3)

# data.serialize("airline-customers-data.rdf", format="pretty-xml", max_depth=3)
