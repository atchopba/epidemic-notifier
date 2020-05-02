# Overview

Add people with relationship, send them have a test and notify according to result's test

You can easily manage:
- the database: reset data;
- "relations";
- "personnes";
- "tests" ;
- "notifications".

## Benefits 

* Grouping people data.

* Notify people by sms/email when a positive test result is detected.

* Reset the database anytime you want.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Windows 7+ or Linux kernel version 3.10 or higher
* 2.00 GB of RAM
* 3.00 GB of available disk space

Use with Docker http://www.docker.io

### Installation

Pull Docker image on your computer and run:
```
docker pull atchopba/epidemic-notifier

docker run -d -p 5000:5000 --name jobs-web-cli atchopba/epidemic-notifier
```
OR 

You can build a Dcker image on your computer and run :
```
docker build -t epidemic-notifier .

docker run -p 5000:5000 epidemic-notifier
```
Finally, go to your web browser: http://localhost:5000/

#### Screenshots
1. When lauching page in your web browser. 

![Page index](static/images/00-accueil.PNG)

2. Tab "Database" where you can reset the database. 

![Page index](static/images/00-db.PNG)

3. Tab "Relations" where you can manage people's relationship.

![Page index](static/images/01-relation.PNG)

4. Tab "personnes" where you can manage people and add relationship between people.

![Page index](static/images/02-personne.PNG)

5. Tab "tests" where you can manage people's test.

![Page index](static/images/03-test.PNG)

6. Tab "notifications" where you can trigger notifications and an email can be sent to people who have been in contact with a person who has tested positive...
![Page index](04-notification.PNG)

... and the notification is 

![Page index](05-notif_email.PNG)

Otherwise, at each notification, files are created in the "__temp__" directory.

## License & copyright

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details

Set your account less secure
https://myaccount.google.com/lesssecureapps