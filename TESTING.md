# Testing

[README.md](README.md)

## Contents

- [Automated Testing](#Automated-Testing)
  - [Validation](#Validation)
  - [Python unit tests](#Python-unit-tests)
- [Manual Testing](#Manual-Testing)
  - [Testing Environments](#Testing-Environments)
  - [Testing Methodology](#Testing-Methodology)
  - [Unit Testing](#Unit-Testing)
  - [Peer Code Review](#Peer-Code-Review)
  - [Student Checklist](#Student-Checklist)
- [Solved Issues](#Solved-Issues)

## Automated Testing

### Validation

Generated **HTML** and **CSS** code were validated with the W3C Markup and CSS validators. Both were found to have no errors or warnings. Reports can be seen below:

<details>
<summary><b>HTML</b></summary>

</details>

<details>
<summary><b>CSS</b></summary>

</details>

**JavaScript** code was run through [JSHint](https://jshint.com/) to ensure they were syntactically correct. Any errors were corrected and linting re-run until correct.

Pylint was used to verify **Python** code. Any errors were corrected and re-run until correct. Reports can be seen below:


<details>

<summary>Google Chrome's <b>lighthouse</b> was also run and provided the following reports:</summary>

</details>

### Python unit tests

Automated unit tests were created to ensure correct functioning of various components. These include the app database models,
To perform automated testing, from the project root directory type:
`>python3 manage.py test`

## Manual Testing

### Testing Environments

Primary iterative testing was undertaken on a Linux desktop machine with the Firefox browser. Once a feature was considered complete it was tested in other environments.

**Desktop testing**

- Platforms:
  - Custom Desktop (Windows 10, Ubuntu 20.10)
  - Microsoft SurfaceBook 2 (Windows 10)
  - Apple MacBook Air M1 (macOS Big Sur 11.2.3)
- Browsers:
  - Google Chrome/Chromium
  - Microsoft Edge
  - Firefox
  - Opera
  - Safari

**Tablet testing**

- Platforms:
  - Lenovo Tab M10 (Android 10)
- Browsers:
  - Google Chrome
  - Firefox
  - Opera

**Mobile testing**

- Platforms:
  - OnePlus7 (Android 11)
  - Samsung Galaxy J6 (Android 10)
- Browsers:
  - Chrome
  - FireFox
  - Opera

### Testing Methodology

Code changes were tested prior to committing and pushing to github on the local machine. This was in an attempt to prevent faulty or broken code from being pushed to the repository or deployed to the live site. Further, new features were pushed to a separate branch, which wasn't merged to main and deployed to the live site until tested. On occasions where bugs were missed in testing an issue was opened on github if appropriate. Issues were not raised for bugs arising from known feature incomplete code committed to github, as this information was captured in the coding to-do lists. This approach kept most bugs from being uploaded, with only a few cases of bugs either too complex to be fixed for the current release, or those that introduced regressions in existing code being uploaded.

### Unit Testing

Manual unit testing was conducted iteratively by attempting to "break" new code. In this way most bugs were caught and fixed before committing to the repository and live site.

The python print() and JavaScript console.log functions were used to output variable values and breakpoints during development to give hints to where faults were occurring and why.

Final UI testing was conducted prior to submission to confirm the UI fulfilled the required user stories:

### Peer Code Review

The project was submitted for peer review on the code institute slack [channel]().

### Student Checklist

A Final sanity check was done with the student check list to ensure the site fits submission guidelines.

## Solved Issues

## Known Issues
