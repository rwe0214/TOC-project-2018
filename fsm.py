from transitions.extensions import GraphMachine
import json, requests

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

	#input keywords
    
    def search_aqi(self, update):
        text = update.message.text
        return (text.lower() == '沒錢') or (text.lower() == '窮') or (text.lower() == 'no money')
        
    def return_aqi(self, update):
        text = update.message.text
        print(text.lower())
        return len(text) > 0
    
    def wanna_breakfast(self, update):
        text = update.message.text
        return text.lower() == '早餐'

    def wanna_chinese_breakfast(self, update):
        text = update.message.text
        return text.lower() == '中式'
       
    def wanna_western_breakfast(self, update):
        text = update.message.text
        return text.lower() == '西式'
    
    def wanna_lunch(self, update):
        text = update.message.text
        return text.lower() == '午餐'
        
    def wanna_rice_lunch(self, update):
        text = update.message.text
        return text.lower() == '飯'
        
    def wanna_noodle_lunch(self, update):
        text = update.message.text
        return text.lower() == '麵'
        
    def wanna_dinner(self, update):
        text = update.message.text
        return text.lower() == '晚餐'
        
    def wanna_rice_dinner(self, update):
        text = update.message.text
        return text.lower() == '飯'
        
    def wanna_noodle_dinner(self, update):
        text = update.message.text
        return text.lower() == '麵'
        
    def wanna_restart(self, update):
        text = update.message.text
        print('test')
        return text.lower() == '重來'
        
    def make_a_description(self, update):
        text = update.message.text
        print(text.lower())
        return len(text) > 0
    
    #reply text

    def on_enter_init(self, update):
        print("restart")

    def on_enter_aqi(self, update):
        print("In aqi")
        update.message.reply_text("沒錢...吃空氣如何？請輸入所在地點（ Ex: 臺南市 ）");
        
    def on_enter_aqi_result(self, update):
        print("In aqi—result")
        resp = requests.get('http://opendata2.epa.gov.tw/AQI.json')
        datas = json.loads(resp.text)
        found = 0
        for data in datas:
            if data['County'] == update.message.text.lower():
                found = 1
                update.message.reply_text("觀測站: " + data['SiteName'] + "\nAQI: " + data['AQI'] + "\n空氣指標: " + data['Status'])
        if found == 0:
            update.message.reply_text("無此縣市")
        update.message.reply_text("AQI > 50 即代表有污染情形\n看看現在的空氣品質，還是好好存錢吃飯吧！")
        self.go_back(update)

    def on_enter_descript(self, update):
        print('In descript')
        update.message.reply_text("嗨，我是小當家，來協助你解決用餐選擇障礙的困擾，千萬不要擔心這是一種病，因為在下我以前也是這樣，老是想不到等等要吃什麼，可是經過好十幾年的修煉和調教，現在正可謂到了爐火純青的地步了，想吃什麼儘管問，不丟臉不丟臉真的不丟臉！")
        update.message.reply_text("不過，為了我們溝通上的方便，在下我特別訂了一些步驟，請務必確實遵守：\n1. 請先說出想吃\n\t\t\ta. 早餐\n\t\t\tb. 午餐\n\t\t\tc. 晚餐\n2. 接下來請選擇想吃的類型\n\t\t早餐我偷偷做了兩個分類\n\t\t\t\ta. 中式\n\t\t\t\tb. 西式\n\t\t晚餐和午餐也是分成兩類\n\t\t\t\ta. 飯\n\t\t\t\tb. 麵\n")
        self.go_back(update)

    def on_enter_breakfast(self, update):
        print('In breakfast')
        update.message.reply_text("原來大學生也有在吃早餐的，我還以為都是睡到中午吃午餐...\n想吃什麼類型的呢（中式 or 西式）？")
        
    def on_enter_chinese_breakfast(self, update):
        print('In chinese_breakfast')
        update.message.reply_text("生哥豆漿")
        update.message.reply_text("這家的燒餅真不是蓋的好吃！特推燒餅+油條\n貼心小叮嚀，小心排隊人龍")
        update.message.reply_text("位址如下！")
        update.message.reply_location(23.0141284,120.2026313);
        update.message.reply_photo("https://i1.wp.com/ikachalife.com/wp-content/uploads/2016/02/1461266528-903aee675e98a1f9004ceda3b5245187.jpg?w=800&ssl=1")
        self.go_back(update)

    def on_enter_western_breakfast(self, update):
        print('In western_breakfast')
        update.message.reply_text("成大附近唯一推薦元之氣！")
        update.message.reply_location(22.9942857,120.2190532)
        update.message.reply_photo("http://cfcdn3.azsg.opensnap.com/azsg/snapphoto/photo/L9/GT23/3BIMWM133EABD03ABA802Amx.jpg")
        update.message.reply_text("或是位在長榮路轉角的早餐店，推薦土司系列，咬下去會有驚喜喔！")
        update.message.reply_location(22.9927927,120.2216012)
        self.go_back(update)
    	
    def on_enter_lunch(self, update):
        print('In lunch')
        update.message.reply_text("先生午餐請問吃飯吃麵？")
        
    def on_enter_lunch_with_rice(self, update):
        print('In lunch_with_rice')
        update.message.reply_text("無名米糕，一位阿罵和米糕建築起的午餐小店")
        update.message.reply_text("不過我是比較喜歡他的肉燥飯，完完全全打趴任何以前吃過得肉燥飯\n而且重點是便宜！便宜！便宜！\n其他的菜色也是，可以在台南吃到暖暖的古早味，不過缺點是它沒有冷氣夏天去吃可能會稍微熱了一點...")
        update.message.reply_location(22.992679,120.2054885)
        update.message.reply_photo("https://farm9.staticflickr.com/8754/17104544809_c1d86d2d3e_z.jpg")
        self.go_back(update)

    def on_enter_lunch_with_noodle(self, update):
        print('In lunch_with_noodle')
        update.message.reply_text("大肥鴨")
        update.message.reply_text("推薦燻鴨乾麵+燻鴨飯+下水湯")
        update.message.reply_text("打卡老闆招待黑白切！")
        update.message.reply_location(22.9992898,120.2268166)
        self.go_back(update)
    	
    def on_enter_dinner(self, update):
        print('In dinner')
        update.message.reply_text("先生晚餐請問吃飯吃麵？")
        
    def on_enter_dinner_with_rice(self, update):
        print('In dinner_with_rice')
        update.message.reply_text("不管我一定要推薦這家店，加依軒")
        update.message.reply_text("便宜好吃又吃的飽，打卡再送包子，太划算啦！")
        update.message.reply_location(22.995708,120.2153085)
        update.message.reply_photo("http://pics12.yamedia.tw/43/userfile/o/ocean198109/album/156ee15289dffa.jpg")
        self.go_back(update)

    def on_enter_dinner_with_noodle(self, update):
        print('In dinner_with_noodle')
        update.message.reply_text("說到晚餐吃麵，就不能不提成大旁22巷內的小店倫敦派了\n平價好吃的義式料理，特推加價的巧克力馬芬")
        update.message.reply_location(22.9933443,120.2213986)
        update.message.reply_photo("http://pics2.yamedia.tw/34/userfile/r/rockingkai/album/14e8b0064c9ae5.jpg")
        self.go_back(update)

    def on_enter_restart(self, update):
        print('In restart')
        print('Ready to init')
        self.go_back(update)

    #go back condition
    def on_exit_aqi(self, update):
        print('Leaving aqi')
      
    def on_exit_aqi_result(self, update):
        print('Leaving aqi_result')

    def on_exit_descript(self, update):
        print('Leaving descript')

    def on_exit_breakfast(self, update):
        print('Leaving breakfast')
               
    def on_exit_chinese_breakfast(self, update):
        print('Leaving chinese_breakfast')
        
    def on_exit_western_breakfast(self, update):
        print('Leaving western_breakfast')
        
    def on_exit_lunch(self, update):
        print('Leaving lunch')
               
    def on_exit_lunch_with_rice(self, update):
        print('Leaving lunch_with_rice')
        
    def on_exit_lunch_with_noodle(self, update):
        print('Leaving lunch_with_noodle')
        
    def on_exit_dinner(self, update):
        print('Leaving dinner')
               
    def on_exit_dinner_with_rice(self, update):
        print('Leaving dinner_with_rice')
        
    def on_exit_dinner_with_noodle(self, update):
        print('Leaving dinner_with_noodle')
        
    def on_exit_restart(self, update):
        print('Leaving restart')
