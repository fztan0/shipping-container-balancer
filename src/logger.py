import datetime
import manifest_io
import os

events = []
start_time = None

# run this at the start of the day
def initialize_logger():
  global start_time
  start_time = datetime.datetime.now()
  log_message("Program was started.")

def timestamp():
  current_time = datetime.datetime.now()
  return current_time.strftime("%m %d %Y: %H:%M:%S")

def log_message(message):
  events.append(f"{timestamp()} {message}")

# "Manifest (input_file_name) is opened, there are (num_containers) containers on the ship"
def log_manifest_opened(num_containers):
  events.append(f"{timestamp()} Manifest {manifest_io.MANIFEST_FILENAME} is opened, there are {num_containers} on the ship.")

# "Balance solution found, it will require 9 moves/34 minutes."
def log_balance_sol(num_moves, duration):
  events.append(f"{timestamp()} Balance solution found, it will require {num_moves}/{duration} minutes.")

# e.g (01, 04) to (03, 03) // (01, 03) to (03, 04) // (04, 01) to (10, 02)

def log_move_operation(list_moves):
  for i in range(0, len(list_moves), 2):
    prev = list_moves[i]
    updated = list_moves[i+1]

    input_user = input("Select ENTER once move is done or 'M' to log a message")

    if input_user.strip() == "":
      log_message(f"[{prev}] was moved to [{updated}]")

    if input_user == 'm':
      note = input("Enter note:")
      log_message(note)
      log_message(f"[{prev}] was moved to [{updated}]")

    
  

# "Finished a Cycle. Manifest HMMAlgecirasOUTBOUND.txt was written to desktop, and a
# reminder pop-up to operator to send file was displayed"
def log_finish_operation():
  events.append(f"{timestamp()} Finished a Cycle. Manifest {manifest_io.MANIFEST_FILENAME} was written to desktop, and a reminder pop-up to operator to send file was displayed.")

# at the very end of the program / day
def log_kill():
  log_message("Program was shut down.")

def write_logger_to_desktop(): # add a parameter of name_of_port because not all ports will be by MrKeogh
  filename = "KeoghsPort" + start_time.strftime("%m_%d_%Y_%H%M") + ".txt"
  desktop_location = os.path.join(os.path.expanduser("~"), "Desktop", filename)
  
  with open(desktop_location, "w") as f:
    f.write("\n".join(events))