import sys
import os
import requests
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Batch Create Wrapper Validator')
parser.add_argument('workflowparams')
parser.add_argument('pklbinfolder')
parser.add_argument('annotation_table')
parser.add_argument('result_output')
parser.add_argument('new_results_output')
parser.add_argument('output_library')
parser.add_argument('main_execmodule_path')
args = parser.parse_args()

# Making sure the into annotation table has a dummy spectrumID
annotation_table_df = pd.read_csv(args.annotation_table, sep="\t")
temp_annotation_filename = "annotation.tsv"
annotation_table_df["SPECTRUMID"] = "SPECLIBTEMP"
annotation_table_df.to_csv(temp_annotation_filename, sep="\t", index=False)

cmd = "{} ExecSpectraExtractionTable {} -ccms_input_spectradir {} -ccms_table_input {} -ccms_results_dir {} -ccms_newresults_dir {} -ccms_newoutputlibrary {} -ccms 1".format(args.main_execmodule_path, 
    args.workflowparams, args.pklbinfolder, temp_annotation_filename, args.result_output, args.new_results_output, args.output_library)

print(cmd)

os.system(cmd)

# /data/beta-proteomics2/tools/add-batch-annotated-validator/release_20+validator-update/main_execmodule 
# ExecSpectraExtractionTable 
# workflowParameters/params.xml 
# -ccms_input_spectradir spectrapklbin 
# -ccms_results_dir result/52af698dbaf7468f98df89dae45091ad.out 
# -ccms_newresults_dir newspectraResult/06464ac4b44344c5b6a81fa9dcb9bd9d.out 
# -ccms 1 
# -ccms_table_input annotation_table/annotation_table-00000.tsv 
# -ccms_newoutputlibrary new_spectra_mgf/3ec48b86b8b3439aa029463f79b918ce.mgf -ll 9