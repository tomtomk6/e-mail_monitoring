# Overview

As a Performance Planner in a media agency my task was the steering partners in E-Mail-Marketing, which would send up to 2 million mails per month to their databases with the latest offers of one of the major telecommunication companies in Germany.

The e-mail-address market in Germany is very intransparent, so controlling quality, sent date, implementation and possible arbitraging was essential. I researched the main lead generation websites for our providers and registered three mail accounts to be part of our mail campaigns.

Analyzing the mails manually proved to be too difficult, so I created a script to automatically scan the three mail accounts for our mails.

# Functionality

The script can retrieve mails from a POP3 server, analyze contents and store them locally as .HTML documents.

# Frontend

In order to ease accessibility of the tool, I created a Frontend with Qtpy as well. Thus a single file .exe was ready to use.