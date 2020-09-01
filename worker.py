PERCEPTION_RATINGS = {0: 'To Be Decided', 1: 'Major Star', 2: 'Star', 3: 'Well Known', 4: 'Recognisable', 5: 'Unimportant'}

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

    def set_skills(self, skills):
        self.skills = skills
    
    def set_overness(self, overness):
        self.overness = overness

    def get_as_row(self):
        return [self.worker_id, self.name, self.disposition, self.gender, self.role, self.perception, self.momentum] + self.overness.get_as_row() + self.skills.get_as_row()

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

class Skills:
    def __init__(self, row):
        self.id = row['WorkerUID']
        self.brawl = round(int(row['Brawl']) / 10)
        self.air = round(int(row['Air']) / 10)
        self.technical = round(int(row['Technical']) / 10)
        self.power = round(int(row['Power']) / 10)
        self.athletic = round(int(row['Athletic']) / 10)
        self.stamina = round(int(row['Stamina']) / 10)
        self.psych = round(int(row['Psych']) / 10)
        self.basics = round(int(row['Basics']) / 10)
        self.tough = round(int(row['Tough']) / 10)
        self.sell = round(int(row['Sell']) / 10)
        self.charisma = round(int(row['Charisma']) / 10)
        self.mic = round(int(row['Mic']) / 10)
        self.menace = round(int(row['Menace']) / 10)
        self.respect = round(int(row['Respect']) / 10)
        self.reputation = round(int(row['Reputation']) / 10)
        self.safety = round(int(row['Safety']) / 10)
        self.looks = round(int(row['Looks']) / 10)
        self.star = round(int(row['Star']) / 10)
        self.consistency = round(int(row['Consistency']) / 10)
        self.act = round(int(row['Act']) / 10)
        self.injury = round(int(row['Injury']) / 10)
        self.puroresu = round(int(row['Puroresu']) / 10)
        self.flash = round(int(row['Flash']) / 10)
        self.hardcore = round(int(row['Hardcore']) / 10)
        self.announcing = round(int(row['Announcing']) / 10)
        self.colour = round(int(row['Colour']) / 10)
        self.referee = round(int(row['Refereeing']) / 10)
        self.experience = round(int(row['Experience']) / 10)
    
    def get_as_row(self):
        return [self.brawl, self.air, self.technical, self.power,
                self.athletic, self.stamina, self.psych, self.basics, self.tough,
                self.sell, self.charisma, self.mic, self.menace, self.respect, self.reputation,
                self.safety, self.looks, self.star, self.consistency, self.act,
                self.injury, self.puroresu, self.flash, self.hardcore, self.announcing,
                self.colour, self.referee, self.experience]

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
        self.usa_total = [self.great_lakes, self.mid_atlantic, self.mid_south, self.mid_west, self.new_england, self.north_west,
                          self.south_east, self.south_west, self.tri_state, self.puerto_rico, self.hawaii]
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
        self.british_isles_total = [self.midlands, self.northern_england, self.scotland, self.southern_england, self.ireland, self.wales]
        self.british_isles = round(sum(self.british_isles_total) / len(self.british_isles_total) / 10)

        self.tohoku = int(row['Over31'])
        self.kanto = int(row['Over32'])
        self.chubu = int(row['Over33'])
        self.kansai = int(row['Over34'])
        self.chuguko = int(row['Over35'])
        self.shikoku = int(row['Over36'])
        self.kyushu = int(row['Over37'])
        self.hokkaido = int(row['Over38'])
        self.japan_total = [self.tohoku, self.kanto, self.chubu, self.kansai, self.chuguko, self.shikoku, self.kyushu, self.hokkaido]
        self.japan = round(sum(self.japan_total) / len(self.japan_total) / 10)


        self.western_europe = int(row['Over39'])
        self.iberia = int(row['Over40'])
        self.southern = int(row['Over41'])
        self.southern_europe = int(row['Over42'])
        self.central_europe = int(row['Over43'])
        self.scandanavia = int(row['Over44'])
        self.eastern_europe = int(row['Over45'])
        self.russia = int(row['Over46'])
        self.europe_total = [self.western_europe, self.iberia, self.southern, self.southern_europe, self.central_europe, self.scandanavia,
                             self.eastern_europe, self.russia]
        self.europe = round(sum(self.europe_total) / len(self.europe_total) / 10)

        self.new_south_wales = int(row['Over47'])
        self.queensland = int(row['Over48'])
        self.south_australia = int(row['Over49'])
        self.victoria = int(row['Over50'])
        self.western_australia = int(row['Over51'])
        self.tasmania = int(row['Over52'])
        self.new_zealand = int(row['Over53'])
        self.oceania_total = [self.new_south_wales, self.queensland, self.south_australia, self.victoria, self.western_australia, self.tasmania,
                              self.new_zealand]
        self.oceania = round(sum(self.oceania_total) / len(self.oceania_total) / 10)

        self.northern_india = int(row['Over54'])
        self.central_india = int(row['Over55'])
        self.southern_india = int(row['Over56'])
        self.india_total = [self.northern_india, self.central_india, self.southern_india]
        self.india = round(sum(self.india_total) / len(self.india_total) / 10)

    def get_as_row(self, region='canada'):
        return [getattr(self, region)]