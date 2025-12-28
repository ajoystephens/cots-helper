# Circle of the Shepherd Helper Tool
This is a small helper tool that I use to manage my summoned creatures when playing a Circle of the Shepherd druid. It allows you to quickly summon creatures and perform bulk actions like attacking and adding temporary HP. 


## Setup & Run Locally

> [!NOTE]
> This was written using `Python 3.11.3`. I have not tested it with other versions.

Setup your virtual environment and install the required libraries.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the app:
```
streamlit run shepherd.py
```

> [!TIP]
> If you find the above instructions confusing, you can see some more detailed instructions [here](https://docs.google.com/document/d/1M1-WOCFkEJIbO3SpWQ3fq_LtFIVcFFwyWz37AD7-iC0/edit?usp=sharing).



## TODO
* [x] add flanking
* [ ] add conjure woodland beings
* [ ] add conjure fey
* [ ] add more creatures
* [x] create settings page
* [x] settings page: mighty summoner default
* [x] settings page: flanking rule options
* [ ] settings page: crit rule options (also ask james about campaign crit rules)
* [x] settings page: creature select
* [ ] pin requirements file
* [ ] add more detailed less techy instructions
* [ ] consider multiattack (ex. Polar Bear)