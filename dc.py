from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument(r"--user-data-dir=C:\YOUR USER\etfri\AppData\Local\Temp\YOUR_SCOPED_DIR") # <-- replace with you info
site = webdriver.Chrome(executable_path=r"chromedriver.exe", options=chrome_options)

class DeathCount():
    def __init__(self):
        streamer = str(input("What streamer chat would you like to type in?\n> "))
        site.get('https://www.twitch.tv/popout/' + streamer + "/chat?popout=")
        self.chat = site.find_elements_by_tag_name('textarea')[0]

    def set_text(self):
        self.num_counters = int(input("please enter the number of counters you would like to include\n\n>"))
        self.counter = input("Input the text you would like to have accompany the death count. place '\{\}' where you would like the death count to be put in the text, i.e. 'current deaths: \{\}' would yield 'current deaths: 125' For adding a secondary counter, include \{\}, \{\}, etc.\n\n>")
        self.counters = [0]*self.num_counters
        for x in range(self.num_counters):
            self.counters[x] = int(input("Value of {} death counter\n>".format(x+1)))
        self.counter = self.counter.format(*(i for i in self.counters))

    def add_count(self):
        for val in self.counters:
            self.counter = self.counter.replace(str(val),str(val+1))
        print(self.counter)
        self.chat.send_keys(self.counter)
        self.chat.send_keys(Keys.RETURN)
        for num in self.counters:
            self.counters[self.counters.index(num)] = self.counters[self.counters.index(num)]+1

    def repeat(self):
        self.chat.send_keys(self.counter)
        self.chat.send_keys(Keys.RETURN)

first_count = DeathCount()
first_count.set_text()

while True:
    inp = str(input("+ to add count, 'r' to send same count again, '-' to stop\n>"))
    if inp == "+":
        first_count.add_count()
    if inp == "-":
        break
    if inp == "r":
        first_count.repeat()
