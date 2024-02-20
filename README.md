# Designite util

The `postprocessor` script reads the output generated by DesigniteJava tool
and emits the output indexed by filepath.

```
Filepath, smell, project, package, type, method, cause, start_line_no
```

The `designite_diff` script computes the _diff_ (in terms of detected smells) between two output folders generated by DesigniteJava.

## Usage

**post processor**

Run `process` function in `postprocessor.py` with a folder path where files generated from Designite are placed.

**designite_diff**

Run `process` function in `designite_diff.py`. The script accepts two folder paths and assumes that both the folders are generated by DesigniteJava. The script returns the following output parameters.

- 1 : whether both the folders are same from detected smells perspective
- 2 and 3: list of different arch smells in folder 1 and 2 respectively
- 4 and 5: list of different design smells in folder 1 and 2 respectively
- 6 and 7: list of different impl smells in folder 1 and 2 respectively

**designite_reliable**

`designite_reliable` is a script designed for analyzing commits in more reliable way. The script can be used with or without providing an output path. Here are the some scenarios taken into consideration:

- No <output_path> is provided for the script. This will analyze all the commits in the repository provided through the input path. If any commit stop the designite running due to some errors then script will retry it 3 times and if it is still failing then it will be store in 'retry.csv' file to check manually.

  - ```bash
    Python designite_reliable.py -i <input_path>
    ```

- <output_path> is provided for the script. This have many scenarios as given below :
  - ```bash
    Python designite_reliable.py -i <input_path> -o <output_path>
    ```
  - 1: Output path provided with an empty output folder. _Script will analyze all the commits and will retry the failed commits 3 times._
  - 2: Output folder have many unanalyzed commits. _Script will analyze this commits only. Will retry 3 times if it fails._
  - 3: Output folder have commits with no csv files. _Script will analyze this commits only. Will retry 3 times if it fails._
  - 4: Output folder have commits with csv files having no headers or are empty. _Script will analyze this commits if and only if Lines of Code(LOC) is greater then > 0._
