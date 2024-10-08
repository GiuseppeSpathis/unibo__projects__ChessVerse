# ChessVerse

University project for Software Engineering 2023-2024, at the University of Bologna. An online ReallyBadChess game.

## Installation

Clone this repository and launch the provided `docker-compose.yml`.  
First, you need to set up the environment variables: `server-nginx/chessverse.env`, `env/credentials.env` (a script is provided for generating random values), and `.env`.  
We also provide a `chessverse.conf.template` file for an Nginx server. Note that it contains some variables; our approach is to use `envsubst` with the environment file `chessverse.env`.  
This setup does not expose any port, assuming the use of a proxy server (e.g., Nginx), which will communicate with the chessverse containers on the `default` network. You can modify this if you are using a different network.

## Documentation

We strive to keep the documentation clear, consistent, and up-to-date at all times so that both our team and anyone looking at our project can understand it—or at least its structure—despite the large number of files and services.  
All documentation is located in the `doc/` folder.

Here are the main points and paths regarding it:

* Schemas:
  - `infrastructure.drawio`
  - `mockup*.jpg`
  - `repository-structure.md`
  - `schema*.jpg`
* Agile Definitions:
  - `definitions.md`
* Folders containing sprints information:
  - `backlogs`
  - `goals`
  - `retrospective`
  - `review`
  - `slides`
* Project and Development:
  - `code`: actual code documentation
  - `workflow`: conventions about our development process

## Project Development Methods

**Team Members:**
- Giuseppe Spathis (PO) - 0001043077
- Luca Gabellini (SM) - 001020370
- Nico Wu (Dev) - 0001028979
- Francesco Licchelli (Dev) - 0001041426
- Daniele D'Ugo (Dev) - 0001027741
- Cono Cirone (Dev) - 0001029785

---

**Project Description:**

The proposed website is an online gaming platform offering the opportunity to play one or more chess variants. Users can challenge each other to matches, either against the computer's AI or other human players. The platform allows users to search for opponents, agree on game settings and times, and save and view match results.

Additionally, the app will feature a general leaderboard to track player performance over time. Users will have the option to connect with social networks to comment on games, search for partners, and, if desired, play in "mob" mode. Most services will be available only to registered members, although some will also be accessible to non-members.

---

**Development:**
- Intergroup communication methods: Telegram and Mattermost
- Scrum meetings: 3 times a week
- Programming languages: Python, JavaScript
- Database: MySQL
