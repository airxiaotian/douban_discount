import requests_html
import time
import json
import threading
from db_utils import get_all_questions, get_question, save_questions

from model import CustomJSONEncoder, Discount
from model import Question

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5',
    'Connection': 'keep-alive',
    'Cookie': 'bid=ND8gm1cMh6Y; douban-fav-remind=1; __utmc=30149280; __utmz=30149280.1699185795.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ap_v=0,6.0; ll="108169"; push_doumail_num=0; __utmv=30149280.12599; push_noty_num=0; dbcl2="125995854:0d74hJ7W/m0"; ck=SwQM; __utma=30149280.241191094.1699185795.1699236283.1699240520.3; __utmt=1; frodotk="18b21167ffd9e6704a163437ff8db350"; __utmb=30149280.14.3.1699240523069',
    'Host': 'm.douban.com',
    'Origin': 'https://www.douban.com',
    'Referer': 'https://www.douban.com/group/topic/297353185/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

headers2 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5',
    'Connection': 'keep-alive',
    'Cookie': 'bid=lx0-X3YJQOE; __utmc=30149280; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1699264829; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1699264829; trc_cookie_storage=taboola%2520global%253Auser-id%3D22739f63-5eee-454a-96d1-91469401ff71-tuct57d9d8b; _gid=GA1.2.1651359284.1699264830; _ga=GA1.2.760385699.1699239916; _ga_Y4GN1R87RG=GS1.1.1699271839.3.0.1699271841.0.0.0; ap_v=0,6.0; dbcl2="91679349:uLLL5zXftIc"; ck=fkaK; push_noty_num=0; push_doumail_num=0; __utma=30149280.760385699.1699239916.1699324308.1699329962.4; __utmz=30149280.1699329962.4.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmv=30149280.9167; __utmb=30149280.10.8.1699329987940',
    'Host': 'm.douban.com',
    'Origin': 'https://www.douban.com',
    'Referer': 'https://www.douban.com/group/topic/297353185/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

header3 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'bid=lx0-X3YJQOE; _pk_id.100001.8cb4=5bfbb707a49cd487.1699239910.; __utmc=30149280; _gid=GA1.2.1651359284.1699264830; _ga=GA1.2.760385699.1699239916; _ga_Y4GN1R87RG=GS1.1.1699271839.3.0.1699271841.0.0.0; dbcl2="91679349:uLLL5zXftIc"; ck=fkaK; push_noty_num=0; push_doumail_num=0; __utmz=30149280.1699329962.4.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.9167; _pk_ses.100001.8cb4=1; ap_v=0,6.0; __utma=30149280.760385699.1699239916.1699340068.1699348030.6; frodotk_db="bd239d1e675f9a2f376ad75b361ece8d"; ct=y; __utmt=1; __utmb=30149280.100.5.1699351772950',
    'Host': 'www.douban.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


def get_all_question(group, topic, id):
    session = requests_html.HTMLSession()
    all_questions = []
    res = session.get(
        group, headers=header3)
    # print(res.status_code)
    trs = res.html.xpath("//tr[@class='pl']")
    for tr in trs:
        create_time = tr.xpath(
            "//td[@class='td-time']")[0].attrs['title'].replace('"', '\\"')
        title = tr.xpath(
            "//td[@class='td-subject']/a")[0].text.replace('"', '\\"')
        link = tr.xpath("//td[@class='td-subject']/a")[0].attrs['href']

        if (title.startswith(topic)):
            if (get_question(title, id)):
                continue
            all_questions.append(
                Question(title, link, id, create_time))
    return all_questions


def discount_to_json(discount):
    return discount.__dict__


def question_to_json(question):
    return question.__dict__


def answer_question(question, ck, header):
    print(question.title, question.link)
    session = requests_html.HTMLSession()
    try:
        res = session.get(question.link, headers=header)
    except:
        print("get question error")
        return
    question_content = res.html.xpath("//div[@data-entity-type='question']")
    discounts = []
    for content in question_content:
        # print(content.xpath("//div[@class='question-result-answer']"))
        try:
            question_id = content.attrs['data-id']
            res = session.post("https://m.douban.com/rexxar/api/v2/ceorl/poll/question/%s/answer" % question_id, data={
                'answer': 'test', 'ck': ck}, headers=header)
            body = res.json()
            # print(res.status_code)
            content = ""
            answer = ""
            try:
                content = str(body['title']).replace('"', '\\"')
                answer = body['correct_answer'].replace('"', '\\"')
            except:
                print(body)
            discount = Discount("问:" + content, "答:" + answer)
            discounts.append(discount)
        except:
            print("get answer error")
        time.sleep(2)

    question.set_discounts(discounts)


def executeCrawl(groupId, topic, id, ck, header):
    while True:
        session = requests_html.HTMLSession()
        print(time.ctime(), "start", groupId, topic)
        all_questions = []
        for page in range(0, 200, 50):
            douban_url = 'https://www.douban.com/group/search?start=%s&cat=1013&group=%s&sort=time&q=%s' % (str(page),
                                                                                                            groupId, topic)
            questions = get_all_question(douban_url, topic, id)
            all_questions = all_questions + questions

        for question in all_questions:
            answer_question(question, ck, header)
            # time.sleep(1)

        save_questions(all_questions)

        all_questions = get_all_questions(id)
        questions_json = json.dumps(all_questions, cls=CustomJSONEncoder)
        session.post(domain + "/api/hello?id=" + id, headers={'Content-Type': 'application/json'},
                     data=questions_json)
        time.sleep(60)


domain = 'https://show-douban-discount.vercel.app/'
# domain = 'http://localhost:3000/'
try:
    threading.Thread(target=executeCrawl, args=("536786",
                                                "【作业】", 'double11', 'SwQM', headers)).start()
    threading.Thread(target=executeCrawl, args=("656297",
                                                "【开车】", 'cat', 'SwQM', headers)).start()
    threading.Thread(target=executeCrawl, args=("698716",
                                                "【作业】", 'buy', 'fkaK', headers2)).start()
except:
    print("Error: unable to start thread")
