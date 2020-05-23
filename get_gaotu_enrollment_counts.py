import json
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'https://m.gaotu100.com',
    'Accept-Language': 'en-US,en;q=0.9',
}
params = {
    'page_number': 1,
    'query_word': '\u8BED\u6587',
    'page_size': '50',
    'track_id': '0',
}

def is_more(j):
    info = j['course_search_v_o']
    if len(info) == 0 or 'courses' not in info or info['pager']['count'] == 0 or info['pager']['count'] < info['pager']['page_size']:
        return False
    return True

def parse(j):
    info = j['course_search_v_o']
    r = {}
    if len(info) > 0 and "courses" in info:
        courses = info["courses"]
        for c in courses:
            r[c["clazz_id"]] = c
    return r

def search_class(word):
    p = dict(params)
    p['query_word'] = word
    p['page_number'] = 1
    has_more = True
    r = {}
    while has_more:
        response = requests.get('https://api.gaotu100.com/teacher/search', headers=headers, params=p, timeout=(10, 30))
        j = response.json()
        r.update(parse(j))
        has_more = is_more(j)
        p['page_number'] = p['page_number'] + 1
    return r

query_words = [
    u'一年级',
    u'二年级',
    u'三年级',
    u'四年级',
    u'五年级',
    u'六年级',
    u'七年级',
    u'八年级',
    u'九年级',
    u'高一',
    u'高二',
    u'高三',
    u'高考',
    u'语文',
    u'数学',
    u'英语',
    u'物理',
    u'化学',
    u'高分',
    u'生物',
    u'政治',
    u'历史',
    u'地理',
    u'春',
    u'暑',
    u'秋',
    u'冬',
]

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get'https://api.gaotu100.com/teacher/search?page_number=8&query_word=%E8%AF%AD%E6%96%87&page_size=10&track_id=0', headers=headers)

from datetime import datetime
import json

print("Getting all enrollment data from gaotu... ")

all_classes = {}
for word in query_words:
    print("\t\t Using keyword  " + word + " ... " + ". Discovered courses so far: " + str(len(all_classes)))
    classes = search_class(word)
    all_classes.update(classes)

filename = "gaotu100-enrollment-" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".json"
print("Dump all data to " + filename)

# sort for better diff.
sorted_dict = {k: all_classes[k] for k in sorted(all_classes)}
with open(filename, "w") as f:
    json.dump(sorted_dict, f, indent=2, ensure_ascii=False)
