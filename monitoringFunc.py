import poplib
import re
import csv
import quopri
import shutil

refCodeDict = {
    "4409256": "Arena Direkt",
    "5088792": "1A Performance",
    "4576432": "ESC",
    "4948000": "Faust Marketing",
    "4310167": "HelloMail",
    "4318173": "Kajomi",
    "4589627": "Leadspot",
    "4679785": "Makromedia",
    "4471969": "mm3g",
    "4482137": "Performance Advertising",
    "4375373": "Performance Werk",
    "4576429": "ProLeagion",
    "5410356": "ReachAd",
    "4323066": "Skyline Performance",
    "4741113": "Soma",
    "4324320": "Teliatis",
    "5324079": "UIM",
    "5165514": "Zmail",
    "52854052": "Zoomail"
}

# Logs into POP3 server to retrieve E-Mails. #
class account():

    def __init__(self, serverAddress, username, password):
        self.serverAddress = serverAddress
        self.username = username
        self.password = password

    def login(self):
        self.server = poplib.POP3_SSL(self.serverAddress)
        self.server.user(self.username)
        self.server.pass_(self.password)
        self.numMessages = len(self.server.list()[1])

    def quit(self):
        self.server.quit()


# Class mail with different regular expressions to collect data from E-Mail.
class mail():

    def __init__(self, account, id):
        self.account = account
        self.id = id
        self.message = str(self.account.retr(self.id)[1])
        self.messageRaw = self.account.retr(self.id)[1]

    # checks the date the mail was received.
    def checkDate(self):
        try:
            date = re.findall("((?<=(Date: ))[^']+)", self.message)[0]
            date = re.findall("((\d+\s\w+\s\d+))", date[0])[0]
            return date[0]
        except:
            return "not identified"

    # checks the time the mail was received.
    def checkTime(self):
        try:
            time = re.findall("((?<=(Date: ))[^']+)", self.message)[0]
            time = re.findall("((\d+[:]\d+[:]\d+))", time[0])[0]
            return time[0]
        except:
            return "not identified"

    # Partners in E-Mail-Marketing were supplied a ref code in order to identify from which provider the mail was sent.
    def checkRefCode(self):
        try:
            code = re.findall("((?<=(Ref. Code: ))[\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S][\s\S])", self.message)[0]
            code = re.findall("\d", code[0])
            s = ""
            code = s.join(code)
            code = re.findall("\d\d\d\d\d\d\d", code)[0]
            return code
        except:
            return "none"

    # checks if mail template is of a certain brand of Telefonica.
    def checkTypeOfTEF(self):
        try:
            type = re.findall("(o2)", self.message)[0]
            return "o2"
        except:
            return "Blau"

    # checks the title of the Mail.
    def checkTitle(self):
        try:
            title = self.message.replace("=', b'", "")
            title = re.findall("((?<=(<title>))[^<]+)", title)[0][0]
            return title
        except:
            return "not found"

    # in the frontend users could search for a specific item in the body of the mail.
    def checkMatch(self, searchItem):
        try:
            match = self.message.replace("=', b'", "")
            match = re.findall(searchItem, match)[0]
            return match
        except:
            return "no match"

    # check the sender address of the mail.
    def checkSender(self):
        try:
            lines = str(mail(Acc1.server, i).messageRaw)
            sender = re.findall("((From: )[^']+)", lines)
            if len(sender) > 0:
                try:
                    sender = re.findall("([<][\s\S]+)", sender[0][0])
                    print(sender[0])
                except:
                    pass
            return sender
        except:
            return "sender not found"

    def subject(self):
        for i in range(1, 20):
            lines = str(mail(Acc1.server, i).messageRaw)
            subject = re.findall("((Subject: )[^']+)", lines)
            if len(subject) > 0:
                print(subject[0][0])

    # Saves the mail as .html. However coding was a bitch so there where always problems with special characters.
    def saveHTMLFile(self):
        string = ""
        for item in lines:
            item = str(item)
            item = item.replace("b'", "")
            item = item.replace("='", "")
            try:
                item = quopri.decodestring(item).decode("utf-8")
            except:
                pass
            string = string + item
        string = string.replace("'", "")
        filename = str(i) + ".html"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(string)


# For frontend use login data for the mail accounts was stored in a .csv.
def openSettings():
    with open('settings/settings.csv', 'r', newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in file:
            listAccDynamicIn.append([row[0], row[1], row[2], row[3]])

def writeSettings():
    with open('settings/settings.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar='"')
        for line in listAccDynamicOut:
            writer.writerow([line[0], line[1], line[2], line[4]])

def writeReporting():
    with open('settings/reporting.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"')
        for items in newEntries:
            writer.writerow([items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7]])

    shutil.copy('settings/reporting.csv', 'reporting/reporting.csv')

def massSearch(account, searchItem, searchCount):
    searchCount = int(searchCount)
    for i in range(0, searchCount):
        print("E-Mail #" + str(i + 1) + " wird untersucht ...")
        date = mail(account.server, account.numMessages - i).checkDate()
        title = mail(account.server, account.numMessages - i).checkTitle()
        match = mail(account.server, account.numMessages - i).checkMatch(searchItem)
        if(match != "no match"):
            try:
                mail(account.server, account.numMessages - i).saveHTMLFile()
            except:
                pass
            print("E-Mail identifiziert: "+ account.username + " - " + str(mail(account.server, account.numMessages - i).id) + " - " + date + " - " + title)

def massCheck(account, startPoint, endPoint):
    if(endPoint == "all"):
        endPoint = account.numMessages
    for i in range(startPoint, endPoint):
        date = mail(account.server, account.numMessages - i).checkDate()
        time = mail(account.server, account.numMessages - i).checkTime()
        code = mail(account.server, account.numMessages - i).checkRefCode()
        title = mail(account.server, account.numMessages - i).checkTitle()
        if(code != "none"):
            try:
                publisher = refCodeDict[code]
            except:
                publisher = "not identified"
            type = mail(account.server, account.numMessages - i).checkTypeOfTEF()
            print("E-Mail identifiziert: " + account.username + " - " + str(
                mail(account.server, account.numMessages - i).id) + " - " + date + " - " + time + " - " + code + " - " + publisher + " - " + type + " - " + title)
            newEntries.append([account.username, str(mail(account.server, account.numMessages - i).id), date, time, code, publisher, type, title])
    account.lastCrawledId = account.numMessages

    ### Speichern muss noch besser werden

#####

listAccDynamicIn = []
listAccDynamicOut = []
newEntries = []

Acc1.login()
Acc1.quit()