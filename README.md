# Google-Scholar-querier

##### Install dependencies

```sh
$ pip3 install scholarly
```
##### Help message
```sh
$ python3 collect.py --help
Options:
--only-title             Search keyword only in the title. By default, it searches the whole document.
--hide-no-venue          Hide publications that don\'t have a venue. Generally includes Book, Thesis, Citation...
--journal                Journal to search for
--help                   Show this message
--citations              Show the publications that each publication is cited by
--scraperapi             To use ScraperAPI proxy, enter the API key. By default free proxy is used.
Keyword operators: 
--and    All the keywords should appear
--or     At least one of the keywords should appear
--not    Keywords should not appear
--size   Number of the publications to display (By default 10)

Sample commands:
python3 collect.py --only-title --and "game security" --or "cheat hack" --not "theory" --journal ACM --size 10
python3 collect.py --only-title --and "Quick and scalable binary" --hide-no-venue --citations --scraperapi 45aae6...989d92d

Search Query: ""
```
