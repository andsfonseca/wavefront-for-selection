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