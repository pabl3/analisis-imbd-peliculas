import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar el dataset
df = pd.read_csv("imdb_top_1000.csv")

# Normalizar nombres de columnas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Limpiar y convertir columnas
df["released_year"] = pd.to_numeric(df["released_year"], errors="coerce")
df["gross"] = df["gross"].str.replace(",", "").astype(float)
df["runtime"] = df["runtime"].str.replace("min", "").str.strip().astype(int)

# Eliminar duplicados y columnas innecesarias
df.drop_duplicates(inplace=True)
df.drop(columns=["poster_link"], inplace=True)

# Estadísticas generales
print("🔹 Estadísticas generales:")
print("Año más antiguo:", df["released_year"].min())
print("Rating promedio:", np.mean(df["imdb_rating"]))
print("Duración promedio:", np.mean(df["runtime"]))
print("-" * 50)

# Top 10 películas mejor calificadas
top_rated = df.sort_values("imdb_rating", ascending=False).head(10)
print("🔸 Top 10 películas:")
print(top_rated[["series_title", "imdb_rating", "released_year"]])

# Crear columna de década
df["decade"] = (df["released_year"] // 10) * 10

# Visualización: Géneros más frecuentes
df["genre"].value_counts().sort_values().tail(10).plot(kind="barh", color="skyblue")
plt.title("🎥 Géneros más frecuentes")
plt.xlabel("Cantidad de películas")
plt.ylabel("Género")
plt.tight_layout()
plt.savefig("generos_frecuentes.png")
plt.show()

# Visualización: Rating vs Votos
sns.scatterplot(data=df, x="no_of_votes", y="imdb_rating", hue="genre", alpha=0.7)
plt.title("⭐ Rating vs Número de votos")
plt.xlabel("Votos")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig("rating_vs_votos.png")
plt.show()

# Heatmap de correlación
sns.heatmap(df[["gross", "no_of_votes", "imdb_rating"]].corr(), annot=True, cmap="coolwarm")
plt.title("📊 Correlación entre variables")
plt.tight_layout()
plt.savefig("correlacion_variables.png")
plt.show()

# Gráfico interactivo con Plotly
fig = px.scatter(df, x="imdb_rating", y="gross", size="no_of_votes", color="genre",
                 hover_name="series_title", title="💰 Ingresos vs Rating")
fig.show()

# Conclusiones:
# -Los géneros más comunes son Drama, Action y Comedy.
# -Las películas mejor calificadas no siempre tienen mayor recaudación.
# -La década más productiva fue la de los 2000s.
# -No hay una correlación fuerte entre rating y recaudación.