# db file -> html pages (via template) -> styled (via css) -> 

import yaml, os, chevron, datetime
from PIL import Image
import PIL.ExifTags

class Builder:
    def __init__(self):
        self.add_photos()
        
        self.load_site()
        self.load_photos()

    def add_photos(self):
        for file in os.listdir('src/photos'):
            img = Image.open(f'src/photos/{file}')
            exif = img.getexif()
            img.thumbnail((640, 480))
            img.save(f'site/photos/{file}', exif=exif)
            os.remove(f'src/photos/{file}')

    def load_site(self):
        self.db = {}
        with open('src/site.yaml') as f:
            site = yaml.safe_load(f)

            for item in site:
                item_class = list(item.keys())[0]
                if item_class == 'Site':
                    self.db['Site'] = item['Site']
                    continue
                elif item_class == 'Issue':
                    item[item_class]['content'] = self.content_to_html(item[item_class]['content'])
                if item_class not in list(self.db.keys()):
                    self.db[item_class] = []
                self.db[item_class].append(item[item_class])

    def load_photos(self):
        self.db['Photo'] = []
        for file in os.listdir('site/photos'):
            img = Image.open(f'site/photos/{file}')
            exif = img.getexif()
            datetime_taken = datetime.datetime.strptime(exif.get(306), '%Y:%m:%d %H:%M:%S')
            desc = exif.get(0x010E)
            #print(timestamp)
            self.db['Photo'].append({
                'file': f'photos/{file}',
                'date': datetime_taken.strftime('%d/%m/%y %H:%M:%S'),
                'timestamp': datetime_taken.timestamp(),
                'desc': desc
                })
            
            self.db['Photo'].sort(key=lambda x: x['timestamp'], reverse=True)

    def build(self):
        self.build_page('index')
        for page in self.db['Site']['pages']:
            self.build_page(page['file'])

        for issue in self.db['Issue']:
            self.build_issue_page(issue)

    def build_page(self, page):
        with open(f'src/{page}.txt') as f:
            rendered = self.render_template(self.db, f.read())

        with open(f'site/{page}.html', 'w') as f:
            f.write(rendered)


    def build_issue_page(self, issue):
        with open(f'src/issue_template.txt') as f:
            rendered = self.render_template(issue, f.read())

        with open(f'site/issues/{issue["slug"]}.html', 'w') as f:
            f.write(rendered)

    def render_template(self, data, template):
        return chevron.render(template, data)


    def content_to_html(self, content):
        character_index = 0
        html = '<p>'
        while character_index < len(content):
            char = content[character_index]

            if char == '\\':
                character_index += 1
                form = content[character_index]
                character_index += 2
                arg = ''
                while content[character_index] != '}':
                    arg += content[character_index]
                    character_index += 1
                    
                if form == 'i':
                    html += f'<a href="../photos/{arg}"><img src="../photos/{arg}"></a>'
                elif form == 'b':
                    html += f'<b>{arg}</b>'
                elif form == 'i':
                    html += f'<i>{arg}</i>'

            elif char == '\n':
                html += '<br>'
            else:
                html += char
            character_index += 1

        html += '</p>'
        
        return html
        

#sdb = SiteDB()
#with open('src/site.txt') as f:
    #db.load(f)
#print(generate_issues(db.items['Issue']))

builder = Builder()
builder.build()


