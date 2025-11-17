import debug
import manifest_io

def main():
      # example receive
      grid, description = manifest_io.load_manifest_from_user()
      debug.debug_print_formatted_loaded_manifest(grid, description)

      debug.debug_print_raw_loaded_manifest(grid, description)



if __name__ == "__main__":
      main()