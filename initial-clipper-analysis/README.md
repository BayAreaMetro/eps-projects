# Clipper Transactions Exploration

The purpose of this analysis is to investigate the interaction of Clipper users between transportation operators. By knowing which operators have high user overlap and the ridership patterns of those shared users, policy decisions may be informed. 

## Data Aggregation

The Clipper transactions database contains over 330 million records per year. For the sake of computation time, we used SQL queries to aggregate the data to the appropriate level before any extensive analysis. The SQL queries used for aggregation are documented [here](https://github.com/BayAreaMetro/usf-practicum/blob/master/clipper-transactions-exploration/SQLqueries.txt).

## Analysis #1: Clipper user overlap between a given operator and other operators

This analysis looks which other operators Clipper users tend to use for two specific operators, BART and Muni. Data was aggregated in SQL then pulled into Tableau for an interactive visual representation. This analysis was performed for one month, November 2016 for illustrative purposes. 

### Results

The black line represents the total Clipper users for each operator for a November 2016. The blue bar represents the proportion of riders shared by the given operators of interest--for the first screenshot below, BART, and for the second screenshot, Muni. The darker the blue, the higher percentage of overlap with other operators. 

* There is a large overlap between BART/ Muni and most other operators
* There is an interesting exception for the Santa Clara operator, VTA, most likely due to geography. It is very far away from San Francisco where BART and Muni are. 
* On the other hand, Napa Solano is just as far here and we see high interaction with BART

![alt text](https://github.com/BayAreaMetro/usf-practicum/blob/master/images/Overlap_BART_selected.png)

![alt text](https://github.com/BayAreaMetro/usf-practicum/blob/master/images/Overlap_Muni_selected.png)

## Analysis #2: BART ridership patterns of Muni user frequency profiles

This analysis investigates how different types of Muni riders are using BART. Data was first aggregated in SQL then pulled into R (script [here](https://github.com/BayAreaMetro/usf-practicum/blob/master/clipper-transactions-exploration/dataExploration.R)) to explore the distribution of how many time Muni users took Muni in a given month. In this case, we explored November 2016 for illustrative purposes. Tableau was used as the final deliverable as an interactive visualization. 

### Results

The histogram shows the distribution of 5 different Muni user groups, from those who use Muni 1-time in a month, to super users (60+ rides in a month). For each of the Muni user types, we plotted their BART ridership patterns by station. In other words, how Muni riders use the Bart system by their frequency profile. If you follow the trend of commonly used BART stations by Muni user type by selecting the different user group radio buttons (sorry! not ideal for a static screenshot), the commonly used BART stations change from downtown for one-time to medium frequency users to Balboa park for high frequency and super users. 

Why do high frequency Muni riders tend to use the Balboa park BART station most frequently? We have a few theories:

* It is the last stop where the Muni/BART A pass work
* There is a University near Balboa park and student usually use transit
* Alternative 14R/ 14X Muni to get from that location into the city are slow so people prefer BART

![alt text](https://github.com/BayAreaMetro/usf-practicum/blob/master/images/FreqMuniRidersInteraction.png)


