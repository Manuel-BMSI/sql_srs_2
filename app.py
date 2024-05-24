import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")


option = st.selectbox(
    "What do like to review ?",
    ("Joins", "GroupBy", "Windows Functions"),
    index=None,
    placeholder="Select a theme ...",
)

st.write('You selected : ', option)

data = {"a" : [1, 2, 3], "b" : [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["cat", "dog", "owl"])

with tab1:
    # Création d'une relation DuckDB à partir du DataFrame
    relation = duckdb.from_df(df)
    sql_query = st.text_area(label="Entrez votre code ici :")
    if sql_query.strip():  # Ensure the query is not empty
        try:
            result = relation.query("data", sql_query).df()
            st.write(f"Vous avez entré la query suivante : {sql_query}")
            st.dataframe(result)
        except Exception as e:
            st.write("Error executing query: ", e)
    else:
        st.write("Please enter a valid SQL query.")


with tab2:
    st.header("a dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("a owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
