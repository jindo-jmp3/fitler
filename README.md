# OVERVIEW

This script logins to Fitler Club member portal and signs up for a class provided by the user.

## REQUIREMENTS

```
virtualenv fitler ~/virtualenvs
source ~/virtualenvs/fitler/bin/activate
pip install -f requirements.txt
```

## DESCRIPTION

. The script takes the following
  - email
  - password
  - class_key (refer to the ```class_dicts.py``` for details on how to add a class)

the script will start trying to reserve that class at 12pm ET.

## EXAMPLE

Here is how you run the script:
```
python wellness_schedule_appointment.py [email] [password] [key into class dict]
```

And here is an example of a dictionary in the `class_dicts.py` file:
```
'sunday_pilates_burn': {
        'start_time': '9:00am',
        'weekday': 'sunday',
        'class_name': 'pilates burn'
}
```
