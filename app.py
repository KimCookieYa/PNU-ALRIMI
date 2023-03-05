from flask import Flask, render_template, json, request, jsonify
from pymongo import MongoClient
import feedparser as fp
from datetime import date

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbalrimi


### Home
@app.route('/')
def home():
    return render_template('index.html')


### get new post
@app.route('/get/newpost', methods=['POST'])
def getNewPost():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content = content.replace("\n","")
    print(content)
    if content == u"오늘의 메뉴":
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "테스트입니다."
                        }
                    }
                ]
            }
        }
    else:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "error입니다."
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)


def crawlingRSS(url):
    content = fp.parse(url)
    data = []
    for entry in content.entries:
        pubDate = entry.published.split()[0]
        todayDate = date.today().strftime("%Y-%m-%d")
        todayDate = "2023-03-02"
        if pubDate == todayDate:
            print(pubDate, todayDate)
            data += [[entry.title, entry.link, entry.published]]
    #print(data)
        
    return data


### 웹크롤링
@app.route('/get/newpostonweb', methods=['POST'])
def getNewPostOnWeb():
    major = request.form.get('major')
    
    urls = db.pnumajor.find_one({'major': major})
    if urls is None:
        return jsonify({'result': 'missing'})

    pre = urls['pre_url']
    post = urls['post_url']
    newposturl = []
    for i in range(4):
        num = urls['url'+str(i+1)]
        if num != '':
            url = pre + num + post
            newposturl += crawlingRSS(url)
    #print(newposturl)
    return jsonify({'result': 'success', 'data': newposturl})


### 새 전공과 홈페이지rss 주소 저장
@app.route('/post/newmajor', methods=['POST'])
def saveNewMajor():
    major = request.form.get('major')
    pre = request.form.get('pre_url')
    url1 = request.form.get('url1')
    url2 = request.form.get('url2')
    url3 = request.form.get('url3')
    url4 = request.form.get('url4')
    url5 = request.form.get('url5')
    post = request.form.get('post_url')
    
    db.pnumajor.insert_one({'major': major, 'pre_url': pre, 'url1': url1, 'url2': url2, 'url3': url3, 'url4': url4, 'url5': url5, 'post_url': post})
    
    return jsonify({'result': 'success'})
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)