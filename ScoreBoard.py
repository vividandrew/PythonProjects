#!PYTHON3
# Ver:0.02
# The script gets slow when it comes to typing the team names potentially due to the constant listening to key events
# otherwise script is functional

import pyHook, pythoncom

# initialize the variables
T1S = 0
T2S = 0
team1 = ""
team2 = ""
print("""
Press F11 to start program
""")


# The function to save the file as a html file with the names and scores given to it.
def update(team1, T1S, team2, T2S):
    ScoreBoard = open("ScoreBoard.html", "w")

    # Sets the text for the final format, don't edit, may break it! ^^ code must be executed above
    TvT = """

        <head><meta http-equiv="refresh" content="1"></head>
        <body>
        <p>
        <table  width=50%% align="center">
                <tr>
                        <td id="T1N"><h1 align="center">%s</h1></td>
                        <td id="T2N"><h1 align="center">%s</h1></td>
                </tr>
                <tr>
                        <td id="T1S"><h3 align="center">%s</h3>
                        <td id="T2S"><h3 align="center">%s</h3>
                </tr> 
        </table>
        </p>
		<style>
		body{ 
			color:white
			}

		h1 {
			font-style:ariel;
			font-size:40px;
			-webkit-text-stroke-width: 0.5px;
			-webkit-text-stroke-color: black;
			} 

		h3 {
			font-style:ariel;
			font-size:40px;
			-webkit-text-stroke-width: 0.5px;
			-webkit-text-stroke-color: black;
			}
		</style>
        </body>

        """ % (team1, team2, T1S, T2S)

    # ! testing print(TvT)

    ScoreBoard.write(str(TvT))
    ScoreBoard.close()


# Event executed every time the keyboard is pressed.  
    
def OnKeyboardEvent(event):
    
    # calls the global variable to be used locally and stored globally.
    global T1S
    global T2S
    global team1
    global team2
    
    keypressed = event.Key
    #print keypressed
    if keypressed == "F9":
        T1S += 1
        update(team1, T1S, team2, T2S)
    if keypressed == "F10":
        T2S += 1
        update(team1, T1S, team2, T2S)
    if keypressed == "F11":
        print("Enter Team/Player 1")
        team1 = input()
        print("Enter Team/Player 2")
        team2 = input()
        T1S = 0
        T2S = 0
        print("""
Controls;
1. press F9 to increase %s points
2. press F10 to increase %s points
3. press F11 to reset
			""" % (team1, team2))
        update(team1, T1S, team2, T2S) 
    
    # return True to pass the event to other handlers within pyhook
    return True


# create a hook manager
hm = pyHook.HookManager()
# watch for all key down events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# Wait forever
pythoncom.PumpMessages()
    
