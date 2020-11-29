#!/usr/bin/env python3

# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
#
# for use with DDL/Anki's Vector Robot: https://www.anki.com/en-us/vector

import anki_vector
import time
from datetime import date, datetime
from math import ceil
from anki_vector.util import degrees
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from yahoo_fin import stock_info
from PIL import Image, ImageDraw, ImageFont
import sys

t1 = datetime.now().strftime(("%H"))

#comment lines below to enter ticker symbol and percentage on command line
tSymbol = input("Enter the company ticker symbol : ")
percent = int(input("Enter the percentage change (+/-) you would like to be notified of (Minimum 1%) :"))
minutes_in_between_checks = int(input("Enter the duration between checks in minutes (Minimum 1 minute) : "))
#comment the lines below to use cli option above
#tSymbol = ('goog')
#percent = 1

percent_increase = (percent /100) + 1
percent_decrease = 1 - (percent/100)
wait = minutes_in_between_checks * 60

while True:
#    run script only between these times (8am and 10pm shown), comment it out to run all the time.
    if (int(t1)) > 8 and (int(t1)) < 20:
#        Add more ticker symbols here: images have to be 60x60 px, 72px resolution:
        if tSymbol == ('tsla'):
            brand = ('Tesla')
            symbol = ('symbols/tsla.jpg')
#            stock_price1=100
#            This grabs the stock price at the first run of the script, so percentage changes are referenced from the start rather than between each checking period.
            stock_price1=stock_info.get_live_price(tSymbol)

        elif tSymbol == ('amzn'):
            brand = ('Amazon')
            symbol = ('symbols/amzn.jpg')
            stock_price1=stock_info.get_live_price(tSymbol)

        elif tSymbol == ('aapl'):
            brand = ('Apple')
            symbol = ('symbols/aapl.jpg')
            stock_price1=stock_info.get_live_price(tSymbol)

        elif tSymbol == ('goog'):
            brand = ('Google')
            symbol = ('symbols/goog.jpg')
            stock_price1=stock_info.get_live_price(tSymbol)

        while True:
            print(str('Stock Price 1 - {:0.2f}'.format(stock_price1)))
            time.sleep(wait)
#            uncomment line below for testing only!
#            stock_price2=150
            stock_price2=stock_info.get_live_price(tSymbol)
            print(str('Stock Price 2 - {:0.2f}'.format(stock_price2)))
            percent_change = stock_price2 / stock_price1
            percent_digit = (percent_change - 1) * 100
            print(str('Percent Change {}'.format(percent_change)))
            print(str('Percent Digit {:0.2f}%'.format(percent_digit)))

            if stock_price2 > stock_price1:
                if percent_change >= percent_increase:
                    print("Stock price alert! {} has risen in price".format(brand))
                    def make_text_image(text_to_draw, x, y, font=None):
                        dimensions = (124, 96)
                        text_image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
                        dc = ImageDraw.Draw(text_image)
                        dc.text((x, y), text_to_draw, fill=(0, 255, 0, 255), font=font)
                        return text_image
                    try:
                        font_file = ImageFont.truetype("fonts/arial.ttf", 27)
                    except IOError:
                        pass

                    face_sum = (str('''   Price 
   Up 
   ${:0.2f}'''.format(stock_price2)))
                    text_to_draw = face_sum
                    face_image = make_text_image(text_to_draw, 2, 4, font_file)
                    images = (face_image)
                    images = images.convert("RGBA")
                    images.save('2.png', 'png', quality=100)

                    def append_images(images,bg_color=(0,0,0), aligment='top'):
                        widths, heights = zip(*(i.size for i in images))
                        new_width = sum(widths)
                        new_height = max(heights)
                        new_im = Image.new('RGB', (new_width, new_height), color=bg_color)
                        offset = 0
                        for im in images:
                            y = 0
                            if aligment == 'center':
                                y = int((new_height - im.size[1])/2)
                            elif aligment == 'bottom':
                                y = new_height - im.size[1]
                            new_im.paste(im, (offset, y))
                            offset += im.size[0]
                        return new_im

                    l=[(symbol),'2.png']
        #   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++          
                    images = [ Image.open(im) for im in l]
                    combo_2 = append_images(images, aligment='center')
                    combo_2.save('montage.jpg')
                    ticker_image = Image.open('montage.jpg')

                    robot = anki_vector.AsyncRobot()
                    robot.connect()
                    robot.behavior.set_head_angle(degrees(30.0))
                    say_alert1 = robot.behavior.say_text("Stock price alert! {} has risen in price".format(brand))
                    screen_data = anki_vector.screen.convert_image_to_screen_data(ticker_image)
                    robot.screen.set_screen_with_image_data(screen_data, 10.0, interrupt_running=True)
                    say_alert1.result()
                    say_percent = robot.behavior.say_text("Price is up by {:0.2f} percent".format(percent_digit))
                    say_percent.result()
                    say_price = robot.behavior.say_text("and is currently at {:0.2f} dollars per share".format(stock_price2))
                    say_price.result()
                    time.sleep(10)
                    robot.disconnect()
                    time.sleep(2)
                else:
                    print("{} Stock price has risen in price,".format(brand)) 
                    print("but hasn't reached your limit of {}%".format(percent))            
        #   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++     
            if stock_price2 < stock_price1:
                if percent_change <= percent_decrease:
                    print("Stock price alert! {} has fallen in price".format(brand))
                    def make_text_image(text_to_draw, x, y, font=None):
                        dimensions = (124, 96)
                        text_image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
                        dc = ImageDraw.Draw(text_image)
                        dc.text((x, y), text_to_draw, fill=(255, 0, 0, 255), font=font)
                        return text_image
                    try:
                        font_file = ImageFont.truetype("fonts/arial.ttf", 27)
                    except IOError:
                        pass

                    face_sum = (str('''   Price 
   Down 
   ${:0.2f}'''.format(stock_price2)))
                    text_to_draw = face_sum
                    face_image = make_text_image(text_to_draw, 2, 4, font_file)
                    images = (face_image)
                    images = images.convert("RGBA")
                    images.save('2.png', 'png', quality=100)     
        #   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
                    def append_images(images,bg_color=(0,0,0), aligment='top'):
                        widths, heights = zip(*(i.size for i in images))
                        new_width = sum(widths)
                        new_height = max(heights)
                        new_im = Image.new('RGB', (new_width, new_height), color=bg_color)
                        offset = 0
                        for im in images:
                            y = 0
                            if aligment == 'center':
                                y = int((new_height - im.size[1])/2)
                            elif aligment == 'bottom':
                                y = new_height - im.size[1]
                            new_im.paste(im, (offset, y))
                            offset += im.size[0]
                        return new_im

                    l=[(symbol),'2.png']
        #   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
                    images = [ Image.open(im) for im in l]
                    combo_2 = append_images(images, aligment='center')
                    combo_2.save('montage.jpg')
                    ticker_image = Image.open('montage.jpg')

                    robot = anki_vector.AsyncRobot()
                    robot.connect()
                    robot.behavior.set_head_angle(degrees(30.0))
                    say_alert1 = robot.behavior.say_text("Stock price alert! {} has fallen in price".format(brand))
                    screen_data = anki_vector.screen.convert_image_to_screen_data(ticker_image)
                    robot.screen.set_screen_with_image_data(screen_data, 10.0, interrupt_running=True)
                    say_alert1.result()
                    say_percent = robot.behavior.say_text("Price is down by {:0.2f} percent".format(percent_digit))
                    say_percent.result()
                    say_price = robot.behavior.say_text("and is currently at {:0.2f} dollars per share".format(stock_price2))
                    say_price.result()
                    time.sleep(10)
                    robot.disconnect()
                    time.sleep(2)
                else:
                    print("{} Stock price has fallen in price,".format(brand)) 
                    print("but hasn't reached your limit of {}%".format(percent))
