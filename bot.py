import numpy as np
import pandas as pd
import joblib
from command import Command
from buttons import Buttons

class Bot:
    def __init__(self):
        # Load MLP model with confirmation
        try:
            self.model = joblib.load('mlp_fight_model15.pkl')
            print("Successfully loaded mlp_fight_model.pkl")
        except FileNotFoundError:
            print("Error: mlp_fight_model.pkl not found in the current directory")
            raise
        except Exception as e:
            print(f"Error loading mlp_fight_model.pkl: {str(e)}")
            raise

        self.features = ['p1_id', 'p1_health', 'p1_x', 'p1_y', 'p1_jumping', 'p1_crouching',
                         'p2_id', 'p2_health', 'p2_x', 'p2_y', 'p2_jumping', 'p2_crouching', 'timer']
        self.actions = ['up', 'down', 'left', 'right', 'A', 'B', 'X', 'Y', 'start', 'select', 'L', 'R']
        self.my_command = Command()
        self.buttons = Buttons()

    def fight(self, current_game_state, player):
        # Reset buttons
        self.buttons.init_buttons()

        # Check round status
        print(f"Player {player}: Round status - has_round_started: {current_game_state.has_round_started}, is_round_over: {current_game_state.is_round_over}")

        # MLP logic
        print(f"Player {player}: Using MLP model to predict actions")
        # Extract features from the game state
        feature_values = [
            current_game_state.player1.player_id,
            current_game_state.player1.health,
            current_game_state.player1.x_coord,
            current_game_state.player1.y_coord,
            int(current_game_state.player1.is_jumping),
            int(current_game_state.player1.is_crouching),
            current_game_state.player2.player_id,
            current_game_state.player2.health,
            current_game_state.player2.x_coord,
            current_game_state.player2.y_coord,
            int(current_game_state.player2.is_jumping),
            int(current_game_state.player2.is_crouching),
            current_game_state.timer
        ]
        print(f"Player {player}: Input features: {dict(zip(self.features, feature_values))}")  # Debug input features

        # Convert features to a pandas DataFrame with feature names
        X = pd.DataFrame([feature_values], columns=self.features)

        # Predict actions using the MLP model
        predictions = self.model.predict(X)[0]
        print(f"Player {player}: MLP Predictions: {dict(zip(self.actions, predictions))}")

        # Set the predicted actions in the buttons object
        for action, pred in zip(self.actions, predictions):
            setattr(self.buttons, action, bool(pred))

        # Log button states
        button_states = {action: getattr(self.buttons, action) for action in self.actions}
        print(f"Player {player}: Button states: {button_states}")

        # Assign buttons to command
        if player == "1":
            self.my_command.player_buttons = self.buttons
        else:
            self.my_command.player2_buttons = self.buttons

        # Debug the raw command being sent to Bizhawk
        if player == "1":
            raw_command = self.my_command.player_buttons.__dict__
        else:
            raw_command = self.my_command.player2_buttons.__dict__
        print(f"Player {player}: Raw command sent to Bizhawk: {raw_command}")

        # CSV logging (commented out)
        """
        csv_file = 'dataset.csv'
        headers = [
            'player', 'p1_id', 'p1_health', 'p1_x', 'p1_y', 'p1_jumping', 'p1_crouching', 'p1_move_id',
            'p2_id', 'p2_health', 'p2_x', 'p2_y', 'p2_jumping', 'p2_crouching', 'p2_move_id',
            'timer', 'has_round_started', 'is_round_over',
            'up', 'down', 'left', 'right', 'A', 'B', 'X', 'Y', 'start', 'select', 'L', 'R'
        ]
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

        # Prepare the data row
        if player == "1":
            buttons = self.my_command.player_buttons
        else:
            buttons = self.my_command.player2_buttons

        row = [
            player,
            current_game_state.player1.player_id,
            current_game_state.player1.health,
            current_game_state.player1.x_coord,
            current_game_state.player1.y_coord,
            int(current_game_state.player1.is_jumping),
            int(current_game_state.player1.is_crouching),
            current_game_state.player1.move_id,
            current_game_state.player2.player_id,
            current_game_state.player2.health,
            current_game_state.player2.x_coord,
            current_game_state.player2.y_coord,
            int(current_game_state.player2.is_jumping),
            int(current_game_state.player2.is_crouching),
            current_game_state.player2.move_id,
            current_game_state.timer,
            int(current_game_state.has_round_started),
            int(current_game_state.is_round_over),
            int(buttons.up),
            int(buttons.down),
            int(buttons.left),
            int(buttons.right),
            int(buttons.A),
            int(buttons.B),
            int(buttons.X),
            int(buttons.Y),
            int(buttons.start),
            int(buttons.select),
            int(buttons.L),
            int(buttons.R)
        ]

        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        """

        # Previous minimal logic (commented out)
        """
        # Minimal logic to test movement
        print(f"Player {player}: Applying minimal logic")
        
        # Reset buttons
        self.buttons.init_buttons()

        # Force right movement to test BizHawk
        self.buttons.right = True
        print(f"Player {player}: Forcing right movement")

        # Log button states
        button_states = {action: getattr(self.buttons, action) for action in self.actions}
        print(f"Player {player}: Button states: {button_states}")

        # Assign buttons to command
        if player == "1":
            self.my_command.player_buttons = self.buttons
        else:
            self.my_command.player2_buttons = self.buttons
        """

        # Previous rule-based logic (commented out)
        """
        # Rule-based logic
        print(f"Player {player}: Applying rule-based logic")
        
        # Reset buttons
        self.buttons.init_buttons()

        # Calculate x-coordinate difference
        try:
            if player == "1":
                diff = current_game_state.player2.x_coord - current_game_state.player1.x_coord
            else:
                diff = current_game_state.player1.x_coord - current_game_state.player2.x_coord

            # Move toward opponent
            if diff > 20:  # Opponent is to the right
                self.buttons.right = True
                print(f"Player {player}: Moving right (diff: {diff})")
            elif diff < -20:  # Opponent is to the left
                self.buttons.left = True
                print(f"Player {player}: Moving left (diff: {diff})")

            # Occasionally jump or attack
            import random
            action_choice = random.randint(0, 10)
            if action_choice == 0:
                self.buttons.up = True
                print(f"Player {player}: Jumping")
            elif action_choice == 1:
                self.buttons.A = True
                print(f"Player {player}: Attacking with A")
            elif action_choice == 2:
                self.buttons.Y = True
                print(f"Player {player}: Attacking with Y")
        except AttributeError as e:
            print(f"Error accessing game state attributes: {e}")
            # Fallback to basic movement
            self.buttons.right = True
            print(f"Player {player}: Fallback - Forcing right movement")

        # Ensure at least one action is set
        if not any(getattr(self.buttons, action) for action in self.actions):
            self.buttons.right = True
            print(f"Player {player}: No actions set, forcing right movement")

        # Log button states
        button_states = {action: getattr(self.buttons, action) for action in self.actions}
        print(f"Player {player}: Button states: {button_states}")

        # Assign buttons to command
        if player == "1":
            self.my_command.player_buttons = self.buttons
        else:
            self.my_command.player2_buttons = self.buttons
        """

        # Previous rule-based logic with run_command (commented out)
        """
        # Previous rule-based logic
        if player=="1":
            #print("1")
            #v - < + v - < + B spinning
            if( self.exe_code!=0  ):
               self.run_command([],current_game_state.player1)
            diff=current_game_state.player2.x_coord - current_game_state.player1.x_coord
            if (  diff > 60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command([">+^ +Y",">+^ +Y",">+^ +Y","!>+!^ +!Y"],current_game_state.player1)
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
                elif ( toss==1 ):
                    self.run_command([">+^ +B",">+^ +B","!>+!^ +!B"],current_game_state.player1)
                else: #fire
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
            elif (  diff < -60 ) :
                toss=np.random.randint(3)
                if (toss==0):#spinning
                    #self.run_command(["<+^ +Y","<+^ +Y","<+^ +Y","!<+!^ +!Y"],current_game_state.player1)
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
                elif ( toss==1):#
                    self.run_command(["<+^ +B","<+^ +B","!<+!^ +!B"],current_game_state.player1)
                else: #fire
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
            else:
                toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
                if ( toss>=1 ):
                    if (diff>0):
                        self.run_command(["<","<","!<"],current_game_state.player1)
                    else:
                        self.run_command([">",">","!>"],current_game_state.player1)
                else:
                    self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player1)
            self.my_command.player_buttons=self.buttn
        elif player=="2":
            if( self.exe_code!=0  ):
               self.run_command([],current_game_state.player2)
            diff=current_game_state.player1.x_coord - current_game_state.player2.x_coord
            if (  diff > 60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command([">+^ +Y",">+^ +Y","!>+!^ +!Y"],current_game_state.player2)
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
                elif ( toss==1 ):
                    self.run_command([">+^ +B",">+^ +B","!>+!^ +!B"],current_game_state.player2)
                else:
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
            elif ( diff < -60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command(["<+^ +Y","<+^ +Y","!>+!^ +!Y"],current_game_state.player2)
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
                elif ( toss==1):
                    self.run_command(["<+^ +B","<+^ +B","!<+!^ +!B"],current_game_state.player2)
                else:
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
            else:
                toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
                if ( toss>=1 ):
                    if (diff<0):
                        self.run_command(["<","<","!<"],current_game_state.player2)
                    else:
                        self.run_command([">",">","!>"],current_game_state.player2)
                else:
                    self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player2)
            self.my_command.player2_buttons=self.buttn
        """

        # Previous run_command method (commented out)
        """
        def run_command(self, com, player):
            if self.exe_code-1==len(self.fire_code):
                self.exe_code=0
                self.start_fire=False
                print ("compelete")
                #exit()
                # print ( "left:",player.player_buttons.left )
                # print ( "right:",player.player_buttons.right )
                # print ( "up:",player.player_buttons.up )
                # print ( "down:",player.player_buttons.down )
                # print ( "Y:",player.player_buttons.Y )
            elif len(self.remaining_code)==0 :
                self.fire_code=com
                #self.my_command=Command()
                self.exe_code+=1
                self.remaining_code=self.fire_code[0:]
            else:
                self.exe_code+=1
                if self.remaining_code[0]=="v+<":
                    self.buttn.down=True
                    self.buttn.left=True
                    print("v+<")
                elif self.remaining_code[0]=="!v+!<":
                    self.buttn.down=False
                    self.buttn.left=False
                    print("!v+!<")
                elif self.remaining_code[0]=="v+>":
                    self.buttn.down=True
                    self.buttn.right=True
                    print("v+>")
                elif self.remaining_code[0]=="!v+!>":
                    self.buttn.down=False
                    self.buttn.right=False
                    print("!v+!>")
                elif self.remaining_code[0]==">+Y":
                    self.buttn.Y= True #not (player.player_buttons.Y)
                    self.buttn.right=True
                    print(">+Y")
                elif self.remaining_code[0]=="!>+!Y":
                    self.buttn.Y= False #not (player.player_buttons.Y)
                    self.buttn.right=False
                    print("!>+!Y")
                elif self.remaining_code[0]=="<+Y":
                    self.buttn.Y= True #not (player.player_buttons.Y)
                    self.buttn.left=True
                    print("<+Y")
                elif self.remaining_code[0]="!<+!Y":
                    self.buttn.Y= False #not (player.player_buttons.Y)
                    self.buttn.left=False
                    print("!<+!Y")
                elif self.remaining_code[0]==">+^ +L":
                    self.buttn.right=True
                    self.buttn.up=True
                    self.buttn.L= not (player.player_buttons.L)
                    print(">+^ +L")
                elif self.remaining_code[0]=="!>+!^ +!L":
                    self.buttn.right=False
                    self.buttn.up=False
                    self.buttn.L= False #not (player.player_buttons.L)
                    print("!>+!^ +!L")
                elif self.remaining_code[0]==">+^ +Y":
                    self.buttn.right=True
                    self.buttn.up=True
                    self.buttn.Y= not (player.player_buttons.Y)
                    print(">+^ +Y")
                elif self.remaining_code[0]=="!>+!^ +!Y":
                    self.buttn.right=False
                    self.buttn.up=False
                    self.buttn.Y= False #not (player.player_buttons.L)
                    print("!>+!^ +!Y")
                elif self.remaining_code[0]==">+^ +R":
                    self.buttn.right=True
                    self.buttn.up=True
                    self.buttn.R= not (player.player_buttons.R)
                    print(">+^ +R")
                elif self.remaining_code[0]=="!>+!^ +!R":
                    self.buttn.right=False
                    self.buttn.up=False
                    self.buttn.R= False #ot (player.player_buttons.R)
                    print("!>+!^ +!R")
                elif self.remaining_code[0]==">+^ +A":
                    self.buttn.right=True
                    self.buttn.up=True
                    self.buttn.A= not (player.player_buttons.A)
                    print(">+^ +A")
                elif self.remaining_code[0]=="!>+!^ +!A":
                    self.buttn.right=False
                    self.buttn.up=False
                    self.buttn.A= False #not (player.player_buttons.A)
                    print("!>+!^ +!A")
                elif self.remaining_code[0]==">+^ +B":
                    self.buttn.right=True
                    self.buttn.up=True
                    self.buttn.B= not (player.player_buttons.B)
                    print(">+^ +B")
                elif self.remaining_code[0]=="!>+!^ +!B":
                    self.buttn.right=False
                    self.buttn.up=False
                    self.buttn.B= False #not (player.player_buttons.A)
                    print("!>+!^ +!B")
                elif self.remaining_code[0]=="<+^ +L":
                    self.buttn.left=True
                    self.buttn.up=True
                    self.buttn.L= not (player.player_buttons.L)
                    print("<+^ +L")
                elif self.remaining_code[0]="!<+!^ +!L":
                    self.buttn.left=False
                    self.buttn.up=False
                    self.buttn.L= False  #not (player.player_buttons.Y)
                    print("!<+!^ +!L")
                elif self.remaining_code[0]=="<+^ +Y":
                    self.buttn.left=True
                    self.buttn.up=True
                    self.buttn.Y= not (player.player_buttons.Y)
                    print("<+^ +Y")
                elif self.remaining_code[0]="!<+!^ +!Y":
                    self.buttn.left=False
                    self.buttn.up=False
                    self.buttn.Y= False  #not (player.player_buttons.Y)
                    print("!<+!^ +!Y")
                elif self.remaining_code[0]=="<+^ +R":
                    self.buttn.left=True
                    self.buttn.up=True
                    self.buttn.R= not (player.player_buttons.R)
                    print("<+^ +R")
                elif self.remaining_code[0]="!<+!^ +!R":
                    self.buttn.left=False
                    self.buttn.up=False
                    self.buttn.R= False  #not (player.player_buttons.Y)
                    print("!<+!^ +!R")
                elif self.remaining_code[0]=="<+^ +A":
                    self.buttn.left=True
                    self.buttn.up=True
                    self.buttn.A= not (player.player_buttons.A)
                    print("<+^ +A")
                elif self.remaining_code[0]="!<+!^ +!A":
                    self.buttn.left=False
                    self.buttn.up=False
                    self.buttn.A= False  #not (player.player_buttons.Y)
                    print("!<+!^ +!A")
                elif self.remaining_code[0]=="<+^ +B":
                    self.buttn.left=True
                    self.buttn.up=True
                    self.buttn.B= not (player.player_buttons.B)
                    print("<+^ +B")
                elif self.remaining_code[0]="!<+!^ +!B":
                    self.buttn.left=False
                    self.buttn.up=False
                    self.buttn.B= False  #not (player.player_buttons.Y)
                    print("!<+!^ +!B")
                elif self.remaining_code[0]=="v+R":
                    self.buttn.down=True
                    self.buttn.R= not (player.player_buttons.R)
                    print("v+R")
                elif self.remaining_code[0]=="!v+!R":
                    self.buttn.down=False
                    self.buttn.R= False  #not (player.player_buttons.Y)
                    print("!v+!R")
                else:
                    if self.remaining_code[0] =="v":
                        self.buttn.down=True
                        print ( "down" )
                    elif self.remaining_code[0] =="!v":
                        self.buttn.down=False
                        print ( "Not down" )
                    elif self.remaining_code[0] =="<":
                        print ( "left" )
                        self.buttn.left=True
                    elif self.remaining_code[0] =="!<":
                        print ( "Not left" )
                        self.buttn.left=False
                    elif self.remaining_code[0] ==">":
                        print ( "right" )
                        self.buttn.right=True
                    elif self.remaining_code[0] =="!>":
                        print ( "Not right" )
                        self.buttn.right=False
                    elif self.remaining_code[0] =="^":
                        print ( "up" )
                        self.buttn.up=True
                    elif self.remaining_code[0] =="!^":
                        print ( "Not up" )
                        self.buttn.up=False
                self.remaining_code=self.remaining_code[1:]
            return
        """

        return self.my_command