## Auction Website
CSCI 5253 Project

## Development Note
- We will keep track of our work [here](https://www.notion.so/invite/980fba7436651721cf51f072c6f90dd0cfde70d3)
- Don't need to push generated files, only push files containing changes or new files you created to Git, 
- Add comments and explainations in the codes for everybody to understand.

## Install dependencies
This is to install Flask library for python
```
$ make
```

## Create/Clear database
Our database will be created in instances/ folder based on the schema `schema.sql`
```
$ make init-db
```

## Run the app
Flask has auto-reloading for debug mode so you don't need to shutdown (Ctr-C) and re-run every time you make changes. When it's running, there might be issue with browser auto-reloading so you need to manually refresh the page (or hit F5) to see your latest changes.
```
$ make run
```

## Run unit test
All unit tests are stored in tests/ folder
```
$ pip install '.[test]'
$ pytest
```

## Test Images url links (free img sourced = https://unsplash.com/s/photos/object)
cacutus - https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8b2JqZWN0fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60
old school phone - https://images.unsplash.com/photo-1557180295-76eee20ae8aa?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8b2JqZWN0fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60
rustic pen - https://images.unsplash.com/photo-1518674660708-0e2c0473e68e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTJ8fG9iamVjdHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60
stool - https://images.unsplash.com/photo-1503602642458-232111445657?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fG9iamVjdHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60

