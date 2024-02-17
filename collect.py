import sys
import getopt
from scholarly import scholarly, ProxyGenerator

def print_help():
    help = "Options:\n"+\
    "--only-title \t\t Search keyword only in the title. By default, it searches the whole document.\n" + \
    "--hide-no-venue \t Hide publications that don\'t have a venue. Generally includes Book, Citation...\n"+\
    "--journal \t\t Journal to search for\n"+\
    "--help \t\t\t Show this message\n"+\
    "Keyword operators: \n"+\
    "--and \t All the keywords should appear\n"+\
    "--or \t At least on of the keywords should appear\n"+\
    "--not \t Keywords should not appear\n"+\
    "--size \t Number of the publications to display (By default 10)\n"+\
    "\nSample command: python3 collect.py --only-title --and \"game security\" --or \"cheat hack\" --not \"theory\" --journal ACM --size 10\n"
    print(help)

def parse_command_line_arguments():
    arguments = sys.argv[1:]

    query = ""
    hide_no_venue = False
    size = 10
    try:
        opts, args = getopt.getopt(arguments, '',["only-title", "hide-no-venue", "help","journal=", "and=","or=","not=","size="])
        for opt, arg in opts:
            
            if opt in ["--hide-no-venue"]:
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
    except:
        print("Error")
    return query[:-1], hide_no_venue, size

def print_publication_bibliography(publication):
    for key, value in publication['bib'].items():
        print(key +": ",end="")
        print(publication['bib'][key])

def print_publication_details(publication):
    for key, value in publication.items():
        print(key +": ",end="")
        print(publication[key])

def get_publication_venue(publication):
    return publication['bib']['venue']


search_query, hide_no_venue, size = parse_command_line_arguments()

print("Search Query: \""+search_query+"\"\n")

if search_query=="":
    sys.exit()

pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)

query_results = scholarly.search_pubs(search_query)

print("Publications: ")
for i in range(size):
    
    try:
        publication = next(query_results)
    except StopIteration:
        print("REACHED THE END!")
        break

    if hide_no_venue and get_publication_venue(publication)=="NA":
        continue
    
    print(str(i)+".")
    print_publication_bibliography(publication)
    print()
