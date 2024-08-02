# Personal expense tracking

- [expenses csv](expenses.csv) contains the expense data
- [analysis py](analysis.py) has the python code for analyzing the expense data and present [report](report.html). This takes a date range as input and uses `plotly` to plot an interactive pie chart for the expenses.
- [webapp py](webapp.py) has a `Flask` web app, that provides a date range selector and then shows the spend analysis for that range of date.
- [templates](templates/) has templates for the webpages, required by `Flask`
- [static styles css](static/styles.css) is the css file for visual presentation.
