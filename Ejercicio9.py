import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Ruta al archivo CSV 
csv_file = 'emails.csv'

# Cargar datos 
df = pd.read_csv(csv_file, sep=';')

# Mostrar las primeras filas para verificar
print("Primeras filas del dataset:")
print(df.head())

# Separa características (X) y etiqueta (y)
X = df.drop('Spam', axis=1)
y = df['Spam']

# Divide datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el clasificador 
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrenar el modelo
clf.fit(X_train, y_train)

# Predecir en el conjunto de prueba
y_pred = clf.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Predicción
nuevo_dato = [[0.5, 0.6, 0.4, 0.3, 0.7]]
prediccion = clf.predict(nuevo_dato)
print(f"\nPredicción para nuevo dato {nuevo_dato}: {prediccion[0]}")

