import json
import datetime

#helper functions:
def offset():
    print ("Would you like to provide an offset?")
    bin = input(" > (y/n): ")
    while bin != 'y' and bin != 'n':
        print ("please enter either a y or an n")
        bin = input(" > (y/n): ")
    if bin == 'y':
        print ("How many minutes would you like to offset by?")
        off = int(input(" > (can be +/-): "))
        return datetime.timedelta(minutes=off)
    else: return -1

#make small class: logEntry
class logEntry:
    def __init__(self, manager, start = None, project = None, end = None, total = None, description = None):
    #attributes:
        #start time
        self.start = start
        #project
        self.project = project
        #end time
        self.end = end
        #total time (in hours)
        self.total = total
        #description of work
        self.description = description
        #project manager
        self.manager = manager
        #session state
        self.open = False

    #member functions:
    
    #clock in function:
    def clock_in(self):
        #open session
        self.open = True
        #ask current project:
        self.manager.display()
        print ("Enter 1-5 to pick existing project or enter new project name")
        p = input(" > project: ")
        valid = False
        if p >= '1' and p <= '5':
            self.project = self.manager.getProject(int(p))
            valid = True
        
        else:
            self.project = p
            self.manager.declareProject(p)
            print("Your project name: ", self.project)

        #get current time/date
        time = datetime.datetime.now()

        #give offset option
        off = offset()
        if off != -1:
            self.start = time + off
        else:
            self.start = time

    #clock out function:
    def clock_out(self):
        #ask for short description of work done
        print ("Please enter a short description of work performed")
        self.description = input(" > ")
        
        #get current time/date
        time = datetime.datetime.now()

        #give offset option
        off = offset()
        if off != -1:
            self.end = time + off
        else:
            self.end = time
        
        #set total hours
        difference = self.end - self.start
        seconds = difference.total_seconds()
        self.total = seconds/3600.0

        #close session
        self.open = False

    #toString:
    def __str__(self):
        #print format: 
        #<start time> - <end time> 
        #   total hours: <total time in hours>, project: <project>
        #   <description>

        return self.start.strftime("%m/%d/%Y %H:%M") + " - " + self.end.strftime("%m/%d/%Y %H:%M") + "\n\ttotal hours: " + str(self.total) + ", project: " + self.project + "\n\t" + self.description + "\n"


#make small class: projectManager
class projectManager:

    def __init__(self, filename):
        #filename
        self.filename = filename
        self.cap = 5
        #stack(LIFO) of recent projects (most recent 5)
        #initialize stack from filename
        try:
            f = open(filename)
            self.stack = json.load(f)
            f.close()
            self.size = len(self.stack)
        except:
            self.stack = []
            self.size = 0
        
    #display most recent projects
    def display(self):
        print("Recent projects: ")
        l = len(self.stack)
        for i in range (1,l+1):
            print(" (", i, ") ", self.stack[i-1])
        
    #use nth most recent project
    def getProject(self, n):
        #move to top of recents
        self.push(self.stack[n-1])
        #return project name
        return self.stack[0]
    
    #create new project
    def declareProject(self, p):
        #add to top of recents
        self.push(p)
        

    def push(self, proj):
        #check if existing
        try:
            i = self.stack.index(proj)
        except:
            i = -1
        #if existing project
        if i != -1:
            #delete from current index
            self.stack.pop(i)
        #else if capacity is reached
        elif self.size == self.cap:
            #delete least recent
            self.stack.pop(self.cap-1)
        #else (not full and not existing)
        else:
            #update size
            self.size += 1
        #every case project being pushed goes in front
        self.stack.insert(0,proj)
        #update file
        self.update()
        
    #update file:
    def update(self):
        f = open(self.filename, 'w')
        json.dump(self.stack, f)

#Entry to dict function for storage
def toDict(entry):
    dick = {"start": datetime.datetime.strftime(entry.start, "%Y-%m-%dT%H:%M"), 
            "project": entry.project,
            "open": entry.open
            }
    return dick

#Dict to entry for retrieval
def toEntry(e, dick):
    e.start = datetime.datetime.strptime(dick["start"], "%Y-%m-%dT%H:%M")
    e.project = dick["project"]
    e.open = dick["open"]

#main function:
def main():
    #initialize projectManager from filename
    manager = projectManager("projList.json")

    #create new logEntry
    log = logEntry(manager)

    f = open('session.json', "r")

    #check for current clock in (from a previous session)
    try:
        entry = json.load(f)
        toEntry(log, entry)
    except:
        #no previous clock in
        pass

    if log.open:
        print ("active session found")

    f.close()

    #action loop:
    while True:
        #if no current clock in:
        if not log.open:
            #clock in
            print("enter anything to Clock In or <q> to quit")
            res = input(" > ") 
            if res == 'q':
                break
            log.clock_in()
            #update session file
            dick = toDict(log)
            fw = open('session.json', 'w')
            json.dump(dick, fw)   
        #if current clock in:
        else:
            #clock out
            print("enter anything to Clock Out or <q> to quit")
            res = input (" > ")
            if res == 'q':
                break
            log.clock_out()
            #update session file
            dick = toDict(log)
            fw = open('session.json', 'w')
            json.dump(dick, fw)
            #update logfile
            logfile = log.project + ".log"
            l = open(logfile, 'a')
            out = log.__str__()
            l.write(out)

           
if __name__ == "__main__":
    main()
