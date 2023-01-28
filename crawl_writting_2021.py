import re
import requests
import json
from bs4 import BeautifulSoup
site = 'https://www.ieltsvietop.vn/blog/tong-hop-de-thi-ielts-writing-2021/'
response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')

a = soup.html.body
b = a.find('div',{'id':'content'})
c = b.find('article',{'id':'post-154088'})
d = c.find('div',{'class':'entry-content'})

#print(d.prettify())

container = d 

dictionary = { }
current_month = False 
current_date = False
state = False
current_topic = False
task1_has_pic = False
elements = container.find_all(['h3', 'h2', 'p','ol','li','figure','img'])
for element in elements:
    if element.name == "h2":
        print(element.get_text())
        dictionary[element.get_text()] = {}
        current_month = element.get_text()
    if element.name == "h3":
        current_date = element.get_text()
        if re.findall(r'\d{1,2}[-/.]\d{1,2}[-/.]\d{4}', current_date): 
            current_date = re.findall(r'\d{1,2}[-/.]\d{1,2}[-/.]\d{4}', current_date)[0]
            print(current_date)
            dictionary[current_month][current_date] = {}
        else:
            dictionary[current_month][current_date] = {}
    if  'Task 1:' in element.get_text(): 
        state = 'Task 1'
        dictionary[current_month][current_date][state] = {}
        dictionary[current_month][current_date][state]['question'] = []
        print(element.get_text())
        if element.get_text().replace('Task 1:','').strip() != '': 
            pass
        else : 
            dictionary[current_month][current_date][state]['question'].append(element.get_text().replace('Task 1:','').strip())
        task1_has_pic = False
    if 'Part 2:' in element.get_text() : 
        state = 'Task 2'
        task2 = element.get_text()
        task2=task2.replace('Part 2:','').strip()

        dictionary[current_month][current_date][state] = task2
        #print(element.get_text())
    elif 'Task 2:' in element.get_text(): 
        state = 'Task 2'
        task2 = element.get_text()
        task2=task2.replace('Task 2:','').strip()
        dictionary[current_month][current_date][state] = task2
    if element.name == 'img': 
        if state == 'Task 1':
            url = element['src']
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            if filename and task1_has_pic == False: 
                print(filename.group(1))
                with open(r'F:\Document\Python_files\crawl\crawl_ilet\task1_2021_writting_diagrams\\'+filename.group(1), 'wb') as f:
                    if 'http' not in url:
                        url = '{}{}'.format(site, url)
                    response = requests.get(url)
                    f.write(response.content) 
                    dictionary[current_month][current_date][state]['address'] = filename.group(1)
                    task1_has_pic = True
    else : 
        if state== 'Task 1': 
            if element.name == 'p' : 
                dictionary[current_month][current_date][state]['question'].append(element.get_text().replace('Task 1:','').strip())

# Serializing json
json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
 
# Writing to sample.json
with open("ieltswritting2021.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_object)   
# image_tags = soup.find_all('img')
# urls = [img['src'] for img in image_tags]
# for url in urls:
#     filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
#     if not filename:
#          print("Regular expression didn't match with the url: {}".format(url))
#          continue
#     with open(filename.group(1), 'wb') as f:
#         if 'http' not in url:
#             url = '{}{}'.format(site, url)
#         response = requests.get(url)
#         f.write(response.content)
# print("Download complete, downloaded images can be found in current directory!")