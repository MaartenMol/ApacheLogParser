# Log Parser by Maarten Mol
# Version 1.2
# Made for Individual Propedeuse Assessment @ HU

# Define imports
import sys
import os
import os.path
import configparser
import time

# Config parsing for config.ini
# The config.ini is loaded in function: startUp
config = configparser.ConfigParser()

# Set default variable for the settings menu if restart is required after altering settings
restartRequired = False

# Define clear command to clear console/interface
clear = lambda: os.system('cls')

# Define colors and styling
class sCol:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    CRIT = '\033[91m'
    ENDC = '\033[0m'
    B = '\033[1m'
    U = '\033[4m'

# Process raw log file
# Splits every line in specified blocks
# After split, every line is a list, this list is then added in a list with all the other lines
def logProc():
    log = open(logFile, mode='r')

    for x in log.readlines():
        hostname = x.split(' ')[0]
        time = x.split('[', 1)[1].split(']')[0]
        request = x.split('"', 1)[1].split('"')[0]
        status = x.split(' ')[-2]
        size = x.split(' ')[-1].replace('\n', '')

        logLine = [hostname, time, request, status, size]
        logData.append(logLine)

        if debugMode == True:
            print(logLine)

    log.close()

# Process processed log file by status code
# Reads the logData list and opens every list in it for the status code value
# If the status code already exists it will be added to the dictionary
# If the status code doesn't exist a new key will be created in the dictionary
def errorCodeProc():
    global replyCodes

    replyCodes = {}

    for item in logData:
        if item[3] in replyCodes:
            replyCodes[item[3]].append(item)
            replyCodes[item[3]][0] += 1
        elif item[3] not in replyCodes:
            replyCodes[item[3]] = []
            replyCodes[item[3]].append(1)
            replyCodes[item[3]].append(item)

# Request logs by code and output in HTML
# Reads the dictionary and looks for the given status code
# Results are printed in HTML if debug mode is enabled it is also printed in console
def errorCodeCheck(Code):
    results = open(resultsFile, mode='w')

    results.write('<!DOCTYPE html>\n')
    results.write('<html lang="en">\n')
    results.write('<head>\n')
    results.write('<meta charset="UTF-8">\n')
    results.write('<title>Log Parser by Maarten Mol</title>\n')
    results.write('<style type="text/css">\n')
    results.write('table {width : 100%; table-layout: fixed; white-space: nowrap;}\n')
    results.write('td {display: inline-block; max-width: 20%; min-width: 20%; overflow: hidden; text-overflow: ellipsis; vertical-align: top; white-space: nowrap;}\n')
    results.write('td:hover {text-overflow: clip; white-space: normal; word-break: break-all;}\n')
    results.write('</style>\n')
    results.write('</head>\n')
    results.write('<body>\n')
    results.write('<p style="font-size:25px">Total lines: <i>{}</i> with filter: <b>Status Code:</b> <i>{}</i></p>'.format(replyCodes[Code][0], Code))
    results.write('<table>\n')
    results.write("<tr><td><b>Host</b></td><td><b>Day & Time</b></td><td><b>Request</b></td><td><b>Status</b></td><td><b>Size</b></td></tr>\n")

    for item in replyCodes[Code]:
        if type(item) == int:
            continue
        else:
            results.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4])))

            if debugMode == True:
                print(item)

    results.write('</table>\n')
    results.write('</body>\n')
    results.write('</html>\n')

    results.close()

# Process processed log file by hostname
# Reads the logData list and opens every list in it for the host value
# If the host already exists it will be added to the dictionary
# If the host doesn't exist a new key will be created in the dictionary
def errorHostProc():
    global replyHosts
    replyHosts = {}

    for item in logData:
        if item[0] in replyHosts:
            replyHosts[item[0]].append(item)
            replyHosts[item[0]][0] += 1
        elif item[0] not in replyHosts:
            replyHosts[item[0]] = []
            replyHosts[item[0]].append(1)
            replyHosts[item[0]].append(item)

# Request logs by hostname
# Reads the dictionary and looks for the given host
# Results are printed in HTML if debug mode is enabled it is also printed in console
def errorHostCheck(host):
    results = open(resultsFile, mode='w')

    results.write('<!DOCTYPE html>\n')
    results.write('<html lang="en">\n')
    results.write('<head>\n')
    results.write('<meta charset="UTF-8">\n')
    results.write('<title>Log Parser by Maarten Mol</title>\n')
    results.write('<style type="text/css">\n')
    results.write('table {width : 100%; table-layout: fixed; white-space: nowrap;}\n')
    results.write('td {display: inline-block; max-width: 20%; min-width: 20%; overflow: hidden; text-overflow: ellipsis; vertical-align: top; white-space: nowrap;}\n')
    results.write('td:hover {text-overflow: clip; white-space: normal; word-break: break-all;}\n')
    results.write('</style>\n')
    results.write('</head>\n')
    results.write('<body>\n')
    results.write('<p style="font-size:25px">Total lines: <i>{}</i> with filter: <b>Host:</b> <i>{}</i></p>'.format(replyHosts[host][0], host))
    results.write('<table>\n')
    results.write("<tr><td><b>Host</b></td><td><b>Day & Time</b></td><td><b>Request</b></td><td><b>Status</b></td><td><b>Size</b></td></tr>\n")

    for item in replyHosts[host]:
        if type(item) == int:
            continue
        else:
            results.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4])))

            if debugMode == True:
                print(item)

    results.write('</table>\n')
    results.write('</body>\n')
    results.write('</html>\n')

    results.close()

# Request logs per host and count
# Reads the logData list and opens every list in it for the host value
# If the host already exists the value in the dictionary of that host will be +1
# If the host doesn't exist a new key will be created in the dictionary with a value of 1
def errorCountHost():
    unique_dict = {}

    for item in logData:
        if item[0] in unique_dict:
            unique_dict[item[0]] += 1
        elif item[0] not in unique_dict:
            unique_dict[item[0]] = 1

    results = open(resultsFile, mode='w')

    results.write('<!DOCTYPE html>\n')
    results.write('<html lang="en">\n')
    results.write('<head>\n')
    results.write('<meta charset="UTF-8">\n')
    results.write('<title>Log Parser by Maarten Mol</title>\n')
    results.write('<style type="text/css">\n')
    results.write('table {width : 100%; table-layout: fixed; white-space: nowrap;}\n')
    results.write('td {display: inline-block; max-width: 20%; min-width: 20%; overflow: hidden; text-overflow: ellipsis; vertical-align: top; white-space: nowrap;}\n')
    results.write('td:hover {text-overflow: clip; white-space: normal; word-break: break-all;}\n')
    results.write('</style>\n')
    results.write('</head>\n')
    results.write('<body>\n')
    results.write('<p style="font-size:25px">List of all hosts with filter: <i>count unique hosts</i></p>')
    results.write('<table>\n')
    results.write("<tr><td><b>Host</b></td><td><b>Counter</b></td></tr>\n")

    for item in unique_dict:
        results.write('<tr><td>{}</td><td>{}</td></tr>\n'.format(str(item), str(unique_dict[item])))

        if debugMode == True:
                print(item + ': ' + str(unique_dict[item]))

    results.write('</table>\n')
    results.write('</body>\n')
    results.write('</html>\n')

    results.close()

# Request all logs
# Reads and prints all from logData
def errorLogs():
    results = open(resultsFile, mode='w')

    results.write('<!DOCTYPE html>\n')
    results.write('<html lang="en">\n')
    results.write('<head>\n')
    results.write('<meta charset="UTF-8">\n')
    results.write('<title>Log Parser by Maarten Mol</title>\n')
    results.write('<style type="text/css">\n')
    results.write('table {width : 100%; table-layout: fixed; white-space: nowrap;}\n')
    results.write('td {display: inline-block; max-width: 20%; min-width: 20%; overflow: hidden; text-overflow: ellipsis; vertical-align: top; white-space: nowrap;}\n')
    results.write('td:hover {text-overflow: clip; white-space: normal; word-break: break-all;}\n')
    results.write('</style>\n')
    results.write('</head>\n')
    results.write('<body>\n')
    results.write('<p style="font-size:25px">All logs</p>')
    results.write('<table>\n')
    results.write("<tr><td><b>Host</b></td><td><b>Day & Time</b></td><td><b>Request</b></td><td><b>Status</b></td><td><b>Size</b></td></tr>\n")

    for item in logData:
        results.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4])))

        if debugMode == True:
                print(item)

    results.write('</table>\n')
    results.write('</body>\n')
    results.write('</html>\n')

    results.close()

# Startup script
# Config file will be loaded here to simply reload if something changes and not load it when unnecessary
# Config file is being checked, if it doesn't exist it will be created with default values
# If the config file exists but misses certain parameters or sections they will be added
# The log file is being checked if it exists, if not you will be redirected to the settings menu immediately
def startUp():
    global logFile, resultsFile, debugMode, exitMode, restartRequired, logData

    # Define empty list for first log processing from raw log file
    logData = []

    configFile = "config.ini"

    checkConfigStatus = os.path.isfile(configFile)

    if checkConfigStatus == False:

        print(sCol.CRIT + "Config file not found! Generating one with default settings now..." + sCol.ENDC)

        configWriter = open(configFile, mode='w')
        configWriter.write('[global]\n')
        configWriter.write('logfile = epa-http.txt\n')
        configWriter.write('resultsfile = results.html\n')
        configWriter.write('debugmode = false\n')
        configWriter.write('exitmode = true')
        configWriter.close()

        clear()

    config.read("config.ini")

    if config.has_section("global"):
        print(sCol.WARNING + "Config file loaded!" + sCol.ENDC)
    else:
        print(sCol.CRIT + "Config file is missing global section, setting now..." + sCol.ENDC)
        configFile = open("config.ini", mode='w')
        configFile.write('[global]')
        configFile.close()

        config.read("config.ini")

    if config.has_option("global", "LogFile"):
        logFile = config.get("global", "LogFile")
    else:
        print(sCol.CRIT + "Config file is missing LogFile parameter, setting now..." + sCol.ENDC)
        configFile = open("config.ini", mode='w')
        config.set('global','LogFile',"epa-http.txt")
        config.write(configFile)
        configFile.close()

        config.read("config.ini")
        logFile = config.get("global", "LogFile")

    if config.has_option("global", "ResultsFile"):
        resultsFile = config.get("global", "ResultsFile")
    else:
        print(sCol.CRIT + "Config file is missing ResultsFile parameter, setting now..." + sCol.ENDC)
        configFile = open("config.ini", mode='w')
        config.set('global','ResultsFile',"results.html")
        config.write(configFile)
        configFile.close()

        config.read("config.ini")
        resultsFile = config.get("global", "ResultsFile")

    if config.has_option("global", "DebugMode"):
        debugMode = config.getboolean("global", "DebugMode")
    else:
        print(sCol.CRIT + "Config file is missing DebugMode parameter, setting now..." + sCol.ENDC)
        configFile = open("config.ini", mode='w')
        config.set('global','DebugMode',"false")
        config.write(configFile)
        configFile.close()

        config.read("config.ini")
        debugMode = config.getboolean("global", "DebugMode")

    if config.has_option("global", "ExitMode"):
        exitMode = config.getboolean("global", "ExitMode")
    else:
        print(sCol.CRIT + "Config file is missing ExitMode parameter, setting now..." + sCol.ENDC)
        configFile = open("config.ini", mode='w')
        config.set('global','ExitMode',"true")
        config.write(configFile)
        configFile.close()

        config.read("config.ini")
        exitMode = config.getboolean("global", "ExitMode")

    if debugMode == True:
        print(sCol.WARNING + "Debug mode is enabled!" + sCol.ENDC)
        time.sleep(1)
        print("")
        print(sCol.WARNING + "Check log file availability..." + sCol.ENDC)

    checkFileStatus = os.path.isfile(logFile)

    if checkFileStatus == False:
        print(sCol.CRIT + "Log file not found! Please use settings to enter a correct log file!" + sCol.ENDC)
        if debugMode == True:
            print(sCol.WARNING + "Redirecting to settings menu..." + sCol.ENDC)
        time.sleep(2)
        restartRequired = True
        settings()

    if debugMode == True:
        print("")
        print(sCol.OK + "File is OK!" + sCol.ENDC)
        time.sleep(1)

    clear()

    print(sCol.OK + "Starting program..." + sCol.ENDC)
    time.sleep(1)

    print(sCol.WARNING + "Processing your log file..." + sCol.ENDC)

    logProc()

    clear()

# Main menu
# Here you make your choice what command you want to run
def mainMenu():

    clear()

    print(sCol.HEADER + "Log Parser by Maarten Mol" + sCol.ENDC)
    print("")
    print(sCol.OK + "1: Search for specific status code" + sCol.ENDC)
    print(sCol.OK + "2: Search for specific host name or ip" + sCol.ENDC)
    print(sCol.OK + "3: View statistics for all hosts" + sCol.ENDC)
    print(sCol.OK + "4: View all logs" + sCol.ENDC)
    print("")
    print(sCol.WARNING + "8: Settings" + sCol.ENDC)
    print("")
    print(sCol.CRIT + "9: Quit" + sCol.ENDC)
    print("")

    if debugMode == True:
        print(sCol.WARNING + "##########################################" + sCol.ENDC)
        print(sCol.CRIT + "Debug mode is enabled!" + sCol.ENDC)
        print(sCol.OK + "Log file loaded: " + logFile + sCol.ENDC)
        print(sCol.OK + "Results file: " + resultsFile + sCol.ENDC)
        print(sCol.WARNING + "##########################################" + sCol.ENDC)
        print("")

    mainMenuChoice = input(sCol.BLUE + "Please choose an option: " + sCol.ENDC)

    clear()

    if mainMenuChoice == str(1):
        print(sCol.WARNING + "Processing logs by status codes..." + sCol.ENDC)
        time.sleep(1)

        errorCodeProc()

        clear()

        codeChoice = input(sCol.BLUE + "Please enter the status code you want to view: " + sCol.ENDC)

        clear()

        if debugMode == True:
            print(sCol.WARNING + "Checking your status code: " + codeChoice + sCol.ENDC)
            print("")
            time.sleep(1)
            clear()

        if codeChoice not in replyCodes:
            print(sCol.CRIT + "This is not a correct status code" + sCol.ENDC)

            if debugMode == True:
                print(sCol.WARNING + "Redirecting to main menu..." + sCol.ENDC)

            time.sleep(1)
            clear()
            mainMenu()

        elif codeChoice in replyCodes:
            print(sCol.WARNING + "Generating results..." + sCol.ENDC)

            errorCodeCheck(codeChoice)
            time.sleep(1)
            clear()

            print(sCol.WARNING + "Opening results in default HTML viewer..." + sCol.ENDC)

            if debugMode == True:
                print("")
                print(sCol.WARNING + "Opening: " + resultsFile + sCol.ENDC)

            time.sleep(1)
            os.system("start "+resultsFile)

            if exitMode == True:
                if debugMode == True:
                    print("")
                    print(sCol.WARNING + "Exit mode is enabled, quiting... " + sCol.ENDC)
                    time.sleep(1)
                sys.exit()
            else:
                if debugMode == True:
                    print("")
                    print(sCol.WARNING + "Exit mode is disabled, opening main menu... " + sCol.ENDC)
                    time.sleep(1)
                mainMenu()

    elif mainMenuChoice == str(2):
        print(sCol.WARNING + "Processing logs by hosts..." + sCol.ENDC)
        time.sleep(1)

        errorHostProc()

        clear()

        hostChoice = input(sCol.BLUE + "Please enter the host you want to view: " + sCol.ENDC)

        clear()

        if debugMode == True:
            print(sCol.WARNING + "Checking your host: " + hostChoice + sCol.ENDC)
            print("")
            time.sleep(1)
            clear()

        if hostChoice not in replyHosts:
            print(sCol.CRIT + "This is not a correct host" + sCol.ENDC)

            if debugMode == True:
                print(sCol.WARNING + "Redirecting to main menu..." + sCol.ENDC)

            time.sleep(1)
            clear()
            mainMenu()

        elif hostChoice in replyHosts:
            print(sCol.WARNING + "Generating results..." + sCol.ENDC)

            errorHostCheck(hostChoice)
            time.sleep(1)
            clear()

            print(sCol.WARNING + "Opening results in default HTML viewer..." + sCol.ENDC)

            if debugMode == True:
                print("")
                print(sCol.WARNING + "Opening: " + resultsFile + sCol.ENDC)

            time.sleep(1)
            os.system("start "+resultsFile)

            if exitMode == True:
                if debugMode == True:
                    print("")
                    print(sCol.WARNING + "Exit mode is enabled, quiting... " + sCol.ENDC)
                    time.sleep(1)
                sys.exit()
            else:
                if debugMode == True:
                    print("")
                    print(sCol.WARNING + "Exit mode is disabled, opening main menu... " + sCol.ENDC)
                    time.sleep(1)
                mainMenu()

    elif mainMenuChoice == str(3):
        print(sCol.WARNING + "Processing statistics from log..." + sCol.ENDC)
        time.sleep(1)

        errorCountHost()

        clear()

        print(sCol.WARNING + "Generating results..." + sCol.ENDC)

        time.sleep(1)
        clear()

        print(sCol.WARNING + "Opening results in default HTML viewer..." + sCol.ENDC)

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Opening: " + resultsFile + sCol.ENDC)

        time.sleep(1)
        os.system("start "+resultsFile)

        if exitMode == True:
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Exit mode is enabled, quiting... " + sCol.ENDC)
                time.sleep(1)
            sys.exit()
        else:
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Exit mode is disabled, opening main menu... " + sCol.ENDC)
                time.sleep(1)
            mainMenu()

    elif mainMenuChoice == str(4):
        print(sCol.WARNING + "Processing all logs..." + sCol.ENDC)
        time.sleep(1)

        errorLogs()

        clear()

        print(sCol.WARNING + "Generating results..." + sCol.ENDC)

        time.sleep(1)
        clear()

        print(sCol.WARNING + "Opening results in default HTML viewer..." + sCol.ENDC)

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Opening: " + resultsFile + sCol.ENDC)

        time.sleep(1)
        os.system("start "+resultsFile)

        if exitMode == True:
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Exit mode is enabled, quiting... " + sCol.ENDC)
                time.sleep(1)
            sys.exit()
        else:
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Exit mode is disabled, opening main menu... " + sCol.ENDC)
                time.sleep(1)
            mainMenu()

    elif mainMenuChoice == str(8):
        if debugMode == True:
            print(sCol.WARNING + "Opening settings menu..." + sCol.ENDC)
            time.sleep(1)
        settings()

    elif mainMenuChoice == str(9):
        if debugMode == True:
            print(sCol.WARNING + "Quiting application..." + sCol.ENDC)
            print("")
            print(sCol.WARNING + "Bye...!" + sCol.ENDC)
            time.sleep(1)
        sys.exit()

    else:
        print("")
        print(sCol.WARNING + "Please choose a correct option!" + sCol.ENDC)
        if debugMode == True:
            print(sCol.WARNING + "Option does not exist!" + sCol.ENDC)
        time.sleep(1)
        clear()
        mainMenu()

# Settings menu
# Here you can set all settings in the config.ini
# If a settings requires a restart a flag will be set and when returning to main menu it will start the startUp function
def settings():

    global restartRequired

    clear()

    print(sCol.HEADER + "Log Parser by Maarten Mol" + sCol.ENDC)
    print("")
    print(sCol.OK + "1: Configure the log file path" + sCol.ENDC)
    print(sCol.OK + "2: Configure the results file path" + sCol.ENDC)
    print(sCol.OK + "3: Enable or disable debug mode" + sCol.ENDC)
    print(sCol.OK + "4: Enable or disable exit mode" + sCol.ENDC)
    print("")

    if restartRequired == False:
        print(sCol.WARNING + "9: Go back to main menu" + sCol.ENDC)
    if restartRequired == True:
        print(sCol.WARNING + "9: Restart and go back to main menu" + sCol.ENDC)

    print("")

    settingsMenuChoice = input(sCol.BLUE + "Please choose an option: " + sCol.ENDC)

    clear()

    if settingsMenuChoice == str(1):

        if debugMode == True:
            print(sCol.WARNING + "Opening config.ini" + sCol.ENDC)
            time.sleep(1)
            clear()

        configFile = open("config.ini", mode='w')

        logFileChoice = input(sCol.BLUE + "New path: " + sCol.ENDC)

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Writing to config.ini and flagging for required restart..." + sCol.ENDC)
            time.sleep(1)
            clear()

        config.set('global','LogFile',logFileChoice)
        config.write(configFile)
        configFile.close()

        restartRequired = True

    elif settingsMenuChoice == str(2):

        if debugMode == True:
            print(sCol.WARNING + "Opening config.ini" + sCol.ENDC)
            time.sleep(1)
            clear()

        configFile = open("config.ini", mode='w')

        resultsFileChoice = input(sCol.BLUE + "New path: " + sCol.ENDC)

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Writing to config.ini and flagging for required restart..." + sCol.ENDC)
            time.sleep(1)
            clear()

        config.set('global','ResultsFile',resultsFileChoice)
        config.write(configFile)
        configFile.close()

        restartRequired = True

    elif settingsMenuChoice == str(3):

        if debugMode == True:
            print(sCol.WARNING + "Opening config.ini" + sCol.ENDC)
            time.sleep(1)
            clear()

        configFile = open("config.ini", mode='w')

        print(sCol.OK + "1: Enable debug mode" + sCol.ENDC)
        print(sCol.OK + "2: Disable debug mode" + sCol.ENDC)
        print("")

        debugModeChoice = input(sCol.BLUE + "Choose an option: " + sCol.ENDC)

        if debugModeChoice == str(1):
            debugModeChoiceBol = "true"
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Chosen for debug mode enabled" + sCol.ENDC)
                time.sleep(1)

        elif debugModeChoice == str(2):
            debugModeChoiceBol = "false"
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Chosen for debug mode disabled" + sCol.ENDC)
                time.sleep(1)

        else:
            print("")
            print(sCol.WARNING + "Please choose a correct option!" + sCol.ENDC)
            if debugMode == True:
                print(sCol.WARNING + "Option does not exist!" + sCol.ENDC)
            time.sleep(1)
            clear()
            settings()

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Writing to config.ini and flagging for required restart..." + sCol.ENDC)
            time.sleep(1)
            clear()

        config.set('global','DebugMode',debugModeChoiceBol)
        config.write(configFile)
        configFile.close()

        restartRequired = True

    elif settingsMenuChoice == str(4):

        if debugMode == True:
            print(sCol.WARNING + "Opening config.ini" + sCol.ENDC)
            time.sleep(1)
            clear()

        configFile = open("config.ini", mode='w')

        print(sCol.OK + "1: Enable exit mode" + sCol.ENDC)
        print(sCol.OK + "2: Disable exit mode" + sCol.ENDC)
        print("")

        exitModeChoice = input(sCol.BLUE + "Choose an option: " + sCol.ENDC)

        if exitModeChoice == str(1):
            exitModeChoiceBol = "true"
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Chosen for exit mode enabled" + sCol.ENDC)
                time.sleep(1)

        elif exitModeChoice == str(2):
            exitModeChoiceBol = "false"
            if debugMode == True:
                print("")
                print(sCol.WARNING + "Chosen for exit mode disabled" + sCol.ENDC)
                time.sleep(1)

        else:
            print("")
            print(sCol.WARNING + "Please choose a correct option!" + sCol.ENDC)
            if debugMode == True:
                print(sCol.WARNING + "Option does not exist!" + sCol.ENDC)
            time.sleep(1)
            clear()
            settings()

        if debugMode == True:
            print("")
            print(sCol.WARNING + "Writing to config.ini and flagging for required restart..." + sCol.ENDC)
            time.sleep(1)
            clear()

        config.set('global','ExitMode',exitModeChoiceBol)
        config.write(configFile)
        configFile.close()

        restartRequired = True

    elif settingsMenuChoice == str(9):

        if restartRequired == False:
            mainMenu()
        if restartRequired == True:
            main()

    else:
        print("")
        print(sCol.WARNING + "Please choose a correct option!" + sCol.ENDC)
        if debugMode == True:
            print(sCol.WARNING + "Option does not exist!" + sCol.ENDC)
        time.sleep(1)
        clear()
        settings()

    settings()

# Main application
# This will run the main application at once
def main():
    startUp()
    mainMenu()

# Run application
if __name__ == '__main__':
    main()
