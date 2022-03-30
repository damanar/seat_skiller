###### qTqCxiIfAzqRh6Co3pczDeDcIXNNDFCV

import requests
import json
import time

#api_token = "qTqCxiIfAzqRh6Co3pczDeDcIXNNDFCV"
api_token = "gx3Qvzjamx9Hvp4qDCBywy0icsdadxKl"
api_url_base = 'http://auth.njed-eve.com/api/'
headers = {'Content-Type': 'application/json/; charset=utf-8',
            'X-Token': api_token }
output = 'char_skills.txt'
character_list = []
relevant_skills = [ 'Gunnery',
                        'Small Projectile Turret',
                            'Small Autocannon Specialization',
                            'Small Artillery Specialization',
                        'Medium Projectile Turret',
                            'Medium Autocannon Specialization',
                            'Medium Artillery Specialization',
                        'Large Projectile Turret',
                            'Large Autocannon Specialization',
                            'Large Artillery Specialization',
                        'Small Hybrid Turret',
                            'Small Blaster Specialization',
                            'Small Railgun Specialization',
                        'Medium Hybrid Turret',
                            'Medium Blaster Specialization',
                            'Medium Railgun Specialization',
                        'Large Hybrid Turret',
                            'Large Blaster Specialization',
                            'Large Railgun Specialization',
                        'Small Energy Turret',
                            'Small Pulse Laser Specialization',
                            'Small Beam Laser Specialization',
                        'Medium Energy Turret',
                            'Medium Pulse Laser Specialization',
                            'Medium Beam Laser Specialization',
                        'Large Energy Turret',
                            'Large Pulse Laser Specialization',
                            'Large Beam Laser Specialization',
                        'Small Precursor Weapon',
                            'Small Disintegrator Specialization',
                        'Medium Precursor Weapon',
                            'Medium Disintegrator Specialization',
                        'Large Precursor Weapon',
                            'Large Disintegrator Specialization',
                    'Missile Launcher Operation',
                        'Rockets',
                            'Rocket Specialization',
                        'Light Missiles',
                            'Light Missile Specialization',
                        'Heavy Assault Missiles',
                            'Heavy Assault Missile Specialization',
                        'Heavy Missiles',
                            'Heavy Missile Specialization',
                        'Torpedoes',
                            'Torpedoe Specialization',
                        'Cruise Missiles',
                            'Cruise Missile Specialization',
                    'Skirmish Command Specialist',
                    'Information Command Specialist',
                    'Armored Command Specialist',
                    'Shield Command Specialist',
                    'Spaceship Command',
                    'Advanced Spaceship Command',
                        'Amarr Frigate',
                        'Amarr Destroyer',
                        'Amarr Tactical Destroyer',
                        'Amarr Cruiser',
                        'Amarr Strategic Cruiser',
                        'Amarr Battlecruiser',
                        'Amarr Battleship',

                        'Caldari Frigate',
                        'Caldari Destroyer',
                        'Caldari Tactical Destroyer',
                        'Caldari Cruiser',
                        'Caldari Strategic Cruiser',
                        'Caldari Battlecruiser',
                        'Caldari Battleship',

                        'Gallente Frigate',
                        'Gallente Destroyer',
                        'Gallente Tactical Destroyer',
                        'Gallente Cruiser',
                        'Gallente Strategic Cruiser',
                        'Gallente Battlecruiser',
                        'Gallente Battleship',

                        'Minmatar Frigate',
                        'Minmatar Destroyer',
                        'Minmatar Tactical Destroyer',
                        'Minmatar Cruiser',
                        'Minmatar Strategic Cruiser',
                        'Minmatar Battlecruiser',
                        'Minmatar Battleship',

                        'Precursor Frigate',
                        'Precursor Destroyer',
                        'Precursor Cruiser',
                        'Precursor Battlecruiser',
                        'Precursor Battleship',
                    'Assault Frigates',
                    'Electronic Attack Ships',
                    'Interceptors',
                    'Logistic Frigates',
                    'Covert Ops',
                    'Interdictors',
                    'Command Destroyers',
                    'Heavy Assault Cruisers',
                    'Logistic Cruisers',
                    'Recon Ships',
                    'Heavy Interdiction Cruisers',
                    'Marauders',
                    'Black Ops'
                ]

class Character:
    def __init__(self, charID, name, bday, sp, usp):
        self.charID = charID
        self.name = name
        self.bday = bday
        self.sp = sp
        self.usp = usp
        self.skills = []
        self.relevantSkills = []

    def filterSkills(self, relevant ):
        for rel in relevant:
            toggle = False
            for skill in self.skills:
                if rel == skill['typeName']:
                    toggle = True
                    self.relevantSkills.append(skill['level'])
                    break
            if toggle == False:
                self.relevantSkills.append('None')

    def printChar(self):
        print( self.name, self.bday, self.sp, self.usp, self.skills, sep='\t')

    def printCharRel(self):
        print( self.name,  self.bday, self.sp, self.usp, self.relevantSkills, sep='\t')

    def writeCharRel(self):
        writeFile = ""
        for ele in [self.name, self.bday, self.sp, self.usp]:
            writeFile += str(ele)+'\t'
        for ele in self.relevantSkills:
            writeFile += str(ele)+'\t'
        writeFile += '\n'
        f = open(output, "a")
        f.write(writeFile)
        f.close()

def requestCharData(charID):
    api_url = '%scharacter/sheet/%s'%(api_url_base, charID)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8') )
        c = Character(  charID,
                        response['data']['name'],
                        response['data']['birthday'],
                        response['data']['skillpoints']['total_sp'],
                        response['data']['skillpoints']['unallocated_sp']
                        )
        time.sleep(2.4)
        requestCharSkills(c, 1)
        c.filterSkills( relevant_skills )
        #print( response['data']['name'] )
        c.writeCharRel()

def requestCharSkills(character, page):
    api_url = '%scharacter/skills/%s?page=%d'%(api_url_base, character.charID, page)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8') )
        for skill in response['data']:
            character.skills.append({
                'level': skill['trained_skill_level'],
                'typeID': skill['type']['typeID'],
                'groupID': skill['type']['groupID'],
                'typeName': skill['type']['typeName']
                })
        if response['links']['next'] != None:
            page += 1
            time.sleep(2.4)
            requestCharSkills(character, page)

def requestChars(corpID, page):
    api_url = '%scorporation/member-tracking/%s?page=%d'%(api_url_base, corpID, page)

    #print(api_url)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8') )
        getCharsFromResponse( response )
        if response['links']['next'] != None:
            
            page += 1
            time.sleep(2.4)
            requestChars(corpID, page)

def getCharsFromResponse(response):
    for char in response['data']:
        character_list.append(char['character_id'])
        #print(char['character_id'])

if __name__ == "__main__":
    writeFile = ""
    for ele in ['Name', 'Birthday', 'SP', 'Unspent']:
        writeFile += str(ele)+'\t'
    for ele in relevant_skills:
        writeFile += str(ele)+'\t'
    writeFile += '\n'

    f = open(output, "w")
    f.write(writeFile)
    f.close()

    requestChars("98367024", 1)#NJED
    time.sleep(2.4)
    requestChars("98473505", 1)#Paranoia Overload


    #requestCharData('94409075')
    for charID in character_list:
        requestCharData(charID)
    print(character_list, len(character_list))

