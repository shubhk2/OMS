"""
Database migration script to add curr_salary column to Employee table
and create company_settings table with default values.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'office.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add curr_salary column to Employee table if it doesn't exist
        cursor.execute("PRAGMA table_info(Employee)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'curr_salary' not in columns:
            print("Adding curr_salary column to Employee table...")
            cursor.execute("""
                ALTER TABLE Employee ADD COLUMN curr_salary DECIMAL(10, 2) DEFAULT 0.00
            """)
            print("curr_salary column added successfully.")
        else:
            print("curr_salary column already exists.")
        
        # Create company_settings table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key VARCHAR(100) UNIQUE NOT NULL,
                value VARCHAR(500),
                description VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("company_settings table created/verified.")
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_company_settings_updated_at
            AFTER UPDATE ON company_settings
            FOR EACH ROW
            BEGIN
                UPDATE company_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END
        """)
        
        # Insert default company settings if they don't exist
        default_settings = [
            ('wfh_salary_deduction_percent', '10', 'Percentage deduction from salary for Work From Home'),
            ('ot_salary_addition_percent', '15', 'Percentage addition to hourly rate for Overtime per hour'),
            ('default_unpaid_leaves', '5', 'Default number of unpaid/medical leaves allowed'),
            ('leave_paid_by_default', 'true', 'Whether leaves are paid by default (true/false)'),
        ]
        
        for key, value, description in default_settings:
            cursor.execute("SELECT COUNT(*) FROM company_settings WHERE key = ?", (key,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO company_settings (key, value, description)
                    VALUES (?, ?, ?)
                """, (key, value, description))
                print(f"Default setting '{key}' added.")
        
        conn.commit()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()
