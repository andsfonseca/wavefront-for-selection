import json
import os
import sys
import re

BIT_8 = 2**8
BIT_16 = 2**16
BIT_32 = 2**32

MAX_DECIMAL_NUMBERS = 7

class WavefrontForSelection:
    """This class is responsible for transforming wavefront files into a format that allows texture selection.
    """
    @staticmethod
    def perform(original_path, result_path="", initial_index=1, save_dictionary_json=True, type="Uint8", mode="Texture", ensureNormalization = False):
        """Given a wavefront, recreates a file that allows texture selection.

        Parameters:
            original_path (String): Path to original file.
            result_path (String): Path to resulting file. If empty, the suffix '_picking' is used.
            initial_index (Integer): Initial Index for ID generation.
            save_dictionary_json (Boolean): Informs whether to save the identifiers in a json. (Can change the output)
            type (String): Type of Indexing that must be created. Accepted arguments: 'Uint8' and 'Float32'.
        Returns:
            (tuple[String, String]): Location of resulting file and json
            (tuple[String, Dict]): Location of resulting file and the identifiers dictionary 
        """

        #Warning
        if(type == "Float32" or type == "Binary16"):
            print("Warning: All floating point values cannot be stored exactly as they are in memory. \
So, if we want to store an Id, the 'floating' cannot store it as is. Instead, the binary can \
only store a closer approximation value.")

        #Create Safe Names
        result_folder_path, result_full_path, result_basename, result_mtl_full_path, result_mtl_filename = WavefrontForSelection.createSafeNames(original_path, result_path)

        # Create OBJFile
        obj_file = open(result_full_path, "w")

        #Dictionary of Ids
        idsDictionary = {}

        #Current Index
        index = initial_index

        #Write a texture file
        if(mode == "Texture"):

            # Create MTLFile
            mtl_file = open(result_mtl_full_path, "w")

            # Initialize OBJFile
            obj_file.write(f"mtllib {result_mtl_filename}\n")

            # Reading Wavefront
            with open(original_path) as f:

                #For each line
                for line in f:

                    split = str.split(line, " ", 1)

                    if(split[0] == "o"):

                        # Create New Color ID
                        colors = WavefrontForSelection.generateColorId(index, type)

                        # Associate to MTL
                        mtl_file.write(f"newmtl {index}\n")
                        mtl_file.write(f"Ka 1.0\n")
                        mtl_file.write(f"Kd {colors[0]:.7f} {colors[1]:.7f} {colors[2]:.7f}\n")

                        # Associate to OBJ
                        obj_file.write(f"usemtl {index}\n")
                        obj_file.write(line)

                        idsDictionary[index] = str.split(split[1], "\n")[0]

                        index += 1

                    elif(split[0] == "v" or split[0] == "vn" or split[0] == "f"):
                        obj_file.write(line)
                    elif(split[0] == "usemtl" or "mtllib"):
                        pass
                    else:
                        print(f"Unknown {split[0]}")

            mtl_file.close()
        
        #Write in w
        elif(mode == "Vertex"):

            # Reading Wavefront
            with open(original_path) as f:
                index -= 1
                #For each line
                for line in f:

                    split = str.split(line, " ", 1)

                    if(split[0] == "o"):
                        obj_file.write(line)
                        idsDictionary[index] = str.split(split[1], "\n")[0]
                        index += 1
                    elif(split[0] == "v" ):
                        values = re.findall(r"[-+]?\d*\.\d+|\d+", split[1])
                        if(len(values) == 4):
                            print("W value is used, exiting...")
                            return None, None

                        obj_file.write(f"v {values[0]} {values[1]} {values[2]} {index}.0\n")

                    elif(split[0] == "vn" or split[0] == "f"):
                        obj_file.write(line)
                    elif(split[0] == "usemtl" or "mtllib"):
                        pass
                    else:
                        print(f"Unknown {split[0]}")
        
        #Write in Texture Coordinates:
        elif (mode == "TextureCoordinates"):
            # Reading Wavefront
            with open(original_path) as f:
                index -= 1
                vertex_count = 0
                #For each line
                for line in f:

                    split = str.split(line, " ", 1)

                    if(split[0] == "o"):
                        for _ in range(vertex_count):
                            obj_file.write(f"vt {(index/BIT_32):.7f}\n")

                        obj_file.write(line)
                        idsDictionary[index] = str.split(split[1], "\n")[0]
                        index += 1
                    elif (split[0] == "v"):
                        vertex_count += 1
                        obj_file.write(line)
                    elif(split[0] == "vn" or split[0] == "f"):
                        for _ in range(vertex_count):
                            obj_file.write(f"vt {(index/BIT_32):.7f} 0.0\n")
                        vertex_count = 0
                        obj_file.write(line)
                    elif(split[0] == "usemtl" or "mtllib"):
                        pass
                    else:
                        print(f"Unknown {split[0]}")

        #Write in Normal:
        elif (mode == "Normal"):
            # Reading Wavefront
            with open(original_path) as f:
                index -= 1
                vertex_count = 0
                #For each line
                string = ""
                for line in f:

                    split = str.split(line, " ", 1)
                    
                    if(split[0] == "o"):
                        # Create New Color ID
                        colors = WavefrontForSelection.generateColorId(index+1, type)

                        if ensureNormalization:
                            if colors[0] > 0:
                                print("Index overflow. Reconsider using a larger type!")

                            colors[0] = 1 - (colors[1] + colors[2])

                        string = f"vn {colors[0]:.7f} {colors[1]:.7f} {colors[2]:.7f}\n"

                        idsDictionary[index] = str.split(split[1], "\n")[0]
                        index += 1

                    elif (split[0] == "v"):
                        obj_file.write(line)
                        obj_file.write(string)
                    elif(split[0] == "f"):
                        vertex_count = 0
                        obj_file.write(line)
                    elif(split[0] == "usemtl" or split[0] == "mtllib" or split[0] == "vn"):
                        pass
                    else:
                        print(f"Unknown {split[0]}")
        obj_file.close()
        # If True return the paths
        if save_dictionary_json:
            result_json_full_path = result_folder_path + "\\" + result_basename + ".json"
            dict_file = open(result_json_full_path, "w")
            json.dump(idsDictionary, dict_file, indent=6)
            dict_file.close()

            return result_full_path, result_json_full_path

        return result_full_path, idsDictionary

    @staticmethod
    def generateColorId(id, type="Uint8"):
        """Given a identifier, generates a specific color

        Parameters:
            id (number): identifier or any number
            type (String): Type of Indexing that must be created. Accepted arguments: 'Uint8' and 'Float32'.
        Returns:
            Array: The color of the identifier 
        """

        colors = [0.0, 0.0, 0.0]
        value = id
        division = 1
        index = 2

        bit = BIT_8

        if(type == "Binary16"):
            bit = BIT_16
        elif(type == "Float32"):
            bit = BIT_32

        while(division != 0):
            rest = value % bit
            division = value // bit
            colors[index] = rest / bit
            value = division

            index -= 1

            if(index == -1):
                print("Index overflow. Reconsider using a larger type!")
                break

        return colors

    def createSafeNames(original_path, result_path=""):
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

        return result_folder_path, result_full_path, result_basename, result_mtl_full_path, result_mtl_filename      

if __name__ == "__main__":

    def cli():

        n_args = len(sys.argv)

        showHelp = False

        original_file_path = ""
        result_file_path = ""
        initial_index = 1
        ignore_json = False
        type = "Uint8"
        mode = "Texture"

        # If Only One Argument
        if(n_args == 1):
            raise ValueError("No path")

        if(n_args == 2):

            # First Argument - Original File Path
            original_file_path = sys.argv[1]

            showHelp = original_file_path == "-h" or original_file_path == "--help"

        if(n_args > 2):
            args_index = 1

            while(args_index < n_args):
                if(sys.argv[args_index] == "-i" or sys.argv[args_index] == "--input"):
                    if(args_index + 1 >= n_args):
                        raise ValueError("no value")

                    original_file_path = sys.argv[args_index+1]

                    args_index += 2

                elif(sys.argv[args_index] == "-o" or sys.argv[args_index] == "--output"):
                    if(args_index + 1 >= n_args):
                        raise ValueError("no value")

                    result_file_path = sys.argv[args_index+1]

                    args_index += 2

                elif(sys.argv[args_index] == "-ii" or sys.argv[args_index] == "--initial_index"):
                    
                    if(args_index + 1 >= n_args):
                        raise ValueError("no value")
                    
                    initial_index = int(sys.argv[args_index+1])

                    args_index += 2

                elif(sys.argv[args_index] == "-ij" or sys.argv[args_index] == "--ignore-json"):
                    ignore_json = True
                    args_index += 1
                
                elif(sys.argv[args_index] == "-m" or sys.argv[args_index] == "--mode"):

                    if(args_index + 1 >= n_args):
                        raise ValueError("no value")
                    
                    mode = sys.argv[args_index+1]

                    args_index += 2
                elif(sys.argv[args_index] == "-t" or sys.argv[args_index] == "--type"):

                    if(args_index + 1 >= n_args):
                        raise ValueError("no value")
                    
                    type = sys.argv[args_index+1]

                    args_index += 2
                else:
                    args_index +=1

        # Help
        if(showHelp):
            print("""
Usage: python wavefront-for-selection.py <file> 
       python wavefront-for-selection.py [options]

Allows you to transform wavefront files into a format that allows texture selection.

Options:
  <file>                            Path to original file.
  [-i, --input] <file>              Path to original file.
  [-o, --output] <file>             Path to resulting file. (default: '')
  [-ii, --initial_index] <index>    Initial Index for ID generation (default: 1)
  -ij, --ignore-json                Skip creating a JSON with the Ids and their original names
  [-m, --mode] <mode>               ID generation strategy, informs whether the identifier should be
                                    placed on the texture or on the vertex. Accepted arguments:
                                    'Texture' and 'Vertex'. (default: 'Texture') 
  [-t, --type] <type>               Texture mode only. Type of Indexing that must be created. Accepted
                                    arguments: 'Uint8' and 'Float32'. (default: 'Uint8') 
  -h, --help                        display help for command.""")

        else:
            
            WavefrontForSelection.perform(original_file_path, result_file_path,initial_index, not ignore_json, type, mode)

    cli()
