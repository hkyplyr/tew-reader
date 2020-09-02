from args import args

PERCEPTION_RATINGS = {
    0: 'To Be Decided',
    1: 'Major Star',
    2: 'Star',
    3: 'Well Known',
    4: 'Recognisable',
    5: 'Unimportant'}


def get_momentum_text(rating):
    if rating > 500:
        return 'White Hot'
    elif rating > 400:
        return 'Red Hot'
    elif rating > 300:
        return 'Very Hot'
    elif rating > 200:
        return 'Hot'
    elif rating > 100:
        return 'Very Warm'
    elif rating > 0:
        return 'Warm'
    elif rating == 0:
        return 'Neutral'
    elif rating < -300:
        return 'Very Cold'
    elif rating < -200:
        return 'Cold'
    elif rating < -100:
        return 'Chilly'
    elif rating < 0:
        return 'Cooled'


class Worker:
    def __init__(self, row):
        self.worker_id = row['WorkerUID']
        self.name = row['Name']
        self.raw_disposition = int(row['Face'])
        self.disposition = 'Face' if self.raw_disposition else 'Heel'
        self.raw_gender = int(row['Male'])
        self.gender = 'Male' if self.raw_gender else 'Female'
        self.raw_perception = int(row['Perception'])
        self.perception_score = int(row['PerceptionScore'])
        self.perception = PERCEPTION_RATINGS.get(self.raw_perception)
        self.raw_momentum = int(row['ContractMomentum'])
        self.momentum = get_momentum_text(self.raw_momentum)
        self.role = self.__get_role(row)

    def get_sort_key(self, sort_key, region='canada'):
        if sort_key == 'perception':
            return self.perception_score
        elif sort_key == 'momentum':
            return self.raw_momentum
        elif sort_key == 'overness':
            return getattr(self.overness, region)
        try:
            return getattr(self, sort_key)
        except AttributeError:
            return getattr(self.skills, sort_key)

    def set_age(self, age):
        self.age = age

    def set_skills(self, skills):
        self.skills = skills

    def set_overness(self, overness):
        self.overness = overness

    def get_as_row(self):
        return [self.name, self.age, self.disposition, self.gender, self.role, self.perception,
                self.momentum] + self.overness.get_as_row() + self.skills.get_as_row()

    def __get_role(self, row):
        if int(row['Position_Wrestler']):
            return 'Wrestler'
        elif int(row['Position_Occasional']):
            return 'Occasional'
        elif int(row['Position_Referee']):
            return 'Referee'
        elif int(row['Position_Announcer']):
            return 'Announcer'
        elif int(row['Position_Colour']):
            return 'Colour'
        elif int(row['Position_Manager']):
            return 'Manager'
        elif int(row['Position_Personality']):
            return 'Personality'
        elif int(row['Position_Roadagent']):
            return 'Road Agent'
        else:
            return 'Unknown'

    @staticmethod
    def get_header_names():
        return ['Name', 'Age', 'Disposition', 'Gender', 'Role', 'Perception', 'Momentum'] \
            + Overness.get_header_names() \
            + Skills.get_header_names()


class Skills:
    def __init__(self, row):
        self.worker_id = row['WorkerUID']

        self.brawl = self.__get_tew_value(row, 'Brawl')
        self.puroresu = self.__get_tew_value(row, 'Puroresu')
        self.hardcore = self.__get_tew_value(row, 'Hardcore')
        self.technical = self.__get_tew_value(row, 'Technical')
        self.air = self.__get_tew_value(row, 'Air')
        self.flash = self.__get_tew_value(row, 'Flash')
        self.primary_total = [self.brawl, self.puroresu, self.hardcore, self.technical, self.air, self.flash]
        self.primary = round(sum(self.primary_total) / len(self.primary_total))

        self.psych = self.__get_tew_value(row, 'Psych')
        self.experience = self.__get_tew_value(row, 'Experience')
        self.respect = self.__get_tew_value(row, 'Respect')
        self.reputation = self.__get_tew_value(row, 'Reputation')
        self.mental_total = [self.psych, self.experience, self.respect, self.reputation]
        self.mental = round(sum(self.mental_total) / len(self.mental_total))

        self.charisma = self.__get_tew_value(row, 'Charisma')
        self.mic = self.__get_tew_value(row, 'Mic')
        self.act = self.__get_tew_value(row, 'Act')
        self.star = self.__get_tew_value(row, 'Star')
        self.looks = self.__get_tew_value(row, 'Looks')
        self.menace = self.__get_tew_value(row, 'Menace')
        self.performance_total = [self.charisma, self.mic, self.act, self.star, self.looks, self.menace]
        self.performance = round(sum(self.performance_total) / len(self.performance_total))

        self.basics = self.__get_tew_value(row, 'Basics')
        self.sell = self.__get_tew_value(row, 'Sell')
        self.consistency = self.__get_tew_value(row, 'Consistency')
        self.safety = self.__get_tew_value(row, 'Safety')
        self.fundamental_total = [self.basics, self.sell, self.consistency, self.safety]
        self.fundamental = round(sum(self.fundamental_total) / len(self.fundamental_total))

        self.stamina = self.__get_tew_value(row, 'Stamina')
        self.athletic = self.__get_tew_value(row, 'Athletic')
        self.power = self.__get_tew_value(row, 'Power')
        self.tough = self.__get_tew_value(row, 'Tough')
        self.injury = self.__get_tew_value(row, 'Injury')
        self.pysical_total = [self.stamina, self.athletic, self.power, self.tough, self.injury]
        self.physical = round(sum(self.pysical_total) / len(self.pysical_total))

        self.announcing = self.__get_tew_value(row, 'Announcing')
        self.colour = self.__get_tew_value(row, 'Colour')
        self.referee = self.__get_tew_value(row, 'Refereeing')
        self.other_total = [self.announcing, self.colour, self.referee]
        self.other = round(sum(self.other_total) / len(self.other_total))

    def get_as_row(self):
        if args.type == 'simple':
            return [self.primary, self.mental, self.performance, self.fundamental, self.physical, self.other]
        elif args.type == 'complex':
            return [self.brawl, self.puroresu, self.hardcore, self.technical, self.air, self.flash,
                    self.psych, self.experience, self.respect, self.reputation, self.charisma, self.mic,
                    self.act, self.star, self.looks, self.mental, self.basics, self.sell, self.consistency,
                    self.safety, self.stamina, self.athletic, self.power, self.tough, self.injury,
                    self.announcing, self.colour, self.referee]

            return [self.brawl, self.air, self.technical, self.power,
                    self.athletic, self.stamina, self.psych, self.basics, self.tough,
                    self.sell, self.charisma, self.mic, self.menace, self.respect, self.reputation,
                    self.safety, self.looks, self.star, self.consistency, self.act,
                    self.injury, self.puroresu, self.flash, self.hardcore, self.announcing,
                    self.colour, self.referee, self.experience]

    def __get_tew_value(self, row, name):
        return round(int(row[name]) / 10)

    @staticmethod
    def get_header_names():
        if args.type == 'simple':
            return ['Primary', 'Mental', 'Performance', 'Fundamental', 'Physical', 'Other']
        elif args.type == 'complex':
            return ['Brawl', 'Puroresu', 'Hardcore', 'Technical', 'Aerial', 'Flashiness', 'Psychology', 'Experience',
                    'Respect', 'Reputation', 'Charisma', 'Microphone', 'Acting', 'Star Quality', 'Sex Appeal', 'Menace',
                    'Basics', 'Selling', 'Consistency', 'Safety', 'Stamina', 'Athleticism', 'Power', 'Toughness',
                    'Resilience', 'Announcing', 'Colour', 'Refereeing']


class Overness:
    def __init__(self, row):
        self.worker_id = row['WorkerUID']

        self.great_lakes = int(row['Over1'])
        self.mid_atlantic = int(row['Over2'])
        self.mid_south = int(row['Over3'])
        self.mid_west = int(row['Over4'])
        self.new_england = int(row['Over5'])
        self.north_west = int(row['Over6'])
        self.south_east = int(row['Over7'])
        self.south_west = int(row['Over8'])
        self.tri_state = int(row['Over9'])
        self.puerto_rico = int(row['Over10'])
        self.hawaii = int(row['Over11'])
        self.usa_total = [self.great_lakes, self.mid_atlantic, self.mid_south, self.mid_west, self.new_england,
                          self.north_west, self.south_east, self.south_west, self.tri_state, self.puerto_rico,
                          self.hawaii]
        self.usa = round(sum(self.usa_total) / len(self.usa_total) / 10)

        self.maritimes = int(row['Over12'])
        self.quebec = int(row['Over13'])
        self.ontario = int(row['Over14'])
        self.alberta = int(row['Over15'])
        self.saskatchewan = int(row['Over16'])
        self.manitoba = int(row['Over17'])
        self.british_columbia = int(row['Over18'])
        self.canada_total = [self.maritimes, self.quebec, self.ontario, self.alberta, self.saskatchewan, self.manitoba,
                             self.british_columbia]
        self.canada = round(sum(self.canada_total) / len(self.canada_total) / 10)

        self.noreste = int(row['Over19'])
        self.noroccidente = int(row['Over20'])
        self.sureste = int(row['Over21'])
        self.sur = int(row['Over22'])
        self.centro = int(row['Over23'])
        self.occidente = int(row['Over24'])
        self.mexico_total = [self.noreste, self.noroccidente, self.sureste, self.sur, self.centro, self.occidente]
        self.mexico = round(sum(self.mexico_total) / len(self.mexico_total) / 10)

        self.midlands = int(row['Over25'])
        self.northern_england = int(row['Over26'])
        self.scotland = int(row['Over27'])
        self.southern_england = int(row['Over28'])
        self.ireland = int(row['Over29'])
        self.wales = int(row['Over30'])
        self.british_isles_total = [self.midlands, self.northern_england, self.scotland, self.southern_england,
                                    self.ireland, self.wales]
        self.british_isles = round(sum(self.british_isles_total) / len(self.british_isles_total) / 10)

        self.tohoku = int(row['Over31'])
        self.kanto = int(row['Over32'])
        self.chubu = int(row['Over33'])
        self.kansai = int(row['Over34'])
        self.chuguko = int(row['Over35'])
        self.shikoku = int(row['Over36'])
        self.kyushu = int(row['Over37'])
        self.hokkaido = int(row['Over38'])
        self.japan_total = [self.tohoku, self.kanto, self.chubu, self.kansai, self.chuguko, self.shikoku, self.kyushu,
                            self.hokkaido]
        self.japan = round(sum(self.japan_total) / len(self.japan_total) / 10)

        self.western_europe = int(row['Over39'])
        self.iberia = int(row['Over40'])
        self.southern = int(row['Over41'])
        self.southern_europe = int(row['Over42'])
        self.central_europe = int(row['Over43'])
        self.scandanavia = int(row['Over44'])
        self.eastern_europe = int(row['Over45'])
        self.russia = int(row['Over46'])
        self.europe_total = [self.western_europe, self.iberia, self.southern, self.southern_europe, self.central_europe,
                             self.scandanavia, self.eastern_europe, self.russia]
        self.europe = round(sum(self.europe_total) / len(self.europe_total) / 10)

        self.new_south_wales = int(row['Over47'])
        self.queensland = int(row['Over48'])
        self.south_australia = int(row['Over49'])
        self.victoria = int(row['Over50'])
        self.western_australia = int(row['Over51'])
        self.tasmania = int(row['Over52'])
        self.new_zealand = int(row['Over53'])
        self.oceania_total = [self.new_south_wales, self.queensland, self.south_australia, self.victoria,
                              self.western_australia, self.tasmania, self.new_zealand]
        self.oceania = round(sum(self.oceania_total) / len(self.oceania_total) / 10)

        self.northern_india = int(row['Over54'])
        self.central_india = int(row['Over55'])
        self.southern_india = int(row['Over56'])
        self.india_total = [self.northern_india, self.central_india, self.southern_india]
        self.india = round(sum(self.india_total) / len(self.india_total) / 10)

    def get_as_row(self, region='canada'):
        return [getattr(self, region)]

    @staticmethod
    def get_header_names():
        return ['Overness']
