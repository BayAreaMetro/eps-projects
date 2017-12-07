####Clipper Transaction Exploration####

#libraries used
library(dplyr)
library(RPostgreSQL)
library(data.table)
library(tidyr)
library(chron) 
library(optmatch)

#connecting to Redshift database
drv <- dbDriver("PostgreSQL")
conn <- dbConnect(drv, 
                  host="****", 
                  port="****",
                  dbname="****",
                  user="****", 
                  password="****")

#send query to Redshift and retrive result
df_muni <- dbGetQuery(conn, 'select * from "clipper"."rpt-munifrequency" order by applicationserialnumber asc')

#getting rid of the outliers
df_muni <- subset(df_muni, df_muni$num <= 200)

#creating a histogram of the frequency of Muni Ridership
hist(df_muni$num, breaks = 500, xlab = "Number of Rides Taken in November 2016", ylab = "Frequency", main = "Muni Ridership Frequency (November 2016)")

#running a query from Redshift that will contain the Origin Location and Destination location per Clipper Number for November 2016
df_origin <- dbGetQuery(conn, 
                        'select originlocation, destinationlocation, applicationserialnumber 
                        from "clipper"."sfofaretransaction" 
                        where applicationserialnumber in 
                        (select distinct applicationserialnumber 
                        from "clipper"."sfofaretransaction" 
                        where operatorid = 18 and date_part("year", starttime) = 2016 and date_part("month", starttime) = 11) 
                        and date_part("year", starttime) = 2016 and date_part("month", starttime) = 11 and operatorid = 4')

#joining the two tables together on Clipper Number 
df_bart_muni <- inner_join(df_origin,df_muni,by = "applicationserialnumber")

#getting rid of unknown Destination Location which corresponds to 65535
df <- df_bart_muni[-grep(65535,df_bart_muni$destinationlocation),]

#creating different dataframes for each of the 5 user groups
one_time <- as.data.frame(subset(df, df$num < 2))
low_freq <- as.data.frame(subset(df, df$num > 1 & df$num <= 4))
med_freq <- as.data.frame(subset(df, df$num > 4 & df$num <= 35))
high_freq <- as.data.frame(subset(df, df$num > 35 & df$num <= 59))
super_freq <- as.data.frame(subset(df, df$num > 60))

#reading the table that includes the distinct Bart Station Name and the respective Location Code
bart_loc <- read.csv("/Users/.../bart_location.csv")


###1-time ridership 
##origin location
#group by the Origin Location and count the frequency
one_time_origin <- one_time%>%
  select(originlocation)%>%
  group_by(originlocation)%>%
  summarise(n=n())

#joining the two tables to get the Bart Station Name
one_time_origin_f <- left_join(one_time_origin, bart_loc, by = c("originlocation" = "LocationCode"))

#adding a column of the user group tag name to the dataframe
one_time_origin_f["frequency_tag"] <- "1-time"
#adding a column of Origin/Destination tag to the dataframe
one_time_origin_f["O/D"] <- "Origin"

##destination location
#group by the Destination Location and count the frequency
one_time_dest <- one_time  %>%
  select(destinationlocation)%>%
  group_by(destinationlocation)%>%
  summarise(n=n())

#joining the two tables to get the Bart Station Name
one_time_destination_f <- left_join(one_time_dest, bart_loc, by = c("destinationlocation" = "LocationCode"))

#adding a column of the user group tag name to the dataframe
one_time_destination_f["frequency_tag"] <- "1-time"
#adding a column of Origin/Destination tag to the dataframe
one_time_destination_f["O/D"] <- "Destination"


###Low Frequency 
low_freq_origin <- low_freq   %>%
  select(originlocation)%>%
  group_by(originlocation)%>%
  summarise(n=n())

low_freq_origin_f <- left_join(low_freq_origin, bart_loc, by = c("originlocation" = "LocationCode"))
low_freq_origin_f["frequency_tag"] <- "Low Frequency"
low_freq_origin_f["O/D"] <- "Origin"

low_freq_dest <- low_freq   %>%
  select(destinationlocation)%>%
  group_by(destinationlocation)%>%
  summarise(n=n())
low_freq_dest_f <- left_join(low_freq_dest, bart_loc, by = c("destinationlocation" = "LocationCode"))
low_freq_dest_f["frequency_tag"] <- "Low Frequency"
low_freq_dest_f["O/D"] <- "Destination"


#Medium Frequency
med_freq_origin <- med_freq   %>%
  select(originlocation)%>%
  group_by(originlocation)%>%
  summarise(n=n())

med_freq_origin_f <- left_join(med_freq_origin, bart_loc, by = c("originlocation" = "LocationCode"))
med_freq_origin_f["frequency_tag"] <- "Medium Frequency"
med_freq_origin_f["O/D"] <- "Origin"

med_freq_dest <- med_freq   %>%
  select(destinationlocation)%>%
  group_by(destinationlocation)%>%
  summarise(n=n())

med_freq_dest_f <- left_join(med_freq_dest, bart_loc, by = c("destinationlocation" = "LocationCode"))
med_freq_dest_f["frequency_tag"] <- "Medium Frequency"
med_freq_dest_f["O/D"] <- "Destination"


#High Frequency
high_freq_origin <- high_freq   %>%
  select(originlocation)%>%
  group_by(originlocation)%>%
  summarise(n=n())

high_freq_origin_f <- left_join(high_freq_origin, bart_loc, by = c("originlocation" = "LocationCode"))
high_freq_origin_f["frequency_tag"] <- "High Frequency"
high_freq_origin_f["O/D"] <- "Origin"

high_freq_dest <- high_freq   %>%
  select(destinationlocation)%>%
  group_by(destinationlocation)%>%
  summarise(n=n())

high_freq_destination_f <- left_join(high_freq_dest, bart_loc, by = c("destinationlocation" = "LocationCode"))
high_freq_destination_f["frequency_tag"] <- "High Frequency"
high_freq_destination_f["O/D"] <- "Destination"


#Super Users
super_freq_origin <- super_freq   %>%
  select(originlocation)%>%
  group_by(originlocation)%>%
  summarise(n=n())

super_freq_origin_f <- left_join(super_freq_origin, bart_loc, by = c("originlocation" = "LocationCode"))
super_freq_origin_f["frequency_tag"] <- "Super User"
super_freq_origin_f["O/D"] <- "Origin"

super_freq_dest <- super_freq   %>%
  select(destinationlocation)%>%
  group_by(destinationlocation)%>%
  summarise(n=n())

super_freq_destination_f <- left_join(super_freq_dest, bart_loc, by = c("destinationlocation" = "LocationCode"))
super_freq_destination_f["frequency_tag"] <- "Super User"
super_freq_destination_f["O/D"] <- "Destination"

#loading plyr before dplyr to avoid conflict between the two
library(plyr); library(dplyr)

#binding all the dataframes together
final <- rbind.fill(one_time_origin_f, one_time_destination_f, low_freq_origin_f, low_freq_dest_f, 
                    med_freq_origin_f, med_freq_dest_f, high_freq_origin_f, high_freq_destination_f, 
                    super_freq_origin_f, super_freq_destination_f)

#dropping the columns of the Origin Location Number and Destination Location Number
drops <- c("originlocation","destinationlocation")
final1 <- final[ , !(names(final) %in% drops)]

#exporting the dataframe
write.csv(final1, file = "file.csv")







