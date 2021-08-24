import sys

if __name__ == "__main__":

    def cli():

        n_args = len(sys.argv)

        #First Argument - Original File Path
        original_file_path = sys.argv[1]

        #Help
        if(original_file_path == "-h" or original_file_path == "--help"):
            print("""
Usage: python wavefront-for-selection.py <file>
       python wavefront-for-selection.py <file> <result_file>
       python wavefront-for-selection.py [options]

Allows you to transform wavefront files into a format that allows texture selection.

Options:
  <file>                 Path to file to be processed.
  <result_file>          Path to file to be returned.
  -h, --help             display help for command.""")

        #Second Argument - Result File Path
        result_file_path = "" if n_args < 3 else sys.argv[2]

        print(original_file_path)
        print(result_file_path)

    cli()