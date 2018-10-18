import requests
import bs4 
import re

@bot.on(events.NewMessage(outgoing=True,pattern='.imdb (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.imdb (.*)'))
async def imdb(e):
    movie_name = e.pattern_match.group(1)
    remove_space = movie_name.split(' ')
    final_name = '+'.join(remove_space)
    page = requests.get("https://www.imdb.com/find?ref_=nv_sr_fn&q="+final_name+"&s=all")
    lnk = str(page.status_code)
    soup = bs4.BeautifulSoup(page.content,'lxml')
    results = soup.findAll("td","result_text")
    mov_title = results[0].text
    mov_link = "http://www.imdb.com/"+results[0].a['href'] 
    page1 = requests.get(mov_link)
    soup = bs4.BeautifulSoup(page1.content,'lxml')
    story_line = soup.find('div', "inline canwrap")
    story_line = story_line.findAll("p")[0].text
    info = soup.findAll('div', "txt-block")
    for node in info:
      a = node.findAll('a')
      for i in a:
        if "country_of_origin" in i['href']:
          mov_country = i.string
    for node in info:
      a = node.findAll('a')
      for i in a:
        if "primary_language" in i['href']:
          mov_language = i.string
    rating = soup.findAll('div',"ratingValue")
    for r in rating:
      mov_rating = r.strong['title']
    await e.respond('**Title : **`'+mov_title+'`\n**Rating : **`'+mov_rating+'`\n**Country : **`'+mov_country+'`\n**Language : **`'+mov_language+'`\n**IMDB Url : **`'+mov_link+'`\n**Story Line : **`'+story_line+'`')
