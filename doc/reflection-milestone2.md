## Dashboard Implementation and Reflection

## Tab 0: Overview 

### Implemented Features:

1. The dashboard visualizes the spatial distribution of malnutrition indicators across continents using an interactive Plotly choropleth map.
2. It offers a comparative and general malnutrition analysis between continents.
3. There are detailed tooltips available for data points on the maps and charts, providing additional context and information.
4. A general introductory quote is present, setting the context for the global malnutrition situation.
5. The dashboard lists noteworthy points from the dataset, highlighting key insights such as the highest rates of severe wasting and overweight children by continent.

### Not Yet Implemented:

1. Improve the css to the layout.
2. Add poverty comparison and analysis between continents

### Reflection:

The Overview tab serves as a comprehensive introduction to the global situation of malnutrition, effectively combining quantitative data with qualitative insights. The use of Plotly for choropleth maps enables a clear spatial representation of malnutrition indicators, which, along with the comparative analysis between continents, provides a quick understanding of the geographic distribution of the problem.

The introductory quote and the noteworthy points at the bottom offer context and a summary of the critical findings, respectively, making the data more accessible to stakeholders. The detailed tooltips are a great feature as they provide instant access to more in-depth information without cluttering the visual presentation.

For future improvements, enhancing the CSS layout could make the dashboard more aesthetically pleasing and user-friendly. Additionally, incorporating interactive elements such as filtering options or more dynamic comparative analysis tools could further engage users and allow for more personalized data exploration. It would also be beneficial to ensure that the data presented in the tooltips is aligned with the latest research and statistics for accuracy and credibility.


## Tab 1: Malnutrition 
### Implemented Features:
1. The dashboard displays the spatial distribution of seven malnutrition indicators using Plotly/choropleth map.
2. Temporal distribution of fatality count and poverty indicator for selected nations using the Altair package.
3. Comparative analysis between countries.
4. Detailed tooltips for data points on the maps and charts.

### Not Yet Implemented:
1. Improve the css to the layout

### Reflection:
The dashboard effectively presents spatial and temporal trends in malnutrition indicators. However, the lack of interactivity limits user exploration. Future improvements could include interactive filtering, comparative analysis tools, and detailed tooltips for a better understanding of data points.

## Tab 2: World Poverty
### Implemented Features:
1. The world map displays 6 key indicators of poverty by country.
2. Drop-down menu for users to select country and region with in that country to compare key poverty indicators in a general/regional perspective.
3. Altair visualization of the key indicators in comparison with general/regional perspective.
4. Bar plot comparison of hovered world-map selected country and drop-down menu selected country.

### Not Yet Implemented:
1. Improve the css to the layout.
2. Rearrange the graphs and charts to make it more readable.

### Reflection:
The dashboard does a good job in showing the key indicators of world poverty categorized by countries. The comparisons between countries and with in countries can give people a understanding of how each country performs in terms of minimizing poverty, and whether the development across regions within a country is balanced. However, due to the complexity of the indicators, users may not have a deep understanding of how the indicators speak for poverty. Future improvements could include providing the users with world mean, median, variance of each key indicators we used to measure world poverty.