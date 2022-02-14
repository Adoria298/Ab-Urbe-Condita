# inspired by https://mobile.twitter.com/Foone/status/1472833909477892098
# summary: AUC dates based on the founding date of the nearest city from Wikipedia
import geocoder
import wikipedia
from functools import cache
from pprint import pprint

def get_current_location(): #
    g = geocoder.ip("me")
    return g

@cache
def disambiguate_wiki(disamb_links, gc):
    temp_links = []
    # let's get rid of the most unlikely candidates
    for page in disamb_links:
        if gc.city not in page and gc.city not in summary:
            continue
        if ", " not in page:
            continue
        temp_links.append(page)
    ranking = {} 
    for page in temp_links:
        ranking[page] = 0
        try:
            summary = wikipedia.summary(page) 
        except wikipedia.exceptions.DisambiguationError as e:
            undisambed = disambiguate_wiki(e.options, gc)
            ranking[undisambed[0]] = undisambed[1]
        except wikipedia.exceptions.PageError:
            continue
        if "city" in summary and "was a city" not in summary:
            ranking[page] += 10
        if gc.city not in summary and gc.city not in page:
            continue
        if ", " in page:
            ranking[page] += 3
        if gc.city in page:
            ranking[page] += 5
        if gc.country in page:
            ranking[page] += 2
        if gc.state in page or gc.state in summary: # allows for England being in summary not titles
            ranking[page] += 2 # no counties
    top = max(ranking, key=lambda x: ranking[x])
    pprint(ranking)
    return top, ranking[top]

def get_wikipedia_article(gc):
    results = wikipedia.search(gc.city)
    if len(results) < 1:
        return wikipedia.page("Rome")
    elif len(results) == 1:
        return wikipedia.page(results[0])
    else: # disambiguate
        try:
            return wikipedia.page(disambiguate_wiki(results, gc)[0]) # .page raises below error if needed
        except wikipedia.exceptions.DisambiguationError as e:
            return wikipedia.page(disambiguate_wiki(e.options, gc)[0])

def get_founding_date(article):
    #TODO: get founding date from article by looking for "Founded"/"Settled"/"Incorporated" from the infobox
    #raise error if none found? or scan summary/history for one?
    # wptools may be useful here
    pass

if __name__ == "__main__":
    print(get_wikipedia_article(get_current_location()))

