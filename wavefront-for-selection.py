from io import StringIO
import os
import sys

class WavefrontForSelection:
    
    @staticmethod
    def perform(original_path, result_path = ""):

        #Definitions
        original_folder_path = os.path.dirname(original_path)
        original_filename = os.path.basename(original_path)
        original_basename = os.path.splitext(original_filename)[0]

        if not result_path:
            result_folder_path = original_folder_path
            result_basename = original_basename + "_picking"
            result_filename = result_basename + ".obj"
            result_mtl_filename = result_basename + ".mtl"
        else:
            result_folder_path = os.path.dirname(result_path)
            result_filename = os.path.basename(result_path)
            result_basename = os.path.splitext(result_filename)[0]
            result_mtl_filename = result_basename + ".mtl"
        
        result_full_path = result_folder_path + "\\" + result_filename
        result_mtl_full_path = result_folder_path + "\\" + result_mtl_filename 

        #Create MTLFile
        mtl_file = open(result_mtl_full_path,"w")

        #Create OBJFile 
        obj_file = open(result_full_path,"w")

        #Initialize OBJFile
        obj_file.write(f"mtllib {result_mtl_filename}\n")

        #Reading Wavefront
        with open(original_path) as f:
            for line in f:

               split = str.split(line, " ", 1)[0]

               if(split[0] == "o"):
                   
                   #Create New Color ID

                   #Associate to MTL

                   #Associate to OBJ
                   pass        

        mtl_file.close()
        obj_file.close()

        pass
    
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

        WavefrontForSelection.perform(original_file_path, result_file_path)

    cli()