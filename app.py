import sys
from io import BytesIO

#-*- coding:utf-8 -*-
import requests
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        print ("data:", data)
        
import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

API_TOKEN = ''

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'init',
        'aqi',
        'aqi_result',
        'descript',
        'breakfast',
        'chinese_breakfast',
        'western_breakfast',       
        'lunch',
        'lunch_with_rice',
        'lunch_with_noodle',
        'dinner',
        'dinner_with_rice',
        'dinner_with_noodle',
        'restart'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'aqi',
            'conditions': 'search_aqi'
        },
        {
            'trigger': 'advance',
            'source': 'aqi',
            'dest': 'aqi_result',
            'conditions': 'return_aqi'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'breakfast',
            'conditions': 'wanna_breakfast'
        },
        {
            'trigger': 'advance',
            'source': 'breakfast',
            'dest': 'chinese_breakfast',
            'conditions': 'wanna_chinese_breakfast'
        },
        {
            'trigger': 'advance',
            'source': 'breakfast',
            'dest': 'western_breakfast',
            'conditions': 'wanna_western_breakfast'
        },    
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'lunch',
            'conditions': 'wanna_lunch'
        },
        {
            'trigger': 'advance',
            'source': 'lunch',
            'dest': 'lunch_with_rice',
            'conditions': 'wanna_rice_lunch'
        },
        {
            'trigger': 'advance',
            'source': 'lunch',
            'dest': 'lunch_with_noodle',
            'conditions': 'wanna_noodle_lunch'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'dinner',
            'conditions': 'wanna_dinner'
        },
        {
            'trigger': 'advance',
            'source': 'dinner',
            'dest': 'dinner_with_rice',
            'conditions': 'wanna_rice_dinner'
        },
        {
            'trigger': 'advance',
            'source': 'dinner',
            'dest': 'dinner_with_noodle',
            'conditions': 'wanna_noodle_dinner'
        },
        {
            'trigger': 'advance',
            'source': [
                'aqi',
                'breakfast',
                'chinese_breakfast',
                'western_breakfast',
                'lunch',
                'lunch_with_rice',
                'lunch_with_noodle',
                'dinner',
                'dinner_with_rice',
                'dinner_with_noodle'
            ],    
            'dest': 'restart',
            'conditions': 'wanna_restart'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'descript',
            'conditions': 'make_a_description'
        },
        {
            'trigger': 'go_back',
            'source': [
                'descript',
                'chinese_breakfast',
                'western_breakfast',
                'lunch_with_rice',
                'lunch_with_noodle',
                'dinner_with_rice',
                'dinner_with_noodle',
                'aqi_result',
                'restart'
            ],
            'dest': 'init'
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    data = requests.get('http://127.0.0.1:4040')
    temp = data.text.replace(' ', '')
    tar = 'command_line(http)'
    index = temp.find(tar)
    temp = temp[index+39:index+56]
    WEBHOOK_URL = 'https://' + temp + '/hook'
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
