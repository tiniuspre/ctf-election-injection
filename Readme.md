# CTF Challenge
###### Author: Tinius
###### [@tiniuspre](https://github.com/tiniuspre)

### Level:
Easy-Medium

### Categories:
Web, sql injection

### Source handout:
Yes, app.zip

### Note:
Each user should have their own instance

## Injection
The app is a voting website where you can vote for the next president. The choices are Trump, Harris or Borat.

The injection challenge is about exploiting a vulnerable login form. It consists of two parts,
1. Login as the admin and get access to all the users and their votes. (flag no.1 )
2. Access all the votes and change them so that Borat gets 100% of the election votes. (flag no.2)


## Starting
1. Change flag1 and flag2 in docker-compose.yaml.
2. Run `docker-compose up --build -d` in the root directory.
3. Visit `localhost:8080` in your browser.

### [Intended Solve](Solve.md)