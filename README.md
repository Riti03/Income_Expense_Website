# Income_Expense_Website
Income Expense Tracker aims to provide an efficient way to regulate our finances in the currency specified by the user. User is able to log in their income and expenses and based on that a report is generated which helps the user to get a glance at their savings and expenses. It generates a visually stimulating report of all financial activities which can be downloaded in a csv/excel format to store the record in offline mode.

# Requirements
Run the following commands-  
pip install psycopg2  
pip install xlwt  
pip install weasyprint  
pip install validate-email  

# Technology used
Django  
HTML  
CSS and Bootstrap  
JavaScript and JQuery alongwith Chart.js  
SQL

# Database used  
Postgresql


# Output  
A first time user has to register themselves by providing valid username, email and password. The username and email should be unique and not in use already in thsi application and the length of the password must be greater than six. Upon registering, an email is sent to the user in the registered email address which contains a verification link through which the user can verify themselves and then login. Without verifying, the user can not login to the application. The add expense and add income feature helps to log in the user's income and expenses. This also has an edit and delete feature which the user can use to edit/delete their income/expense. The user preference section helps the user to select which currency they are using in logging in their income and expenses. The expense summary section shows a graphical representation of the user's expenses sector-wise. The user can also save their income and expenses in a excel/csv format by using the export to excel and export to csv buttons.  
