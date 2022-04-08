# Robert_J_assesement_code
## Ukraine analysis

### To produce visualisations:

1) Clone the repo: git clone git@github.com:robertjohnson2/Robert_J_assesement_code.git
2) Install requirements: pip install -r requirements.txt
3) Go to https://commodities-api.com/ create an account (very quick) and save the API key as COMMODITIES_ACCESS_KEY as an environment variable.
4) Run create_data.py to create local datasets from API 
5) Run make_commodity_plot.py to create plots - some data is in the data folder if you cannot gain access to API 

There are limited monthly free API requests which is why data is saved locally.
