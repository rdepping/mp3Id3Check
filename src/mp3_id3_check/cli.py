#!/usr/bin/env python3

import os
import argparse
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import csv
from pathlib import Path

# Define the expected ID3 tags
expected_tags = [
    'album',
    'albumartist',
    'artist',
    'title',
    'date',
]

# List of headers for exported csv (sermon audio specific)
csv_headers = [
    'series',
    'title',
    'preacher',
    'year',
    'filepath',
    'filename',
]


def title_case_filename_part(value):
    value = re.sub(r'[-_]+', ' ', value)
    value = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', value)
    value = re.sub(r'\s+', ' ', value).strip()
    return value.title()


def suggest_sermon_tags(file_path):
    filename = Path(file_path).stem
    date_match = re.search(r'(20\d{6}|19\d{6}|20\d{2}|19\d{2})$', filename)
    year = ''
    title_source = filename
    if date_match:
        date_value = date_match.group(1)
        year = date_value[:4]
        title_source = filename[:date_match.start()].rstrip('_- ')

    title_parts = re.split(r'[_-]+', title_source, maxsplit=1)
    passage = title_case_filename_part(title_parts[0]) if title_parts else ''
    sermon_title = title_case_filename_part(title_parts[1]) if len(title_parts) > 1 else ''
    title = ' - '.join(part for part in [passage, sermon_title] if part)

    return {
        'album': 'Carrigaline Baptist Church',
        'albumartist': 'Carrigaline Baptist Church',
        'artist': '',
        'title': title,
        'date': year,
    }


def prompt_for_tag(filename, tag, current_value, suggestion):
    default_value = current_value or suggestion
    prompt_parts = [f"{filename} {tag}"]
    if current_value:
        prompt_parts.append(f"current='{current_value}'")
    if suggestion and suggestion != current_value:
        prompt_parts.append(f"suggested='{suggestion}'")
    if default_value:
        prompt_parts.append(f"[{default_value}]")
    prompt = ' '.join(prompt_parts) + ': '
    response = input(prompt).strip()
    return response if response else default_value


def correct_mp3_file(file_path):
    try:
        audio = EasyID3(file_path)
    except ID3NoHeaderError:
        audio = EasyID3()

    suggestions = suggest_sermon_tags(file_path)
    filename = Path(file_path).name
    changed = False

    print(f"\nCorrecting {filename}")
    for tag in expected_tags:
        current_value = audio[tag][0] if tag in audio and audio[tag] else ''
        new_value = prompt_for_tag(filename, tag, current_value, suggestions.get(tag, ''))
        if new_value and new_value != current_value:
            audio[tag] = new_value
            changed = True

    if changed:
        audio.save(file_path)
        print(f"Saved changes to {filename}")
    else:
        print(f"No changes made to {filename}")


def correct_mp3_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            correct_mp3_file(os.path.join(folder_path, filename))


def check_mp3_files_have_tags(folder_path, summary):
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

    print(f"Total files checked: {total_files}, "
          f"Compliant: {total_files - len(non_compliant_files)} "
          f"Non-compliant: {len(non_compliant_files)}")
    for non_compliant_file in non_compliant_files:
        print(f'Non-compliant {non_compliant_file}')

    if summary:
        print("\nTag Summary:")
        for tag in expected_tags:
            print(f"\n=== {tag}:")
            values = tag_summary[tag]
            unique_values = set(values)
            for value in unique_values:
                if value is not None:
                    count = values.count(value)
                    print(f"{value} ({count} file(s))")


def export_sermon_tags_to_csv(folder_path):
    total_files = 0
    file_name = 'sermons.csv'
    with open(file_name, 'w') as f:
        write = csv.writer(f)
        write.writerow(csv_headers)
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp3'):
                total_files += 1
                file_path = os.path.join(folder_path, filename)
                try:
                    audio = EasyID3(file_path)
                    keys = audio.keys()
                    remove_tags = [tag for tag in keys if tag not in expected_tags]
                    if remove_tags:
                        for tag in remove_tags:
                            print(f'Skipping export of tag {tag} from {filename}')
                            audio.pop(tag)
                    # Assume the order of the tag values matches the headers - may not always hold
                    row = audio.values()
                    row.append(audio.filename)  # full path + filename
                    row.append(Path(audio.filename).name)  # just the filename
                    write.writerow(row)
                except Exception as e:
                    print(f"Error processing mp3 file for csv export' {filename}': {str(e)}")
        print(f'Exported {total_files} to {file_name}')


def main():
    parser = argparse.ArgumentParser(description='Check MP3 files for expected ID3 tags.')
    parser.add_argument('folder_path', metavar='FOLDER_PATH', type=str, nargs='?',
                        default='.', help='path to the folder (default: current folder)')
    parser.add_argument('-s', '--summary', help='include a summary',
                        action='store_true')
    parser.add_argument('-c', '--correct', help='prompt to correct tags using filename suggestions',
                        action='store_true')
    parser.add_argument('-x', '--export', help='Export csv summary',
                        action='store_true')
    args = parser.parse_args()

    if args.correct:
        correct_mp3_files(args.folder_path)
    elif args.export:
        export_sermon_tags_to_csv(args.folder_path)
    else:
        check_mp3_files_have_tags(args.folder_path, args.summary)


if __name__ == '__main__':
    main()
