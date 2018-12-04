# BillScrape
# Script to identify bills in my email and save them to gdrive
# 
# Author:   Mark Osborne
# Date:     15.11.2018

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
import oauth2client 
from oauth2client import file,tools
import imapclient 
import vault
import json



# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

# gdrive api
gdrivesecret = vault.get('gdriveapi','secret')

# get user/pass
gmail = vault.get('gmailuser','main')
pcblues = vault.get('pcbluesuser','main')
gmailpass=vault.get('gmailpass',gmail)
pcbluespass=vault.get('pcbluespass',pcblues)


def drivedemo():
    print('\ngdrive')
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = oauth2client.client.flow_from_clientsecrets ('gdrivecred.json', SCOPES)
        flow.client_secret = gdrivesecret
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def doGmail():
    print('\ngmail.com')
    # gmail
    # context manager ensures the session is cleaned up
    with imapclient.IMAPClient(host="imap.gmail.com") as client:
        client.login(gmail,gmailpass)
        client.select_folder('INBOX')

        # search criteria are passed in a straightforward way
        # (nesting is supported)
        messages = client.search(['NOT', 'DELETED'])

        # fetch selectors are passed as a simple list of strings.
        response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

        # `response` is keyed by message id and contains parsed,
        # converted response items.
        for message_id, data in response.items():
            print('{id}: {size} bytes, flags={flags}'.format(
                id=message_id,
                size=data[b'RFC822.SIZE'],
                flags=data[b'FLAGS']))

def doPCBlues():
    print ('\npcblues.com')
    # pcblues
    # context manager ensures the session is cleaned up
    with imapclient.IMAPClient(host="mail.pcblues.com") as client:
        client.login(pcblues, pcbluespass)
        client.select_folder('INBOX')

        # search criteria are passed in a straightforward way
        # (nesting is supported)
        messages = client.search(['NOT', 'DELETED'])

        # fetch selectors are passed as a simple list of strings.
        response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

        # `response` is keyed by message id and contains parsed,
        # converted response items.
        for message_id, data in response.items():
            print('{id}: {size} bytes, flags={flags}'.format(
                id=message_id,
                size=data[b'RFC822.SIZE'],
                flags=data[b'FLAGS']))

drivedemo()
doGmail()
doPCBlues()

