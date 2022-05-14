# th-forexwExcel

## Set up environment

1. (optional) Run `python3 -m venv env` to create the environment
2. (if 1) Enter the environment with `source env/bin/activate`
3. Install all dependancies with `pip install -r requirements.txt`
4. (needed to execute trades from Excel) Install the `xlwings` Excel add-in using `xlwings addin install`
5. Rename `keys/keys_temp.json` to `keys/keys.json`

## Set up APIs

### IG

1. Log in to account and go to https://www.ig.com/uk/myig/settings/api-keys
2. Generate a new API key
3. Fill in information in `keys/keys.json`

### FXCM

1. Log in to account via https://tradingstation.fxcm.com/
2. Click on username in top right corner.
3. In the drop-down menu, select "API Token"
4. Create the token and copy it to `keys/keys.json`

### IB

1. Download Java: https://www.oracle.com/java/technologies/downloads/#jdk18-mac
2. Download client portal gateway: https://www.interactivebrokers.com/en/index.php?f=5041
3. Launch portal with `bin/run.sh root/conf.yaml` (Mac)
