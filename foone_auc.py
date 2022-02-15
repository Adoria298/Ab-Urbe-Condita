# inspired by https://mobile.twitter.com/Foone/status/1472833909477892098
# summary: AUC dates based on the founding date of the nearest city from Wikipedia
import geocoder
import wikipedia

def get_current_location(): #
    g = geocoder.ip("me")
    return g

def disambiguate_wiki(disamb_links, gc) -> str and int: # str is the page and int is its ranking for recursion
    temp_links = []
    # let's get rid of the most unlikely candidates
    for page in disamb_links:
        if gc.city not in page:
            continue
        if ", " not in page:
            continue
        temp_links.append(page)
    if len(temp_links) == 1:
        return temp_links[0], 1000
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
        wpage = wikipedia.page(page) # try and load the page here to check the coordinates
        wlat, wlong = wpage.coordinates
        lat, long = gc.latlng
        if int(lat) - 2 > int(wlat) or int(wlat) > int(lat) + 2: # convert to int to slightly increase range
            ranking[page] -= 1000
        if int(long) - 2 > int(wlong) or int(wlong) > int(long) + 2:
            ranking[page] -= 1000
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
    #pprint(ranking)
    return top, ranking[top]

def get_wikipedia_article(gc):
    latitude, longitude = gc.latlng
    results = wikipedia.geosearch(latitude=latitude, longitude=longitude)
    try:
        if len(results) < 1:
            return wikipedia.page("Rome")
        elif len(results) == 1:
            return wikipedia.page(results[0]) # .page raises DisambiguationError if needed
        else:
            raise wikipedia.exceptions.DisambiguationError(gc.city, results) # used to avoid code reuse
    except wikipedia.exceptions.DisambiguationError as e:
        wpage = disambiguate_wiki(e.options, gc)
        return wikipedia.page(wpage[0])

def get_founding_date(article: wikipedia.WikipediaPage) -> int:
    #TODO: get founding date from article by looking for "Founded"/"Settled"/"Incorporated" from the infobox
    # returns positive for A.D. years and negative for B.C. years
    # remember there is no year zero!
    # returns -752 (752 B.C) if none is found
    # wptools may be useful here
    city = article.title
    print(f"put te in {city} esse.") #TODO: add macrons
    return -752 # Rome's founding date so the default for AUC if all else fails

if __name__ == "__main__":
    print(get_wikipedia_article(get_current_location()))

