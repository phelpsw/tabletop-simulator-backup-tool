#!/usr/bin/env python

import argparse
import codecs
import os
import re
import json
import requests
import urlparse

image_keys = [
    'TableURL',
    'SkyURL',
    'FaceURL',
    'BackURL',
    'ImageURL',
    'DiffuseURL',
    'NormalURL'
]

model_keys = [
    'MeshURL',
    'ColliderURL'
]

image_extensions = [
    'png',
    'jpg',
    'jpeg',
    'bmp'
]

image_urls = []
model_urls = []

def url_to_tts(url):
    url_path = urlparse.urlparse(url).path
    url_ext = os.path.splitext(url_path)[1]
    return "".join([c for c in url if c.isalpha() or c.isdigit()]).rstrip() + url_ext

def infer_type_and_add(url):
    split_name = url_to_tts(url).split('.')
    if len(split_name) == 1:
        # No extension, assuming this is an object
        if url not in model_urls:
            model_urls.append(url)
    elif len(split_name) == 2 and split_name[1].lower() in image_extensions:
        # found image type
        if url not in image_urls:
            image_urls.append(url)
    elif len(split_name) == 2 and split_name[1] != 'obj':
        # as a backup, if we find an unknown extension, assume it is an obj
        if url not in model_urls:
            model_urls.append(url)
    else:
        print('unknown name structure {}'.format(split_name))
        return

def parse_dict(_dict):
    for key, value in _dict.items():
        if key == 'SaveName':
            print(value)
        elif key in image_keys and value:
            # process image url
            #print("Found image URL {}".format(value))
            if value not in image_urls:
                image_urls.append(value)
        elif key in model_keys and value:
            # process model url
            #print("Found model URL {}".format(value))
            if value not in model_urls:
                model_urls.append(value)
        elif key == 'LuaScript' and value:
            matches = [g.group(1) for g in re.compile("\"(http://.*)\"").finditer(value)]
            matches.extend([g.group(1) for g in re.compile("'(http://.*)'").finditer(value)])
            matches.extend([g.group(1) for g in re.compile("\"(https://.*)\"").finditer(value)])
            matches.extend([g.group(1) for g in re.compile("'(https://.*)'").finditer(value)])
            for match in matches:
                infer_type_and_add(match)
        elif type(value) is type([]):
            for elem in value:
                if type(elem) is type({}):
                    parse_dict(elem)
        elif type(value) is type({}):
            parse_dict(value)


def parse_tts_custom_object(_filename):
    print(_filename)
    with codecs.open(_filename, encoding='utf-8') as _file:
        game = json.load(_file)
        if type(game) is not type({}):
            raise TypeError('Unexpected input file format. {}'.\
                            format(_filename))
        parse_dict(game)


def download_file(url, path, replace):
    if not os.path.isfile(path) or replace:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            with open(path, "wb") as outfile:
                outfile.write(r.content)
        else:
            print("Error", url, r.status_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Downloads Tabletop Simulator'\
                                     ' workshop files.")
    parser.add_argument("json_input",
                        help="Path to one or more workshop files.",
                        nargs="+")
    parser.add_argument("--output",
                        "-o",
                        help="Output directory for downloaded content.")
    parser.add_argument("--replace", "-r", help="Replace existing files.")
    args = parser.parse_args()

    for filename in args.json_input:
        try:
            parse_tts_custom_object(filename)
        except TypeError as e:
            print e
            continue


    print('Image Count {}'.format(len(image_urls)))
    print('Model Count {}'.format(len(model_urls)))
    print('Total Count {}'.format(len(image_urls) + len(model_urls)))

    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(
            args.json_input[0])), "Retrieved")

    print("Output directory:", output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_dir = os.path.join(output_dir, "Images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    model_dir = os.path.join(output_dir, "Models")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    total = len(image_urls) + len(model_urls)
    count = 1
    for url in image_urls:
        name = url_to_tts(url)
        path = os.path.join(image_dir, name)
        download_file(url, path, args.replace)
        print("({}/{}) {}".format(count, total, url))
        count += 1

    for url in model_urls:
        name = url_to_tts(url)
        split_name = name.split('.')
        if len(split_name) == 1:
            name = name + '.obj'
        elif len(split_name) == 2 and split_name[1] != 'obj':
            name = split_name[0] + '.obj'
        else:
            print('unknown name structure {}'.format(split_name))
        path = os.path.join(model_dir, name)
        download_file(url, path, args.replace)
        print("({}/{}) {}".format(count, total, url))
        count += 1

    print("Done!")

