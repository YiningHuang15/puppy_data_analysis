# Puppy Potty Data Analysis Using Python, SQL and Tableau
For analyzing my puppy's potty data, this repository is created to contain all the data warehouse/ ETL/ SQL/ dashboard development files.

The ETL diagram is shown below. Incremental data is extracted from excel to postgreSQL twice a day using Python and Shell script. The data is transformed analyzed in postgreSQL. Finally, a tableau dashboard is created to visualize the potty training result.

![alt text](https://github.com/YiningHuang15/puppy_data_analysis/blob/main/viz/etl_diagram.png)


![alt text](https://github.com/YiningHuang15/puppy_data_analysis/blob/main/viz/dashboard_0401.png)
The Tableau dashboard is available in Tableau Public:
[Puppy Potty Training Analysis Dashboard](https://public.tableau.com/app/profile/yi.ning.huang6608/viz/PuppyPottyTrainingAnalysisDashboard/PuppyPottyTrainingAnalysisDashboard?publish=yes)


## Folder Structure
- bin: etl python + shell script 
- config: postgresql ini
- data_model: sql ddl + stored procedure
- dat: excel
- log
- twbx: Tableau workbook
