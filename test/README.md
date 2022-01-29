# UStartNow SQL App

## Description

PostgreSQL scaled down version clone application of Udemy. Includes tools such as Docker, Flask, ORM, pgadmin, insomnia

## API Reference

base_url is http://localhost:5000

| Endpoint Path           | Methods   | Parameter |
| -------------           | --------- | --------- |
| base_url/payments       | GET       |           |
| base_url/payments/{:id} | GET       | id        |
| base_url/payments       | POST      |           |
| base_url/payments/{:id} | DELETE    | id        |
| base_url/payments/{:id} | PUT/PATCH | id        |

## Retrospective

* Project started from an ER diagram using draw.io transitioning to database implementation using PostgreSQL.
* ORM was chosen as the course material provided a good guide example to design, implement, and execute
* Future additions would include a graphical data visualization
