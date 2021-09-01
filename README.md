# Wavefront-for-selection

Allows you to transform wavefront files into a format that allows texture selection. 

## What is?

This code allows you to read a wavefront (.obj). For each mesh of stitches in different groups (separated by name or color), the group will receive a numerical identifier. The original mesh color will be reconstructed to match this new identifier.

## Usage

### Command-line interface - CLI

Open the terminal and type: 

```shell
python wavefrontForSelection.py <file>
```

For more advanced options see the commands with details below :

```shell
python wavefrontForSelection.py -i <file> -o <output_file> -ii <number> [-ij] -t <type>
```

|        Flag               |                                    Description                                    |     Required       |
|:-------------------------:|:---------------------------------------------------------------------------------:|:-------------------:|
| `-i`, `--input`           | Path to original file.                                                            | ✅ Yes              |
| `-o`, `--output`          | Path to resulting file.                                                           | No, default `''`    |
| `-ii`, `--initial_index/` | Initial Index for ID generation.                                                  | No, default `1`     |
| `-ij`, `--ignore-json`    | Skip creating a JSON with the Ids and their original names.                       | No                  |
| `-t`, `--type`            | Type of Indexing that must be created. Accepted arguments: 'Uint8' and 'Float32'. | No, default `Uint8` |
| `-h`, `--help`            | Display help for command.                                                         | No                  |

### Python Import

You can import the library as a Python class: 

```python
from wavefrontForSelection import WavefrontForSelection
```

> Remember to remove hyphens from the folder if necessary. 

The method "perform" offers the same functionality displayed in the CLI:

```python
WavefrontForSelection.perform(file, result_path="",initial_index=1,save_dictionary_json=True, type="Uint8")
```

The method will return two outputs: A path to the OBJ file and another to the JSON with the identifiers 

```python
result_file, result_json = WavefrontForSelection.perform(file)
```

If the method receives "save_dictionary_json" as false, the method will return two different outputs: A path to the OBJ file and a dictionary of identifiers and names

```python
result_file, dictionary_ids = WavefrontForSelection.perform(file)
```

## Issues

Feel free to submit issues and enhancement requests.

## Contribution

1. Fork the project
2. Create a _branch_ for your modification (`git checkout -b my-new-resource`)
3. Do the _commit_ (`git commit -am 'Adding a new resource...'`)
4. _Push_ (`git push origin my-new-resource`)
5. Create a new _Pull Request_ 
