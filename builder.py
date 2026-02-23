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
        #this is all a little odd so i figure you deserve an explanation
        #photos are taken from the src/photos folder
        #converted to gifs with a palette
        #resized to 640x480
        #then copied to the site/photos folder
        #but....
        #because GIFS cant have exif data and i want to keep some of the metadata
        #we extract to parts of the metadata (the time the photo was taken and the desc)
        #however not all cameras store this info in the same place
        #first for datestring we look in DateTimeOriginal 
        #but if that doesnt exist we use DateTime
        #for desc first we look in ImageDescription
        #but if there isnt one we instead just use the camera model
        #and we store both of these in the GIF comment delimited with |
        for file in os.listdir('src/photos'):
            name, ext = file.split('.')
            img = Image.open(f'src/photos/{name}.{ext}')
            exif = img.getexif()
            img.thumbnail((640, 480))
            #img = img.convert(mode='P', palette=Image.Palette.ADAPTIVE, colors=128, dither=Image.Dither.FLOYDSTEINBERG)
            #date_str = date_str = exif.get_ifd(PIL.ExifTags.IFD.Exif)[36867]
            #if date_str is None:
                #exif.get(306)
            #desc = exif.get(270)
            #if desc is None:
                #desc = exif.get(272)
            #desc = desc.replace('\x00', '')
            #info = f'{date_str}|{desc}'
            img.save(f'site/photos/{name}.jpg', exif=exif)
            #os.remove(f'src/photos/{name}.{ext}')

    def get_info_from_exif(self, exif):
        date_str = date_str = exif.get_ifd(PIL.ExifTags.IFD.Exif)[36867]
        if date_str is None:
            exif.get(306)
        desc = exif.get(270)
        if desc is None:
            desc = exif.get(272)
        desc = desc.replace('\x00', '')
        return date_str, desc

    def load_site(self):
        self.db = {}
        with open('src/site.yaml', encoding='utf8') as f:
            site = yaml.safe_load(f)

            for item in site:
                item_class = list(item.keys())[0]
                if item_class == 'Site':
                    self.db['Site'] = item['Site']
                    continue
                if 'richcontent' in item[item_class]:
                    item[item_class]['content'] = self.content_to_html(item[item_class]['richcontent'])
                if item_class not in list(self.db.keys()):
                    self.db[item_class] = []
                self.db[item_class].append(item[item_class])

            self.db['Site']['status'] = f"{self.db['Update'][0]['date']} - {self.db['Update'][0]['title']}"

            #print(self.db['Site']['status']_

    def load_photos(self):
        self.db['Photo'] = []
        for file in os.listdir('site/photos'):
            img = Image.open(f'site/photos/{file}')
            date_string,desc = self.get_info_from_exif(img.getexif())
            datetime_taken = datetime.datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
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

        for project in self.db['Project']:
            self.build_project_page(project)

    def build_page(self, page):
        with open(f'src/{page}.txt', encoding='utf8') as f:
            rendered = self.render_template(self.db, f.read())

        with open(f'site/{page}.html', 'w', encoding='utf8') as f:
            f.write(rendered)


    def build_issue_page(self, issue):
        with open(f'src/issue_template.txt', encoding='utf8') as f:
            rendered = self.render_template(issue, f.read())

        with open(f'site/issues/{issue["slug"]}.html', 'w', encoding='utf8') as f:
            f.write(rendered)

    def build_project_page(self, project):
        with open(f'src/project_template.txt', encoding='utf8') as f:
            rendered = self.render_template(project, f.read())

        with open(f'site/projects/{project["slug"]}.html', 'w', encoding='utf8') as f:
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
                    html += f'<a href="../photos/{arg}" target="_blank"><img src="../photos/{arg}"></a>'
                elif form == 'b':
                    html += f'<b>{arg}</b>'
                elif form == 'e':
                    html += f'<i>{arg}</i>'
                elif form == 'l':
                    html += f'<a href="{arg}">{arg}</a>'

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


