import os
import datetime as DT
from github import Github

repository = input("Enter repository : ")

today = DT.date.today()
week_ago = today - DT.timedelta(days=7)
access_token=os.environ.get("GITHUB_TOKEN_NEW")# using an access token
g = Github(access_token)
repo = g.get_repo(repository)
pulls = repo.get_pulls(sort='created',state='all')


email_message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Github $repository repository status report for pull requests

This is an status report for PR's in $repository repository From $from_date to $to_date

 <TABLE>
  <TR>
    <TH>Number</TH>
    <TH>CREATED_AT</TH>
    <TH>STATE</TH>
    <TH>USER</TH>
    <TH>TITLE</TH>
  </TR>

"""



for pr in pulls:

    row_data = """
    <TR>
     <TD>number</TD>
     <TD>created_at</TD>
     <TD>state</TD>
     <TD>user</TD>
     <TD>title</TD>
    </TR>
    """

    if (str(pr.created_at).split(" ")[0]) > str(week_ago):

        char_to_replace = {'number': str(pr.number),
                           'created_at': str(pr.created_at),
                           'state': str(pr.state),
                           'user': str(pr.user)[:-2].split('="')[1],
                           'title': str(pr.title)}

        for key, value in char_to_replace.items():
            row_data = row_data.replace(key, value)

        email_message = email_message + row_data


email_message = email_message + """
</TABLE>
"""
email_message =  email_message.replace("$repository", repository)
email_message =  email_message.replace("$from_date", str(week_ago))
email_message =  email_message.replace("$to_date", str(today))

print (email_message)
