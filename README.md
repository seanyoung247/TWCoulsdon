![TWC Logo](design/images/twc_title.png)
# TWCoulsdon

Invented in 1970, this leading amateur theatre company reinvents itself with every
show from Shakespeare to pantomime.

TWCoulsdon is a website for the Theatre Workshop Coulsdon amateur dramatics group,
intended to replace the group's [current online presence](https://twcoulsdon.org.uk/)
with a new modern web application. It also aims to reduce the groups reliance on
third-party ticketing platforms by moving online ticket sales in-house. This
should give a more seamless end-user experience, while also improving the efficiency
of the box-office and reporting.

## Table of Contents

<TBC>

## User Experience

### Project Goals

### User Stories

**User classes:**

- Site User - General user
- Audience - A user wishing to attend shows/events
- Box Office - Front of house
- Admin - Site super user

<table>
  <tr>
    <th>STORY ID</th>
    <th>AS A</th>
    <th>I WANT TO BE ABLE TO</th>
    <th>SO THAT I CAN</th>
  </tr>

  <tr>
    <td colspan="4"><b>Viewing and Navigation</b></td>
  </tr>
    <tr>
      <td>US101</td>
      <td>Audience</td>
      <td>View a list of current and upcoming events/shows</td>
      <td>Select those I might want to go to</td>
    </tr>
    <tr>
      <td>US102</td>
      <td>Audience</td>
      <td>View individual show details</td>
      <td>Learn about the show and decide if I want to see it</td>
    </tr>
    <tr>
      <td>US103</td>
      <td>Audience</td>
      <td>View my purchases</td>
      <td>Ensure I don't miss a performance I've paid for</td>
    </tr>
    <tr>
      <td>US104</td>
      <td>Site User</td>
      <td>View categories of content</td>
      <td>So I can learn more about the group</td>
    </tr>
  <tr>
    <td colspan="4"><b>Registration and User Accounts</b></td>
  </tr>
    <tr>
      <td>US201</td>
      <td>Site User</td>
      <td>Register for an account</td>
      <td>Have a personalised account and be able to access restricted areas of the site based on my role</td>
    </tr>
    <tr>
      <td>US202</td>
      <td>Site User</td>
      <td>Login or logout</td>
      <td>Access my account, restricted areas of the site and keep my account secure</td>
    </tr>
    <tr>
      <td>US203</td>
      <td>Site User</td>
      <td>Reset my password</td>
      <td>To improve security of my account and recover access if I forget my password</td>
    </tr>
    <tr>
      <td>US204</td>
      <td>Site User</td>
      <td>Have a personalised user profile</td>
      <td>View my interactions and history with the group and save my payment information</td>
    </tr>
  <tr>
    <td colspan="4"><b>Sorting and Searching</b></td>
  </tr>
    <tr>
      <td>US301</td>
      <td>Audience</td>
      <td>Search by name or description</td>
      <td>Find a show or event that has been advertised elsewhere</td>
    </tr>
    <tr>
      <td>US302</td>
      <td>Audience</td>
      <td>Search by date</td>
      <td>Find a show or event occurring within a range of dates</td>
    </tr>
    <tr>
      <td>US303</td>
      <td>Audience</td>
      <td>See what I've searched for and the number of results</td>
      <td>Quickly find what I'm looking for</td>
    </tr>
  <tr>
    <td colspan="4"><b>Purchasing and Checkout</b></td>
  </tr>
    <tr>
      <td>US401</td>
      <td>Audience</td>
      <td>Easily select the number and type of tickets when purchasing them</td>
      <td>Ensure I don't select the wrong tickets</td>
    </tr>
    <tr>
      <td>US402</td>
      <td>Audience</td>
      <td>View the tickets and their types prior in my bag</td>
      <td>Identify the total cost of my tickets and what I will receive</td>
    </tr>
    <tr>
      <td>US403</td>
      <td>Audience</td>
      <td>Adjust the quantity and type of individual tickets in my bag</td>
      <td>Easily make changes to my purchase before checkout</td>
    </tr>
    <tr>
      <td>US404</td>
      <td>Audience</td>
      <td>Easily enter my payment information</td>
      <td>Check out quickly and with no hassles</td>
    </tr>
    <tr>
      <td>US405</td>
      <td>Audience</td>
      <td>Feel my personal and payment information is safe and secure</td>
      <td>Confidently provide the needed information to make a purchase</td>
    </tr>
    <tr>
      <td>US406</td>
      <td>Audience</td>
      <td>View an order confirmation after checkout</td>
      <td>verify the I haven’t made any mistakes and receive my tickets</td>
    </tr>
    <tr>
      <td>US407</td>
      <td>Audience</td>
      <td>Receive and email confirmation after checking out</td>
      <td>Keep the confirmation of what I’ve purchased for my records</td>
    </tr>
  <tr>
    <td colspan="4"><b>Ticketing and reports</b></td>
  </tr>
    <tr>
      <td>US501</td>
      <td>Audience</td>
      <td>Immediately receive my tickets through email/browser</td>
      <td>Save and print them to ensure I can't lose them</td>
    </tr>
    <tr>
      <td>US502</td>
      <td>Box Office</td>
      <td>Get reports on tickets sold by show</td>
      <td>See the total show attendance</td>
    </tr>
    <tr>
      <td>US503</td>
      <td>Box Office</td>
      <td>Get reports on tickets sold by performance</td>
      <td>See patterns, plan attendance and know when a show is sold out</td>
    </tr>
    <tr>
      <td>US504</td>
      <td>Box Office</td>
      <td>Search for individual tickets by name or unique id</td>
      <td>Verify ticket authenticity</td>
    </tr>
  <tr>
    <td colspan="4"><b>Admin and content Management</b></td>
  </tr>
    <tr>
      <td>US601</td>
      <td>Admin</td>
      <td>Add content or show</td>
      <td>Add new shows and content for site users and audiences</td>
    </tr>
    <tr>
      <td>US602</td>
      <td>Admin</td>
      <td>Edit/Update content or shows</td>
      <td>Update descriptions, images, dates and other criteria</td>
    </tr>
    <tr>
      <td>US603</td>
      <td>Admin</td>
      <td>Delete content</td>
      <td>Remove expired content</td>
    </tr>
</table>

## Design

### Database
![TWCoulsdon Entity Relationship Diagram](design/database/twcoulsdon_erd.png)

### Fonts
[Anton](https://fonts.google.com/specimen/Anton?query=Anton) was chosen as the
main title font as it is similar to the group's existing logo branding.
[Roboto](https://fonts.google.com/specimen/Roboto?query=Roboto) was chosen for
the main content font as it is easy to read, matches the overall styling and
compliments Anton well. Roboto also has a wide range of styles giving extra
options for styling and drawing attention to important text.

### Colours

Colours were largely chosen based on the group's existing brand. Rich black and
white are the primary background and foreground colours for content, with cultured
grey as a more general background colour. Tart Orange is the groups main brand
colour, and cobalt blue was chosen as a highlight to complement this. Further, the
group also uses accent colours on a per-show basis that can be incorporated on
show pages.

![pallet](design/images/pallet/pallet.png)

- Tart Orange (#FF3333) - Main site brand colour
- Cobalt Blue (#1B48A1) - Site accent colour
- Rich Black (#14161A) - Content foreground/background
- White (#FFFFFF) - Content background/foreground
- Cultured Grey (#EBEDF0) - General page background

### Layout

<discussing of existing website here>

#### Landing Page

The landing page is used to briefly showcase the group and it's upcoming events.
Full screen images are shown in a carousel to be attention grabbing and pull users
in to other areas of the site.

##### Wireframes
<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/landing_page/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/landing_page/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/landing_page/desktop.png)

</details>

#### Events List

The Event list page lists events based on their type or search criteria. The list
is paginated in a show more style, with the next/current event at the top
followed by past events by default.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/events_list/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/events_list/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/events_list/desktop.png)

</details>

#### Event Page

The event page shows information for individual events. These include past, present
and upcoming events. For current and upcoming events the event page will allow
users to buy tickets. Above the fold a fullscreen title image is displayed with
the page contents below.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

<h6>Above the fold</h6>

![Landing Page Phone Layout](design/wireframes/event_page/title_phone.png)

<h6>Below the fold</h6>

![Landing Page Desktop Layout](design/wireframes/event_page/content_phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

<h6>Above the fold</h6>

![Landing Page Tablet Layout](design/wireframes/event_page/title_tablet.png)

<h6>Below the fold</h6>

![Landing Page Desktop Layout](design/wireframes/event_page/content_tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

<h6>Above the fold</h6>

![Landing Page Desktop Layout](design/wireframes/event_page/title_desktop.png)

<h6>Below the fold</h6>

![Landing Page Desktop Layout](design/wireframes/event_page/content_desktop.png)

</details>

#### Venue Page

The venue page presents basic information on an event location, including it's
address and contact information.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/venue_page/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/venue_page/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/venue_page/desktop.png)

</details>

#### Information Pages

Various pages providing information on the group. May be expanded to also provide blog like functionality if required later.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/information_page/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/information_page/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/information_page/desktop.png)

</details>

#### Add Tickets Modal

Tickets are added through a modal dialogue that allows adding multiple tickets of
different types and dates for a single event to the basket.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/add_to_basket/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/add_to_basket/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/add_to_basket/desktop.png)

</details>

#### Basket

The basket page gives access to the currently selected tickets before purchase
and provides tools to edit items and quantities.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/basket/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/basket/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/basket/desktop.png)

</details>

#### Ticket Validation

The ticket validation is a simple report to confirm a ticket's face value conforms
to the information held on the database. The check order button will only be available
logged in staff members.

##### Wireframes

<details>
<summary><b>Phone</b></summary>

![Landing Page Phone Layout](design/wireframes/ticket_validation/phone.png)

</details>

<details>
<summary><b>Tablet</b></summary>

![Landing Page Tablet Layout](design/wireframes/ticket_validation/tablet.png)

</details>

<details>
<summary><b>Desktop</b></summary>

![Landing Page Desktop Layout](design/wireframes/ticket_validation/desktop.png)

</details>

<details>
<summary><b>Expired tickets</b></summary>

![Landing Page Desktop Layout](design/wireframes/ticket_validation/invalid.png)

</details>



## Features

### Existing Features

### Future Features

## Technologies

### Site architecture

#### Core app

The core app defines a few basic functions and models used throughout the site
that don't fit anywhere else.

#### Home app

Provides models and views for the landing and group information pages.

* Landing page
* About page
* Contact page

#### Events app

Provides models and pages for event and venue information

* Events list
* Event page
* Venue page

#### Profiles app

Provides models and pages for user information and profiles.

* User profile page

#### Box Office app

Provides models and pages for buying tickets, checking their validity and generating show attendence reports.

* Shopping bag
* Checkout
* Show attendence and ticketing reports

### Languages
- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
  - Used as the markup language for the site layout.
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
  - Used to style and colour HTML and dynamic elements.
  - CSS2 is used for generating pdf files.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
  - Used to create and manipulate the site's client-side dynamic elements. Also
  performs AJAX requests for client/server communication.
- [Python](https://www.python.org/)
  - Used for the backend server and running queries to the database.
- [Django Templating Language](https://docs.djangoproject.com/en/3.2/ref/templates/language/)
  - Used to generate HTML from site templates
- [SVG](https://developer.mozilla.org/en-US/docs/Glossary/SVG)
  - Used to define a number of the sites icons and graphical elements.
  - Also used for the site favicon where supported. This allows infinite scalability
  and the use of advanced features, such as automatically changing colours based
  on user theme:
  - ![Favicon](design/images/favicon.png)

### Libraries
- [Django](https://www.djangoproject.com/)
  - The project uses the django web framework to support advanced web server task.
- [JQuery](https://jquery.com)
  - The project uses JQuery to simplify DOM manipulation.
- [Bootstrap](https://getbootstrap.com/)
  - The project uses Bootstrap to aid in responsive design and to provide a number
  of frontend components.
- [Easy Thumbnails](https://pypi.org/project/easy-thumbnails/)
  - Easy Thumbnails is used to automatically generate thumbnails for gallery image.
- [Segno](https://pypi.org/project/segno/)
  - Segno is used to generate QR Codes for ticket validation.
- [django-embed-video](https://pypi.org/project/django-embed-video/)
  - Used to simplify youtube video embedding within django templates.
- [Tinymce](https://www.tiny.cloud/)
  - Used to provide rich text input.
- [WeasyPrint](https://weasyprint.org/)
  - Used to generate pdf files from Django html templates for tickets and reporting.

### Editors
- [Atom](https://atom.io/)
  - Atom was used to write HTML/CSS, Javascript and Python code. It was also use
  to build the readme and testing markdown documentation.
- [dbdiagram](https://dbdiagram.io/home)
  - Used to create Entity Relationship Diagrams of the database.
- [Adobe Photoshop](https://www.adobe.com/products/photoshop.html)
  - Used to create some of the image files used on the site.
- [Adobe Illustrator](https://www.adobe.com/products/illustrator.html)
  - Used to create some of the images and icons used on the site.
- [Inkscape](https://inkscape.org/)
  - Used to produce some svg images and icons.
- [whimsical](https://whimsical.com/)
  - Used to produce the projects wireframes.

### Tools
- [Git](https://git-scm.com/)
  - Used for version control and synchronising local and remote repositories.
- [Coolors](https://coolors.co/)
  - Used to help define the site colour scheme.
- [Autoprefixer](https://autoprefixer.github.io/)
  - Used to ensure backwards CSS compatibility with legacy browsers.

### Platforms
- [Heroku](https://www.heroku.com/platform)
  - The project uses Heroku as it's deployment platform.
- [Amazon S3](https://aws.amazon.com/free/)
  - Used to store site static and media files.
- [Youtube](https://www.youtube.com/)
  - Used for video content.
- [Github](https://github.com/)
  - Used for source control.

## Testing
Information on testing can be found in [TESTING.md](TESTING.md)

## Source Control
The website was developed using the Atom editor with git and github for version control.

New changes to the local copy can be added to the remote repository by first adding:

`git add .`

Committing the changes to local version control:

`git commit -m "<commit message>"`

And pushing them to the remote repository:

`git push`

### Branches

Branches were used to add and develop new features for testing without affecting the main branch and deployed application.

#### Creating a branch

A branch can be created and selected in one operation with:

`git checkout -b <branch name>`

#### Selecting a branch

Switching to an already created branch can be done by:

`git checkout <branch name>`

#### Merging a branch

For merging the commits of one branch to another (for instance when merging a completed development branch to main):

1. Checkout branch to merge into:

   `git checkout <destination branch>`

2. Merge source branch into destination:

   `git merge <source branch>`

#### Deleting a branch

1. Ensure you are not on the branch you want to delete by selecting another

2. Delete the branch locally:

  `git branch - <local branch name>`

3. Delete the branch remotely:

  `git push origin --delete <remote branch name>`

## Deployment

### Database Deployment

Django will do most of the work of preparing and setting up the database through
'migrations'.

To update the database to the latest models, from the project root:
1. First generate the python migration scripts:

  `python3 manage.py makemigrations`

2. Then run the scripts and update the database:

  `python3 manage.py migrate`

### Local Deployment

To deploy the project locally first clone the github repository to a local directory:

- Navigate to the project's github repository (https://github.com/seanyoung247/TWCoulsdon)
- Select the "Code" button above the file listing
  - Select download Zip
- unzip the file to a local directory

#### Python Environment

After cloning the repository the python environment needs to be set up. Ensure python3 is installed and is version 3.8.6 minimum with the command:
`python3 --version`

You will then need to create a virtual environment:
From the projects local root directory run the following command:

`python3 -m venv .`

To activate the virtual environment use the command:

`source bin/activate`

Once the virtual environment is activated the project's python prerequists can be installed with:

`pip3 install -r requirements.txt`

Database migrations should now be run as outlined above.

Once finished working, or if the virtual environment needs to be restarted (for instance if environment varibles have change and need to be reloaded) deactivate by typing:

`deactivate`

#### Environment Variables

The project is configured through various environment variables.

Required variables:

- SECRET_KEY
  - Defines the Django secret key. A helper script has been provided to generate new keys, and can be run by running: `python3 gen_secret_key.py` from the project root.

Optional variables:

- RESULTS_PER_PAGE
  - Defines how many search results should be returned. Ideally multiples of 6, defaults to 12 if not supplied.


- TICKET_CUT_OFF_HOURS
  - How many hours before a performance that tickets will stop being sold. Defaults to 2

Testing variables (should not be set in production):

- DEFAULT_FROM_EMAIL
  - Defines a test email account


- DEVELOPMENT
  - If set puts the project into debug mode.


- TEST_IP
  - Should be set to the IP address of the testing machine. When the server is run with the command: `python3 manage.py runserver 0:8000` other devices on the local network will be able to connect to the site via this address for testing.

Deployment variables:

- EMAIL_HOST
  - The smtp address of the email service provider


- EMAIL_HOST_USER
  - Email username


- EMAIL_HOST_PASS
  - Email password


- DATABASE_URL
  - The URL of the remote database

- USE_AWS
  - If set the project will attempt to use Amazon S3 for static and media file storage.

If using Amazon S3 the following variables will need to be set:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- AWS_S3_REGION_NAME

The suggested method for defining environment variables for local development is with a shell script. Variables can be set with the export command:
`export <key>=<value>` and unset with: `unset <key>`. This can be done automatically when activating and deactivating the python virtual environment. The environment variables can be set within a script with the following template:
```
env_start() {
  <exports here>
}
env_stop() {
  <unsets here>
}
```
Saved to the project root with the filename .env. This can be added to the virtual environment activation by adding the following code to bin/activate:
```
. .env

deactivate () {

...

    # Unset environment
    env_stop
}

...

# Set environment variables
env_start
```

### Remote Deployment

The site is deployed to Heroku at: https://twcoulsdon.herokuapp.com/

Creating the required deployment files in the repository:

- requirements.txt
  - Lists the required python modules for Heroku to install on deployment.
  - To create
    - from the project root directory type:
    - `pip3 freeze > requirements.txt`
- Procfile
  - Tells heroku what command to use to start the app.
  - To create
    - Type the following command into the project root directory:
    - `echo web: gunicorn TWCoulsdon.wsgi:application`
- slugignore (optional)
  - Lists files and directories that shouldn't be deployed to the live app, like testing and development files. Uses a similar syntax to .gitignore.
  - Create a text file.
    - List the files and directories to be excluded from the live deployment
    - Save to the project root directory as ".slugignore"

### Creating a Heroku app

From the Heroku dashboard:

- Select "New"

  - Select "Create new app"

  ![Create Heroku app step one](design/images/docs/new_heroku_app.png)

- Add new app details to form

  - Add app name
  - Select region
  - Click create app

  ![Create Heroku app step 2](design/images/docs/new_heroku_app2.png)

### Setting Environment variables

From the Heroku dashboard:

- Select the app from the list
- Select "Settings" from the menu
  - From the settings menu select "Reveal Config Vars"
  - Add environment variables in key value pairs
  - Click "Add" to add each key/value pair

### Creating the database

Creating the database:

- Select the app from the list
- Select "Resources" from the menu
  - In the addons section select the search bar
  - Type: "Postgres" and select Heroku Postgres
    - From the order form select "submit order form"

The Heroku environment variables will now include a DATABASE_URL which can be used to connect to the remote database.

The site sets itself up automatically for local or remote deployment based on enviroment variables. So migrations can be run locally against the remote database
by ensuring the DATABASE_URL variable is set in the local environment and running
migrations as outlined above. Data from the local database can be uploaded remotely by running the following command before defining DATABASE_URL:

`python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json`

This can then be uploaded to the remote database after defining the DATABASE_URL by:

`python3 manage.py loaddata db.json`
