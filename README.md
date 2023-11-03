# ChessVerse

## Install

Clone this repo and launch the provided `docker-compose.yml`.  
You first need to setup environment variables: `server-nginx/chessverse.env` and `env/credentials.env` (there's a script for generating random ones).  
We also provide a `chessverse.conf.template` file for a nginx server; note that it contaians some variables: our approach is to use `envsubst` and the env file `chessverse.env`.  
This setup doesn't expose any port, but assumes the use of a proxy server (e.g. nginx), which would communicate with the chessverse containers on the `default` network; change it if you use another network.  

## Project development methods

**Membri del Team:**
- Giuseppe Spathis (PO) - 0001043077
- Luca Gabellini (Dev) - 001020370
- Nico Wu (Dev) - 0001028979
- Francesco Licchelli (Dev) - 0001041426
- Daniele D'Ugo (SM) - 0001027741
- Cono Cirone (Dev) - 0001029785

---

**Descrizione del Progetto:**

L'app Desktop proposta è un ambiente di gioco online che offre l'opportunità di giocare a una o più varianti degli scacchi. Gli utenti hanno la possibilità di sfidarsi in partite, sia contro l'intelligenza artificiale del computer che contro altri giocatori umani. La piattaforma consente agli utenti di cercarsi reciprocamente, concordare le modvalità e i tempi di gioco, nonché salvare e visualizzare i risultati delle partite.

Inoltre, l'app fornirà una classifica generale (leaderboard) per tenere traccia delle prestazioni dei giocatori nel tempo. Sarà possibile collegarsi a social network per commentare le partite, cercare partner e, se desiderato, giocare in modalità "mob". Per quanto riguarda l'accesso ai servizi offerti, la maggior parte sarà riservata ai membri iscritti. Tuttavia, alcuni servizi saranno accessibili anche a non soci.

---

**Sviluppo:**
- Modalità di comunicazione intergruppo: Telegram e Mattermost
- Riunioni Scrum: 3 volte alla settimana
- Linguaggio di Programmazione: Python, javascript
- Database: MySQL
