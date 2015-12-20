#!/usr/bin/python3

import json
from copy import copy
import os

def load_replace_rules(rule_file_path):
    with open(rule_file_path, 'r') as rule_file:
        return json.load(rule_file)

def load_template(template_path):
    with open(template_path, 'r') as template_file:
        data = template_file.read()
        return data

def write_thread_file(file_path, string):
    with open(file_path, 'w') as thread_file:
        thread_file.write(string)

def output_threads(folder, threads):
    with open("threads.txt", 'w') as thread_file:
        for key, value in threads.items():
            thread_file.write(key + "\n==========================\n")
            thread_file.write(value + "==========================\n\n")

def create_match_threads(master_template, replace_rules):

    match_threads = {} #dict of strings we will build up with match threads
    for matchType in replace_rules:

        # Replace instances of these replacers
        simple_replacers = ["RoundTitle", "StartDate", "EndDate"]

        # Copy into seperate template to modify based on type parameters
        type_template = master_template
        for replacer in simple_replacers:
            type_template = type_template.replace("<" + replacer + ">", matchType[replacer])

        # Maps must be replaced seperately
        maps = []
        for m in matchType["MapPool"]:
            maps.append("[*]" + m)
        maps = "\n".join(maps)
        type_template = type_template.replace("<MapPool>", maps)

        # and finally for each particular match...
        for match in matchType["Matchups"]:

            thread_title = "{}: {} vs {}".format(matchType["RoundTitle"], match["HomeTeam"], match["AwayTeam"])

            match_thread = type_template
            replacers = ["HomeTeam", "AwayTeam"]
            for replacer in replacers:
                match_thread = match_thread.replace("<" + replacer + ">", match[replacer])

            match_threads[thread_title] = match_thread

    return match_threads

if __name__ == "__main__":
    template = load_template('sc16.txt')
    replace_rules = load_replace_rules('replace_rules.json')
    threads = create_match_threads(template, replace_rules)
    output_threads("outfiles", threads)
