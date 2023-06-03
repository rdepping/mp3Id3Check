#!/usr/bin/env python3

import os
import argparse
from mutagen.easyid3 import EasyID3

# boostrapped via chatgpt - use beware

# Define the expected ID3 tags
expected_tags = {
    'album',
    'albumartist',
    'artist',
    'title',
    'date',
    'genre',
}


def check_mp3_files(folder_path, summary):
    # Initialize counters
    total_files = 0
    compliant_files = 0
    non_compliant_files = []

    # Create a dictionary to store the summary of all tags
    tag_summary = {tag: [] for tag in expected_tags}

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            total_files += 1
            file_path = os.path.join(folder_path, filename)
            try:
                audio = EasyID3(file_path)
                # print(audio.pprint())
                # Check if all expected tags exist
                if all(tag in audio for tag in expected_tags):
                    compliant_files += 1
                else:
                    missing_tags = [tag for tag in expected_tags if tag not in audio]
                    non_compliant_files.append((filename, missing_tags))
                # Store the values for each tag in the summary
                for tag in expected_tags:
                    if tag in audio:
                        tag_summary[tag].append(audio[tag][0])
                    else:
                        tag_summary[tag].append(None)
            except Exception as e:
                print(f"Error processing file '{filename}': {str(e)}")

    print(f"Non-compliant files found: {len(non_compliant_files)}")
    for filename, missing_tags in non_compliant_files:
        print(f"\tFile: {filename} is missing {missing_tags}")

    if summary:
        print(f"Total files checked: {total_files}, "
              f"Compliant: {total_files - len(non_compliant_files)} "
              f"Non-compliant: {len(non_compliant_files)}")

        print("\nTag Summary:")
        for tag in expected_tags:
            print(f"\n=== {tag}:")
            values = tag_summary[tag]
            unique_values = set(values)
            for value in unique_values:
                if value is not None:
                    count = values.count(value)
                    print(f"{value} ({count} file(s))")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check MP3 files for expected ID3 tags.')
    parser.add_argument('folder_path', metavar='FOLDER_PATH', type=str, nargs='?',
                        default='.', help='path to the folder (default: current folder)')
    parser.add_argument('-s', '--summary', help='include a summary',
                        action='store_true')
    parser.add_argument('-c', '--correct', help='(future) automatically correct missing tags where possible',
                        action='store_true')
    args = parser.parse_args()

    check_mp3_files(args.folder_path, args.summary)
