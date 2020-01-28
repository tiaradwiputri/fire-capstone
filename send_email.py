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
  Please prepare an external files containing 2 information: name and email address
  Use the following format: <NAME> <EMAIL> on the flat file
  """
  names = []
  emails = []
  with open(contact_file, mode='r', encoding='utf-8') as contacts:
    for contact in contacts:
      names.append(' '.join(contact.split()[0:-1]))
      emails.append(contact.split()[-1])
  return names, emails

def extract_summary(file_path="data_input/data.csv", id=['936','1178']):
  """   
  Extract all relevant information, containing 6 variables
  start_date, end_date, total_spent, total_conversion, cpc_1, cpc_2
  """
  fb = pd.read_csv(file_path)
  campaigns = fb[fb['campaign_id'].isin(id)]
  campaigns = campaigns[campaigns.spent > 0]

  # Make sure to passed in appropriate preprocessing before extracting the start and end date
  campaigns['reporting_start'] = ___
  start_date = ___.min().strftime(format="%d %b %Y")
  end_date = ___.max().strftime(format="%d %b %Y")

  total_spent = int(___.sum())
  total_conversion = int(___.sum())

  # Create a cost per conversion dictionary per campaign
  # Cost per conversion is spent divided by total conversion
  cpc = campaigns.groupby(['campaign_id'])[[___, ___]].sum()
  cpc['CPC'] = cpc[___]/cpc[___]
  cpc_each = dict()
  for each in id:
    cpc_each[each] = round(float(cpc[cpc.index == each]['CPC']), 2)

  return {
    "start_date": start_date,
    "end_date": end_date,
    "total_spent": total_spent,
    "total_conversion": total_conversion,
    "cpc": cpc_each
  }

def create_template(template_file):
  """   
  Crete template object from template_file
  """
  with open(template_file, mode='r', encoding='utf-8') as template:
    template_content = template.read()
  return Template(template_content)

def unroll_sentence(data_dict):
  """   
  Unroll a dictionary to build a sentence
  """
  list_sentence = ""

  for key in data_dict:
      if key == list(data_dict.keys())[-1]:
          list_sentence += "and "
          list_sentence += str(data_dict[key]) + " "
          list_sentence += "for campaign "+ key
      else: 
          list_sentence += str(data_dict[key]) + " "
          list_sentence += "for campaign "+ key +", "
  return list_sentence

def compose_email(template, name, data_dict):
  """   
  Compose email from template and data, attaching name on the message
  """
  composed = template.substitute(
    PERSON_NAME=name,
    START_DATE=data_dict[___],
    END_DATE=data_dict[___],
    TOTAL_SPENT="{:,}".format(data_dict[___]),
    TOTAL_CONVERSION="{:,}".format(data_dict[___]),
    CPC=unroll_sentence(data_dict['cpc']),
    GITHUB_LINK='https://github.com/tiaradwiputri/fire-capstone'
  )
  return composed

def authenticate_account(EMAIL, PASSWORD, SERVER='outlook'):
  """   
  Authenticate SMTP account for outlook
  Other host is not supported
  """

  if(SERVER == 'outlook'):
    host = 'smtp.office365.com'
    port = 587
  else:
    raise("Email host is not supported")

  s = smtplib.SMTP(host=host, port=port)
  s.starttls()
  s.login(EMAIL, PASSWORD)

  return s

def create_plot(file_path="data_input/data.csv", id=['936', '1178']):
  """   
  Fetch data from data source and export as plot
  """
  fb = pd.read_csv(file_path, parse_dates=[1,2])
  campaigns = fb[fb['campaign_id'].isin(id)]
  campaigns = campaigns[campaigns.spent > 0]

  # Create a grouped dataframe based on campaign id, age group, and reporting date
  # Calculate the total converision of each group
  grouped = campaigns.groupby(by=['___', '___', '___'], as_index=False)['___'].___

  fig = plt.figure(1, figsize=(15,6))

  # Iterate to create 1 plot campaign at a time
  for i, campaign in enumerate(grouped.campaign_id.unique()):
    plt.subplot(1, len(id), i+1)
    
    df = grouped[grouped[___] == campaign].loc[:,['age', 'reporting_start', 'total_conversion']]
    df['reporting_start'] = df['reporting_start'].dt.date
    pivot = df.pivot(index='___', columns='___', values='___').fillna(0)
    pivot.plot.bar(ax=plt.gca())

  fig.suptitle('Campaign Conversion per Age Group', fontsize=20)
  fig.autofmt_xdate()

  # Save file to plot folder
  imagename = 'plot/'+date.today().strftime(format="%d %b %Y")+'.png'
  fig.savefig(imagename)
  return(imagename)

def main(subject, \
  contact_file='___', \
  template_file='templates/body.txt', \
  data_file='data_input/data.csv'):
  """   
  Main function for application
  """

  # // TODO: CHALLENGE 1
  # // Understanding function
  names, emails = extract_contacts(contact_file=contact_file)

  # // TODO: CHALLENGE 2
  # // Extract data and prepare template email
  template = create_template(template_file)
  data_dict = extract_summary(data_file)

  # // TODO: CHALLENGE 3
  # // Log in into Outlook email account
  # // Please use environment variable for security purposes
  s = authenticate_account(EMAIL=os.environ['EMAIL_ADDRESS'], \
    PASSWORD=os.environ['EMAIL_PASSWORD'])

  # Iterate through all extracted contacts
  for name, email in zip(names, emails):
    message = compose_email(template, name, data_dict)

    # Prints out the message body for message cross check
    print(message)

    # setup email message
    msg = MIMEMultipart()   
    # setup the parameters of the message
    msg['From']=os.environ['EMAIL_ADDRESS']
    msg['To']=email
    msg['Subject']=subject
    print('SUBJECT: '+subject)
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # // TODO: CHALLENGE 4
    # // Create, save, and attach plot
    image_name=create_plot(data_file)

    img_data = open(image_name, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(image_name))
    msg.attach(image)
    
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

if __name__ == '__main__':
  # Export to Fire
  fire.Fire(main)