# Auto Generated Email Based Report

This is developed as one of Algoritma Academy Data Analytics Specialization using capstone Projects. The deliverables of this project is a python script to send an automated generated email using SMTP of either Google or Outlook email host. We will also utilize Google's `fire` package for easy interfacing with bash command. 

## Setup

There are few prerequisites needed for this project, first you will need to prepare a new conda environment installed with all package dependencies. Run the following command to create a new conda environment from `environment.yml`:

```
conda env create -f environment.yml
```

We will also utilize Selenium package in exporting the Altair image into png file. To do that you need to make sure you have installed a [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/). Once the driver is added on your system's PATH, Selenium will use it to launch a headless state Chrome Browser and you should be able to save Altair's chart as png or svg.

## Components

### SMTP Setup

The SMTP setup is managed within `authenticate_account` function. The default email host used is Outlook mail. If you are using a google account, make sure to change the default `SERVER` parameter from `outlook` to `gmail`.

The `smtplib` library will managed SSL authetication for your email address. For security purposes, you will need to set up an environment variables on your local machine called `EMAIL_ADDRESS` and `EMAIL_PASSWORD`. This is done to avoid having to hard code your email and password on the script and risking it to be accidentaly shared accross the internet.

To verify your environment variables, run the following python code:

```
import os
os.environ['EMAIL_ADDRESS']
os.environ['EMAIL_PASSWORD']
```

If each line successfuly printed out the respective environment, you should be good to go.

### Report Templates

To compose the email body effectively, we'll be using a `Template` object. The object will be created from an external file stored under `templates/body.txt`. If you open the file, you should see several parameters you will need to fill in as part of the capstone requirement:

- `PERSON_NAME`: You will fill this in on the [Contacts List](#contacts-list) section
- `START_DATE`, `END_DATE`, `TOTAL_SPENT`, `TOTAL_CONVERSION`, `CPC_1`, and `CPC_2`: You need to extract the specified information from the data source under `extract_summary` function using `pandas` exploratory tools you have learned. Please see the full detail for this parameter under the [Data Sumary](#data-summary) section
- `GITHUB_LINK`: You can either change the template txt file into a hard-coded Github link or assign it on your Python script under `compose_email` function

### Contacts List

This module is designed to support email blast to multiple recipients at a time. The contacts list is stored on external file under `templates/contacts.txt`. Each line will represent 1 contact list with the following format:

`person_name email`

The string stated in before email string will be used to address the person in the email. For example the following contact list:

`Team Algoritma mentor@algorit.ma`

will be separated into two variables:
- Name: Team Algoritma
- Email: mentor@algorit.ma

### Altair Export

Implementing what you have learned on the visualization course, please create an Altair plot from the data stored at `data_input/data.csv`. The data is downloaded from [Kaggle dataset repository](https://www.kaggle.com/madislemsalu/facebook-ad-campaign) provided by [Madis_Lemsalu](https://www.kaggle.com/madislemsalu). The data contains daily ads report run on Facebook, showing different marketing campaign from 18th to 30th of August 2017. Please complete the following pre-processing steps:

- Filter the `campaign_id` to only 936 and 1178
- Remove all rows that listed a spent of 0 specified in `spent` column
- Create a grouped information from the two campaigns of its spent and total conversion per age group.

Once you perform the preprocessing steps, recreate the following chart under `create_plot` function and store in under `chart` object. The `chart.save(imagename)` on the end of the function should automatically save your chart into a png file under `plot` folder. The bar chart shown on denotes daily spent for each campaign, while the red line denotes daily total conversion.

![](plot/today.png)

### Data Summary

Since we need to pass in the data summary onto the provided template, please complete `extract_summary` function to return the following variables:

- `start_date`: The earliest date of the report
- `end_date`: The latest date of the report
- `total_spent`: Total spent of the 2 campaigns shown on the plot
- `total_conversion`: Total conversions gained from the 2 campaigns shown on the plot
- `cpc_1`: Cost per conversion from campaign `1178`
- `cpc_2`: Cost per conversion from campaign `936`

### Utilizing `fire`

The `fire` package has been set up to fire `main` function when called. If the script has been set up properly, you should be able to call the function from CLI. The parameter passed into the function can be specify using the syntax: `--param=value`. You can pass in multiple parameters within one line execution, the available parameters are:

- `subject`: Provide your email subject
- `contact_file`: Default set to `templates/contacts.txt`
- `template_file`: Default set to `templates/body.txt`
- `data_file`: Default set to `data_input/data.csv`

The bash command should be able to fire the script using the following syntax:

```
python send_email.py --subject="YOUR SUBJECT"
```

## Final Mission

If all components has been properly set up, you should be able to sent us an auto generated report email to `mentor@algorit.ma`. Your final mission in this capstone project is to send us an email, providing your GitHub link on the email templates with the exported plot attached on the email. Please send the email with the following details:

Subject: 
>[BATCH_NAME DA CAPSTONE] Facebook Email Report

For example:

>[IRIS DA CAPSTONE] Facebook Email Report

Body Template:

> Hi Team Algoritma,
>
>This is an auto-generated email, reporting Facebook ads campaign performance for all listed campaign from \${START_DATE}\$ to \${END_DATE}\$. The total marketing budget spent on the campaign is \${TOTAL_SPENT}\$ with a total coversion of \${TOTAL_CONVERSION}\$. The cost per conversion for gained on the two campaigns is \${CPC_1}\$ and \${CPC_2}\$ respectively.
>
>Please find the complete script on my Github: \${GITHUB_LINK}\$
>
>Best regards,




We are looking forward for your email!

---
Good luck and happy coding!
