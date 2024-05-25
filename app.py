import streamlit as st
import pandas as pd
import duckdb
import io

# création du df beverages
csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(csv))
# con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

# création du df food_items
csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(csv2))
# con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

# correction
answer_str = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(answer_str).df()

st.write("\n" "# SQL SRS\n" "Spaced Repetition System SQL practice\n")

with st.sidebar:
    option = st.selectbox(
        "What do like to review ?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme ...",
    )

    st.write("Votre sélection : ", option)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

# Création d'une relation DuckDB à partir du DataFrame
relation = duckdb.from_df(df)
sql_query = st.text_area(label="Entrez votre code ici :", key="user_input")
if sql_query.strip():  # Ensure the query is not empty
    try:
        result = relation.query("data", sql_query).df()
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
    st.write("table : beverages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("Résultat attendu : ")
    st.dataframe(solution_df)

with tab3:
    st.write(answer_str)
