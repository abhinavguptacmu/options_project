# options_project

The ORATS_SMV_Strikes_20200420.csv is too big to upload to git but can be found at [here](https://s3.amazonaws.com/assets.orats.com/ORATS_SMV_Strikes_20200420.zip). 

Options project, calculating optimal long put strike price according to historical data.

The goal of this model is to fine tune a bull put spread, the strike price of the bull spread are larely left up to the trader but I wanted to create a model which according to the past historical data tells us which delta values for the corresponding strike prices will maximise the profits. This is done by first exporting the historical data and then cleaning it by removing columms which will not be used. Then we filter ourselves down to a certain expiration date (will be changed in the future). We get data about the stock prices 1 day before expiration and then use them to compute our profit and continue with the rest of our data analysis. 
