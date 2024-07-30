# General imports
import pandas as pd
from numpy.random import randint
import sys
from typing import Tuple
# PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QCheckBox, QLineEdit
from PyQt5 import uic
# Reportlab
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

class dietplaner_UI(QMainWindow):
    def __init__(self):
        super(dietplaner_UI, self).__init__()

        # Load UI file and show it
        uic.loadUi('diet_planer.ui', self)
        self.show()

        # Load Data
        self.recepies = pd.read_excel('rezepte.xlsx')
        self.zutaten_ = pd.read_excel('zutaten.xlsx')
        # Make 'zutaten' dictationary
        self.zutaten = {}
        for zut in self.zutaten_.values:
            self.zutaten[zut[0]] = zut[1:]

        # Set Calories
        self.cal_limit_breakfast = self.findChild(QLineEdit, 'txt_cal_fr').text()
        self.cal_limit_lunch = self.findChild(QLineEdit, 'txt_cal_mi').text()
        self.cal_limit_dinner = self.findChild(QLineEdit, 'txt_cal_ab').text()
        self.cal_limit_snack = self.findChild(QLineEdit, 'txt_cal_sn').text()

        # Show all calories
        self.all_cals = self.findChild(QLabel, 'lbl_all_cals')
        new_text = int(self.cal_limit_breakfast) + int(self.cal_limit_lunch)+ int(self.cal_limit_dinner) + int(self.cal_limit_snack)
        new_text = 'Gesamte Kalorien: ' + str(new_text)
        self.all_cals.setText(new_text)

        # Define Widgets
        # Monday
        self.monday_fr = self.findChild(QCheckBox, 'mon_fr')
        self.monday_fr.setChecked(True)
        self.monday_mi = self.findChild(QCheckBox, 'mon_mi')
        self.monday_mi.setChecked(True)
        self.monday_ab = self.findChild(QCheckBox, 'mon_ab')
        self.monday_ab.setChecked(True)
        self.monday_sn = self.findChild(QCheckBox, 'mon_sn')
        self.monday_sn.setChecked(True)
        # Tuesday
        self.tuesday_fr = self.findChild(QCheckBox, 'din_fr')
        self.tuesday_fr.setChecked(True)
        self.tuesday_mi = self.findChild(QCheckBox, 'din_mi')
        self.tuesday_mi.setChecked(True)
        self.tuesday_ab = self.findChild(QCheckBox, 'din_ab')
        self.tuesday_ab.setChecked(True)
        self.tuesday_sn = self.findChild(QCheckBox, 'din_sn')
        self.tuesday_sn.setChecked(True)
        # Wednesday
        self.wednesday_fr = self.findChild(QCheckBox, 'mit_fr')
        self.wednesday_fr.setChecked(True)
        self.wednesday_mi = self.findChild(QCheckBox, 'mit_mi')
        self.wednesday_mi.setChecked(True)
        self.wednesday_ab = self.findChild(QCheckBox, 'mit_ab')
        self.wednesday_ab.setChecked(True)
        self.wednesday_sn = self.findChild(QCheckBox, 'mit_sn')
        self.wednesday_sn.setChecked(True)
        # Thursday
        self.thursday_fr = self.findChild(QCheckBox, 'don_fr')
        self.thursday_fr.setChecked(True)
        self.thursday_mi = self.findChild(QCheckBox, 'don_mi')
        self.thursday_mi.setChecked(True)
        self.thursday_ab = self.findChild(QCheckBox, 'don_ab')
        self.thursday_ab.setChecked(True)
        self.thursday_sn = self.findChild(QCheckBox, 'don_sn')
        self.thursday_sn.setChecked(True)
        # Friday
        self.friday_fr = self.findChild(QCheckBox, 'fre_fr')
        self.friday_fr.setChecked(True)
        self.friday_mi = self.findChild(QCheckBox, 'fre_mi')
        self.friday_mi.setChecked(True)
        self.friday_ab = self.findChild(QCheckBox, 'fre_ab')
        self.friday_ab.setChecked(True)
        self.friday_sn = self.findChild(QCheckBox, 'fre_sn')
        self.friday_sn.setChecked(True)
        # Saturday
        self.saturday_fr = self.findChild(QCheckBox, 'sam_fr')
        self.saturday_fr.setChecked(True)
        self.saturday_mi = self.findChild(QCheckBox, 'sam_mi')
        self.saturday_mi.setChecked(True)
        self.saturday_ab = self.findChild(QCheckBox, 'sam_ab')
        self.saturday_ab.setChecked(True)
        self.saturday_sn = self.findChild(QCheckBox, 'sam_sn')
        self.saturday_sn.setChecked(True)
        # Sunday
        self.sunday_fr = self.findChild(QCheckBox, 'son_fr')
        self.sunday_fr.setChecked(True)
        self.sunday_mi = self.findChild(QCheckBox, 'son_mi')
        self.sunday_mi.setChecked(True)
        self.sunday_ab = self.findChild(QCheckBox, 'son_ab')
        self.sunday_ab.setChecked(True)
        self.sunday_sn = self.findChild(QCheckBox, 'son_sn')
        self.sunday_sn.setChecked(True)

        # Calculation button
        self.calculte = self.findChild(QPushButton, 'btn_calculate')

        #Action for the button
        self.calculte.clicked.connect(self.create_pdf_weekplan)
        self.meals = self.get_meals()

    def check_setting(self)->Tuple[int, int, int, int]:
        '''
        Check how many meals per day a needed.
        Return the number of meals of breaksfasts, lunches, dinners and snakcs.

        Input:
            - None
        Output:
            - num_breakfasts: Number of breakfasts for this week. [int]
            - num_lunch: Number of lunches for this week. [int]
            - num_dinner: Number of dinners for this week. [int]
            - num_snack: Number of snacks for this week. [int]
        '''
        num_breakfasts = 0
        num_lunch = 0
        num_dinner = 0
        num_snack = 0
        # monday
        if self.monday_fr.isChecked():
            num_breakfasts +=1
        if self.monday_mi.isChecked():
            num_lunch +=1
        if self.monday_ab.isChecked():
            num_dinner +=1
        if self.monday_sn.isChecked():
            num_snack +=1

        # tuesday
        if self.tuesday_fr.isChecked():
            num_breakfasts +=1
        if self.tuesday_mi.isChecked():
            num_lunch +=1
        if self.tuesday_ab.isChecked():
            num_dinner +=1
        if self.tuesday_sn.isChecked():
            num_snack +=1

        # wednesday
        if self.wednesday_fr.isChecked():
            num_breakfasts +=1
        if self.wednesday_mi.isChecked():
            num_lunch +=1
        if self.wednesday_ab.isChecked():
            num_dinner +=1
        if self.wednesday_sn.isChecked():
            num_snack +=1

        # thursday
        if self.thursday_fr.isChecked():
            num_breakfasts +=1
        if self.thursday_mi.isChecked():
            num_lunch +=1
        if self.thursday_ab.isChecked():
            num_dinner +=1
        if self.thursday_sn.isChecked():
            num_snack +=1

        # friday
        if self.friday_fr.isChecked():
            num_breakfasts +=1
        if self.friday_mi.isChecked():
            num_lunch +=1
        if self.friday_ab.isChecked():
            num_dinner +=1
        if self.friday_sn.isChecked():
            num_snack +=1

        # saturday
        if self.saturday_fr.isChecked():
            num_breakfasts +=1
        if self.saturday_mi.isChecked():
            num_lunch +=1
        if self.saturday_ab.isChecked():
            num_dinner +=1
        if self.saturday_sn.isChecked():
            num_snack +=1

        # sunday
        if self.sunday_fr.isChecked():
            num_breakfasts +=1
        if self.sunday_mi.isChecked():
            num_lunch +=1
        if self.sunday_ab.isChecked():
            num_dinner +=1
        if self.sunday_sn.isChecked():
            num_snack +=1

        return num_breakfasts, num_lunch, num_lunch, num_snack

    def extract_meal(self, start:int, end:int, meal:str):
        '''
        Extract the meals (ingredients) from the excel file. Has the "meal" variable as
        input and output, always adding a new meal with each call of this function.

        Input:
            - start: starting index of a meal in the excel file. [int]
            - end: ending index of a meal in the excel file. [int]
            - meal: name of the meal that should be extracted from the excel file. [str]

        Output:
            - meals: dictionary that contains all the meals of the excel file. [dict]
        '''
        new_meal = {}
        for idx in range(start, end):
            new_meal[self.recepies.values[idx,1]] = self.recepies.values[idx,2]
        meal[self.recepies.values[start,0]] = new_meal
        return meal
    
    def get_meals(self):
        '''
        In this function all the different meals for breakfast, lunch, dinner and snack are
        extracted from the excel file by recursively calling the "extract_meal" function.

        Input:
            - None

        Output:
            - meals: Meals object that contain every meal. [dict]
        '''
        num_rows = self.recepies.values.shape[0]
        row_ = []
        for row_idx in range(num_rows):
            if isinstance(self.recepies.values[row_idx,0], str):
                row_.append(row_idx)
        row_.append(num_rows-1)
        meals = {'Frühstück':{}, 'Mittagessen':{}, 'Abendessen':{}, 'Snack':{}}
        for idx, row in enumerate(row_):
            # find eating time
            if self.recepies.values[row,3] == 1.0:
                meals['Frühstück'] = self.extract_meal(row_[idx], row_[idx+1], meals['Frühstück'])
            if self.recepies.values[row,4] == 1.0:
                meals['Mittagessen'] = self.extract_meal(row_[idx], row_[idx+1], meals['Mittagessen'])
            if self.recepies.values[row,5] == 1.0:
                meals['Abendessen'] = self.extract_meal(row_[idx], row_[idx+1], meals['Abendessen'])
            if self.recepies.values[row,6] == 1.0:
                meals['Snack'] = self.extract_meal(row_[idx], row_[idx+1], meals['Snack'])

        return meals
    
    def choose_meals(self,
                     key:str, num_meals:int): # return list of num_meals meals
        '''
        Choose random meals based on the given meals in the .xlsx file

        Input:
            - key: key string that defines which meal type is used. Possible values are "Frühstück", "Mittagessen", "Abendessen" und "Snack". [str]
            - num_meals: number of meals that are needed for e.g., breakfasts. [int]

        Output:
            - possible_meals: dictionaries that contain the ingredients for every meal that is returned. [list of dicts]
            - possible_meals_keys: list of keys that represent the meal for which the ingredients are listed in variable "possible_meals". [list of str]
        '''

        possible_meals = self.meals[key]
        possible_meals_idx = randint(0, len(possible_meals), size=num_meals)
        possible_meals_keys = [list(possible_meals.keys())[idx] for idx in possible_meals_idx]
        possible_meals = [possible_meals[key_] for key_ in possible_meals_keys ]
        return possible_meals, possible_meals_keys

    def adjust_portion(self, meals_, meal_type):
        '''
        Adjust the portion size of all meals for one meal_type, e.g., breakfast.

        Input: 
            - meals_: all meals that are listed for one meal_type, e.g., breakfast. List with two entries.
            First entry is the dict. that contains all the ingredients of the meals.
            The second entry stores all the meals'names. [list]
            meal_type: type of meal the is adjusted, e.g., breakfast. [str]
        
        Outout: 
            - adjusted meal ingredients. [list of dicts]
            - meal names. [list of str]
        '''
        def myround(x, base=5):
            return base * round(x/base)
        
        def get_calories(meal):
            ingredients = list(meal.keys())
            cals = 0
            for ing in ingredients:
                cals += self.zutaten[ing][0] * float(meal[ing]) / 100
            return cals
        
        meals = meals_[0]
        if meal_type == 'Frühstück': # set calorie limit
            for idx, meal in enumerate(meals):
                cals = get_calories(meal)
                refactor = cals / float(self.cal_limit_breakfast)
                meal_keys = [list(meal.keys())[idx] for idx in range(len(meal))]
                for key_ in meal_keys:
                    meals[idx][key_] = str(myround(float(meal[key_]) / refactor))

        elif meal_type == 'Mittagessen':
            for idx, meal in enumerate(meals):
                cals = get_calories(meal)
                refactor = cals / float(self.cal_limit_lunch)
                meal_keys = [list(meal.keys())[idx] for idx in range(len(meal))]
                for key_ in meal_keys:
                    meals[idx][key_] = str(myround(float(meal[key_]) / refactor))

        elif meal_type == 'Abendessen':
            for idx, meal in enumerate(meals):
                cals = get_calories(meal)
                refactor = cals / float(self.cal_limit_dinner)
                meal_keys = [list(meal.keys())[idx] for idx in range(len(meal))]
                for key_ in meal_keys:
                    meals[idx][key_] = str(myround(float(meal[key_]) / refactor))

        elif meal_type == 'Snack':
            for idx, meal in enumerate(meals):
                cals = get_calories(meal)
                refactor = cals / float(self.cal_limit_snack)
                meal_keys = [list(meal.keys())[idx] for idx in range(len(meal))]
                for key_ in meal_keys:
                    meals[idx][key_] = str(myround(float(meal[key_]) / refactor))
        
        meals = [list(meal.items()) for meal in meals]
        return meals, meals_[1]

    def calculate_meals(self):
        '''
        Main function to calculate the meals for each week. First checks how many meals per day
        and time are necessary, then chooses the meals and adjusts them accoridng to the given calorie limits

        Input:
            - 

        Output:
            - breakfasts: All meals that are listed for breakfast. List with two entries.
            First entry is the dict. that contains all the ingredients of the meals.
            The second entry stores all the meals'names. [list]
            - lunches: All meals that are listed for lunches. List with two entries.
            First entry is the dict. that contains all the ingredients of the meals.
            The second entry stores all the meals'names. [list]
            - dinners: All meals that are listed for dinners. List with two entries.
            First entry is the dict. that contains all the ingredients of the meals.
            The second entry stores all the meals'names. [list]
            - snacks: All meals that are listed for snacks. List with two entries.
            First entry is the dict. that contains all the ingredients of the meals.
            The second entry stores all the meals'names. [list]
        '''
        num_breakfasts, num_lunch, num_dinner, num_snack = self.check_setting()
        breakfasts = self.adjust_portion(self.choose_meals('Frühstück', num_breakfasts), 'Frühstück') # get list of dicts of breakfasts
        lunches = self.adjust_portion(self.choose_meals('Mittagessen', num_lunch), 'Mittagessen') # get list of dicts of lunches
        dinners = self.adjust_portion(self.choose_meals('Abendessen', num_dinner), 'Abendessen') # get list of dicts of dinners
        snacks = self.adjust_portion(self.choose_meals('Snack', num_snack), 'Snack') # get list of dicts of snacks
        return breakfasts, lunches, dinners, snacks
        
    def create_pdf_weekplan(self):
        '''
        This function is called when the "Create Weekplan" button is pushed on the UI.
        It calculates the meals and puts them into a PDF as well as a shopping
        list, which is created in a seperate PDF file.

        Input:
            - 

        Output:
            - 
        '''
        def create_pdf_data(breakfasts, lunches, dinners, snacks):
            data_pdf = [['', 'Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag']]
            indices = []
            def add_meals(data_pdf, key, meals, indices):
                first_line = [key]
                indices.append(len(data_pdf))
                for elem in meals[1]:
                    first_line.append(elem)
                data_pdf.append(first_line)
                max_rows = max([len(meals[0][i]) for i in range(len(meals[0]))])
                for i in range(max_rows):
                    new_row = ['']
                    for j in range(7):
                        try:
                            entry = meals[0][j][i]
                            entry = entry[0] + ', ' + entry[1] + 'g'
                        except:
                            entry = ''
                        new_row.append(entry)
                    data_pdf.append(new_row)
                return data_pdf, indices

            data_pdf, indices = add_meals(data_pdf, 'Frühstück', breakfasts, indices)
            data_pdf, indices = add_meals(data_pdf, 'Mittagessen', lunches, indices)
            data_pdf, indices = add_meals(data_pdf, 'Abendessen', dinners, indices)
            data_pdf, indices = add_meals(data_pdf, 'Snack', snacks, indices)
            
            
            return data_pdf, indices

        def create_shopping_list(breakfasts, lunches, dinners, snacks):
            def add_items_to_shoppinglist(shopping_list, mealtime):
                for meal in mealtime[0]:
                    for ingredient in meal:
                        if ingredient[0] in shopping_list.keys():
                            shopping_list[ingredient[0]] += int(ingredient[1])
                        else:
                            shopping_list[ingredient[0]] = int(ingredient[1])
                return shopping_list
            shopping_list = {}
            shopping_list = add_items_to_shoppinglist(shopping_list, breakfasts)
            shopping_list = add_items_to_shoppinglist(shopping_list, lunches)
            shopping_list = add_items_to_shoppinglist(shopping_list, dinners)
            shopping_list = add_items_to_shoppinglist(shopping_list, snacks)
            return shopping_list


        breakfasts, lunches, dinners, snacks = self.calculate_meals()

        # PDF SHOPPING LIST
        shopping_lst_data = create_shopping_list(breakfasts, lunches, dinners, snacks)
        pdf = SimpleDocTemplate(
                                filename='einkaufsliste.pdf',
                                pagesize=A4,
                                topMargin=5, bottomMargin=5
                                )

        data_shopping_lst_title = [['Zutat', 'Menge in g']]
        data_shopping_lst = [[elem[0], elem[1]] for elem in shopping_lst_data.items()]
        data_shopping_lst_title.extend(data_shopping_lst)
        table = Table(data_shopping_lst_title)
        elems = []
        elems.append(table)

        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for headers
                            ('FONTSIZE', (0, 1), (-1, -1), 8)  # Font size for the rest of the table
                            ])
        table.setStyle(style)
        pdf.build(elems)

        # PDF WEEKPLAN
        data_pdf, indices = create_pdf_data(breakfasts, lunches, dinners, snacks)
        pdf = SimpleDocTemplate(
                                filename='ernaehrungsplan.pdf',
                                pagesize=landscape(A4),
                                topMargin=5, bottomMargin=5
                                )

        data_pdf1 = [data_pdf[i][:5] for i in range(len(data_pdf))]
        first_col = [entry[0] for entry in data_pdf]
        data_pdf2 = [[first_col[idx]] + val[5:] for idx, val in enumerate(data_pdf)]
        
        table1 = Table(data_pdf1)
        table2 = Table(data_pdf2)
        elems = []
        elems.append(table1)
        elems.append(PageBreak())
        elems.append(table2)

        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                            ('BACKGROUND', (0, 0), (0, -1), colors.darkgreen),
                            ('BACKGROUND', (0, 0), (0, 0), colors.lightgreen),
                            ('BACKGROUND', (1, indices[0]), (-1, indices[0]), colors.lightgreen),
                            ('BACKGROUND', (1, indices[1]), (-1, indices[1]), colors.lightgreen),
                            ('BACKGROUND', (1, indices[2]), (-1, indices[2]), colors.lightgreen),
                            ('BACKGROUND', (1, indices[3]), (-1, indices[3]), colors.lightgreen),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for headers
                            ('FONTSIZE', (0, 1), (-1, -1), 8)  # Font size for the rest of the table
                            ])
        table1.setStyle(style)
        table2.setStyle(style)

        
        pdf.build(elems)

        

app = QApplication(sys.argv)
UIWindow = dietplaner_UI()
app.exec_()