from send_email import extract_contacts, extract_summary, create_template, compose_email
import fire

def debug(subject, \
  contact_file='templates/contacts.txt', \
  template_file='templates/body.txt', \
  data_file='data_input/data.csv'):

    names, emails = extract_contacts(contact_file=contact_file)

    # // TODO: CHALLENGE 2
    # // Extract data and prepare template email
    data_dict = extract_summary(data_file)
    template = create_template(template_file)

    # Print for debugging purposes
    print(compose_email(template, "debugger", data_dict))
if __name__ == '__main__':
  # Export to Fire
  fire.Fire(debug)