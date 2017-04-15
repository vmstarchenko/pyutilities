#! /usr/bin/env python3

import json
import os
import zipfile
import shutil


def save_page(page, url):
    cmd = ' '.join(('wget',
                    '--page-requisites',
                    '--html-extension',
                    '--convert-links',
                    '--restrict-file-names=unix',
                    '-e robots=off',
                    '--directory-prefix=%s' % os.path.join(CACHEDIR_TMP, page),
                    '"%s"' % url))
    print('Load: ', cmd)
    os.system(cmd)


CONFIG = 'cache_config.json'
CACHEDIR = '.page_cache'
CACHEDIR_TMP = '.page_cache_tmp'

def unzip_cache():
    with zipfile.ZipFile(CACHEDIR) as zip_file:
        zip_file.extractall(CACHEDIR_TMP)

def zip_cache():
    with zipfile.ZipFile(CACHEDIR, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        rootlen = len(CACHEDIR_TMP) + 1
        for base, dirs, files in os.walk(CACHEDIR_TMP):
            for file in files:
                filename = os.path.join(base, file)
                zip_file.write(filename, filename[rootlen:])

    shutil.rmtree(CACHEDIR_TMP)

def main():
    # read config
    try:
        with open(CONFIG) as config_file:
            config = json.loads(config_file.read())
    except FileNotFoundError:
        raise FileNotFoundError("Can\'t find config file (%s)" % CONFIG)

    unzip_cache()
    cached_pages = set(os.listdir(CACHEDIR_TMP))
    for page, url in config.items():
        if page in cached_pages:
            print('Skip page:\n  %s\n  %s' % (page, url))
            continue
        save_page(page, url)

    zip_cache()

if __name__ == '__main__':
    main()
