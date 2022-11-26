## Auction Website
CSCI 5253 Project

## Development Note
- Don't need to push generated files, only push files containing changes or new files you created to Git, 
- Add comments and explainations in the codes for everybody to understand.

## Install dependencies
This is to install Flask library for python
```
make
```

## Create/Clear database
Our database will be created in instances/ folder based on the schema `schema.sql`
```
make init-db
```

## Run the app
Flask has auto-reloading for debug mode so you don't need to shutdown (Ctr-C) and re-run every time you make changes. When it's running, there might be issue with browser auto-reloading so you need to manually refresh the page (or hit F5) to see your latest changes.
```
make run
```

