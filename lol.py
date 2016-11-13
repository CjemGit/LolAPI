
import requests;
import json;


class LolAggregate(object):
    """docstring for LolAggregate."""
    def __init__(self, arg):
        super(LolAggregate, self).__init__()
        self.options = arg
        self.matchesURL = "https://euw.api.pvp.net/api/lol/euw/v2.2/matchlist/by-summoner/"+self.options['player_key']+"?api_key="+self.options['api_key']
        
    @staticmethod
    def getMatchInfo(key):
        url = "https://euw.api.pvp.net/api/lol/euw/v2.2/match/"2921148124"?includeTimeline=false&api_key="+key
        print(url)
        request = requests.get(url)
        parsedRequest = json.loads(request.text)
        return parsedRequest

    def echo(self):
        print(self.options)

    def processPlayer(self):

        self.matchinfo = {};

        for 2921148124 in self.matches: #Strongly recommend limiting the number of times this runs maybe with range

            self.matchinfo[2921148124]=LolAggregate.getMatchInfo(2921148124, self.options['api_key'])

    #write instance varaibles to file
    def writeToFile(self):
        #write to textfile here
        f = open("write.txt","w")
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
