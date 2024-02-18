import sys
import getopt
from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException

def print_help():
    help = "Options:\n"+\
    "--only-title \t\t Search keyword only in the title. By default, it searches the whole document.\n" + \
    "--hide-no-venue \t Hide publications that don\'t have a venue. Generally includes Book, Thesis, Citation...\n"+\
    "--journal \t\t Journal to search for\n"+\
    "--help \t\t\t Show this message\n"+\
    "--citations \t\t Show the publications that each publication is cited by\n"+\
    "--scraperapi \t\t To use ScraperAPI proxy, enter the API key. By default free proxy is used.\n"+\
    "Keyword operators: \n"+\
    "--and \t All the keywords should appear\n"+\
    "--or \t At least one of the keywords should appear\n"+\
    "--not \t Keywords should not appear\n"+\
    "--size \t Number of the publications to display (By default 10)\n"+\
    "\nSample commands:\n"+\
    "python3 collect.py --only-title --and \"game security\" --or \"cheat hack\" --not \"theory\" --journal ACM --size 10\n"+\
    "python3 collect.py --only-title --and \"Quick and scalable binary\" --hide-no-venue --citations --scraperapi 45aae6...989d92d\n"
    print(help)

def parse_command_line_arguments():
    arguments = sys.argv[1:]

    query = ""
    hide_no_venue = False
    size = 10
    retrieve_citations = False
    scraperapi_key = None

    try:
        opts, args = getopt.getopt(arguments, '',["citations", "scraperapi=", "only-title", "hide-no-venue", "help","journal=", "and=","or=","not=","size="])
 
        for opt, arg in opts:
            
            if opt in ["--scraperapi"]:
                scraperapi_key = arg
            elif opt in ["--citations"]:
                retrieve_citations = True
            elif opt in ["--hide-no-venue"]:
                hide_no_venue = True
            elif opt in ["--size"]:
                size = int(arg)
            elif opt in ["--help"]:
                print_help()
            elif opt in ["--only-title"]:
                query += "allintitle: "
            elif opt in ["--and"]:
                for str in arg.split():
                    query += str+" "
            elif opt in ["--or"]:
                for str in arg.split():
                    query += str+" OR "
                query = query[:-3]
            elif opt in ["--not"]:
                for str in arg.split():
                    query += "-"+str+" "
            elif opt in ["--journal"]:
                query += "source:"+arg+" "
    except Exception as e:
        print("Error. Check your input arguments.")
        raise e
    return query[:-1], hide_no_venue, size, retrieve_citations, scraperapi_key

def print_publication_bibliography(publication, prepend_tab=False):
    for key, value in publication['bib'].items():
        if prepend_tab: print("\t",end="")
        print(key +": ",end="")
        print(publication['bib'][key])

def print_publication_details(publication):
    for key, value in publication.items():
        print(key +": ",end="")
        print(publication[key])

def get_publication_venue(publication):
    return publication['bib']['venue']


def get_citations(publication):
    print("\tCited by:\n")
    
    try:
        citations = scholarly.citedby(publication)

        i=1
        while True:
            citation = next(citations)
            print("\tCitation #"+str(i))
            print_publication_bibliography(citation, True)
            print()
            i+=1
    except StopIteration:
        return
    except MaxTriesExceededException:
        print("Google blocked")
        return

def setup_proxy(scraperapi_key):
    pg=None
    success=False

    if scraperapi_key==None:
        print("Setting up free proxy")
        pg = ProxyGenerator()
        success = pg.FreeProxies()
        scholarly.use_proxy(pg)
    else:
        print("Setting up ScraperAPI proxy")
        pg = ProxyGenerator()
        success = pg.ScraperAPI(scraperapi_key)
        scholarly.use_proxy(pg)

    if success: print("Proxy Successful")
    else: print("Proxy Failed")
    print()


search_query, hide_no_venue, size, retrieve_citations, scraperapi_key = parse_command_line_arguments()

print("Search Query: \""+search_query+"\"\n")

if search_query=="":
    sys.exit()


setup_proxy(scraperapi_key)


query_results = scholarly.search_pubs(search_query)

print("Publications: \n")
for i in range(size):
    
    try:
        publication = next(query_results)
    except StopIteration:
        print("REACHED THE END!")
        break

    if hide_no_venue and get_publication_venue(publication)=="NA":
        continue
    
    print("Publication #"+str(i+1))
    print_publication_bibliography(publication)
    print()
    if retrieve_citations:
        get_citations(publication)
    print()
    

