📱 B.A.D.I. Mobile Survey App – Python Flet

1️⃣ What is the purpose of this project?

This project is a mobile data collection application developed using Python (Flet) for field workers of Banco de Alimentos de Imbabura (B.A.D.I.).

The purpose of this application is to:

Digitally collect household survey data in the field

Provide a structured and dynamic form interface

Store data locally using SQLite

Synchronize collected data with a centralized MySQL database via REST API

Ensure reliable and consistent data submission

The app serves as the mobile client of the larger B.A.D.I. data management system.

2️⃣ What problem does it solve?

Field data collection presents several operational challenges:

Paper-based surveys are slow and error-prone

Lack of offline capability in rural areas

Delays in transferring data to central systems

Risk of data loss

Inconsistent field validation

This mobile application solves these problems by:

Providing structured digital forms

Enabling local SQLite storage for temporary offline persistence

Validating data before submission

Synchronizing securely with the backend system through API communication

3️⃣ Tech Stack

Mobile Framework: Python (Flet)

Local Database: SQLite

Backend API: PHP (CodeIgniter)

Central Database: MySQL

Communication: REST API (JSON)

Version Control: Git & GitHub

4️⃣ Key Features

Dynamic household registration form

Conditional input fields based on survey logic

Local SQLite storage for offline capability

API-based synchronization with MySQL server

Data validation before submission

User authentication

5️⃣ Technical Challenges Solved

Implemented local-first architecture using SQLite

Designed API integration for reliable data synchronization

Managed JSON serialization/deserialization between mobile and backend

Handled relational data submission (household + multiple members)

Ensured consistency between local and remote databases

6️⃣ Methodology
![image alt](https://github.com/nathan314159/bancoAlimentos/blob/c0a38eb5b3efd1f07f61f5bcda81b7f42c3666de/metodologia.pptx.png)

7️⃣ System Architecture
![image alt](https://github.com/nathan314159/bancoAlimentos/blob/768df928da3f0f4f14d5475d513dacebcbe304f5/arquitectura.pptx.png)
8️⃣ Screenshots
![image alt](https://github.com/nathan314159/bancoAlimentos/blob/c0a38eb5b3efd1f07f61f5bcda81b7f42c3666de/celular%20badi.pptx.png)
![image alt](https://github.com/nathan314159/bancoAlimentos/blob/c0a38eb5b3efd1f07f61f5bcda81b7f42c3666de/dashboard.pptx.png
)
![image alt](https://github.com/nathan314159/bancoAlimentos/blob/c0a38eb5b3efd1f07f61f5bcda81b7f42c3666de/login.pptx.png
)



