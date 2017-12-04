# Summarize Bridge Transactions
# Data is obtained from Sylvia Cox as Spreadsheets for 6 month increments.
# Need to investigate how this data is prepared so that I can determine a better path forward for automating the data processing for these metrics.

setwd("~/Box/Fastrak Users")
# setwd("~/Documents/Projects/Fastrak Users")
library(readxl)
library(dplyr)
library(plyr)
library(gsubfn)
library(stringr)
library(tibble)
library(sqldf)
library(tidyr)
library(chron) 
library(data.table)
library(lubridate)
library(anytime)

rm(ForSummary)

# Read in Data for 2015
x2015_Jul <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-JUL")
x2015_Aug <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-AUG")
x2015_Sep <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-Sep")
x2015_Oct <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-Oct")
x2015_Nov <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-Nov")
x2015_Dec <- read_excel("~/Box/Fastrak Users/unprocessed/2015_Jul-Dec.xlsx", sheet = "2015-Dec")

# Read in Data for 2016
x2016_Jan <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-JAN")
x2016_Feb <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-FEB")
x2016_Mar <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-Mar")
x2016_Apr <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-Apr")
x2016_May <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-May")
x2016_Jun <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jan-Jun.xlsx", sheet = "2016-Jun")

x2016_Jul <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jul-Sep.xlsx", sheet = "2016-Jul")
x2016_Aug <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jul-Sep.xlsx", sheet = "2016-Aug")
x2016_Sep <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Jul-Sep.xlsx", sheet = "2016-Sep")
x2016_Oct <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Oct-Dec.xlsx", sheet = "2016-Oct")
x2016_Nov <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Oct-Dec.xlsx", sheet = "2016-Nov")
x2016_Dec <- read_excel("~/Box/Fastrak Users/unprocessed/2016_Oct-Dec.xlsx", sheet = "2016-Dec")
#Fix Columns
x2016_Dec <- x2016_Dec[1:5]

#Read Data for 2017
x2017_Jan <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Jan-Mar.xlsx", sheet = "2017-Jan")
x2017_Feb <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Jan-Mar.xlsx", sheet = "2017-Feb")
x2017_Mar <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Jan-Mar.xlsx", sheet = "2017-Mar")
x2017_Apr <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Apr-Jun.xlsx", sheet = "2017-Apr")
x2017_May <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Apr-Jun.xlsx", sheet = "2017-May")
x2017_Jun <- read_excel("~/Box/Fastrak Users/unprocessed/2017_Apr-Jun.xlsx", sheet = "2017-Jun")

BridgeTransactions <- rbind(x2015_Jul,
                            x2015_Aug,
                            x2015_Sep,
                            x2015_Oct,
                            x2015_Nov,
                            x2015_Dec,
                            x2016_Jan,
                            x2016_Feb,
                            x2016_Mar,
                            x2016_Apr,
                            x2016_May,
                            x2016_Jun,
                            x2016_Jul,
                            x2016_Aug,
                            x2016_Sep,
                            x2016_Oct,
                            x2016_Nov,
                            x2016_Dec,
                            x2017_Jan,
                            x2017_Feb,
                            x2017_Mar,
                            x2017_Apr,
                            x2017_May,
                            x2017_Jun)

#Add Bridge Field to hold Bridge names
BridgeTransactions$Bridge <- NA
# Rename Columns to Match ca_zips
names(BridgeTransactions) <- c("TxnDate", "PlazaAgency","PlazaID","POSTCODE","Count", "Bridge")

# separate(data, col, into, sep = "[^[:alnum:]]+", remove = TRUE,
#          convert = FALSE, extra = "warn", fill = "warn", ...)

# Should fix this so that we convert the values to integers
# See example here: http://tidyr.tidyverse.org/reference/separate.html
# Fix TxnDate Values
BridgeTransactions <- separate(BridgeTransactions, TxnDate, c("xDay", "xMonth", "xYear"), sep="-", remove = FALSE, convert = TRUE)

br <- sqldf("select Distinct xMonth From BridgeTransactions")
brbad <- subset(BridgeTransactions, is.na(xMonth)) 
brgood <- subset(BridgeTransactions, !is.na(xMonth)) 
brbad$TxnDate <- as.character(structure(brbad$TxnDate, class = c("POSIXct", "POSIXt")))
brbad<- separate(brbad, TxnDate, c("yr", "mon", "dy"), sep="-", remove = FALSE, convert = TRUE)
brbad$dy <- substr(brbad$dy,1,2)
brbad$xYear <- brbad$yr
brbad$xMonth <-brbad$mon
brbad$xDay <- as.integer(brbad$dy)
brbad$TxnDate <- as.Date( paste(brbad$xYear, brbad$xMonth, brbad$xDay  ,   sep = "-" )  , format = "%Y-%m-%d" )
brbad <- brbad[,-c(2,3,4)]

brgood$xMonth <- match(brgood$xMonth,month.abb)
brgood$xDay <- as.integer(brgood$xDay)
brgood$TxnDate <-as.Date( paste(brgood$xYear, brgood$xMonth,brgood$xDay  ,   sep = "-" )  , format = "%Y-%m-%d" )
BridgeTransactions <- rbind(brbad, brgood)

# Remove uneeded DFs
rm(x2015_Jul,
x2015_Aug,
x2015_Sep,
x2015_Oct,
x2015_Nov,
x2015_Dec,
x2016_Jan,
x2016_Feb,
x2016_Mar,
x2016_Apr,
x2016_May,
x2016_Jun,
x2016_Jul,
x2016_Aug,
x2016_Sep,
x2016_Oct,
x2016_Nov,
x2016_Dec,
x2017_Jan,
x2017_Feb,
x2017_Mar,
x2017_Apr,
x2017_May,
x2017_Jun,
brbad, brgood)


# import ca_zips into environment
us_zips <- read.csv2("processed/zcta_county_rel_10.csv", header = TRUE, sep = ",")
us_zips <- us_zips[1:3]
us_zips <- as_data_frame(us_zips)
# Some zip codes cross county boundaries. There are 253 duplicate records in this view.  This removes the duplicates
us_zips <- us_zips[!duplicated(us_zips$ZCTA5), ]
names(us_zips) <- c("POSTCODE","State","County")
#reorder fields
ca_zips <- sqldf("select POSTCODE, County, State from us_zips where State = 6")
rm(us_zips)
#Rename BridgeID
# 02- Antioch
# 03- Richmond San Rafael
# 04- San Francisco Oakland Bay Bridge
# 05 – San Mateo Hayward
# 06 - Dumbarton
# 07- Carquinez
# 08 – Benicia Martinez
# 49 – Golden Gate Bridge

BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 2] <- "Antioch Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 3] <- "Richmond San Rafael Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 4] <- "San Francisco Oakland Bay Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 5] <- "San Mateo Hayward Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 6] <- "Dumbarton Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 7] <- "Carquinez Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 8] <- "Benicia Martinez Bridge"
BridgeTransactions$Bridge[BridgeTransactions$PlazaID == 49] <- "Golden Gate Bridge"


# Same as Reduce Function
#Total Transactions are 1646462
TransactionsByBridgeByZipByCounty <- merge(BridgeTransactions, ca_zips, by="POSTCODE") #1606369 
rm(BridgeTransactions)
rm(br2, badrecords, br, brbad, brgood)
# Select only zipcode records from California
CaliforniaTransactions <- sqldf("select xDay, xMonth, xYear, TxnDate, Bridge, PlazaAgency, POSTCODE, Count, 'Unclassified' as NAME, County from TransactionsByBridgeByZipByCounty Order by TxnDate, Bridge, PlazaAgency, POSTCODE, Count, County")


#In Region
InRegion <- sqldf("select * from CaliforniaTransactions where County in (1,13,41,55,75,81,85,95,97)")
#Update County Names
InRegion %>% 
  mutate(NAME = ifelse(County == 1, "Alameda", NAME)) %>%
  mutate(NAME = ifelse(County == 13, "Contra Costa", NAME)) %>%
  mutate(NAME = ifelse(County == 41, "Marin", NAME)) %>%
  mutate(NAME = ifelse(County == 55, "Napa", NAME)) %>%
  mutate(NAME = ifelse(County == 75, "San Francisco", NAME)) %>%
  mutate(NAME = ifelse(County == 81, "San Mateo", NAME)) %>%
  mutate(NAME = ifelse(County == 85, "Santa Clara", NAME)) %>%
  mutate(NAME = ifelse(County == 95, "Solano", NAME)) %>%
  mutate(NAME = ifelse(County == 97, "Sonoma", NAME))-> InRegion
#Out of Region
OutRegion <- sqldf("select * from CaliforniaTransactions where County not in (1,13,41,55,75,81,85,95,97)")
# Update County Names to Out of Region
OutRegion$NAME <- "Out of Region"
ForSummary <- rbind(InRegion, OutRegion)

ForSummary <- sqldf("select xYear, xMonth, XDay, TxnDate, Bridge, PlazaAgency, POSTCODE, Count, NAME, County as CountyFIP from ForSummary")

###add FY 

ForSummary <- ForSummary %>%
  mutate(FY = case_when(TxnDate >= as.Date("2015-07-01") & TxnDate < as.Date("2016-07-01")~ "FY 15/16",
                         TxnDate >= as.Date("2016-07-01") & TxnDate < as.Date("2017-07-01")~ "FY 16/17"))%>%
  mutate(xWeekday = weekdays(as.Date(TxnDate)))


#Cleanup Data
rm(InRegion,OutRegion,TransactionsByBridgeByZipByCounty,CaliforniaTransactions,ca_zips)

# Export Summary
setwd("~/Box/Fastrak Users/processed/")
write.csv(ForSummary, file="FT_trans_by_month.csv")

SummaryByBridgeByZipByCounty <- aggregate(list(ForSummary$Count), by = list(ForSummary$NAME, ForSummary$POSTCODE, ForSummary$Bridge), sum)
names(SummaryByBridgeByZipByCounty) <- c("County","ZipCode","Bridge","TotalTransactions")

SummaryByWeekdayByBridgeByCounty <- aggregate(list(ForSummary$Count), by = list(ForSummary$TxnDate, ForSummary$NAME, ForSummary$Bridge), sum)
names(SummaryByWeekdayByBridgeByCounty) <- c("WeekdayYear", "County","Bridge","TotalTransactions")

SummaryByBridgeByCounty <- aggregate(list(ForSummary$Count), by = list(ForSummary$NAME, ForSummary$Bridge), sum)
names(SummaryByBridgeByCounty) <- c("County","Bridge","TotalTransactions")

# rm(a)

write.csv(SummaryByBridgeByCounty, file="SummaryByBridgeByCounty.csv")
write.csv(SummaryByBridgeByZipByCounty, file="SummaryByBridgeByCountyByZip.csv")
write.csv(SummaryByWeekdayByBridgeByCounty, file="SummaryByWeekdayByBridgeByCounty.csv")

