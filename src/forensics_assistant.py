"""
File: forensics_assistant.py
Author: Savannah Alfaro, sea2985@rit.edu
"""

# Standard Imports
import sys
import json

# Third Party Imports
from colorama import init
from termcolor import colored
import google.generativeai as genai

# Gemini API Key from the config file
with open('../config.json') as f:
    config = json.load(f)
API_KEY = config['api_key']


def read_file(filename):
    """
    Reads an input file and returns the file content.
    :param filename: (String) the input filename
    :return: (String[]) the file content
    """
    # read content from the input file
    print(colored("[*] Reading content from {}".format(filename), "cyan"))
    try:
        with open(filename) as file:
            return file.readlines()
    except Exception as e:
        print(colored("\tUnable to read content from {}.\n\t{}".format(filename, e), "red"))


def call_gemini(content):
    """
    Calls the Gemini-Pro model and returns the model's response.
    :param content: (String []) the file content
    :return: (String) the model's response
    """
    # configure the model and response
    print(colored("[*] Configuring the Gemini-Pro model", "cyan"))
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content("Below is a chat log from a forensic investigation. Please extract any "
                                      "necessary information for a forensic report and provide a brief summary: {}"
                                      .format(content))
    except Exception as e:
        print(colored("\tFailed to retrieve a response from the model.\n\t{}".format(e), "red"))


def write_report(response, filename):
    """
    Writes the model's response to an output file.
    :param response: (String) the model's response
    :param filename: (String) the output filename
    :return: None
    """
    # write response to an output file
    print(colored("[*] Writing the response to {}".format(filename), "cyan"))
    try:
        with open(output_filename, 'w') as file:
            file.writelines(response.text)
        print("\tSuccessfully wrote {} lines to {}".format(len(response.text), filename))
    except Exception as e:
        print(colored("\tUnable to write content to {}.\n\t{}".format(filename, e), "red"))


if __name__ == "__main__":
    # initialize colorama
    init()

    # command line arguments
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # read the file content
    file_content = read_file(input_filename)

    # call gemini-pro
    gemini_response = call_gemini(file_content)

    # construct the forensic report
    write_report(gemini_response, output_filename)
