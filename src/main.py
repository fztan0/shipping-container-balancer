import debug
import manifest_io


def main():
      grid, desc = manifest_io.load_manifest_from_user()

      debug.debug_print_loaded_manifest(grid, desc)



if __name__ == "__main__":
      main()