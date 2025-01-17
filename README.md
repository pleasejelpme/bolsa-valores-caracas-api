# Bolsa de Valores de Caracas API
Api desarrollada en FastAPI que proporciona datos de las acciones listadas en la [Bolsa de Valores de Caracas](https://www.bolsadecaracas.com/).

---

## 🛠 Tecnologias Utilizadas
- [Python](https://www.python.org)
- [FastApi](https://fastapi.tiangolo.com/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Reportlab](https://www.reportlab.com/)

---

## 🔩 Instalación
Puedes hacer la instalación usando Docker siguiendo las siguientes [instrucciones](README.Docker.md).

Para una instalacion manual:
``` 
python -m venv .env 
```

En windows 
```
.env\scripts\activate
```
En linux 
```
source .env/bin/activate
```

Luego, instalar dependencias con: 
```
pip install -r requirements.txt
```

Finalmente para levantar el servidor:
```
fastapi dev main.py
```

Documentación de la API en ```http://127.0.0.1:8000/docs```