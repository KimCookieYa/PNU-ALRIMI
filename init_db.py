from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbalrimi

db.pnumajor.insert_one({'major': '정보컴퓨터공학부',
                        "pre_url": "https://cse.pusan.ac.kr/bbs/cse/",
                        "url1": "2605",
                        "url2": "2616",
                        "url3": "12278",
                        "url4": "2617",
                        "url5": "2618",
                        "post_url": "/rssList.do?row=10"})
db.pnumajor.insert_one({'major': '전기공학과',
                        "pre_url": "https://eec.pusan.ac.kr/bbs/eehome/",
                        "url1": "2650",
                        "url2": "2654",
                        "url3": "2655",
                        "url4": "",
                        "url5": "",
                        "post_url": "/rssList.do?row=10"})