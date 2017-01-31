import tweepy, json, requests, time, datetime, os, ConfigParser

# Function to access the access token stored within the configuration file
def ConfigSectionMap(section):
    Config = ConfigParser.ConfigParser()
    Config.read("/root/***/**.ini")

    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

CONSUMER_KEY = ConfigSectionMap("auth_parms")['consumer_key']
CONSUMER_SECRET = ConfigSectionMap("auth_parms")['consumer_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ConfigSectionMap("auth_parms")['access_token'], ConfigSectionMap("auth_parms")['access_secret'])

competitors = json.loads(ConfigSectionMap("competitors")['names'])

api = tweepy.API(auth)

def get_data(competitor):
        data = api.get_user(competitor)
        return data

capture_date = time.strftime("%Y-%m-%d"" ""%H:%M:%S")

file_name = "/root/katara-arabic/data/user_details/" + str(datetime.datetime.now().day) + str(datetime.datetime.now().month) + \
                str(datetime.datetime.now().year) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + '_user_details'

print 'Location of file: ' + file_name

target1 = open(file_name, 'w')

def writef(field,eof):
        if field is None:
                target1.write('NULL') #print NULL is not data found
        else:
                target1.write(field)
        if eof == 'N':
                target1.write('`')
        elif eof == 'Y':
                target1.write("\n")

def write_data(data):
        try:
                writef(str(capture_date),'N')
                writef(str(data.screen_name.encode('utf-8')),'N')
                writef(str(data.id_str),'N')
                writef(str(data.followers_count),'N')
                writef(str(data.statuses_count),'N')
                writef(str(data.favourites_count),'N')
                writef(str(data.friends_count),'N')
                writef(str(data.listed_count),'N')
                writef(str(data.time_zone),'N')
                writef(str(data.listed_count),'Y')
        except KeyError, e:
                writef(None,'N')

class Scrape:
        for competitor in competitors['competitor']:
                data1 = get_data(competitor)
                write_data(data1)

if __name__ == "__main__":
    s = Scrape()
