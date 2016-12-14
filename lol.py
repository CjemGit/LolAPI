##
# League of Legends API Call
# This works, It does the call for the player and then individual calls for each match returned by the first request
#
# The API seems to be incredibly flaky and seems to run forever so i'm not entirely sure I'm making the requests correctly
# you definitely need to reduce the number or returned requests this process returned a 75MB file.
#
# I did this with Python, because i thought it would be a larf
# couldve used anything, i guess
#
# Code By Jossy
#
##


#module imports
import sys;
import requests;
import json;

#define class
class LolAggregate(object):
    """docstring for LolAggregate."""
    def __init__(self, arg):
        super(LolAggregate, self).__init__()
        self.options = arg
        self.matchesURL = "https://euw.api.pvp.net/api/lol/euw/v2.2/matchlist/by-summoner/"+self.options['player_key']+"?api_key="+self.options['api_key']

    #Static methods are on the class not the object. they are called using the classname e.g LolAggregate.doCurl()
    #These differ from instance methods e.g. obj.doCurl wont work.
    #You can also call them without instantiating an object; LolAggregate.doCurl(url) will always work
    #I'm not sure i'm using them correctly but here are some examples.

    @staticmethod
    def doCurl(url):
        request = requests.get(url)
        parsedRequest = json.loads(request.text)
        return parsedRequest

    @staticmethod
    def getMatchInfo(matchID,key):
        url = "https://euw.api.pvp.net/api/lol/euw/v2.2/match/"+str(matchID)+"?includeTimeline=false&api_key="+key
        print(url)
        request = requests.get(url)
        print(request.encoding)
        parsedRequest = json.loads(request.text)
        return parsedRequest

    @staticmethod
    def getParticipantId(userID,matchInfo):
        #print json.dumps(matchInfo, indent=4, sort_keys=True)
        success = True if "participantIdentities" in matchInfo else False
        print("participants found "+ str(success))
        if success == True:
            for participant in matchInfo["participantIdentities"]:
                if participant["player"]["summonerId"]==int(userID):
                    return participant["participantId"]
        else:
            return False

    #debug methods
    def echo(self):
        print(self.options)

    #do curls on instance variables
    def processPlayer(self):

        self.matches = [];
        self.matchinfo = {};
        self.info = [];
        self.parsedMatches = LolAggregate.doCurl(self.matchesURL)
        #print json.dumps(self.parsedMatches, indent=4, sort_keys=True)
        #loop through response matches, append to matches instance variable
        fail = True if "status" in self.parsedMatches["matches"] else False
        if fail==False:
            for match in self.parsedMatches["matches"]:
                 self.matches.append(match["matchId"])

            #for each matchid, do curl on API, add to matchinfo instance variable
            #for matchid in self.matches: #Strongly recommend limiting the number of times this runs maybe with range
            requests = 0
            for matchid in self.matches:

                requests+=1
                # https://wiki.python.org/moin/ForLoop
                #This line runs for every match returned by the first request.
                #Petey has played a shit load of this game
                info = {}
                info["matchid"] = matchid
                info["stats"] = {}

                #traverse returned objects for info
                self.matchinfo[matchid]=LolAggregate.getMatchInfo(matchid, self.options['api_key'])
                fail = True if "status" in self.matchinfo[matchid] == "Present" else False
                if fail==False:
                    participant = LolAggregate.getParticipantId(self.options["player_key"],self.matchinfo[matchid])
                    if participant:
                        lane = self.matchinfo[matchid]["participants"][participant-1]["timeline"]["lane"]
                        stats = self.matchinfo[matchid]["participants"][participant-1]["stats"]

                        #assemble object
                        info["stats"]["assists"] = stats["assists"];
                        info["stats"]["goldEarned"] = stats["goldEarned"];
                        info["stats"]["kills"] = stats["kills"];
                        info["stats"]["totalDamageDealt"] = stats["totalDamageDealt"];
                        info["stats"]["winner"] = stats["winner"];
                        info["stats"]["lane"] = lane;

                        #append to instance variable "info"
                        self.info.append(info)
                else:
                    continue

                #break if request limit is set
                try:
                    self.options["request_limit"]
                except NameError:
                    print("unset")
                else:
                  if requests>=self.options["request_limit"]:
                      break
            else:
                print("fail on initial request")

    #write instance varaibles to file
    def writeToFile(self):
        #write to textfile here
        f = open("write.txt","w")
        # f.write(json.dumps(self.parsedMatches, indent=4, sort_keys=True))
        # f.write(json.dumps(self.matches, indent=4, sort_keys=True))
        # f.write(json.dumps(self.matchinfo, indent=4, sort_keys=True))
        f.write(json.dumps(self.info, indent=4, sort_keys=True))
        f.close();

#arguments passed to new object
arguments = {
"api_key":"RGAPI-5a0bc5da-5244-45f6-bfe1-b1a42b892835",
"player_key":"36098962", #change the player id here, by changing this number you could get your own info instead of Pete's
"request_limit":20 # will limit the number of requests by stopping loop after this number of requests
}

#Main script calls

#create object, parsing in the arguments
obj = LolAggregate(arguments)

#call methods

#do requests
obj.processPlayer();

#write to external file
obj.writeToFile();
