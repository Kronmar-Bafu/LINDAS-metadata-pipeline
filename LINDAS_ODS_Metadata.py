from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF
from dateutil.parser import parse
import yaml
from datetime import datetime


#instantiate namespace
schema = Namespace("http://schema.org/")
dcat = Namespace("http://www.w3.org/ns/dcat#")
dct = Namespace("http://purl.org/dc/terms/")

#parse input
with open("input_Form.yml", "rt", encoding='utf8') as yml_input:
    input_data = yaml.load(yml_input, yaml.Loader)
    
try:
    with open("ODS_Form.yml", "rt", encoding='utf8') as ods_input:
        ODS_data = yaml.load(ods_input, yaml.Loader)
    if ODS_data.get("identifier"):
        ODS_flag = True
    else:
        ODS_flag = False
        print("No opendata.swiss metadata was provided")
except(FileNotFoundError):
    print("No opendata.swiss metadata form was provided")



#instantiate graph
g = Graph()

#could add the option to read an existing graph (for example a generated cube constraint and observation set)

#set dataset URI to attach metadata to
dataset_URL = input_data.get("dataset-URI")
if dataset_URL[-1] != "/":
    dataset_URL = dataset_URL+"/"
dataset = URIRef(dataset_URL)
g.add((dataset, RDF.type, schema.Dataset))
if ODS_flag:
    g.add((dataset, RDF.type, dcat.Dataset))

#for each metadata point the following steps need to be checked through
# 1. get from dict
# 2. check rough conformance of datatype if possible
# 3. assign URIRef or Literal
# 4. write triples

#name
name_DE = input_data.get("name_DE")
if name_DE:
    de_name = Literal(name_DE.strip(), lang="de")
    g.add((dataset, schema.name, de_name))
    if ODS_flag:
        g.add((dataset, dct.title, de_name))
else:
    print("Missing German dataset name")
name_FR = input_data.get("name_FR")
if name_FR:
    fr_name = Literal(name_FR.strip(), lang="fr")
    g.add((dataset, schema.name, fr_name))
    if ODS_flag:
        g.add((dataset, dct.title, fr_name))
else:
    print("Missing French dataset name")
name_IT = input_data.get("name_IT")
if name_IT:
    it_name = Literal(name_IT.strip(), lang="it")
    g.add((dataset, schema.name, it_name))
    if ODS_flag:
        g.add((dataset, dct.title, it_name))
else:
    print("Missing Italian dataset name")
name_EN = input_data.get("name_EN")
if name_EN:
    en_name = Literal(name_EN.strip(), lang="en")
    g.add((dataset, schema.name, en_name))
    if ODS_flag:
        g.add((dataset, dct.title, en_name))
else:
    print("Missing English dataset name")
description_DE = input_data.get("description_DE")
if description_DE:
    de_description = Literal(description_DE.strip(), lang="de")
    g.add((dataset, schema.description, de_description))
    if ODS_flag:
        g.add((dataset, dct.description, de_description))
else:
    print("Missing German dataset description")
description_FR = input_data.get("description_FR")
if description_FR:
    fr_description = Literal(description_FR.strip(), lang="fr")
    g.add((dataset, schema.description, fr_description))
    if ODS_flag:
        g.add((dataset, dct.description, fr_description))
else:
    print("Missing French dataset description")
description_IT = input_data.get("description_IT")
if description_IT:
    it_description = Literal(description_IT.strip(), lang="it")
    g.add((dataset, schema.description, it_description))
    if ODS_flag:
        g.add((dataset, dct.description, it_description))
else:
    print("Missing Italian dataset description")
description_EN = input_data.get("description_EN")
if description_EN:
    en_description = Literal(description_EN.strip(), lang="en")
    g.add((dataset, schema.description, en_description))
    if ODS_flag:
        g.add((dataset, dct.description, en_description))
else:
    print("Missing English dataset description")

#contact point
contact_name = input_data.get("contact-point name")
contact_mail = input_data.get("contact-point email")
if contact_name and contact_mail:
    if "@" in contact_mail:
        contact_point = BNode()
        con_name = Literal(contact_name)
        con_mail = Literal(contact_mail)
        g.add((dataset, schema.contactPoint, contact_point))
        g.add((contact_point, schema.name, con_name))
        g.add((contact_point, schema.email, con_mail))
        if ODS_flag:
            ODS_contact = BNode()
            g.add((dataset, dcat.contactPoint, ODS_contact))
            g.add((ODS_contact, RDF.type, URIRef("http://www.w3.org/2006/vcard/ns#Organization")))
            g.add((ODS_contact, URIRef("http://www.w3.org/2006/vcard/ns#fn"), con_name))
            g.add((ODS_contact, URIRef("http://www.w3.org/2006/vcard/ns#hasEmail"), con_mail))
    else:
        print("Contact point email address is not in correct format")
elif contact_name:
    print("Contact Point email address is missing")
else:
    print("Contact Point name is missing")

#dates: to be tested using datetime
date_format = "%Y-%m-%d"

#creation date
creation_date = input_data.get("source creation-date")
if creation_date:
    try: 
        datetime.strptime(str(creation_date), date_format)
        cre_date = Literal(creation_date, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))
        g.add((dataset, schema.dateCreated, cre_date))
    except(ValueError):
        print("creation date is not formatted as xsd:date")
else:
    print("Missing source creation date")

#modification date
modification_date = input_data.get("source modification-date")
if modification_date:
    try: 
        parse(str(modification_date))
        mod_date = Literal(modification_date, datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime'))
        g.add((dataset, schema.dateModified, mod_date))
        if ODS_flag:
            g.add((dataset, dct.modified, mod_date))
    except(ValueError):
        print("modification date is not formatted as xsd:dateTime")
else:
    print("Missing source modification date")

#publication date
publication_date = input_data.get("dataset publication-date")
if publication_date:
    try: 
        datetime.strptime(str(publication_date), date_format)
        pub_date = Literal(publication_date, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))
        g.add((dataset, schema.datePublished, pub_date))
        if ODS_flag:
            issue_date = parse(str(publication_date))
            g.add((dataset, dct.issued, Literal(issue_date, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))))
    except(ValueError):
        print("publication date is not formatted as xsd:date")
else:
    print("Missing dataset publication date")
    
#work example application
work_example_app = input_data.get("work example application").split(";")
for app in work_example_app:
    if app.strip() == "visualize":
        visualize_link = URIRef("https://ld.admin.ch/application/visualize")
        g.add((dataset, schema.workExample, visualize_link))
        #could also be made redundant if automatically added when there is a visualize work example. Left for now in case there are datasets that are on visualize without providing a work example URL
    elif app.strip() == "opendata.swiss":
        ODS_link = URIRef("https://ld.admin.ch/application/opendataswiss")
        g.add((dataset, schema.workExample, ODS_link))
        #possibly this metadata can be used to determine whether ODS metadata should be added or there could be a separate field in the YAML form for whether ODS publication is desired, which automatically adds this triple as well
    else:
        if app.strip():
            other_app_URI = URIRef("https://ld.admin.ch/application/"+app.strip())
            g.add((dataset, schema.workExample, other_app_URI))
        else:
            pass
        #work example application YAML form field is still required even if the main two applications would be automatically added elsewhere in case of other custom applications

#work example visualize
visualize_URL = input_data.get("work example visualize")
if visualize_URL:
    if "https://visualize.admin.ch/" in visualize_URL:
        visualize_example = Literal(visualize_URL)
        visualize_BN = BNode()
        g.add((dataset, schema.workExample, visualize_BN))
        g.add((visualize_BN, schema.url, visualize_example))
        g.add((visualize_BN, schema.name, Literal("visualize.admin.ch", lang="de")))
        g.add((visualize_BN, schema.name, Literal("visualize.admin.ch", lang="fr")))
        g.add((visualize_BN, schema.name, Literal("visualize.admin.ch", lang="it")))
        g.add((visualize_BN, schema.name, Literal("visualize.admin.ch", lang="en")))
        #This is how Cube Creator formats it, but is it really necessary to add 4 triples with different language tags for the same string?
        g.add((visualize_BN, schema.encodingFormat, Literal("text/html", datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))))
        g.add((visualize_BN, RDF.type, schema.CreativeWork))
        if visualize_link:
            pass
        else:
            visualize_link = URIRef("https://ld.admin.ch/application/visualize")
            g.add((dataset, schema.workExample, visualize_link))
    else:
        print("Visualize work example link is not correctly formatted")
else:
    print("Visualize work example link is missing")
    
#work example SPARQL endpoint
example_sparql = input_data.get("work example SPARQLendpoint")
if example_sparql:
    if "https://lindas.admin.ch/sparql/" in example_sparql:
        sparql_work = Literal(example_sparql)
        sparql_BN = BNode()
        g.add((dataset, schema.workExample, sparql_BN))
        g.add((sparql_BN, schema.url, sparql_work))
        g.add((sparql_BN, schema.name, Literal("SPARQL Endpoint mit Vorauswahl des Graph", lang="de")))
        g.add((sparql_BN, schema.name, Literal("SPARQL Endpoint avec présélection du graphe", lang="fr")))
        g.add((sparql_BN, schema.name, Literal("SPARQL Endpoint con preselezione del grafo", lang="it")))
        g.add((sparql_BN, schema.name, Literal("SPARQL Endpoint with graph preselection", lang="en")))
        g.add((sparql_BN, schema.encodingFormat, Literal("application/sparql-query", datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))))
        g.add((sparql_BN, RDF.type, schema.CreativeWork))
    else:
        print("SPARQL work example link is not correctly formatted")
else:
    print("SPARQL work example link is missing")

#SPARQL endpoint
sparql_url = input_data.get("SPARQL endpoint")
if sparql_url:
    sparql_end = Literal(sparql_url)
    end_prop = URIRef("http://rdfs.org/ns/void#sparqlEndpoint")
    g.add((dataset, end_prop, sparql_end))
else:
    print("SPARQL endpoint is missing")
    
#optional metadata
creator = input_data.get("dataset creator") 
if creator:
    if "http" in creator:
        creator_URI = URIRef(creator)
        g.add((dataset, schema.creator, creator_URI))
    else:
        print("dataset creator not formatted correctly")
else:
    print("Optional: no dataset creator provided")
contributor = input_data.get("dataset contributor")
if contributor:
    if "http" in contributor:
        contributor_URI = URIRef(contributor)
        g.add((dataset, schema.contributor, contributor_URI))
    else:
        print("dataset contributor not formatted correctly")
else:
    print("Optional: no dataset contributor provided") 
publisher = input_data.get("dataset publisher")
if publisher:
    if "http" in publisher:
        publisher_URI = URIRef(publisher)
        g.add((dataset, schema.publisher, publisher_URI))
    else:
        print("dataset publisher not formatted correctly")
else:
    print("Optional: no dataset publisher provided") 

next_modification = input_data.get("next modification date") 
if next_modification:
    try: 
        datetime.strptime(str(next_modification), date_format)
        next_mod = Literal(next_modification, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))
        g.add((dataset, URIRef("https://schema.ld.admin.ch/datasetNextDateModified"), next_mod))
    except(ValueError):
        print("next modification date is not formatted as xsd:dateTime")
    
else:
    print("Optional: no next modification date provided")

example_resource = input_data.get("example resource")
if example_resource:
    data_URI = "/".join(dataset_URL.split("/")[:3])
    if data_URI in example_resource:
        g.add((dataset, URIRef("https://schema.ld.admin.ch/exampleResource"), URIRef(example_resource)))
else:
    print("Optional: no example resource provided")
    
# ODS metadata
if ODS_flag:
    ID = ODS_data.get("identifier")
    if "@" in ID:
        g.add((dataset, dct.identifier, Literal(ID)))
    else: print("opendata.swiss identifier not formatted correctly")
   
    creator_ODS = ODS_data.get("creator")
    if creator_ODS:
        if "https://register.ld.admin.ch/opendataswiss/org" in creator_ODS:
            g.add((dataset, dct.creator, URIRef(creator_ODS)))
            if not creator:
                g.add((dataset, schema.creator, URIRef(creator_ODS)))
            else: pass
        else: print("opendata.swiss creator was not formatted correctly")
    else: print("opendata.swiss creator missing")
    publisher_ODS = ODS_data.get("publisher")
    if publisher_ODS:
        g.add((dataset, dct.publisher, Literal(publisher_ODS)))
    else: print("opendata.swiss publisher missing")
    license_ODS = ODS_data.get("license")
    #this script follows the current implementation of "dct:license" on LINDAS rather than the ideal description in the DCAT-AP handbook
    if license_ODS:
        if "https://" and "fedlex" and ".admin.ch" in license_ODS:
            g.add((dataset, dct.rights, URIRef(license_ODS)))
        else: print("opendata.swiss license not formatted correctly")
    else: print("opendata.swiss license missing")
    
    rights = ODS_data.get("rights")
    #this script follows the current implementation of "dct:rights" on LINDAS rather than the ideal description in the DCAT-AP handbook
    if rights:
        if "https://ld.admin.ch/vocabulary/TermsOfUse" in rights:
            g.add((dataset, dct.rights, URIRef(rights)))
        else: print("opendata.swiss rights not formatted correctly")
    else: print("opendata.swiss rights missing")
    
    accrual = ODS_data.get("accrual periodicity")
    if accrual:
        if "http://publications.europa.eu/resource/authority/frequency" in accrual:
            g.add((dataset, dct.accrualPeriodicity, Literal(accrual)))
        else: print("opendata.swiss accrual periodicity not formatted correctly")
    else: print("opendata.swiss accrual periodicity missing")
    
    themes = ODS_data.get("themes").split(";")
    if themes[0]:
        for theme in themes:
            if not theme:
                pass
            elif "https://register.ld.admin.ch/opendataswiss/category/" in theme.strip():
                    g.add((dataset, dcat.theme, URIRef(theme.strip())))
            else: print("opendata.swiss theme was not formatted correctly")
    else: print("opendata.swiss theme was not provided")
    keys_DE = ODS_data.get("keywords_DE").split(";")
    if keys_DE[0]:
        for key_DE in keys_DE:
            if key_DE.strip():
                g.add((dataset, dcat.keyword, Literal(key_DE.strip(), lang="de")))
            else: pass
    else: print("opendata.swiss german keywords were not provided")      
    keys_FR = ODS_data.get("keywords_FR").split(";")
    if keys_FR[0]:
        for key_FR in keys_FR:
            if key_FR.strip():
                g.add((dataset, dcat.keyword, Literal(key_FR.strip(), lang="fr")))
            else: pass
    else: print("opendata.swiss french keywords were not provided")  
    keys_IT = ODS_data.get("keywords_IT").split(";")
    if keys_IT[0]:
        for key_IT in keys_IT:
            if key_IT.strip():
                g.add((dataset, dcat.keyword, Literal(key_IT.strip(), lang="it")))
            else: pass    
    else: print("opendata.swiss italian keywords were not provided")  
    keys_EN = ODS_data.get("keywords_EN").split(";")
    if keys_EN[0]:
        for key_EN in keys_EN:
            if key_EN.strip():
                g.add((dataset, dcat.keyword, Literal(key_EN.strip(), lang="en")))
            else: pass
    else: print("opendata.swiss english keywords were not provided")
    
    langs = ODS_data.get("language").split(";")
    if langs[0]:
        for language in langs:
            if language:
                language = language.strip()
                g.add((dataset, dct.language, Literal(language, lang=language)))
            else: pass 
    else: print("opendata.swiss languages missing")

    page = ODS_data.get("landing page")
    if not page: print("opendata.swiss landing page missing")
    elif "https://" in page:
        g.add((dataset, dcat.landingPage, URIRef(page)))
    else: print("opendata.swiss landing page not formatted correctly")

    docu = ODS_data.get("documentation").split(";")
    if docu[0]:
        for doc in docu:
            if not doc: pass
            else: 
                g.add((dataset, URIRef("http://xmlns.com/foaf/0.1/page"), Literal(doc.strip(), datatype="http://xmlns.com/foaf/0.1/Document")))
    else: 
        print("Optional: no opendata.swiss documentation pages provided")
    
    rel_res = ODS_data.get("related resource").split(";")
    if rel_res[0]:
        for res in rel_res:
            if not res: pass
            elif "https://" in res:
                g.add((dataset, dct.relation, Literal(res.strip(), datatype="http://www.w3.org/2000/01/rdf-schema#Resource")))
            else: print("Optional: opendata.swiss related resource not formatted correctly")
    else: print("Optional: no opendata.swiss related resource provided")
    
    qual_rel = ODS_data.get("qualified relation").split(";")
    if qual_rel[0]:
        for rel in qual_rel:
            if not rel: pass
            elif "https://" in rel:
                rel_BN = BNode()
                g.add((dataset, dcat.qualifiedRelation, rel_BN))
                g.add((rel_BN, RDF.type, dcat.Relationship))
                g.add((rel_BN, dcat.hadRole, schema.sameAs))
                g.add((rel_BN, dct.relation, Literal(rel.strip(), datatype="http://www.w3.org/2000/01/rdf-schema#Resource")))
            else: print("Optional: opendata.swiss qualified relation not formatted correctly")
    else: print("Optional: no opendata.swiss qualified relation provided")
    
    temp_start = ODS_data.get("temporal start").split(";")
    if temp_start[0]:
        for tem_sta in temp_start:
            if not tem_sta: pass
            try: 
                datetime.strptime(str(tem_sta).strip(), date_format)
                g.add((dataset, schema.dateCreated, Literal(tem_sta, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))))
            except(ValueError):
                print("Optional: opendata.swiss temporal start not formatted correctly")
    else: print("Optional: no opendata.swiss temporal start provided")
    temp_end = ODS_data.get("temporal end").split(";")
    if temp_end[0]:
        for tem_end in temp_end:
            if not tem_end: pass
            try: 
                datetime.strptime(str(tem_end).strip(), date_format)
                g.add((dataset, schema.dateCreated, Literal(tem_end, datatype=URIRef('http://www.w3.org/2001/XMLSchema#date'))))
            except(ValueError):
                print("Optional: opendata.swiss temporal end not formatted correctly")
    else: print("Optional: no opendata.swiss temporal end provided")
    
    spatial = ODS_data.get("spatial")
    if spatial:
        g.add((dataset, dct.spatial, Literal(spatial, lang = "en")))
    else: print("Optional: opendata.swiss spatial information missing")

if name_DE: filename= name_DE.replace(" ", "_").replace(":","")+".ttl"
elif name_FR: filename= name_FR.replace(" ", "_").replace(":","")+".ttl"
elif name_IT: filename= name_IT.replace(" ", "_").replace(":","")+".ttl"
else: filename= name_EN.replace(" ", "_").replace(":","")+".ttl"
g.serialize(destination=filename)
