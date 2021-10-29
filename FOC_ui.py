from FOC_build_fighters import build_fighter_object_dictionary
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
from PIL.ImageQt import ImageQt
import requests
from PIL import Image
from urllib3.exceptions import InsecureRequestWarning
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
import io
import PIL
from FOC_get_fighter_images import read_fighter_image_links_from_file
from FOC_Fighter import Fighter
from FOC_calculate_basic_fight_odds import read_glicko_ranking, find_basic_odds
from PyQt5.QtCore import *

WINDOW_WIDTH = 1700
FIGHTER_PANE_WIDTH = int(WINDOW_WIDTH * (5/12))

# Next time: Create empty odds pane. Add fighterA and fighterB as parameters to OddsPane.Call the UI method externally

class ComparisonPane(QWidget):

    def __init__(self, fighterA_obj, fighterB_obj):
        super().__init__()
        self.fighterA_obj = fighterA_obj
        self.fighterB_obj = fighterB_obj
        self.UI()

    def UI(self):
        main_vlayout = QVBoxLayout()
        if not self.fighterA_obj.stats_dict or not self.fighterB_obj.stats_dict:
            for i in range (0,8):
                main_vlayout.addWidget(QLabel("---"))
        else:
            diff1 = str(round(float(self.fighterA_obj.stats_dict['SLpM']) - float(self.fighterB_obj.stats_dict['SLpM']), 2))
            parsed2 = (self.fighterA_obj.stats_dict['StrAcc'][:-1], self.fighterB_obj.stats_dict['StrAcc'][:-1])
            diff2 = str(float(parsed2[0]) - float(parsed2[1])) + "%"
            diff3 = str(round(float(self.fighterA_obj.stats_dict['SApM']) - float(self.fighterB_obj.stats_dict['SApM']), 2))
            parsed4 = (self.fighterA_obj.stats_dict['StrDef'][:-1], self.fighterB_obj.stats_dict['StrDef'][:-1])
            diff4 = str(float(parsed4[0]) - float(parsed4[1])) + "%"
            diff5 = str(round(float(self.fighterA_obj.stats_dict['TDAvg']) - float(self.fighterB_obj.stats_dict['TDAvg']), 2))
            parsed6 = (self.fighterA_obj.stats_dict['TDAcc'][:-1], self.fighterB_obj.stats_dict['TDAcc'][:-1])
            diff6 = str(float(parsed6[0]) - float(parsed6[1])) + "%"
            parsed7 = (self.fighterA_obj.stats_dict['TDDef'][:-1], self.fighterB_obj.stats_dict['TDDef'][:-1])
            diff7 = str(float(parsed7[0]) - float(parsed7[1])) + "%"
            diff8 = str(round(float(self.fighterA_obj.stats_dict['SubAvg']) - float(self.fighterB_obj.stats_dict['SubAvg']), 2))
            diff_list = [diff1, diff2, diff3, diff4, diff5, diff6, diff7, diff8]
            for i in range(0,8):
                if diff_list[i][-1] == "%":
                    a_number = float(diff_list[i][:-1])
                else:
                    a_number = float(diff_list[i])
                a_label = QLabel(diff_list[i])
                a_label.setAlignment(Qt.AlignHCenter)
                if a_number < 0:
                    a_label.setStyleSheet('color: red')
                else:
                    a_label.setStyleSheet("color: green")
                main_vlayout.addWidget(a_label)
        main_vlayout.setAlignment(Qt.AlignBottom)
        self.setLayout(main_vlayout)

class EmptyComparisonPane(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        a_layout = QVBoxLayout()
        for i in range(0,8):
            a_layout.addWidget(QLabel("---"))
        self.setLayout(a_layout)

class OddsPane(QWidget):

    def __init__(self, fighterA, fighterB):
        super().__init__()
        self.fighterA = fighterA
        self.fighterB = fighterB
        self.UI()

    def UI(self):
        a_glicko_dict = read_glicko_ranking("FOC_rankings_generator/FOC_glicko2.txt")
        odds = find_basic_odds(self.fighterA, self.fighterB, a_glicko_dict)
        test_layout = QVBoxLayout()
        a_str1 = "Odds for a match between:\n" + self.fighterA + " and " + self.fighterB
        text_label = QLabel(a_str1)
        text_label.setAlignment(Qt.AlignHCenter)
        a_str2 = "The favorite is " + odds[0] + "\nwith odds: " + str(odds[1])
        print(type(a_str2))
        a_favorite_label = QLabel(a_str2)
        a_favorite_label.setAlignment(Qt.AlignHCenter)
        test_layout.addWidget(text_label)
        test_layout.addWidget(a_favorite_label)

        a_dict = build_fighter_object_dictionary()
        test_layout.addWidget(ComparisonPane(a_dict[self.fighterA], a_dict[self.fighterB]))
        self.setLayout(test_layout)


class EmptyOddsPane(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        title = "Odds"
        title_label = QLabel(title)
        odds_label = QLabel("---")
        favorite_label = QLabel("None")

        main_vlayout = QVBoxLayout()
        main_vlayout.setAlignment(Qt.AlignHCenter)
        main_vlayout.addWidget(title_label)
        main_vlayout.addWidget(favorite_label)
        main_vlayout.addWidget(odds_label)
        main_vlayout.addWidget(EmptyComparisonPane())
        self.setLayout(main_vlayout)


class StatsPane(QWidget):

    def __init__(self, fighter_obj, name):
        super().__init__()
        self.fighter_obj = fighter_obj
        self.name = name
        #print("My height: " + self.height)
        #self.setFixedWidth(FIGHTER_PANE_WIDTH)
        self.UI()

    def UI(self):
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(QLabel("Divisions:"))
        vlayout1.addWidget(QLabel("Weight:"))
        vlayout1.addWidget(QLabel("Strikes landed per minute: "))
        vlayout1.addWidget(QLabel("Striking accuracy %: "))
        vlayout1.addWidget(QLabel("Strikes absorbed per minute: "))
        vlayout1.addWidget(QLabel("Striking defense %: "))
        vlayout1.addWidget(QLabel("Takedown average per 15 minutes: "))
        vlayout1.addWidget(QLabel("Takedown accuracy %: "))
        vlayout1.addWidget(QLabel("Takedown defense %: "))
        vlayout1.addWidget(QLabel("Submissions attempted per 15 minutes: "))

        a_test_string = ""
        if len(self.fighter_obj.division) > 1:
            for s in self.fighter_obj.division:
                a_test_string += s + ", "
            a_test_string = a_test_string[:-2]
        else:
            a_test_string += self.fighter_obj.division[0]
        detailed = self.fighter_obj.stats_dict

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(QLabel(a_test_string))
        vlayout2.addWidget(QLabel(self.fighter_obj.weight))
        vlayout2.addWidget(QLabel(detailed['SLpM']))
        vlayout2.addWidget(QLabel(detailed['StrAcc']))
        vlayout2.addWidget(QLabel(detailed['SApM']))
        vlayout2.addWidget(QLabel(detailed['StrDef']))
        vlayout2.addWidget(QLabel(detailed['TDAvg']))
        vlayout2.addWidget(QLabel(detailed['TDAcc']))
        vlayout2.addWidget(QLabel(detailed['TDDef']))
        vlayout2.addWidget(QLabel(detailed['SubAvg']))

        stats_h = QHBoxLayout()
        stats_h.setAlignment(Qt.AlignHCenter)
        stats_h.addLayout(vlayout1)
        stats_h.addLayout(vlayout2)
        self.setLayout(stats_h)

class EmptyStatsPane(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        a_layout1 = QVBoxLayout()
        a_layout1.addWidget(QLabel("Divisions:"))
        a_layout1.addWidget(QLabel("Weight:"))
        a_layout1.addWidget(QLabel("Strikes landed per minute: "))
        a_layout1.addWidget(QLabel("Striking accuracy %: "))
        a_layout1.addWidget(QLabel("Strikes absorbed per minute: "))
        a_layout1.addWidget(QLabel("Striking defense %: "))
        a_layout1.addWidget(QLabel("Takedown average per 15 minutes: "))
        a_layout1.addWidget(QLabel("Takedown accuracy %: "))
        a_layout1.addWidget(QLabel("Takedown defense %: "))
        a_layout1.addWidget(QLabel("Submissions attempted per 15 minutes: "))

        a_layout2 = QVBoxLayout()
        for i in range(0,8):
            a_layout2.addWidget(QLabel("---"))

        stats_h = QHBoxLayout()
        stats_h.setAlignment(Qt.AlignHCenter)
        stats_h.addLayout(a_layout1)
        stats_h.addLayout(a_layout2)
        self.setLayout(stats_h)



class FighterPane(QWidget):

    def __init__(self, url, fighter_name, fighter_obj):
        super().__init__()
        self.url = url
        self.fighter_name = fighter_name
        self.fighter_obj = fighter_obj
        self.setFixedWidth(FIGHTER_PANE_WIDTH)
        self.UI()

    def UI(self):
        layout = QVBoxLayout(self)
        name_label = QLabel(self.fighter_name)
        name_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(name_label)
        image_label = self.get_image_label()
        image_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(image_label)
        layout.addWidget(StatsPane(self.fighter_obj, self.fighter_name))
        self.setLayout(layout)

    def get_image_label(self):
        """ Returns a label containing the image of the fighter """
        if self.url == "":
            pixmap = self.get_default_image_pixmap()
        else:
            try:
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                response = requests.get(self.url, verify=False, stream=True)
                image_bytes = io.BytesIO(response.content)
                img = PIL.Image.open(image_bytes)
                qim = ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(qim)
            except Exception as e:
                print(e)
                pixmap = self.get_default_image_pixmap()
        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(image_label.size(), QtCore.Qt.KeepAspectRatio))
        return image_label

    def get_default_image_pixmap(self):
        with open("blank_profile.png", "rb") as fh:
            content = fh.read()
        fighter_image = QImage()
        fighter_image.loadFromData(content)
        pixmap = QtGui.QPixmap.fromImage(fighter_image)
        return pixmap


class EmptyFighterPane(QWidget):
    def __init__(self, fighter_name):
        super().__init__()
        self.fighter_name = fighter_name
        self.setFixedWidth(FIGHTER_PANE_WIDTH)
        self.UI()

    def UI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        a_label = QLabel(self.fighter_name)
        a_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(a_label)
        image_label = self.get_image_label()
        image_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(image_label)
        layout.addWidget(EmptyStatsPane())
        self.setLayout(layout)

    def get_image_label(self):
        with open("blank_profile.png", "rb") as fh:
            content = fh.read()
        fighter_image = QImage()
        fighter_image.loadFromData(content)
        pixmap = QtGui.QPixmap.fromImage(fighter_image)
        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(image_label.size(), QtCore.Qt.IgnoreAspectRatio))
        return image_label


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.w = None
        self.UI()

    def UI(self):
        url_dict = read_fighter_image_links_from_file("FOC_fighter_image_links.json")
        a_fighter_object_dict = build_fighter_object_dictionary()

        top_hlayout = QHBoxLayout()
        textbox = QLineEdit("Input fighter text here")
        search_button = QPushButton("Add fighter")
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help_window)

        top_hlayout.addWidget(textbox)
        top_hlayout.addWidget(search_button)
        top_hlayout.addWidget(help_button)

        top_vlayout = QVBoxLayout()
        top_vlayout.addLayout(top_hlayout)
        response_label = QLabel("Reponse is gonna appear here!")
        response_label.setFixedHeight(25)
        top_vlayout.addWidget(response_label)

        middle_hlayout = QHBoxLayout()
        a_list = ["FighterA", "FighterB"]
        empty1 = EmptyFighterPane("FighterA")
        empty2 = EmptyFighterPane("FighterB")
        slot1 = QVBoxLayout()
        slot2 = QVBoxLayout()
        slot1.addWidget(empty1)
        slot2.addWidget(empty2)

        odds = EmptyOddsPane()
        odds_layout = QVBoxLayout()
        odds_layout.addWidget(odds)

        middle_hlayout.addLayout(slot1)
        middle_hlayout.addLayout(odds_layout)
        middle_hlayout.addLayout(slot2)
        search_button.clicked.connect(lambda: self.add_fighter(response_label, textbox, slot1, slot2, a_list, a_fighter_object_dict, url_dict, odds_layout))

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_vlayout)
        main_layout.addLayout(middle_hlayout)

        self.setLayout(main_layout)
        self.setGeometry(100, 100, WINDOW_WIDTH, 900)
        self.setWindowTitle("MMA Fighter Odds Calculator")
        self.show()

    def show_help_window(self, checked):
        if self.w is None:
            self.w = HelpWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def add_fighter(self, the_response_label, the_textbox, layoutA, layoutB, a_list, a_fighter_dict, a_url_dict, an_odds_layout):
        query = the_textbox.text()
        if query not in a_fighter_dict:
            the_response_label.setText('Couldn\'t find "' + query + '"')
        else:
            if a_list[0] == "FighterA":
                a_list[0] = query
            else:
                a_list[1] = a_list[0]
                a_list[0] = query
            print(a_list)
            if a_list[1] == "FighterB":
                name1 = a_list[0]
                url1 = a_url_dict[name1]
                for i in reversed(range(layoutA.count())):
                    layoutA.itemAt(i).widget().setParent(None)
                layoutA.addWidget(FighterPane(url1, name1, a_fighter_dict[name1]))
            else:
                for i in reversed(range(layoutA.count())):
                    layoutA.itemAt(i).widget().setParent(None)
                for i in reversed(range(layoutB.count())):
                    layoutB.itemAt(i).widget().setParent(None)
                name1 = a_list[0]
                name2 = a_list[1]
                url1 = a_url_dict[name1]
                url2 = a_url_dict[name2]
                fighter1 = FighterPane(url1, name1, a_fighter_dict[name1])
                fighter2 = FighterPane(url2, name2, a_fighter_dict[name2])
                assert(type(fighter1) == FighterPane)
                assert(type(fighter2) == FighterPane)
                layoutA.addWidget(FighterPane(url1, name1, a_fighter_dict[name1]))
                layoutB.addWidget(FighterPane(url2, name2, a_fighter_dict[name2]))
        glicko = read_glicko_ranking("FOC_rankings_generator/FOC_glicko2.txt")
        if query in a_fighter_dict:
            if a_list[0] != "FighterA" and a_list[1] != "FighterB":
                self.update_stats_pane(an_odds_layout, name1, name2)
            else:
                print("Don't update odds pane")

    def update_stats_pane(self, odds_layout, fighterA_name, fighterB_name):
        # Have to check for valid/invalid weight classes here
        for i in reversed(range(odds_layout.count())):
            odds_layout.itemAt(i).widget().setParent(None)
        an_odds_pane = OddsPane(fighterA_name, fighterB_name)
        odds_layout.addWidget(an_odds_pane)


class HelpWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        layout = QVBoxLayout()
        text_edit = QPlainTextEdit()
        text = open('FOC_helper.txt').read()
        text_edit.setPlainText(text)
        layout.addWidget(text_edit)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 1500, 700)
        self.setLayout(layout)

def main():

    app = QApplication([])
    #app.setStyleSheet("QLineEdit { background-color: yellow }")
    w = MainWindow()
    #search_button.clicked.connect(lambda: say_hello(textbox.text(), label))



    app.exec_()


if __name__ == "__main__":
    main()
