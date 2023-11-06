import requests_html
import time
import json


class Question:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def set_discounts(self, discounts):
        self.discounts = discounts

    def add_discount(self, discount):
        self.discounts.append(discount)


class Discount:
    def __init__(self, title, content, timeout):
        self.title = title
        self.content = content
        self.timeout = timeout


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


session = requests_html.HTMLSession()


def get_all_question():
    all_questions = []
    res = session.get(
        "https://www.douban.com/group/536786", headers=headers)
    # print(res.status_code)
    links = res.html.xpath("//a[@class='item-containor']")
    for link in links:
        if (link.attrs['title'].startswith("【作业】")):
            all_questions.append(
                Question(str(link.attrs['title']), 'https://www.douban.com' + link.attrs['href']))
    return all_questions


def discount_to_json(discount):
    return discount.__dict__


def question_to_json(question):
    return question.__dict__


def answer_question(question):
    # print(question.title, question.link)
    res = session.get(question.link, headers=headers)
    question_content = res.html.xpath("//div[@data-entity-type='question']")
    discounts = []
    for content in question_content:
        # print(content.xpath("//div[@class='question-result-answer']"))
        try:
            question_id = content.attrs['data-id']
            res = session.post("https://m.douban.com/rexxar/api/v2/ceorl/poll/question/%s/answer" % question_id, data={
                'answer': 'test', 'ck': 'SwQM'}, headers=headers)
            body = res.json()
            print(res.status_code)
            title = ""
            answer = ""
            try:
                title = str(body['title'])
                answer = body['correct_answer']
            except:
                print(body)
            discount = Discount("问:" + title, "答:" + answer, '')
            discounts.append(discount)
        except:
            print("error")
        time.sleep(1)

    question.set_discounts([discount_to_json(discount)
                           for discount in discounts])


while True:
    print(time.ctime())
    all_questions = get_all_question()

    # answer_question(all_questions[1])
    for question in all_questions:
        answer_question(question)
        time.sleep(1)

    questions_json = [question_to_json(question) for question in all_questions]
    data = json.dumps(questions_json)
    session.post("http://localhost:3000/api/hello", headers={'Content-Type': 'application/json'},
                 data=data)

    time.sleep(60)
