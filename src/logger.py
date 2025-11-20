import datetime

events = []
start_time = None

def initialize_logger():
  global start_time
  start_time = datetime.datetime.now
  log_message("Program was started.")

def timestamp():
  current_time = datetime.now()
  return current_time.strftime("%m %d %Y: %H:%M")

def log_message(message):
  events.append(f"{timestamp()} {message}")

def log_manifest_opened(input_file, num_containers):
  events.append(f"{timestamp()} Manifest {input_file} is opened, there are {num_containers} on the ship.")

def log_balance_sol(num_moves, duration):
  events.append(f"{timestamp()} Balance solution found, it will require {num_moves}/{duration} minutes.")

def log_move_operation(prev, updated): # need to format input coordinate
  events.append(f"{timestamp()} {prev} was moved to {updated}")

def log_finish_operation(input_file):
  events.append(f"{timestamp()} Finished a Cycle. Manifest {input_file} was written to desktop, and a reminder pop-up to operator to send file was displayed.")

def log_kill():
  log_message("Program was shut down.")
  