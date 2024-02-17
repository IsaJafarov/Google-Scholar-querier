# Google-Scholar-querier

##### install dependencies

```sh
$ pip3 install scholarly
```
##### Help message
```sh
$ python3 collect.py --help
Options:
--only-title             Search keyword only in the title. By default, it searches the whole document.
--hide-no-venue          Hide publications that don\'t have a venue. Generally includes Book, Citation...
--journal                Journal to search for
--help                   Show this message
Keyword operators: 
--and    All the keywords should appear
--or     At least one of the keywords should appear
--not    Keywords should not appear
--size   Number of the publication to display (By default 10)

Sample command: python3 collect.py --only-title --and "game security" --or "cheat hack" --not "theory" --journal ACM --size 10

Search Query: ""
```
