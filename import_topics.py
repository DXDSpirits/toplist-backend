import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toplist.settings")

import codecs
from django.conf import settings
from os import listdir, makedirs
from os.path import isfile, isdir, join
import shutil

from topics.models import Topic, Candidate


def create_candidate(topic, title, rank):
    return Candidate(topic=topic, title=title, rank=rank + 1,
                     picture='topic/%d/%d.jpg' % (topic.id, rank))


def create_topic(lines):
    topic = Topic.objects.create(title=lines[0].strip(),
                                 description=lines[1].strip())
    candidates = [create_candidate(topic, title.strip(), rank + 1)
                  for rank, title in enumerate(lines[2:]) if title]
    Candidate.objects.bulk_create(candidates)
    return topic


def list_files(topic_dir):
    print topic_dir
    for name in listdir(topic_dir):
        topic_file = join(topic_dir, name)
        if isfile(topic_file) and topic_file.endswith('.txt'):
            with codecs.open(topic_file, 'r', 'gbk') as f:
                lines = f.readlines()
    topic = create_topic(lines)
    # Copy pictures
    picture_dir = join(settings.MEDIA_ROOT, 'topic/%d' % topic.id)
    makedirs(picture_dir)
    for name in listdir(topic_dir):
        topic_file = join(topic_dir, name)
        if isfile(topic_file) and topic_file.endswith('.jpg'):
            dest = join(picture_dir, name)
            shutil.copy(topic_file, dest)


def list_dirs(root_dir):
    for name in listdir(root_dir):
        topic_dir = join(root_dir, name)
        if isdir(topic_dir):
            list_files(topic_dir)


if __name__ == "__main__":
    list_dirs('D:\\toplist_import')
