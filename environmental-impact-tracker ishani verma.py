import datetime
import json
import os
from collections import defaultdict

class EnvironmentalTracker:
    def __init__(self):
        self.activities = []
        
        # Carbon emission factors (kg CO2 per unit)
        self.emission_factors = {
            'car': 0.171,        # kg CO2 per km
            'bus': 0.089,        # kg CO2 per km
            'train': 0.041,      # kg CO2 per km
            'bike': 0,           # kg CO2 per km
            'walk': 0,           # kg CO2 per km
            'electricity': 0.475, # kg CO2 per kWh
            'waste': 0.5         # kg CO2 per kg waste
        }
    
    def add_transport_activity(self, transport_type, distance):
        """Add a transportation activity"""
        if transport_type not in ['car', 'bus', 'train', 'bike', 'walk']:
            print("❌ Invalid transportation type!")
            return
        
        emissions = self.emission_factors[transport_type] * distance
        activity = {
            'type': 'transport',
            'subtype': transport_type,
            'distance': distance,
            'emissions': emissions,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        
        self.activities.append(activity)
        print(f"✅ Added: {transport_type.capitalize()} - {distance} km ({emissions:.2f} kg CO2)")
    
    def add_electricity_activity(self, kwh):
        """Add electricity usage activity"""
        emissions = self.emission_factors['electricity'] * kwh
        activity = {
            'type': 'electricity',
            'kwh': kwh,
            'emissions': emissions,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        
        self.activities.append(activity)
        print(f"✅ Added: Electricity - {kwh} kWh ({emissions:.2f} kg CO2)")
    
    def add_water_activity(self, litres):
        """Add water usage activity"""
        activity = {
            'type': 'water',
            'litres': litres,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        
        self.activities.append(activity)
        print(f"✅ Added: Water usage - {litres} litres")
    
    def add_waste_activity(self, kg):
        """Add waste generation activity"""
        emissions = self.emission_factors['waste'] * kg
        activity = {
            'type': 'waste',
            'kg': kg,
            'emissions': emissions,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        
        self.activities.append(activity)
        print(f"✅ Added: Waste - {kg} kg ({emissions:.2f} kg CO2)")
    
    def calculate_carbon_footprint(self):
        """Calculate total carbon footprint"""
        total = sum(activity.get('emissions', 0) for activity in self.activities)
        return round(total, 2)
    
    def calculate_water_usage(self):
        """Calculate total water usage"""
        total = sum(activity.get('litres', 0) for activity in self.activities 
                   if activity['type'] == 'water')
        return round(total, 2)
    
    def view_summary(self):
        """Display summary of environmental impact"""
        print("\n" + "=" * 60)
        print(" " * 15 + "ENVIRONMENTAL IMPACT SUMMARY")
        print("=" * 60)
        print(f"🌍 Total Carbon Footprint: {self.calculate_carbon_footprint()} kg CO2")
        print(f"💧 Total Water Usage: {self.calculate_water_usage()} litres")
        print(f"📊 Total Activities Logged: {len(self.activities)} activities")
        
        # Additional statistics
        transport_count = sum(1 for a in self.activities if a['type'] == 'transport')
        electricity_count = sum(1 for a in self.activities if a['type'] == 'electricity')
        water_count = sum(1 for a in self.activities if a['type'] == 'water')
        waste_count = sum(1 for a in self.activities if a['type'] == 'waste')
        
        print(f"\n📈 Activity Breakdown:")
        print(f"   🚗 Transport: {transport_count}")
        print(f"   ⚡ Electricity: {electricity_count}")
        print(f"   💧 Water: {water_count}")
        print(f"   🗑️  Waste: {waste_count}")
        print("=" * 60 + "\n")
    
    def view_activities(self):
        """Display all logged activities"""
        if not self.activities:
            print("\n❌ No activities logged yet!\n")
            return
        
        print("\n" + "=" * 60)
        print(" " * 20 + "ACTIVITY LOG")
        print("=" * 60)
        
        for i, activity in enumerate(self.activities, 1):
            print(f"\n{i}. Date: {activity['date']}")
            
            if activity['type'] == 'transport':
                print(f"   Type: Transportation ({activity['subtype'].capitalize()})")
                print(f"   Distance: {activity['distance']} km")
                print(f"   Emissions: {activity['emissions']:.2f} kg CO2")
            
            elif activity['type'] == 'electricity':
                print(f"   Type: Electricity Usage")
                print(f"   Consumption: {activity['kwh']} kWh")
                print(f"   Emissions: {activity['emissions']:.2f} kg CO2")
            
            elif activity['type'] == 'water':
                print(f"   Type: Water Usage")
                print(f"   Amount: {activity['litres']} litres")
            
            elif activity['type'] == 'waste':
                print(f"   Type: Waste Generation")
                print(f"   Amount: {activity['kg']} kg")
                print(f"   Emissions: {activity['emissions']:.2f} kg CO2")
        
        print("\n" + "=" * 60 + "\n")
    
    def get_suggestions(self):
        """Generate sustainability suggestions based on tracked data"""
        carbon = self.calculate_carbon_footprint()
        water_usage = self.calculate_water_usage()
        suggestions = []
        
        # Carbon footprint suggestions
        if carbon > 50:
            suggestions.append("🚌 Your carbon footprint is high! Consider using public transport or cycling more often")
            suggestions.append("💡 Reduce electricity usage by turning off unused devices")
        elif carbon > 10:
            suggestions.append("🚶 Try to walk or bike for short distances to reduce emissions")
            suggestions.append("💡 Switch to LED bulbs and energy-efficient appliances")
        
        # Water usage suggestions
        if water_usage > 500:
            suggestions.append("🚿 Your water usage is high! Take shorter showers to conserve water")
            suggestions.append("🔧 Fix any leaking taps in your home")
        elif water_usage > 100:
            suggestions.append("💧 Consider collecting rainwater for plants")
            suggestions.append("🚰 Turn off taps while brushing teeth or washing dishes")
        
        # Waste suggestions
        if any(a['type'] == 'waste' for a in self.activities):
            total_waste = sum(a.get('kg', 0) for a in self.activities if a['type'] == 'waste')
            if total_waste > 10:
                suggestions.append("♻️  Practice recycling and composting to reduce waste")
                suggestions.append("🛍️  Use reusable bags and containers")
        
        # Transport-specific suggestions
        car_activities = [a for a in self.activities if a.get('subtype') == 'car']
        if len(car_activities) > 5:
            suggestions.append("🚗 Consider carpooling or using public transport for your commute")
        
        # Positive reinforcement
        if not suggestions:
            suggestions.append("🌟 Great job! Keep maintaining your eco-friendly habits")
            suggestions.append("🌱 You're making a positive impact on the environment!")
        
        return suggestions
    
    def show_suggestions(self):
        """Display sustainability suggestions"""
        print("\n" + "=" * 60)
        print(" " * 15 + "SUSTAINABILITY SUGGESTIONS")
        print("=" * 60)
        
        suggestions = self.get_suggestions()
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        print("=" * 60 + "\n")
    
    def delete_activity(self, index):
        """Delete an activity by index (1-based)"""
        if 1 <= index <= len(self.activities):
            deleted = self.activities.pop(index - 1)
            print(f"✅ Deleted activity from {deleted['date']}")
        else:
            print("❌ Invalid activity index!")
    
    def save_to_file(self, filename='environmental_data.json'):
        """Save activities to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.activities, f, indent=2)
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def load_from_file(self, filename='environmental_data.json'):
        """Load activities from a JSON file"""
        try:
            with open(filename, 'r') as f:
                self.activities = json.load(f)
            print(f"✅ Data loaded from {filename} ({len(self.activities)} activities)")
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except json.JSONDecodeError:
            print(f"❌ Error reading file - invalid JSON format!")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def view_statistics(self):
        """Display detailed statistics"""
        if not self.activities:
            print("\n❌ No data available for statistics!\n")
            return
        
        print("\n" + "=" * 60)
        print(" " * 18 + "DETAILED STATISTICS")
        print("=" * 60)
        
        # Calculate statistics by type
        stats = defaultdict(lambda: {'count': 0, 'total': 0, 'emissions': 0})
        
        for activity in self.activities:
            activity_type = activity['type']
            stats[activity_type]['count'] += 1
            stats[activity_type]['emissions'] += activity.get('emissions', 0)
            
            if activity_type == 'transport':
                stats[activity_type]['total'] += activity.get('distance', 0)
            elif activity_type == 'electricity':
                stats[activity_type]['total'] += activity.get('kwh', 0)
            elif activity_type == 'water':
                stats[activity_type]['total'] += activity.get('litres', 0)
            elif activity_type == 'waste':
                stats[activity_type]['total'] += activity.get('kg', 0)
        
        # Display statistics
        for activity_type, data in stats.items():
            print(f"\n📊 {activity_type.upper()}:")
            print(f"   Activities: {data['count']}")
            
            if activity_type == 'transport':
                print(f"   Total Distance: {data['total']:.2f} km")
            elif activity_type == 'electricity':
                print(f"   Total Consumption: {data['total']:.2f} kWh")
            elif activity_type == 'water':
                print(f"   Total Usage: {data['total']:.2f} litres")
            elif activity_type == 'waste':
                print(f"   Total Waste: {data['total']:.2f} kg")
            
            if data['emissions'] > 0:
                print(f"   Total Emissions: {data['emissions']:.2f} kg CO2")
        
        print("\n" + "=" * 60 + "\n")
    
    def compare_with_average(self):
        """Compare your impact with average values"""
        carbon = self.calculate_carbon_footprint()
        water = self.calculate_water_usage()
        
        # Average daily values (approximate)
        avg_daily_carbon = 11.0  # kg CO2 per day (global average)
        avg_daily_water = 150    # litres per day (global average)
        
        print("\n" + "=" * 60)
        print(" " * 12 + "COMPARISON WITH GLOBAL AVERAGES")
        print("=" * 60)
        
        print(f"\n🌍 Carbon Footprint:")
        print(f"   Your Total: {carbon:.2f} kg CO2")
        print(f"   Daily Average: {avg_daily_carbon:.2f} kg CO2")
        
        if carbon < avg_daily_carbon:
            print(f"   ✅ You're below average! Keep it up!")
        else:
            print(f"   ⚠️  You're above average. Try to reduce emissions.")
        
        print(f"\n💧 Water Usage:")
        print(f"   Your Total: {water:.2f} litres")
        print(f"   Daily Average: {avg_daily_water:.2f} litres")
        
        if water < avg_daily_water:
            print(f"   ✅ You're conserving water well!")
        else:
            print(f"   ⚠️  Consider reducing water consumption.")
        
        print("=" * 60 + "\n")
    
    def clear_all_data(self):
        """Clear all activities"""
        confirm = input("⚠️  Are you sure you want to delete all data? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.activities = []
            print("✅ All data cleared!")
        else:
            print("❌ Operation cancelled.")


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print(" " * 10 + "ENVIRONMENTAL IMPACT TRACKER - MAIN MENU")
    print("=" * 60)
    print("  1. Add transport activity")
    print("  2. Add electricity usage")
    print("  3. Add water usage")
    print("  4. Add waste generation")
    print("  5. View summary")
    print("  6. View activity log")
    print("  7. Get sustainability suggestions")
    print("  8. Delete activity")
    print("  9. Save data to file")
    print(" 10. Load data from file")
    print(" 11. View detailed statistics")
    print(" 12. Compare with global averages")
    print(" 13. Clear all data")
    print(" 14. Exit")
    print("=" * 60)


def main():
    """Main program function"""
    tracker = EnvironmentalTracker()
    
    print("\n" + "=" * 60)
    print("🌍 Welcome to Environmental Impact Tracker! 🌍")
    print("=" * 60)
    print("Track your carbon footprint and water usage for a sustainable future.")
    print("Every small action counts towards a better planet! 🌱")
    print("=" * 60)
    
    # Try to load existing data
    if os.path.exists('environmental_data.json'):
        load_prompt = input("\n📂 Found existing data file. Load it? (yes/no): ").strip().lower()
        if load_prompt == 'yes':
            tracker.load_from_file()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-14): ").strip()
        
        if choice == '1':
            print("\n" + "-" * 50)
            print("ADD TRANSPORT ACTIVITY")
            print("-" * 50)
            print("Options: car, bus, train, bike, walk")
            transport = input("Enter transport type: ").strip().lower()
            try:
                distance = float(input("Enter distance in km: "))
                if distance < 0:
                    print("❌ Distance cannot be negative!")
                else:
                    tracker.add_transport_activity(transport, distance)
            except ValueError:
                print("❌ Invalid distance value!")
        
        elif choice == '2':
            print("\n" + "-" * 50)
            print("ADD ELECTRICITY USAGE")
            print("-" * 50)
            try:
                kwh = float(input("Enter electricity consumption in kWh: "))
                if kwh < 0:
                    print("❌ Consumption cannot be negative!")
                else:
                    tracker.add_electricity_activity(kwh)
            except ValueError:
                print("❌ Invalid kWh value!")
        
        elif choice == '3':
            print("\n" + "-" * 50)
            print("ADD WATER USAGE")
            print("-" * 50)
            print("Reference: shower (5min) = 45-50L, dishwasher = 15-25L")
            try:
                litres = float(input("Enter water usage in litres: "))
                if litres < 0:
                    print("❌ Water usage cannot be negative!")
                else:
                    tracker.add_water_activity(litres)
            except ValueError:
                print("❌ Invalid water usage value!")
        
        elif choice == '4':
            print("\n" + "-" * 50)
            print("ADD WASTE GENERATION")
            print("-" * 50)
            try:
                kg = float(input("Enter waste amount in kg: "))
                if kg < 0:
                    print("❌ Waste amount cannot be negative!")
                else:
                    tracker.add_waste_activity(kg)
            except ValueError:
                print("❌ Invalid kg value!")
        
        elif choice == '5':
            tracker.view_summary()
        
        elif choice == '6':
            tracker.view_activities()
        
        elif choice == '7':
            tracker.show_suggestions()
        
        elif choice == '8':
            tracker.view_activities()
            if tracker.activities:
                try:
                    index = int(input("\nEnter activity number to delete: "))
                    tracker.delete_activity(index)
                except ValueError:
                    print("❌ Invalid activity index!")
        
        elif choice == '9':
            filename = input("Enter filename (press Enter for default 'environmental_data.json'): ").strip()
            if not filename:
                filename = 'environmental_data.json'
            tracker.save_to_file(filename)
        
        elif choice == '10':
            filename = input("Enter filename (press Enter for default 'environmental_data.json'): ").strip()
            if not filename:
                filename = 'environmental_data.json'
            tracker.load_from_file(filename)
        
        elif choice == '11':
            tracker.view_statistics()
        
        elif choice == '12':
            tracker.compare_with_average()
        
        elif choice == '13':
            tracker.clear_all_data()
        
        elif choice == '14':
            print("\n" + "=" * 60)
            print("🌿 Thank you for caring about the environment! 🌿")
            print("Remember: Every small action counts towards sustainability!")
            print("=" * 60 + "\n")
            
            # Ask to save before exiting
            if tracker.activities:
                save_prompt = input("💾 Do you want to save your data before exiting? (yes/no): ").strip().lower()
                if save_prompt == 'yes':
                    tracker.save_to_file()
            
            break
        
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 14.")


if __name__ == "__main__":
    main()
