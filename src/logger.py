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

def log_balance_sol(num_moves, duration):
  events.append(f"{timestamp()} Balance solution found, it will require {num_moves} moves/{duration:.2f} seconds.")

# "Finished a Cycle. Manifest HMMAlgecirasOUTBOUND.txt was written to desktop, and a
# reminder pop-up to operator to send file was displayed"
def log_finish_operation():
  new_output = os.path.splitext(manifest_io.MANIFEST_FILENAME)[0]
  events.append(f"{timestamp()} Finished a Cycle. Manifest {new_output}OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed.")

# at the very end of the program / day
def log_kill():
  log_message("Program was shut down.")

def write_logger_to_desktop(): # add a parameter of name_of_port because not all ports will be by MrKeogh
  new_output = os.path.splitext(manifest_io.MANIFEST_FILENAME)[0]

  filename = new_output + "OUTBOUND" + start_time.strftime("%m_%d_%Y_%H%M") + ".txt"
  #desktop_location = os.path.join(os.path.expanduser("~"), "Desktop", filename)
  output_path = os.path.join(os.getcwd(), "output", filename)
  os.makedirs(os.path.join(os.getcwd(), "output"), exist_ok = True)

  
  with open(output_path, "w") as f:
    f.write("\n".join(events))