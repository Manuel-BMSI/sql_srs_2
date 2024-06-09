"""
# docsting :
Code utilisé pour développer l'app SQL_SRS
"""

import io
import ast

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# correction
# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """

st.markdown("\n" "# SQL SRS\n" "Spaced Repetition System SQL practice\n")

with st.sidebar:
    theme = st.selectbox(
        "What do like to review ?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme ...",
    )
    st.write("Votre sélection : ", theme)

    exo = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exo)

    exo_name = exo.loc[0, "exo_name"]
    with open(f"answers/{exo_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

# # Création d'une relation DuckDB à partir du DataFrame

st.header("Entrez votre code :")
sql_query = st.text_area(label="Entrez votre code ici :", key="user_input")
if sql_query.strip():  # Ensure the query is not empty
    result = con.execute(sql_query).df()
    st.dataframe(result)
    try:
        st.markdown(
            f"Vous avez entré le code suivant :\n\n {sql_query}\n\n Voici le résultat de cette requête : \n",
            unsafe_allow_html=False,
        )
        st.dataframe(result)

        # comparaison nb colonnes
        nb_col_diff = len(solution_df.columns) - len(result.columns)
        if nb_col_diff != 0:
            st.write(
                f"Comparaison du nb de colonnes : {nb_col_diff} colonnes de différence"
            )
        else:
            st.write("Comparaison du nb de colonnes : OK")

            # trier les colonnes du result comme celles de la solution
            result = result[solution_df.columns]

        # comparaison nb lignes
        nb_lignes_diff = result.shape[0] - solution_df.shape[0]
        if nb_lignes_diff != 0:
            st.write(
                f"Comparaison du nb de lignes : {nb_lignes_diff} lignes de différence"
            )
        else:
            st.write("Comparaison du nb de lignes : OK")

        try:
            result.compare(solution_df)
            if not result.compare(solution_df).empty:
                st.write("Comparaison des valeurs : des différences existent :")
                st.dataframe(result.compare(solution_df))
            else:
                st.write(
                    "Comparaison des valeurs : aucune différence avec la solution, bravo !"
                )
        except:
            st.write("Comparaison des valeurs : comparaison impossible")

    except Exception as e:
        st.write("Error executing query: ", e)
else:
    st.write("Veuillez entre votre code SQL ci-dessus.")

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    #exo_tables = ast.literal_eval(exo.loc[0, "tables"])
    exo_tables = exo.loc[0, "tables"]
    for table in exo_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
#     st.write("Résultat attendu : ")
#     st.dataframe(solution_df)
#
with tab3:
    st.write(answer)
