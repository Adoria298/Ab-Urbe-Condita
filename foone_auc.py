# inspired by https://mobile.twitter.com/Foone/status/1472833909477892098
# summary: AUC dates based on the founding date of the nearest city from Wikipedia
import geocoder
import wikipedia
from pprint import pprint

def get_current_location(): #
    g = geocoder.ip("me")
    return g

def disambiguate_wiki(disamb_links, gc):
    ranking = {}
    for page in disamb_links:
        ranking[page] = 0
        if "disambiguation" in page:
            summary = ""
        else:
            summary = wikipedia.summary(page) 
        if "city" in summary and "was a city" not in summary:
            ranking[page] += 10
        if ", " in page:
            ranking[page] += 3
        if gc.city in page:
            ranking[page] += 5
        if gc.country in page:
            ranking[page] += 2
        if gc.state in page:
            ranking[page] += 2 # no counties
    top = max(ranking, key=lambda x: ranking[x])
    pprint(ranking)
    return top

def get_wikipedia_article(gc):
    results = wikipedia.search(gc.city)
    if len(results) < 1:
        return wikipedia.page("Rome")
    elif len(results) == 1:
        return wikipedia.page(results[0])
    else: # disambiguate
        try:
            return wikipedia.page(disambiguate_wiki(results, gc)) # .page raises below error if needed
        except wikipedia.exceptions.DisambiguationError as e:
            return wikipedia.page(disambiguate_wiki(e.options, gc))

def get_founding_date(article):
    #TODO: get founding date from article by looking for "Founded"/"Settled"/"Incorporated" from the infobox
    #raise error if none found? or scan summary/history for one?
    # wptools may be useful here
    pass

if __name__ == "__main__":
    print(get_wikipedia_article(get_current_location()))

