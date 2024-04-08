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
        off = input(" > (can be +/-): ")
        return datetime.timedelta(minutes=off)
    else: return -1

#make small class: logEntry
class logEntry:
    def __init__(self, manager, start = None, project = None):
    #attributes:
        #start time
        self.start = start
        #project
        self.project = project
        #end time
        self.end
        #total time (in hours)
        self.total
        #description of work
        self.description
        #project manager
        self.manager = manager
        #session state
        self.open


    #member functions:
    
    #clock in function:
    def clock_in(self):
        #open session
        self.open = True
        #ask current project:
        self.manager.display()
        print ("Enter 1-5 to pick existing project or enter new project name")
        p = input(" > project: ")
        if p >= 1 and p <= 5:
            self.project = self.manager.getProject(p)
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
        difference = self.start - self.end
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

        return self.start.strftime() + " - " + self.end.strftime() + "\n\ttotal hours: " + str(self.total) + ", project: " + self.project + "\n\t" + self.description + "\n"


#make small class: projectManager
class projectManager:

    def __init__(self, filename):
        #filename
        self.filename = filename
        #stack(LIFO) of recent projects (most recent 5)
        #initialize stack from filename
        f = open(filename)
        self.stack = json.load(f)
        f.close()
        
    #display most recent projects
    def display(self):
        print("Recent projects: ")
        l = len(self.stack)
        for i in range (1,l+1):
            print(" (", i, ") ", self.stack[i-1])
        
    #use nth most recent project
    def getProject(self, n):
        #move to top of recents
        self.push(self, self.stack[n-1], n-1)
        #return project name
        return self.stack[0]
    
    #create new project
    def declareProject(self, p):
        #add to top of recents
        self.push(self, p, len(self.stack)-1)

    def push(self, proj, n):
        for i in range (n-1, -1, -1):
            self.stack[i+1] = self.stack[i]
        self.stack[0] = proj
        #update file
        self.update()
        
    #update file:
    def update(self):
        f = open(self.filename, 'w')
        json.dump(self.stack, f)


#main function:
def main():
    #initialize projectManager from filename
    manager = projectManager("projList.json")
    #check for current clock in (from a previous session)
    f = open('session.json')
    entry = json.load(f)
    cur = False
    if entry.open:
        print ("active session found")
        cur = True
    #action loop:
        #create logEntry
        log = logEntry(manager)
        #if no current clock in:
        if not cur:
            #clock in
            print("type 'clock_in' when ready")
            input(" > ") 
            log.clock_in()
            #update session file
            json.dump(log, f)
        #if current clock in:
        else:
            #get current clock in information
            log = entry #I know this doesn't work but i still don't know how the jsom file thing works
        #clock out
        print("type 'clock_out' when ready")
        input (" > ")
        log.clock_out()
        #update session file
        json.dump(log, f)
        #update logfile
        l = open("timesheet.log", 'a')
        out = log.__str__()
        l.write(out)

           
if __name__ == "__main__":
    main()
