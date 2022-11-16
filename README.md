# ASEBAtranscription

This is a script and library for transcribing ASEBA (CBCL/YSR) data that has been entered in to REDcap or another tabular format in to a JSON file that can be imported into the ASEBA scoring software for scoring. To be clear, this will not score the instruments for you, it simply allows you to avoid manually transcribing the data in to ASEBA from another source.

This product is not endorsed in any way by Thomas Achenbach, the Research Center for Children, Youth, & Families, or the University of Vermont. It is provided for non-commercial use and at your own risk, with no guarantees as to the quality of the resulting data.

# Usage

python3 TranscribeAseba.py (mapping) (cbcl) (ysr)

* mapping: specify the CSV file with the study variable mappings.
* cbcl: Specify the CSV with the CBCL school age (6-18) form data.
* ysr: Specify the CSV with the YSR school age (6-18) form data.

All input files must be in UTF-8 (redcap should output this, but if it's not working you should open in excel and save as 'csv utf-8'.

Output json will be written to the 'output/' folder.

Probably, the first time you do this it will fail. You will need to adjust the 'mapping' file so that the values describe python expressions that produce the value ASEBA expects.

N.B. your questionnaire may contain comment fields. These values may contain identifiable info, so you may wish to edit that out before you import the data in to ASEBA.

# About the 'mapping' file.

The mapping file is a three column csv document which contains three columns:

* *$QuestionId$*: this corresponds to question ID's in the output json file (set by ASEBA -- don't change)
* *SourceField*: python code that evaluates to the value you want. In this column dat['X'] corresponds to the values of the column named 'X' in the redcap data files. Some values will need to be recoded and you can include python code to do that here. There are a few helper functions included to help do this:
  * arithcode: This adds a constant to a numeric value in the redcap data and returns a string with the resulting number. Used for recording
  * sdlabrelcalc: This is only used for the 'relationship' field and performs a 1 for 1 recode.
* *SourceCommentField*: Same as above, but for comment fields. This gets used, for example, every time there is an 'other value'. In the redcap data, it's a separate column, in the JSON it is a separate property of the question.
* *Notes*: Comments with no programatic effect.

Note that the first row (1000) is a special field with a string that corresponds to the ID column in the redcap data files.

# Dependencies:

The following packages are required:

* json
* csv
* argparse
* pprint
* warnings
* time
* numpy




