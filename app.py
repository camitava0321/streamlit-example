#!/usr/bin/env python
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
"""
# Amitava Chakraborty
"""

# env variables
DATA_FILEPATH = "litcovid.export.all.tsv"
# First, we load a TSV as a dataframe and cache the data:
@st.cache
def load_data(filepath:str) -> pd.DataFrame:
    """ Load data from local TSV """
    return pd.read_csv(filepath, sep="\\t", skiprows=33).fillna("")

#Next, we create a function to search the dataframe. 
# This is done by checking to see if a column has rows 
# where our search term is a substring:
def search_dataframe(df:pd.DataFrame, column:str, search_str:str) -> pd.DataFrame:
    """ Search a column for a substring and return results as df """
    results = df.loc[df[column].str.contains(search_str, case=False)]
    return results


# One of the best features of Streamlit is 
# interactive plotting and visualization. 
# At ScienceIO, we love to use Altair plots which are easily converted from static to dynamic. 
# Let’s add an interactive bar plot that shows the top journals in our search results.
# we can use altair to turn our results dataframe into a bar chart of top journal
def generate_barplot(results:pd.DataFrame, count_column:str, top_n:int=10):
    """load results from search_dataframe() and create barplot """
    return alt.Chart(results).transform_aggregate(
        count='count()',
        groupby=[f'{count_column}']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(
        alt.datum.rank < top_n
    ).mark_bar().encode(
        y=alt.Y(f'{count_column}:N', sort='-x'),
        x='count:Q',
        tooltip=[f'{count_column}:N', 'count:Q']
    ).properties(
        width=700,
        height=400
    ).interactive()


def app():
    """ Search Streamlit App """
    # app title
    st.title("Text Search 📝")

    # We want to load the data once the application starts:
    # within app(): load data from local tsv as dataframe
    df = load_data(DATA_FILEPATH)

    # search box
    with st.form(key='Search'):
        text_query = st.text_input(label='Enter text to search')
        submit_button = st.form_submit_button(label='Search')
    
    # Next, we needed our app to do something when we clicked the button. 
    # So we set up a spinner for the user to see that a search was happening 
    # while we retrieved the results:
    #Now when we click on st.form_submit_button, we’ll run the search, notify the user of the number of results found, and display the first ten hits:

    results=None

    # if button is clicked, run search
    if submit_button:
        with st.spinner("Searching (this could take a minute...) :hourglass:"):

            # search logic goes here! - search titles for keyword
            results = search_dataframe(df, "title_e", text_query)

            #Once the spinner was done, we used success to show that the search was complete:
            # notify when search is complete
            st.success(f"Search is complete :rocket: — **{len(results):,}** results found in {len(df):,}  papers.")

        # display the first 10 results
        st.table(results.head(n=10))

        # display a bar chart of top journals
        st.altair_chart(
            generate_barplot(results, "journal", 10)
        )

    #Video
    #st.video('recorded_screencast.mp4')
    
    #Default Input Data
    txt = st.text_area('Text to analyze', value='It was the best of times')
    
    #Tooltips
    st.title('Tooltips in Streamlit')
    st.radio("Pick a number", [1, 2, 3], help='Select a number out of 3 choices')
    
    # Tooltips also support markdown
    radio_markdown = '''
    Select a number, you have **3** choices!
    '''.strip()
    
    st.header('Tooltips with Markdown')
    st.radio("Pick a number", [1, 2, 3], help=radio_markdown)
    
    
    
    num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
    num_turns = st.slider("Number of turns in spiral", 1, 300, 31)
    
    indices = np.linspace(0, 1, num_points)
    theta = 2 * np.pi * num_turns * indices
    radius = indices
    
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    
    df = pd.DataFrame({
        "x": x,
        "y": y,
        "idx": indices,
        "rand": np.random.randn(num_points),
    })
    
    st.altair_chart(alt.Chart(df, height=700, width=700)
        .mark_point(filled=True)
        .encode(
            x=alt.X("x", axis=None),
            y=alt.Y("y", axis=None),
            color=alt.Color("idx", legend=None, scale=alt.Scale()),
            size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
        ))

if __name__ == '__main__':
    app()
