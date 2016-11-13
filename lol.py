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
        parsedRequest = json.loads(request.text)
        return parsedRequest

    #debug methods
    def echo(self):
        print(self.options)

    #do curls on instance variables
    def processPlayer(self):

        self.matches = [];
        self.matchinfo = {};

        self.parsedMatches = LolAggregate.doCurl(self.matchesURL)

        #loop through response matches, append to matches instance variable
        for match in self.parsedMatches["matches"]:
            self.matches.append(match["matchId"])

        #for each matchid, do curl on API, add to matchinfo instance variable
        for matchid in self.matches: #Strongly recommend limiting the number of times this runs maybe with range

      #  for matchid in range(0, self.matches[matchid] clem lol


            # https://wiki.python.org/moin/ForLoop
            #This line runs for every match returned by the first request.
            #Petey has played a shit load of this game
            self.matchinfo[matchid]=LolAggregate.getMatchInfo(matchid, self.options['api_key'])

    #write instance varaibles to file
    def writeToFile(self):
        #write to textfile here
        f = open("write.txt","w")
        f.write(json.dumps(self.parsedMatches, indent=4, sort_keys=True))
        f.write(json.dumps(self.matches, indent=4, sort_keys=True))
        f.write(json.dumps(self.matchinfo, indent=4, sort_keys=True))
        f.close();

#arguments passed to new object
arguments = {
"api_key":"RGAPI-5a0bc5da-5244-45f6-bfe1-b1a42b892835",
"player_key":"36098962" #change the player id here, by changing this number you could get your own info instead of Pete's
}

#Main script calls

#create object, parsing in the arguments
obj = LolAggregate(arguments)

#call methods

#do requests
obj.processPlayer();

#write to external file
obj.writeToFile();
