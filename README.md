# Environmental-tracker
import datetime
import json

class EnvironmentalTracker:
    def _init_(self):
        self.activities = []
        self.emission_factors = {
            'car': 0.171,
            'bus': 0.089,
            'train': 0.041,
            'bike': 0,
            'walk': 0,
            'electricity': 0.475,
            'waste': 0.5
        }

    def add_transport_activity(self, transport_type, distance):
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

    def add_electricity_activity(self, kWh):
        emissions = self.emission_factors['electricity'] * kWh
        activity = {
            'type': 'electricity',
            'kWh': kWh,
            'emissions': emissions,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        self.activities.append(activity)
        print(f"✅ Added: Electricity - {kWh} kWh ({emissions:.2f} kg CO2)")

    def add_water_activity(self, litres):
        activity = {
            'type': 'water',
            'litres': litres,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        }
        self.activities.append(activity)
        print(f"✅ Added: Water Usage - {litres} litres")

    def add_waste_activity(self, kg):
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
        total = sum(a.get('emissions', 0) for a in self.activities)
        return round(total, 2)

    def calculate_water_usage(self):
        total = sum(a.get('litres', 0) for a in self.activities if a['type'] == 'water')
        return round(total, 2)

    def view_summary(self):
        print("\n" + "="*60)
        print("          🌍 ENVIRONMENTAL IMPACT SUMMARY")
        print("="*60)
        print(f"🌫 Total Carbon Footprint: {self.calculate_carbon_footprint()} kg CO2")
        print(f"💧 Total Water Usage: {self.calculate_water_usage()} litres")
        print(f"📊 Total Activities Logged: {len(self.activities)}")
        print("="*60 + "\n")

    def view_activities(self):
        if not self.activities:
            print("\n❌ No activities logged yet!\n")
            return

        print("\n" + "="*60)
        print("                 ACTIVITY LOG")
        print("="*60)

        for i, activity in enumerate(self.activities, 1):
            print(f"\n{i}. Date: {activity['date']}")

            if activity['type'] == 'transport':
                print(f" Type: Transport ({activity['subtype'].capitalize()})")
                print(f" Distance: {activity['distance']} km")
                print(f" Emissions: {activity['emissions']:.2f} kg CO2")

            elif activity['type'] == 'electricity':
                print(f" Type: Electricity")
                print(f" Consumption: {activity['kWh']} kWh")
                print(f" Emissions: {activity['emissions']:.2f} kg CO2")

            elif activity['type'] == 'water':
                print(f" Type: Water")
                print(f" Usage: {activity['litres']} litres")

            elif activity['type'] == 'waste':
                print(f" Type: Waste")
                print(f" Amount: {activity['kg']} kg")
                print(f" Emissions: {activity['emissions']:.2f} kg CO2")

        print("\n" + "="*60 + "\n")

    def get_suggestions(self):
        suggestions = []
        carbon = self.calculate_carbon_footprint()
        water = self.calculate_water_usage()

        if carbon > 10:
            suggestions.append("🚌 Try using public transport or cycling more.")
            suggestions.append("💡 Reduce electricity use by turning off unused devices.")

        if water > 100:
            suggestions.append("🚿 Take shorter showers to save water.")
            suggestions.append("🔧 Fix leaks to reduce water loss.")

        if any(a['type'] == 'waste' for a in self.activities):
            suggestions.append("♻ Try recycling and reducing waste.")

        if not suggestions:
            suggestions.append("🌟 Great job! You're being eco-friendly.")

        return suggestions

    def show_suggestions(self):
        print("\n" + "="*60)
        print("         🌱 SUSTAINABILITY SUGGESTIONS")
        print("="*60)
        for s in self.get_suggestions():
            print(f"✅ {s}")
        print("="*60 + "\n")

    def delete_activity(self, index):
        if 0 <= index < len(self.activities):
            deleted = self.activities.pop(index)
            print(f"✅ Deleted activity from {deleted['date']}")
        else:
            print("❌ Invalid activity index!")

    def save_to_file(self, filename='environmental_data.json'):
        with open(filename, 'w') as f:
            json.dump(self.activities, f, indent=2)
        print(f"✅ Data saved to {filename}")

    def load_from_file(self, filename='environmental_data.json'):
        try:
            with open(filename, 'r') as f:
                self.activities = json.load(f)
            print(f"✅ Data loaded from {filename}")
        except FileNotFoundError:
            print("❌ File not found!")


# -------------------- MENU PROGRAM --------------------

def display_menu():
    print("\n🌍 ENVIRONMENTAL IMPACT TRACKER - MENU")
    print(" 1️⃣  Add transport activity")
    print(" 2️⃣  Add electricity usage")
    print(" 3️⃣  Add water usage")
    print(" 4️⃣  Add waste generation")
    print(" 5️⃣  View summary")
    print(" 6️⃣  View activity log")
    print(" 7️⃣  Get sustainability suggestions")
    print(" 8️⃣  Delete activity")
    print(" 9️⃣  Save data to file")
    print(" 🔟  Load data from file")
    print(" 0️⃣  Exit")
    print("-"*60)

def main():
    tracker = EnvironmentalTracker()

    print("\n🌱 Welcome to the Environmental Impact Tracker! 🌱")
    print("Track your daily footprint for a greener future.\n")

    while True:
        display_menu()
        choice = input("Enter your choice (0-10): ").strip()

        if choice == '1':
            print("\n-- Add Transport Activity --")
            transport = input("Enter type (car/bus/train/bike/walk): ").strip().lower()
            try:
                distance = float(input("Enter distance (km): "))
                tracker.add_transport_activity(transport, distance)
            except ValueError:
                print("❌ Invalid distance!")

        elif choice == '2':
            print("\n-- Add Electricity Usage --")
            try:
                kWh = float(input("Enter electricity usage (kWh): "))
                tracker.add_electricity_activity(kWh)
            except ValueError:
                print("❌ Invalid value!")

        elif choice == '3':
            print("\n-- Add Water Usage --")
            try:
                litres = float(input("Enter litres used: "))
                tracker.add_water_activity(litres)
            except ValueError:
                print("❌ Invalid value!")

        elif choice == '4':
            print("\n-- Add Waste Generation --")
            try:
                kg = float(input("Enter waste (kg): "))
                tracker.add_waste_activity(kg)
            except ValueError:
                print("❌ Invalid value!")

        elif choice == '5':
            tracker.view_summary()

        elif choice == '6':
            tracker.view_activities()

        elif choice == '7':
            tracker.show_suggestions()

        elif choice == '8':
            tracker.view_activities()
            try:
                index = int(input("Enter activity number to delete: ")) - 1
                tracker.delete_activity(index)
            except ValueError:
                print("❌ Invalid index!")

        elif choice == '9':
            filename = input("Enter filename (default: environmental_data.json): ").strip()
            if not filename:
                filename = 'environmental_data.json'
            tracker.save_to_file(filename)

        elif choice == '10':
            filename = input("Enter filename (default: environmental_data.json): ").strip()
            if not filename:
                filename = 'environmental_data.json'
            tracker.load_from_file(filename)

        elif choice == '0':
            print("\n🌿 Thank you for caring about the environment! 🌿")
            print("Every small action matters. 💚\n")
            break

        else:
            print("❌ Invalid choice! Please select from the menu.")

# Run the program
if _name_ == "_main_":
    main()
    
