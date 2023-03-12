import random
import json

# from graia.ariadne.message.formatter import Formatter
from graia.ariadne.message.element import Face

class arkGetCard:
    def __init__(self, times, no_six):
        self.jsonFile = json.load(open("modules/arkCard/config.json"))
        self._box = self.get_card(times = int(times))
        self.no_six = int(no_six)

        self.six_box = self.jsonFile["addition"]["normal_six"]
        self.five_box = self.jsonFile["addition"]["normal_five"]
        self.four_box = self.jsonFile["addition"]["normal_four"]
        self.three_box = self.jsonFile["addition"]["normal_three"]

    def get_card(self, times):

        box = []
        for i in range(times):
            box.append(random.uniform(1,101))


        return box

    def norm_pool(self):
        no_six = self.no_six

        six_prob = 1
        five_prob = 3
        four_prob = 11
        three_prob = 61

        six_ups = self.jsonFile["addition"]["opening"]["常驻池"][0:2]    # up六星
        five_ups = self.jsonFile["addition"]["opening"]["常驻池"][2:]

        
        six_final = self.six_box
        for i in six_ups:six_final.remove(i)    # 未up六星

        five_final = self.five_box
        for i in five_ups:five_final.remove(i)

        box = []
        for val in self._box:
            if no_six < 50:
                six_baodi = 0
            else:
                six_baodi = no_six - 50
            if val >= six_prob and val <= (five_prob + 2*six_baodi):
                if val <= (six_prob + five_prob + 2*six_baodi) / 2:
                    # box.append(f"{random.choice(six_ups)}")
                    # box.append(Formatter("{doge}{doge}{doge}{doge}{doge}{doge}{mes}\n".format(doge=Face(277), mes=random.choice(six_ups))))
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_ups)}\n"])
                else:
                    # box.append(random.choice(six_final))
                    # box.append(Formatter("{doge}{doge}{doge}{doge}{doge}{doge}{mes}\n".format(doge=Face(277), mes=random.choice(six_final))))
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_final)}\n"])
                no_six = 0
            elif val > five_prob + 2*six_baodi and val <= four_prob + 2*2*six_baodi/3:
                if val <= (five_prob + 2*six_baodi + four_prob + 2*2*six_baodi/3) / 2:
                    # box.append(random.choice(five_ups))
                    # box.append(Formatter("{doge}{doge}{doge}{doge}{doge}{mes}\n".format(doge=Face(277), mes=random.choice(five_ups))))
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_ups)}\n"])
                else:
                    # box.append(random.choice(five_final))
                    # box.append(Formatter("{doge}{doge}{doge}{doge}{doge}{mes}\n".format(doge=Face(277), mes=random.choice(five_final))))
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_final)}\n"])
                no_six += 1
            elif val > four_prob + 2*2*six_baodi/3 and val <= three_prob + 3*2*six_baodi/3:
                # box.append(random.choice(self.four_box))
                # box.append(Formatter("{doge}{doge}{doge}{doge}{mes}\n".format(doge=Face(277), mes=random.choice(self.four_box))))
                box.append([Face(277),Face(277),Face(277),Face(277),f"{random.choice(self.four_box)}\n"])
                no_six += 1
            elif val > (three_prob + 3*2*six_baodi/3) and val <= 101:
                # box.append(random.choice(self.three_box))
                box.append([Face(277),Face(277),Face(277),f"{random.choice(self.three_box)}\n"])
                no_six += 1

        return box

    def pool_120(self):
        no_six = self.no_six

        six_prob = 1
        five_prob = 3
        four_prob = 11
        three_prob = 61

        six_ups = self.jsonFile["addition"]["opening"]["怪猎联动池"][0:1]
        five_ups = self.jsonFile["addition"]["opening"]["怪猎联动池"][1:]

        six_final = self.six_box
        five_final = self.five_box

        box = []
        for val in self._box:
            if no_six < 50:
                six_baodi = 0
            else:
                six_baodi = no_six - 50
            if val >= six_prob and val <= (five_prob + 2*six_baodi):
                if val <= (six_prob + five_prob + 2*six_baodi) / 2:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_ups)}\n"])
                else:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_final)}\n"])
                no_six = 0
            elif val > five_prob + 2*six_baodi and val <= four_prob + 2*2*six_baodi/3:
                if val <= (five_prob + 2*six_baodi + four_prob + 2*2*six_baodi/3) / 2:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_ups)}\n"])
                else:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_final)}\n"])
                no_six += 1
            elif val > four_prob + 2*2*six_baodi/3 and val <= three_prob + 3*2*six_baodi/3:
                box.append([Face(277),Face(277),Face(277),Face(277),f"{random.choice(self.four_box)}\n"])
                no_six += 1
            elif val > (three_prob + 3*2*six_baodi/3) and val <= 101:
                box.append([Face(277),Face(277),Face(277),f"{random.choice(self.three_box)}\n"])
                no_six += 1
        return box

    def limit_pool(self, pooltype):
        dict = {"春节":"years","周年庆":"celebrate","夏活":"summer"}
        no_six = self.no_six

        six_prob = 1
        five_prob = 3
        four_prob = 11
        three_prob = 61

        six_ups = self.jsonFile["addition"]["opening"]["双up限定池"][0:2]
        five_ups = self.jsonFile["addition"]["opening"]["双up限定池"][2:]

        six_final = self.six_box
        six_final.remove(six_ups[1])
        six_5up = self.jsonFile["addition"][dict[pooltype]]    
        six_5up.remove(six_ups[0])    # 将五倍权重的部分单独划出来
        five_final = self.five_box
        for i in five_ups:five_final.remove(i)

        allunup = len(six_final) + 5*len(six_5up)

        box = []
        for val in self._box:
            if no_six < 50:
                six_baodi = 0
            else:
                six_baodi = no_six - 50
            if val >= six_prob and val <= (five_prob + 2*six_baodi):
                if val <= (six_prob + (five_prob + 2*six_baodi - six_prob) * 0.7):
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_ups)}\n"])
                elif val > (six_prob + (five_prob + 2*six_baodi - six_prob) * 0.7) and val < (six_prob + (five_prob + 2*six_baodi - six_prob) * 0.7 + (five_prob + 2*six_baodi - six_prob)*0.3*(5*len(six_5up)/allunup)):
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_5up)}\n"])
                else:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(six_final)}\n"])
                no_six = 0
            elif val > five_prob + 2*six_baodi and val <= four_prob + 2*2*six_baodi/3:
                if val <= (five_prob + 2*six_baodi + four_prob + 2*2*six_baodi/3) / 2:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_ups)}\n"])
                else:
                    box.append([Face(277),Face(277),Face(277),Face(277),Face(277),f"{random.choice(five_final)}\n"])
                no_six += 1
            elif val > four_prob + 2*2*six_baodi/3 and val <= three_prob + 3*2*six_baodi/3:
                box.append([Face(277),Face(277),Face(277),Face(277),f"{random.choice(self.four_box)}\n"])
                no_six += 1
            elif val > (three_prob + 3*2*six_baodi/3) and val <= 101:
                box.append([Face(277),Face(277),Face(277),f"{random.choice(self.three_box)}\n"])
                no_six += 1

        return box
    