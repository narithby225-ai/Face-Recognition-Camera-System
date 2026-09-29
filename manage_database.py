"""
Database Management Utility
Manage persons and face encodings in the database.
"""

import argparse
import json
import sys
import os

from src.database_manager import DatabaseManager


def load_config(config_path: str = "config/config.json") -> dict:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def list_persons(db_manager: DatabaseManager):
    """List all registered persons."""
    persons = db_manager.get_all_persons()
    
    if not persons:
        print("\n📋 Database is empty.")
        return
    
    print("\n" + "="*90)
    print("📋 REGISTERED PERSONS")
    print("="*90)
    print(f"{'ID':<6} {'Name':<25} {'Registered':<20} {'Last Seen':<20} {'Notes'}")
    print("-"*90)
    
    for person in persons:
        person_id = person['id']
        name = person['name'][:24]
        reg_date = person['registration_date'][:19] if person['registration_date'] else 'N/A'
        last_seen = person['last_seen'][:19] if person['last_seen'] else 'Never'
        notes = person['notes'][:20] if person['notes'] else ''
        
        print(f"{person_id:<6} {name:<25} {reg_date:<20} {last_seen:<20} {notes}")
    
    print("-"*90)
    print(f"Total: {len(persons)} person(s)")
    print("="*90 + "\n")


def view_person(db_manager: DatabaseManager, person_id: int):
    """View detailed information about a person."""
    person = db_manager.get_person_by_id(person_id)
    
    if not person:
        print(f"\n❌ Person with ID {person_id} not found.")
        return
    
    print("\n" + "="*60)
    print("👤 PERSON DETAILS")
    print("="*60)
    print(f"ID:           {person['id']}")
    print(f"Name:         {person['name']}")
    print(f"Registered:   {person['registration_date']}")
    print(f"Last Seen:    {person['last_seen'] or 'Never'}")
    print(f"Notes:        {person['notes'] or 'None'}")
    print("="*60 + "\n")


def delete_person(db_manager: DatabaseManager, person_id: int, force: bool = False):
    """Delete a person from database."""
    person = db_manager.get_person_by_id(person_id)
    
    if not person:
        print(f"\n❌ Person with ID {person_id} not found.")
        return
    
    print(f"\n⚠️  About to delete: {person['name']} (ID: {person_id})")
    
    if not force:
        confirm = input("Are you sure? This cannot be undone. (yes/no): ")
        if confirm.lower() != 'yes':
            print("Deletion cancelled.")
            return
    
    if db_manager.delete_person(person_id):
        print(f"✓ Successfully deleted {person['name']} (ID: {person_id})")
    else:
        print("❌ Failed to delete person")


def search_person(db_manager: DatabaseManager, query: str):
    """Search for persons by name."""
    persons = db_manager.get_all_persons()
    
    matches = [p for p in persons if query.lower() in p['name'].lower()]
    
    if not matches:
        print(f"\n📋 No persons found matching '{query}'")
        return
    
    print(f"\n📋 Found {len(matches)} match(es) for '{query}':")
    print("-"*60)
    
    for person in matches:
        print(f"ID: {person['id']:<6} Name: {person['name']}")
    
    print("-"*60 + "\n")


def export_database(db_manager: DatabaseManager, output_file: str):
    """Export database to JSON file."""
    persons = db_manager.get_all_persons()
    
    if not persons:
        print("\n❌ Database is empty, nothing to export.")
        return
    
    # Remove binary data for JSON export
    export_data = {
        'persons': persons,
        'total_count': len(persons)
    }
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n✓ Exported {len(persons)} person(s) to {output_file}")


def get_statistics(db_manager: DatabaseManager):
    """Display database statistics."""
    persons = db_manager.get_all_persons()
    encodings, person_ids, names = db_manager.get_all_encodings()
    
    total_persons = len(persons)
    total_encodings = len(encodings)
    avg_encodings = total_encodings / total_persons if total_persons > 0 else 0
    
    # Count persons with/without last_seen
    seen_count = sum(1 for p in persons if p['last_seen'])
    never_seen_count = total_persons - seen_count
    
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    print(f"Total Persons:           {total_persons}")
    print(f"Total Face Encodings:    {total_encodings}")
    print(f"Avg Encodings/Person:    {avg_encodings:.1f}")
    print(f"Persons Seen:            {seen_count}")
    print(f"Persons Never Seen:      {never_seen_count}")
    print("="*60 + "\n")


def backup_database(db_path: str, backup_path: str):
    """Create a backup of the database file."""
    import shutil
    from datetime import datetime
    
    if not os.path.exists(db_path):
        print(f"\n❌ Database file not found: {db_path}")
        return
    
    # Generate backup filename with timestamp
    if not backup_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"faces_backup_{timestamp}.db")
    
    shutil.copy2(db_path, backup_path)
    print(f"\n✓ Database backed up to: {backup_path}")


def main():
    """Main database management entry point."""
    parser = argparse.ArgumentParser(
        description='Database Management Utility for Face Recognition System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_database.py --list                    # List all persons
  python manage_database.py --view 1                  # View person ID 1
  python manage_database.py --search "John"           # Search by name
  python manage_database.py --delete 1                # Delete person ID 1
  python manage_database.py --export persons.json     # Export to JSON
  python manage_database.py --stats                   # Show statistics
  python manage_database.py --backup                  # Create backup
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all registered persons'
    )
    
    parser.add_argument(
        '--view',
        type=int,
        metavar='ID',
        help='View detailed information for person ID'
    )
    
    parser.add_argument(
        '--delete',
        type=int,
        metavar='ID',
        help='Delete person by ID'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        metavar='QUERY',
        help='Search for persons by name'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        metavar='FILE',
        help='Export database to JSON file'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display database statistics'
    )
    
    parser.add_argument(
        '--backup',
        nargs='?',
        const='',
        metavar='FILE',
        help='Create database backup'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    db_manager = DatabaseManager(config['database']['path'])
    
    # Execute commands
    if args.list:
        list_persons(db_manager)
    
    elif args.view is not None:
        view_person(db_manager, args.view)
    
    elif args.delete is not None:
        delete_person(db_manager, args.delete, args.force)
    
    elif args.search:
        search_person(db_manager, args.search)
    
    elif args.export:
        export_database(db_manager, args.export)
    
    elif args.stats:
        get_statistics(db_manager)
    
    elif args.backup is not None:
        backup_database(config['database']['path'], args.backup)
    
    else:
        # No arguments, show interactive menu
        print("\n" + "="*60)
        print("🗄️  DATABASE MANAGEMENT UTILITY")
        print("="*60)
        print("1. List all persons")
        print("2. View person details")
        print("3. Search by name")
        print("4. Delete person")
        print("5. Show statistics")
        print("6. Export database")
        print("7. Backup database")
        print("8. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            list_persons(db_manager)
        elif choice == '2':
            person_id = int(input("Enter person ID: "))
            view_person(db_manager, person_id)
        elif choice == '3':
            query = input("Enter search query: ")
            search_person(db_manager, query)
        elif choice == '4':
            person_id = int(input("Enter person ID to delete: "))
            delete_person(db_manager, person_id)
        elif choice == '5':
            get_statistics(db_manager)
        elif choice == '6':
            output_file = input("Enter output filename (e.g., persons.json): ")
            export_database(db_manager, output_file)
        elif choice == '7':
            backup_database(config['database']['path'], '')
        elif choice == '8':
            print("Goodbye!")
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
