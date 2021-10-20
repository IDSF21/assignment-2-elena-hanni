**Exploration of Chocolate Bar Ratings**

**Project Goal:**

Description from the original dataset: Chocolate is one of the most popular candies in the world. Each year, residents of the United States collectively eat more than 2.8 billions pounds. 
However, not all chocolate bars are created equal! This dataset contains expert ratings of over 1,700 individual chocolate bars, along with information on their regional origin, percentage of cocoa, the variety of chocolate bean used and where the beans were grown.
Link to Kaggle Dataset: https://www.kaggle.com/rtatman/chocolate-bar-ratings

With the background information about the dataset, I want to solve the following questions:

*1. What factors are related to rating for chocolate bars?*

This question aims to reach the goal of finding out what external factors might influence the rating, and understand what rating score represents.

*2. What’s the relationship between cacao solids percentage and rating?*

This question aims to reach the goal of finding out the relationship between cacao solids percentage and rating, as this also helps us understand how rating might be developed and how to choose chocolate with different cocoa percentage.

*3. Which countries produce the highest-rated bars?*

This question aims to reach the goal of finding the countries of chocolate production companies. This helps users/customers find the best chocolate bars avaialble at their local shops/ online stores.

*4. Where are the best cocoa beans grown?*

This question aims to reach the goal of finding the best origin of cocoa beans when users/customers want to try some new, high quality chocolates they have never seen.

By solving these questions through this application, we will be able to find out what factors are related to the rating and how we can better choose the chocolates bars next time we are at the shop with the help of rating.

**Rational for design decisions:**

1. For the first visualization, I chose to use box plots considering that I am looking for the relationship between a continuous variable(rating) and some categorical variables. 
   
   In this case, box plots are helpful in the sense that we can display the categories on the x-axis, and easily observe the distribution of rating on the y-axis. We can also get the mean on one category and check if there exists outliers. 
   
   For the input widgets, I used select box, since I only want to compare one categorical variable with rating at a time. Also, since there are few options, using select box is efficient and easy to choose from. I also considered using scatter plot, but since there are many points that overlapped with each other, I decided to use boxplot.
   

2. For the second visualization, I chose to use scatter plot with a linear regression line to visualize the relationship between cacao percentage and rating. The reason I chose to use scatter plots is that both variables are continuous, and the scatter plot works well with the linear regression line to observe how well the regression model fits the sample points. 
   
   For the input widgets, I decided to use select slider, because this allows users to easily checking any specific year, all years, or a specific period of years. I also tried with multiselect, but didn't use it because it would be very complex select all, or some continuous period compared to select slider. Other options I considered includes box plots, because percentage can also be categorized in some sense, but it didn't work out with the regression line.
   

3. For the third visualization, I decided to use bar charts, because I want users to have a simple and clear visual comparisons of ratings among each company's country location. For selecting countries, I decided to use multiselect because users can just select the countries that they are specifically interested in; in this case select slider would not work because there is no connection between these countries. 
   
   Some other options I considered for the visualization includes using world maps, but since these country names are familiar to most people, and depends on the countries users select, the map can be too sparse that users need to zoom frequently to find the results they want, also they need to furthur interact with the map to get rating numbers. Thus, I decided to stick with bar charts.
   

4. For the last visualization, I decided to use map, because among all locations, many of them might be some specific locations that people, or normal customers, would not be familiar with the location. With the help of using count of chocolate bar locations as the radius of points on the map, the users can get a sense of the general rating of that location and decide whether to buy the products from that location or not. The hovering functionality helps users know about rating numbers if they want to know more than general rating indicated by the color. 
   
   Some other methods I considered includes bar charts, but there are too many choices for the multiselect part, and it would be helpful for users to get a sense of which regions have the best chocolates.


**Development process:**

Since I am not working in a team for this homework, I did all the work included in this project.

The development process starts with choosing the dataset on Kaggle(2 hrs). This step took much longer time than I expected, because I didn't notice the difficulty to find a dataset that is good in size for this limited time, and includes multiple types of information.

The next step I took is data cleaning(1 hr) and exploratory data analysis(1 hr). This part is also time-consuming because I decided to add two columns, longitude, and latitude based on the general origin of cacao beans. With these additional rows, I will be able to visualize ratings on a world map to help users understand the locations, as many of the city names might be not that familiar to most people. For the exploratory data analysis, I used bar plots, box plots, and scatter plots to get a general sense of distribution of each variables and potential relationship between variables. The code that I used to process the raw dataset are in load_data.py, and the processed dataset is saved in output.csv.

After that, the step I took is developing the website with streamlit(5 hrs). Specifically, I spent about 0.5 hrs considering about the questions that I want to solve with this dataset, and about 2 hrs on the map visualization, and 2.5 hrs on other visualizations. 

Next, I spent about 1 hr to write the documentations and comments on the website. 

Last but not least, I tried to deploy the website(0.5hr).

Therefore, I spent a total of ~11 hrs on this homework, and the developing website and interactions step took me 
the longest time(~5hrs).

