# ASEBAtranscription

This is a script and library for transcribing ASEBA (CBCL/YSR) data that has been entered in to REDcap or another tabular format in to a JSON file that can be imported into the ASEBA scoring software for scoring. To be clear, this will not score the instruments for you, it simply allows you to avoid manually transcribing the data in to ASEBA from another source.

This product is not endorsed in any way by Thomas Achenbach, the Research Center for Children, Youth, & Families, or the University of Vermont. It is provided for non-commercial use and at your own risk, with no guarantees as to the quality of the resulting data.

# Usage

python3 TranscribeAseba.py (mapping) (cbcl) (ysr)

* mapping: specify the CSV file with the study variable mappings.
* cbcl: Specify the CSV with the CBCL school age (6-18) form data.
* ysr: Specify the CSV with the YSR school age (6-18) form data.

Output json will be written to the 'output/' folder.

Probably, the first time you do this it will fail. You will need to adjust the 'mapping' file so that the values describe python expressions that produce the value ASEBA expects.

N.B. your questionnaire may contain comment fields. These values may contain identifiable info, so you may wish to edit that out before you import the data in to ASEBA.

# Dependencies:

The following packages are required:

* json
* csv
* argparse
* pprint
* warnings
* time
* numpy




