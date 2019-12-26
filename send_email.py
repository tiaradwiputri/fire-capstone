import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
import os
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import fire
 
def extract_contacts(contact_file):
  """
  Return two lists contacts, containing names and email addresses
  """
  names = []
  emails = []
  with open(contact_file, mode='r', encoding='utf-8') as contacts:
    for contact in contacts:
      names.append(' '.join(contact.split()[0:-1]))
      emails.append(contact.split()[-1])
  return names, emails

def create_message(template_file):
  """   
  Crete template object from template_file
  """
  with open(template_file, mode='r', encoding='utf-8') as template:
    template_content = template.read()
  return Template(template_content)

def compose_email(template, name, data_file):
  """   
  Compose email from template and data
  // TODO read data once
  """
  start_date, end_date, total_spent, total_conversion, cpc_1, cpc_2 = extract_summary(data_file)
  composed = template.substitute(
    PERSON_NAME=name,
    START_DATE=start_date,
    END_DATE=end_date,
    TOTAL_SPENT="{:,}".format(total_spent),
    TOTAL_CONVERSION="{:,}".format(total_conversion),
    CPC_1="{:,}".format(cpc_1),
    CPC_2="{:,}".format(cpc_2),
    GITHUB_LINK='https://github.com/google/python-fire'
  )
  return composed

def authenticate_account(EMAIL, PASSWORD, SERVER='outlook'):
  """   
  Authenticate SMTP account for two host: gmail or outlook
  """
  if(SERVER == 'gmail'):
    host = 'smtp.gmail.com'
    port = 587
  elif(SERVER == 'outlook'):
    host = 'smtp.office365.com'
    port = 587
  else:
    raise("Email host is not supported")

  s = smtplib.SMTP(host=host, port=port)
  s.starttls()
  s.login(EMAIL, PASSWORD)
  return s

def create_plot(file_path="data_input/data.csv"):
  """   
  Fetch data from data source and export a plot
  // TODO change plot to pandas matplotlib
  """
  fb = pd.read_csv(file_path, parse_dates=[1,2])
  campaigns = fb[fb['campaign_id'].isin(['936', '1178'])]
  campaigns = campaigns[campaigns.spent > 0]
  grouped = campaigns.groupby(by=['campaign_id', 'age', 'reporting_start'], as_index=False)\
    [['interest1', 'interest2', 'interest3', 'impressions', 'clicks', 'spent', 'total_conversion']].\
    sum()

  fig = plt.figure(1, figsize=(15,6))

  for i, campaign in enumerate(grouped.campaign_id.unique()):
      plt.subplot(1, 2, i+1)
      df = grouped[grouped.campaign_id == campaign].loc[:,['age', 'reporting_start', 'total_conversion']]
      df.reporting_start = df.reporting_start.dt.date
      df.pivot(index='reporting_start', columns='age', values='total_conversion').fillna(0).plot.bar(ax=plt.gca())

  fig.suptitle('Campaign Conversion per Age Group', fontsize=20)
  fig.autofmt_xdate()

  imagename = 'plot/'+date.today().strftime(format="%d %b %Y")+'.png'
  fig.savefig(imagename)
  return(imagename)

  
def extract_summary(file_path="data_input/data.csv"):
  fb = pd.read_csv(file_path, parse_dates=[1,2])
  campaigns = fb[fb['campaign_id'].isin(['936', '1178'])]
  campaigns = campaigns[campaigns.spent > 0]

  start_date = campaigns.reporting_start.min().date().strftime(format="%d %b %Y")
  end_date = campaigns.reporting_start.max().date().strftime(format="%d %b %Y")

  total_spent = int(campaigns.spent.sum())
  total_conversion = int(campaigns.total_conversion.sum())

  cpc = campaigns.groupby(['campaign_id'])[['spent', 'total_conversion']].sum()
  cpc['CPC'] = cpc['spent']/cpc['total_conversion']

  cpc_1 = cpc['CPC'][0].round(2)
  cpc_2 = cpc['CPC'][1].round(2)

  return(start_date, end_date, total_spent, total_conversion, cpc_1, cpc_2)

def main(subject, \
  contact_file='templates/contacts.txt', \
  template_file='templates/body.txt', \
  data_file='data_input/data.csv'):
  """   
  Return two lists names, emails containing names and email addresses
  read from a file specified by filename.
  """
  s = authenticate_account(EMAIL=os.environ['EMAIL_ADDRESS'], \
    PASSWORD=os.environ['EMAIL_PASSWORD'])
  names, emails = extract_contacts(contact_file=contact_file)
  for name, email in zip(names, emails):
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message_template = create_message(template_file)

    message = compose_email(message_template, name, data_file)

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From']=os.environ['EMAIL_ADDRESS']
    msg['To']=email
    msg['Subject']=subject
    print('SUBJECT: '+subject)
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    image_name=create_plot(data_file)

    img_data = open(image_name, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(image_name))
    msg.attach(image)
    
    
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

if __name__ == '__main__':
  fire.Fire(main)