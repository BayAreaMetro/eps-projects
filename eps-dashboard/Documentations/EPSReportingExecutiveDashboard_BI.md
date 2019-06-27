# EPS Reporting Executive Dashboard Power BI

The dashboard is requested by Lysa Hale. The goal is to build a dashboard to replace the PDF report sent to the board of members. Jacques is assigned to build the prototype with Power BI.

![Screenshot](images/bi_coverpage.png)
Figure 1

## Persona
Jacques Sham is the creator.<br>
Lysa Hale from EPS request the project.<br>
Lysa Hale and the board of executives are the target audience.<br>
Sean Bugler is the IT contact for Power BI and Share Point.

## Microsoft Power BI
Power BI is a Microsoft business intelligence tool that is included in the Microsoft Office 365 subscription in MTC. There are two versions for Power BI - Power BI Desktop and Power BI Service Online. When building dashboard, you need to connect to Microsoft Remote Desktop to build the dashboard with Power BI Desktop and upload to Power BI Service Online. 

## Data Access and Dashboard Size
Power BI query data from AWS Redshift directly every time when viewers use it, the data does not underlie with the file. MTC has total storage of 25 TB and has been used up less than 5 TB, as of Jun 26, 2019. The dashboard Jacques has created take about 2 MB per file. 


## Basics
First, connect the data source. Power BI allows you to upload Excel or csv files from local or connect to database. AWS Redshift itself is one category in Power BI set up, do not click on datebase, click on AWS Redshift.

<br>
Screenshot is not available on Github<br>
Figure 2
<br>
The best practices of making visualizing is:
1. Select visualization
2. Drag the desired columns to the axis or value. Axis is x-axis and values is y-axis.
3. Make filter/Rename columns/Formatting
You may see that selections of visualization and columns on Figure 2
<br><br>
Screenshot is not available on Github<br>
Figure 3
<br><br>
Figure 3 shows you where to change colour, title, legend on the visualization. 


## Renaming columns
Power BI allows you to change columns names in report level and visualization level. For instance, if we have a column name of clipper_transaction from AWS Redshift, the column name will be show on the tooltip in all visualization. To avoid that, there are two ways: Change column names in visualization column or filed column.
<br>
Screenshot is not available on Github<br>
Figure 4

<br><br>
In Figure 4, you may select the arrow of individual column in Fields column and click "Rename", the column name will be changed and apply to all pages in the the report. It means once you have changed the name, the column name change will be effective to all visualizations in every page in the report.
<br><br>
However, if you want the change to be effective to only one visualization. You should go to the visualization column and select the arrow of individual column in Fields column and click "Rename", like in Figure 5. Therefore, the column name change will be only effective to this particular visualization.

<br>
Screenshot is not available on Github<br>
Figure 5

## Formatting
All the detail formatting is needed to be done in Desktop version because the functionalities in desktop do not exist in Service Online, except KPI scoreboard formatting. For example, if you want to have numbers to have commas on tooltips, the formatting have to be done in desktop version because the tool bar which allows you to reformat the column does not exist in Service Online. 

<br>
Screenshot is not available on Github<br>
Figure 6
<br><br>
In this case, you need to select a column, then go to "Modeling" on the tool bar, and select the comma button like you do in Excel. You may see Figure 6 for reference. Note that this tool bar does not exist in Service Online version, so any functionality located on the toolbar has to be done in Desktop version.
<br><br>
Except the case of formatting KPI Scoreboard. If you look at Figure 7, the indicator of visualization column in desktop version do not allow you to change the font size of KPI scoreboard. It is also the case for font size and font style in Title of KPI scoreboard.
<br>
<br>
Screenshot is not available on Github<br>
Figure 7
<br>
The solution is to set up a KPI scoreboard in Desktop version and change the font size and font style in Service Online version, like in Figure 8.<br>

<br>
Screenshot is not available on Github<br>
Figure 8
<br>
Once you have done outlining the EPS Dashboard in Desktop version, you will have to publish the dashboard to Service Online version, like in Figure 9. Then, log in to MTC's Office 365 and launch Power BI. You will find you dashboard and select "My workplace"  then "Reports", your EPS dashboard been uploaded to the Power BI dashboard and open it. After you have adjusted the detail, you will have to publish this EPS dashboard to the web in order for embedding in SharePoint. In Figure 10, you may find the how to publish to the web.  Then you will receive a html syntax for you to embed in html file or SharePoint, like in Figure 11.
<br>
<br>
Screenshot is not available on Github<br>
Figure 9
<br>
<br>
Screenshot is not available on Github<br>
Figure 10
<br>
<br>
Screenshot is not available on Github<br>
Figure 11
<br><br>
For SharePoint, it is only allow to embed iframe. 
<br>
Also note that, the dashboard in Service Online version can be downloaded to local machines and open in Desktop version. However, the Desktop version in MTC is not up-to-date. It means the Desktop version is not able to open the pbix files downloaded from Service Online version. The best practice is to have a one-way work flow to build dashboard in Desktop version, upload to Service Online, and Get the embed code (Do not work backward at any given point).
<br>
## Drill Through Data
Power BI allows you to drill through data. For instance, if you have a bar chart and you are allowed to click on one of the bars and drill through it. This dashboard did not have such functionality but potentially it could have. There is a link for further detail about this:
<a href="https://docs.microsoft.com/en-us/power-bi/desktop-drillthrough">here</a>
<br>

## Filter
The visualizations here filter based on date from the slide bar because the slider is functioning as a filter in page level. The visualization is able to disconnect to the slider but it does not make sense to do such. Filter is able to do visualization, page, and report level. You have control on this setting. There is a link for further detail about this:
<a href="https://docs.microsoft.com/en-us/power-bi/power-bi-report-add-filter">here</a>
