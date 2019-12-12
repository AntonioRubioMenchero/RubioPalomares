#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader
'''

import sys
import hashlib
import os.path
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    
    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Downloader function
        '''
        file_downloader = download_mp3(url)
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file_downloader)
        fileInfo.hash = calculate_hash(fileInfo.name)
        orchest = self.event_file.getPublisher()
        orchest = TrawlNet.UpdateEventPrx.uncheckedCast(orchest)
        orchest.newFile(fileInfo)
        return fileInfo

    def __init__(self, event):
        self.event_file = event


def calculate_hash(file_name_hash):
    '''
    Calculate hash
    '''
    file2Hash = hashlib.sha256()
    with open(file_name_hash, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            file2Hash.update(chunk)
    return file2Hash.hexdigest()


class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server instance
    '''
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv): # pylint: disable=W0613
        '''
        Run Server
        '''
        topic_name = "UpdateEvents"
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            return 2
        
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        downloader = DownloaderI(topic)
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy_dwn = adapter.add(downloader, broker.stringToIdentity("downloader"))
        print(proxy_dwn, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class NullLogger:
    '''
    NullLogger
    '''
    def debug(self, msg):
        '''
        debug method
        '''
        pass

    def warning(self, msg):
        '''
        warning method
        '''
        pass

    def error(self, msg):
        '''
        error method
        '''
        pass

_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination='./'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        '''
        progress hook
        '''
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']




SERVER = Server()
sys.exit(SERVER.main(sys.argv))
