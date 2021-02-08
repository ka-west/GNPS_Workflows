import os
import sys
import numpy as np
import pandas as pd

import argparse
import uuid
import glob
import shutil
from scipy import integrate

def calculate_xic(filename, mz, rt, mz_tolerance, rt_min, rt_max, msaccess_path, feature_name):
    temp_result_folder = os.path.join(str(uuid.uuid4()))

    mz_lower = mz - mz_tolerance
    mz_upper = mz + mz_tolerance

    command = 'export LC_ALL=C && {} {} -o {} -x "tic mz={},{} delimiter=tab" --filter "msLevel 1" --filter "scanTime ["{},{}"]"'.format(
                    msaccess_path, filename, temp_result_folder, mz_lower, mz_upper, rt_min, rt_max)

    print(command)
    os.system(command)

    result_filename = glob.glob(os.path.join(temp_result_folder, "*"))[0]
    result_df = pd.read_csv(result_filename, sep="\t", skiprows=1)

    xic_df = pd.DataFrame()
    xic_df["rt"] = result_df["rt"] / 60.0
    xic_df["int"] = result_df["sumIntensity"]

    # Remove temp folder
    shutil.rmtree(temp_result_folder)

    return xic_df


def main():
    parser = argparse.ArgumentParser(description='Creating XIC')
    parser.add_argument('input_folder', help='input_mgf')
    parser.add_argument('output_results', help='output_results')
    parser.add_argument('msaccess_path', help='msaccess_path')
    parser.add_argument('--mz', default=None, help='mz')
    parser.add_argument('--rt', default=None, help='rt')
    parser.add_argument('--mztol', default=None, help='mztol')
    parser.add_argument('--rttol', default=None, help='rttol')
    
    args = parser.parse_args()

    all_input_files = glob.glob(os.path.join(args.input_folder, "*"))

    output_list = []

    for filename in all_input_files:
        mz = float(args.mz)
        rt = float(args.rt)

        xic_df = calculate_xic(filename, 
                                mz, rt, 
                                float(args.mztol), 
                                float(args.rt) - float(args.rttol), 
                                float(args.rt) + float(args.rttol), args.msaccess_path, str(args.mz))

        integration_value = integrate.trapz(xic_df["int"], x=xic_df["rt"])
        
        output_dict = {}
        output_dict["filename"] = os.path.basename(filename)
        output_dict["integration_value"] = integration_value
        output_dict["mz"] = mz
        output_dict["rt"] = rt

        output_list.append(output_dict)

    results_df = pd.DataFrame(output_list)
    results_df.to_csv(args.output_results, sep="\t", index=False)

if __name__ == "__main__":
    main()
