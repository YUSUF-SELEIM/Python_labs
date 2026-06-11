import sqlite3
from datetime import datetime

class Database:
    """Database management for employee records"""
    
    def __init__(self, db_name='employees.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create the employees table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                employee_type TEXT NOT NULL,
                managed_department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def insert_employee(self, first_name, last_name, age, department, salary, employee_type, managed_department=None):
        """Insert a new employee record"""
        self.cursor.execute('''
            INSERT INTO employees (first_name, last_name, age, department, salary, employee_type, managed_department)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, department, salary, employee_type, managed_department))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_department(self, employee_id, new_department):
        """Update employee's department"""
        self.cursor.execute('''
            UPDATE employees SET department = ? WHERE id = ?
        ''', (new_department, employee_id))
        self.conn.commit()
    
    def delete_employee(self, employee_id):
        """Delete an employee record"""
        self.cursor.execute('''
            DELETE FROM employees WHERE id = ?
        ''', (employee_id,))
        self.conn.commit()
    
    def get_all_employees(self):
        """Get all employees from database"""
        self.cursor.execute('SELECT * FROM employees')
        return self.cursor.fetchall()
    
    def get_employee_by_id(self, employee_id):
        """Get employee by ID"""
        self.cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        return self.cursor.fetchone()
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
