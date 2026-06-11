from database import Database

class Employee:
    """Employee class with employee management capabilities"""
    
    # Static list containing all employees
    employees = []
    db = None
    next_id = 1
    
    @classmethod
    def get_db(cls):
        """Get or initialize database"""
        if cls.db is None:
            cls.db = Database()
        return cls.db
    
    def __init__(self, first_name, last_name, age, department, salary):
        """
        Constructor - Initialize employee attributes and add to list and database
        
        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            age: Employee's age
            department: Department where employee works
            salary: Employee's salary
        """
        self.id = Employee.next_id
        Employee.next_id += 1
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.department = department
        self.salary = salary
        self.employee_type = 'Employee'
        
        # Add to static list
        Employee.employees.append(self)
        
        # Insert into database
        self._save_to_database()
    
    def _save_to_database(self):
        """Save employee to database"""
        Employee.get_db().insert_employee(
            self.first_name,
            self.last_name,
            self.age,
            self.department,
            self.salary,
            self.employee_type
        )
    
    def transfer(self, new_department):
        """
        Transfer employee to a new department and update database
        
        Args:
            new_department: The new department name
        """
        print(f"\n✓ {self.first_name} {self.last_name} has been transferred from {self.department} to {new_department}")
        self.department = new_department
        
        # Update database
        Employee.get_db().update_department(self.id, new_department)
    
    def fire(self):
        """Remove employee from the list and database"""
        if self in Employee.employees:
            Employee.employees.remove(self)
            Employee.get_db().delete_employee(self.id)
            print(f"\n✓ {self.first_name} {self.last_name} has been removed from the system")
        else:
            print(f"\n✗ Employee not found")
    
    def show(self):
        """Print all employee data"""
        print("\n" + "="*60)
        print(f"Employee Information")
        print("="*60)
        print(f"ID:              {self.id}")
        print(f"Name:            {self.first_name} {self.last_name}")
        print(f"Age:             {self.age}")
        print(f"Department:      {self.department}")
        print(f"Salary:          ${self.salary:,.2f}")
        print(f"Type:            {self.employee_type}")
        print("="*60)
    
    @staticmethod
    def list_employees():
        """Select all employees and print their data"""
        if not Employee.employees:
            print("\n✗ No employees in the system")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Department':<20} {'Salary':<15}")
        print("="*80)
        
        for emp in Employee.employees:
            print(f"{emp.id:<5} {emp.first_name + ' ' + emp.last_name:<20} {emp.age:<5} {emp.department:<20} ${emp.salary:<14,.2f}")
        
        print("="*80)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_type})"


class Manager(Employee):
    """Manager class inheriting from Employee with additional managed_department attribute"""
    
    def __init__(self, first_name, last_name, age, department, salary, managed_department):
        """
        Constructor - Initialize manager with all employee attributes plus managed_department
        
        Args:
            first_name: Manager's first name
            last_name: Manager's last name
            age: Manager's age
            department: Department where manager works
            salary: Manager's salary
            managed_department: Department managed by this manager
        """
        super().__init__(first_name, last_name, age, department, salary)
        self.managed_department = managed_department
        self.employee_type = 'Manager'
        
        # Update database with manager info
        Employee.get_db().cursor.execute('''
            UPDATE employees SET employee_type = ?, managed_department = ?
            WHERE id = (SELECT MAX(id) FROM employees)
        ''', (self.employee_type, self.managed_department))
        Employee.get_db().conn.commit()
    
    def show(self):
        """Print all manager data with salary shown as confidential"""
        print("\n" + "="*60)
        print(f"Manager Information")
        print("="*60)
        print(f"ID:              {self.id}")
        print(f"Name:            {self.first_name} {self.last_name}")
        print(f"Age:             {self.age}")
        print(f"Department:      {self.department}")
        print(f"Salary:          [CONFIDENTIAL]")
        print(f"Type:            {self.employee_type}")
        print(f"Manages:         {self.managed_department}")
        print("="*60)
