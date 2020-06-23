# Overview

During an epidemic period, manage the people in contact and notify them when the test result is positive! you also have the possibility of configuring symptoms, giving them scores and knowing automatically after a diagnosis whether a person is potentially sick or not.

You can easily manage:
- the database: reset data;
- "relations";
- "personnes" with "conditions de vie / consultation / contact / diagnostic". You have a graph realized with the [D3.js v4 Force Directed Graph with Labels](https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8) project;
- "tests" ;
- "notifications".

## Benefits 

* Grouping people data.

* Possibility of estimating people's probabilities of illness based on the symptoms developed.

* Notify people by sms/email when a positive test result is detected.

* Reset the database anytime you want.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

- Rename "init.env" to ".env"
- Edit ".env" file and put the right values.
- Account to log in: medec1 / medec1


Log on to [Gmail](http://www.gmail.com) and activate the option ["Less secure access to applications" ]( https://myaccount.google.com/lesssecureapps ).

### Prerequisites

* Windows 7+ or Linux kernel version 3.10 or higher
* 2.00 GB of RAM
* 3.00 GB of available disk space

Use with Docker http://www.docker.io

### Installation

Pull Docker image on your computer and run:
```
docker pull atchopba/epidemic-notifier

docker run -d -p 5000:5000 --name epidemic-notifier atchopba/epidemic-notifier
```
OR 

You can build a Dcker image on your computer and run :
```
docker build -t epidemic-notifier .

docker run -p 5000:5000 epidemic-notifier
```
Finally, go to your web browser: http://localhost:5000/

#### Screenshots
1. When lauching page in your web browser, you arrive to the log in page. (medec1/medec1) to log in.

![Page index](epidemic_notifier/static/images/00-0-login.PNG)

Then, the home page.

![Page index](epidemic_notifier/static/images/00-accueil.PNG)

2. Tab "Database" where you can reset the database. 

![Page index](epidemic_notifier/static/images/01-db.PNG)

3. Tab "personnes" where you can manage people and ...

![Page index](epidemic_notifier/static/images/03-personne.PNG)

... add relationship between people.

![Page index](epidemic_notifier/static/images/04-personne_relations.png)

... add diagnostic

![Page index](epidemic_notifier/static/images/04-personne_diagnostic.png)

... add consultation

![Page index](epidemic_notifier/static/images/04-personne_consultation.png)

... add life condition

![Page index](epidemic_notifier/static/images/04-personne_condition_vie.png)

... add test

![Page index](epidemic_notifier/static/images/04-04-personne_test.png)

The "guerison" is to set how personne was healed

![Page index](epidemic_notifier/static/images/04-personne_guerison.png)

4. Tab "Graphe personnes" where you visualize relations between all personnes.

![Page index](epidemic_notifier/static/images/05-graph.PNG)

5. Tab "notifications" where you can trigger notifications and an email can be sent to people who have been in contact with a person who has tested positive...

![Page index](epidemic_notifier/static/images/08-notification.PNG)

... and the notification is 

![Page index](epidemic_notifier/static/images/09-notif_email.PNG)

Otherwise, at each notification, files are created in the "__temp__" directory.

![Page index](epidemic_notifier/static/images/10-tree.PNG)

## License & copyright

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details

Set your account less secure
