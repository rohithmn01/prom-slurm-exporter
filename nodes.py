#!/usr/bin/env python3

import subprocess
import re
from collections import defaultdict


def run_command(cmd):
    """Executes a shell command and returns the output as a string."""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {cmd}: {e.stderr}")
        return ""


def parse_sinfo_output(output):
    """Parses the output of the sinfo command into a dictionary of node states."""
    lines = output.strip().split("\n")
    nodes = defaultdict(float)  # Defaulting counts to 0

    # Regular expressions for node states
    states = {
        'alloc': re.compile(r'^alloc'),
        'comp': re.compile(r'^comp'),
        'down': re.compile(r'^down'),
        'drain': re.compile(r'^drain'),
        'fail': re.compile(r'^fail'),
        'err': re.compile(r'^err'),
        'idle': re.compile(r'^idle'),
        'maint': re.compile(r'^maint'),
        'mix': re.compile(r'^mix'),
        'resv': re.compile(r'^res'),
    }

    # Process each line of sinfo output
    for line in lines:
        if ',' in line:
            split = line.split(',')
            count = float(split[0].strip())  # Node count
            state = split[1].strip()  # Node state

            # Check which state matches and update the corresponding count
            for state_name, pattern in states.items():
                if pattern.match(state):
                    nodes[state_name] += count
                    break
    return nodes


def main():
    # Execute sinfo command to get node information
    sinfo_output = run_command(['sinfo', '-h', '-o', '%D,%T'])

    # Print the sinfo output for debugging purposes
    print("SINFO Output:")
    print(sinfo_output)

    # Parse the sinfo output to get node state metrics
    nodes = parse_sinfo_output(sinfo_output)

    # Print the results
    print("\nParsed Node States:")
    for state, count in nodes.items():
        print(f"Metric: slurm_nodes_{state}, Value: {count}")


if __name__ == '__main__':
    main()
