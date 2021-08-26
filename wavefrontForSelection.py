import json
import os
import sys

class WavefrontForSelection:

    @staticmethod
    def perform(original_path, result_path="", initial_index = 1, save_dictionary_json = True):

        # Definitions
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

        # Fix: Same Folder
        result_folder_path = "." if not result_folder_path else result_folder_path

        result_full_path = result_folder_path + "\\" + result_filename
        result_mtl_full_path = result_folder_path + "\\" + result_mtl_filename
        # Create MTLFile
        mtl_file = open(result_mtl_full_path, "w")
        # Create OBJFile
        obj_file = open(result_full_path, "w")
        # Initialize OBJFile
        obj_file.write(f"mtllib {result_mtl_filename}\n")

        idsDictionary  = {}
        
        index = initial_index

        # Reading Wavefront
        with open(original_path) as f:
            for line in f:

                split = str.split(line, " ", 1)

                if(split[0] == "o"):
                    
                    # Create New Color ID
                    colors = WavefrontForSelection.generateHexadecimalId(index)

                    # Associate to MTL
                    mtl_file.write(f"newmtl {index}\n")
                    mtl_file.write(f"Ka 1.0\n")
                    mtl_file.write(f"Kd {colors[0]} {colors[1]} {colors[2]}\n")
                    
                    # Associate to OBJ
                    obj_file.write(f"usemtl {index}\n")
                    obj_file.write(line)
                    
                    idsDictionary [index] = str.split(split[1], "\n")[0]
                    
                    index += 1
                
                elif(split[0] == "v" or split[0] == "vn" or split[0] == "f"):
                    obj_file.write(line)
                elif(split[0] == "usemtl" or "mtllib"):
                    pass
                else:
                    print(f"Unknown {split[0]}")

        mtl_file.close()
        obj_file.close()
        
        # If True return the paths
        if save_dictionary_json:
            result_json_full_path = result_folder_path + "\\" + result_basename + ".json"
            dict_file = open(result_json_full_path, "w") 
            json.dump(idsDictionary, dict_file, indent = 6) 
            dict_file.close()
            
            return result_full_path, result_json_full_path

        return result_full_path, idsDictionary

    @staticmethod
    def generateHexadecimalId(id):
        colors = [0.0, 0.0, 0.0]

        value = id
        division = 1
        index = 2

        while(division != 0):
            rest = value % 256
            division = value // 256
            colors[index] = rest / 256
            value = division

            index -= 1

            if(index == -1):
                print("Overflow")
                break;
        
        return colors


if __name__ == "__main__":

    def cli():

        n_args = len(sys.argv)

        # First Argument - Original File Path
        original_file_path = sys.argv[1]

        # Help
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

        # Second Argument - Result File Path
        result_file_path = "" if n_args < 3 else sys.argv[2]

        WavefrontForSelection.perform(original_file_path, result_file_path)

    cli()
