from employee import Employee, Manager

class EmployeeManagementSystem:
    """CLI-based Employee Management System"""
    
    def __init__(self):
        from employee import Employee
        self.db = Employee.get_db()
        self.running = True
        self.load_employees_from_db()
    
    def load_employees_from_db(self):
        """Load existing employees from database on startup"""
        all_records = self.db.get_all_employees()
        for record in all_records:
            emp_id, first_name, last_name, age, department, salary, emp_type, managed_dept, created_at = record
            
            if emp_type == 'Manager':
                emp = Manager(first_name, last_name, age, department, salary, managed_dept)
            else:
                emp = Employee(first_name, last_name, age, department, salary)
            
            # Restore the original ID
            emp.id = emp_id
    
    def display_menu(self):
        """Display the main menu"""
        print("       EMPLOYEE MANAGEMENT SYSTEM - MAIN MENU")
        print("'add'   - Add new employee")
        print("'list'  - List all employees")
        print("'view'  - View specific employee")
        print("'transfer' - Transfer employee to new department")
        print("'fire'  - Remove employee from system")
        print("'q'     - Exit the program")
    
    def get_employee_type(self):
        """Get the type of employee to add"""
        print("\nSelect employee type:")
        print("'e' - Employee")
        print("'m' - Manager")
        choice = input("Enter your choice (e/m): ").strip().lower()
        
        return choice
    
    def add_employee(self):
        """Add a new employee to the system"""
        emp_type = self.get_employee_type()
        
        if emp_type not in ['e', 'm']:
            print("✗ Invalid choice")
            return
        
        print("\n" + "-"*40)
        print("ENTER EMPLOYEE INFORMATION")
        print("-"*40)
        
        try:
            first_name = input("First Name: ").strip()
            if not first_name:
                print("✗ First name cannot be empty")
                return
            
            last_name = input("Last Name: ").strip()
            if not last_name:
                print("✗ Last name cannot be empty")
                return
            
            age = int(input("Age: ").strip())
            if age <= 0 or age > 120:
                print("✗ Invalid age")
                return
            
            department = input("Department: ").strip()
            if not department:
                print("✗ Department cannot be empty")
                return
            
            salary = float(input("Salary: $").strip())
            if salary < 0:
                print("✗ Salary cannot be negative")
                return
            
            if emp_type == 'e':
                emp = Employee(first_name, last_name, age, department, salary)
                print(f"\n✓ Employee '{first_name} {last_name}' has been added successfully!")
                emp.show()
            else:  # Manager
                managed_department = input("Managed Department: ").strip()
                if not managed_department:
                    print("✗ Managed department cannot be empty")
                    return
                
                emp = Manager(first_name, last_name, age, department, salary, managed_department)
                print(f"\n✓ Manager '{first_name} {last_name}' has been added successfully!")
                emp.show()
        
        except ValueError:
            print("✗ Invalid input. Please enter correct data types.")
    
    def list_all_employees(self):
        """List all employees"""
        Employee.list_employees()
    
    def view_employee(self):
        """View a specific employee's details"""
        if not Employee.employees:
            print("\n✗ No employees in the system")
            return
        
        self.list_all_employees()
        
        try:
            emp_id = int(input("\nEnter employee ID to view: ").strip())
            
            for emp in Employee.employees:
                if emp.id == emp_id:
                    emp.show()
                    return
            
            print(f"\n✗ Employee with ID {emp_id} not found")
        except ValueError:
            print("✗ Invalid ID format")
    
    def transfer_employee(self):
        """Transfer an employee to a new department"""
        if not Employee.employees:
            print("\n✗ No employees in the system")
            return
        
        self.list_all_employees()
        
        try:
            emp_id = int(input("\nEnter employee ID to transfer: ").strip())
            
            for emp in Employee.employees:
                if emp.id == emp_id:
                    new_dept = input("Enter new department: ").strip()
                    if not new_dept:
                        print("✗ Department cannot be empty")
                        return
                    emp.transfer(new_dept)
                    return
            
            print(f"\n✗ Employee with ID {emp_id} not found")
        except ValueError:
            print("✗ Invalid ID format")
    
    def fire_employee(self):
        """Remove an employee from the system"""
        if not Employee.employees:
            print("\n✗ No employees in the system")
            return
        
        self.list_all_employees()
        
        try:
            emp_id = int(input("\nEnter employee ID to remove: ").strip())
            
            for emp in Employee.employees[:]:  # Create a copy for iteration
                if emp.id == emp_id:
                    confirm = input(f"Are you sure you want to remove {emp.first_name} {emp.last_name}? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        emp.fire()
                    else:
                        print("✗ Operation cancelled")
                    return
            
            print(f"\n✗ Employee with ID {emp_id} not found")
        except ValueError:
            print("✗ Invalid ID format")
    
    def run(self):
     
        while self.running:
            self.display_menu()
            
            user_input = input("\nEnter command: ").strip().lower()
            
            if user_input == 'add':
                self.add_employee()
            elif user_input == 'list':
                self.list_all_employees()
            elif user_input == 'view':
                self.view_employee()
            elif user_input == 'transfer':
                self.transfer_employee()
            elif user_input == 'fire':
                self.fire_employee()
            elif user_input == 'q':
                self.running = False
            else:
                print("✗ Invalid command. Please try again.")
        
        # Clean up
        self.db.close()


def main():
    """Main entry point"""
    system = EmployeeManagementSystem()
    system.run()


if __name__ == "__main__":
    main()
