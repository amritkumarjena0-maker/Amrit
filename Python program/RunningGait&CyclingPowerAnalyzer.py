import math
import matplotlib.pyplot as plt
import numpy as np

class RunningGaitAnalyzer:
    """Analyzes running gait metrics and biomechanics"""
    
    def __init__(self):
        self.gravity = 9.81
    
    def analyze_gait(self, stride_length, cadence, ground_contact_time, 
                     flight_time, vertical_oscillation, body_weight):
        """
        Analyze running gait metrics
        
        Parameters:
        - stride_length: length of stride (m)
        - cadence: steps per minute (spm)
        - ground_contact_time: time foot is on ground (ms)
        - flight_time: time both feet are off ground (ms)
        - vertical_oscillation: vertical movement of center of mass (cm)
        - body_weight: runner's weight (kg)
        """
        
        # Calculate speed
        speed = (stride_length * cadence) / 60  # m/s
        pace_min_per_km = 1000 / (speed * 60)  # min/km
        
        # Calculate stride rate (steps per second)
        stride_rate = cadence / 60
        
        # Calculate duty factor (% of stride in contact with ground)
        total_stride_time = (ground_contact_time + flight_time) / 1000  # convert to seconds
        duty_factor = (ground_contact_time / 1000) / total_stride_time * 100
        
        # Calculate vertical stiffness (simplified model)
        vertical_osc_m = vertical_oscillation / 100  # convert cm to m
        vertical_stiffness = (body_weight * self.gravity) / vertical_osc_m
        
        # Calculate ground reaction force (approximate)
        grf_multiplier = 2.5 if speed > 4 else 2.0  # higher for faster running
        peak_grf = body_weight * grf_multiplier
        
        # Calculate power (approximate)
        power = (body_weight * vertical_osc_m * self.gravity * stride_rate)
        
        # Efficiency metrics
        vertical_ratio = (vertical_oscillation / (stride_length * 100)) * 100
        
        # Classification
        gait_efficiency = self._classify_efficiency(vertical_ratio, ground_contact_time, cadence)
        injury_risk = self._assess_injury_risk(ground_contact_time, vertical_oscillation, cadence)
        
        results = {
            'speed_ms': round(speed, 2),
            'speed_kmh': round(speed * 3.6, 2),
            'pace_min_per_km': round(pace_min_per_km, 2),
            'duty_factor': round(duty_factor, 1),
            'vertical_stiffness': round(vertical_stiffness, 1),
            'peak_grf': round(peak_grf, 1),
            'power_watts': round(power, 1),
            'vertical_ratio': round(vertical_ratio, 2),
            'gait_efficiency': gait_efficiency,
            'injury_risk': injury_risk
        }
        
        return results
    
    def _classify_efficiency(self, vertical_ratio, gct, cadence):
        """Classify gait efficiency"""
        score = 0
        
        # Optimal ranges
        if 6 < vertical_ratio < 10:
            score += 1
        if 200 < gct < 250:
            score += 1
        if 170 < cadence < 190:
            score += 1
        
        if score == 3:
            return "Excellent"
        elif score == 2:
            return "Good"
        elif score == 1:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _assess_injury_risk(self, gct, vertical_osc, cadence):
        """Assess injury risk based on gait metrics"""
        risk_factors = 0
        
        if gct > 280:
            risk_factors += 1  # Long ground contact time
        if vertical_osc > 10:
            risk_factors += 1  # Excessive vertical oscillation
        if cadence < 160:
            risk_factors += 1  # Low cadence (overstriding)
        
        if risk_factors == 0:
            return "Low"
        elif risk_factors == 1:
            return "Moderate"
        else:
            return "High"
    
    def plot_gait_comparison(self, current_metrics, optimal_metrics):
        """Plot comparison between current and optimal gait metrics"""
        metrics = ['Cadence\n(spm)', 'Ground Contact\n(ms)', 'Vertical Osc\n(cm)', 
                   'Stride Length\n(m)']
        current = [current_metrics['cadence'], current_metrics['gct'], 
                   current_metrics['vo'], current_metrics['stride']]
        optimal = [optimal_metrics['cadence'], optimal_metrics['gct'], 
                   optimal_metrics['vo'], optimal_metrics['stride']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, current, width, label='Your Gait', color='#3498db')
        bars2 = ax.bar(x + width/2, optimal, width, label='Optimal Range', color='#2ecc71')
        
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title('Running Gait Analysis Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()


class CyclingPowerAnalyzer:
    """Analyzes cycling power output and performance metrics"""
    
    def __init__(self):
        self.air_density = 1.225  # kg/m³
        self.gravity = 9.81
    
    def calculate_power(self, speed_kmh, weight_kg, bike_weight=8, 
                       gradient=0, crr=0.004, cda=0.32, wind_speed=0):
        """
        Calculate cycling power requirements
        
        Parameters:
        - speed_kmh: cycling speed (km/h)
        - weight_kg: rider weight (kg)
        - bike_weight: bike weight (kg, default 8)
        - gradient: road gradient (%, positive = uphill)
        - crr: coefficient of rolling resistance (default 0.004)
        - cda: drag coefficient × frontal area (m², default 0.32)
        - wind_speed: headwind speed (km/h, positive = headwind)
        """
        
        speed_ms = speed_kmh / 3.6
        wind_ms = wind_speed / 3.6
        total_weight = weight_kg + bike_weight
        
        # Power components
        # 1. Rolling resistance
        grade_radians = math.atan(gradient / 100)
        rolling_resistance = crr * total_weight * self.gravity * math.cos(grade_radians) * speed_ms
        
        # 2. Air resistance
        relative_speed = speed_ms + wind_ms
        air_resistance = 0.5 * self.air_density * cda * (relative_speed ** 3)
        
        # 3. Gravitational resistance (climbing)
        climbing_power = total_weight * self.gravity * math.sin(grade_radians) * speed_ms
        
        # Total power
        total_power = rolling_resistance + air_resistance + climbing_power
        
        # Account for drivetrain losses (typically 2-5%)
        drivetrain_efficiency = 0.97
        power_at_pedals = total_power / drivetrain_efficiency
        
        results = {
            'total_power': round(total_power, 1),
            'power_at_pedals': round(power_at_pedals, 1),
            'rolling_resistance': round(rolling_resistance, 1),
            'air_resistance': round(air_resistance, 1),
            'climbing_power': round(climbing_power, 1),
            'power_to_weight': round(power_at_pedals / weight_kg, 2),
            'speed_ms': round(speed_ms, 2)
        }
        
        return results
    
    def analyze_ftp(self, ftp, weight):
        """
        Analyze Functional Threshold Power
        
        Parameters:
        - ftp: Functional Threshold Power (watts)
        - weight: rider weight (kg)
        """
        
        w_per_kg = ftp / weight
        
        # Power zones (based on Coggan's training zones)
        zones = {
            'Active Recovery': (0, 0.55 * ftp),
            'Endurance': (0.55 * ftp, 0.75 * ftp),
            'Tempo': (0.75 * ftp, 0.90 * ftp),
            'Lactate Threshold': (0.90 * ftp, 1.05 * ftp),
            'VO2 Max': (1.05 * ftp, 1.20 * ftp),
            'Anaerobic': (1.20 * ftp, 1.50 * ftp),
            'Neuromuscular': (1.50 * ftp, float('inf'))
        }
        
        # Performance classification
        if w_per_kg >= 5.0:
            classification = "World Class / Professional"
        elif w_per_kg >= 4.0:
            classification = "Excellent / Cat 1-2"
        elif w_per_kg >= 3.5:
            classification = "Very Good / Cat 3"
        elif w_per_kg >= 3.0:
            classification = "Good / Cat 4"
        elif w_per_kg >= 2.5:
            classification = "Fair / Recreational"
        else:
            classification = "Beginner"
        
        results = {
            'ftp': ftp,
            'w_per_kg': round(w_per_kg, 2),
            'classification': classification,
            'zones': zones
        }
        
        return results
    
    def plot_power_zones(self, ftp_results):
        """Plot power training zones"""
        zones = ftp_results['zones']
        zone_names = list(zones.keys())
        zone_ranges = [zones[z][1] - zones[z][0] for z in zone_names[:-1]]
        zone_ranges.append(ftp_results['ftp'] * 0.5)  # Cap neuromuscular
        
        colors = ['#95a5a6', '#3498db', '#f39c12', '#e74c3c', '#9b59b6', '#e67e22', '#c0392b']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bottom = 0
        for i, (name, range_val) in enumerate(zip(zone_names, zone_ranges)):
            ax.barh(0, range_val, left=bottom, height=0.5, 
                   label=f"{name}", color=colors[i], edgecolor='white', linewidth=2)
            bottom += range_val
        
        ax.set_yticks([])
        ax.set_xlabel('Power (Watts)', fontsize=12)
        ax.set_title(f'Cycling Power Zones (FTP: {ftp_results["ftp"]}W, {ftp_results["w_per_kg"]} W/kg)', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.show()


def main():
    print("="*60)
    print("SPORTS BIOMECHANICS ANALYZER")
    print("="*60)
    print("\nChoose Analysis Type:")
    print("1. Running Gait Analysis")
    print("2. Cycling Power Output Analysis")
    
    choice = input("\nSelect (1-2): ")
    
    if choice == '1':
        print("\n" + "="*60)
        print("RUNNING GAIT ANALYSIS")
        print("="*60)
        
        analyzer = RunningGaitAnalyzer()
        
        try:
            stride_length = float(input("\nStride length (m) [typical: 1.0-1.6]: "))
            cadence = float(input("Cadence (steps/min) [typical: 160-180]: "))
            gct = float(input("Ground contact time (ms) [typical: 200-250]: "))
            flight_time = float(input("Flight time (ms) [typical: 80-120]: "))
            vertical_osc = float(input("Vertical oscillation (cm) [typical: 6-10]: "))
            body_weight = float(input("Body weight (kg): "))
            
            results = analyzer.analyze_gait(stride_length, cadence, gct, 
                                          flight_time, vertical_osc, body_weight)
            
            print("\n" + "="*60)
            print("GAIT ANALYSIS RESULTS")
            print("="*60)
            print(f"Speed:                  {results['speed_ms']} m/s ({results['speed_kmh']} km/h)")
            print(f"Pace:                   {results['pace_min_per_km']} min/km")
            print(f"Duty Factor:            {results['duty_factor']}%")
            print(f"Vertical Stiffness:     {results['vertical_stiffness']} N/m")
            print(f"Peak Ground Force:      {results['peak_grf']} N")
            print(f"Power Output:           {results['power_watts']} W")
            print(f"Vertical Ratio:         {results['vertical_ratio']}%")
            print(f"\nGait Efficiency:        {results['gait_efficiency']}")
            print(f"Injury Risk:            {results['injury_risk']}")
            print("="*60)
            
            print("\nRECOMMENDATIONS:")
            if results['gait_efficiency'] != "Excellent":
                print("• Aim for cadence between 170-180 spm")
                print("• Reduce vertical oscillation to 6-9 cm")
                print("• Keep ground contact time under 250 ms")
            
            if results['injury_risk'] != "Low":
                print("• Consider gait retraining")
                print("• Focus on landing under center of mass")
                print("• Strengthen hip and core muscles")
            
            # Plot option
            plot = input("\nPlot gait comparison? (y/n): ")
            if plot.lower() == 'y':
                current = {'cadence': cadence, 'gct': gct, 'vo': vertical_osc, 'stride': stride_length}
                optimal = {'cadence': 180, 'gct': 220, 'vo': 8, 'stride': 1.3}
                analyzer.plot_gait_comparison(current, optimal)
        
        except ValueError:
            print("Invalid input!")
    
    elif choice == '2':
        print("\n" + "="*60)
        print("CYCLING POWER ANALYSIS")
        print("="*60)
        
        analyzer = CyclingPowerAnalyzer()
        
        sub_choice = input("\n1. Calculate Power Requirements\n2. Analyze FTP Zones\n\nSelect (1-2): ")
        
        if sub_choice == '1':
            try:
                speed = float(input("\nSpeed (km/h) [typical: 25-40]: "))
                weight = float(input("Rider weight (kg): "))
                bike_weight = float(input("Bike weight (kg) [default: 8]: ") or 8)
                gradient = float(input("Gradient (%) [0=flat, positive=uphill]: ") or 0)
                wind = float(input("Headwind (km/h) [0=no wind]: ") or 0)
                
                results = analyzer.calculate_power(speed, weight, bike_weight, 
                                                  gradient, wind_speed=wind)
                
                print("\n" + "="*60)
                print("POWER ANALYSIS RESULTS")
                print("="*60)
                print(f"Total Power Required:   {results['total_power']} W")
                print(f"Power at Pedals:        {results['power_at_pedals']} W")
                print(f"Power-to-Weight:        {results['power_to_weight']} W/kg")
                print(f"\nPower Breakdown:")
                print(f"  Rolling Resistance:   {results['rolling_resistance']} W ({results['rolling_resistance']/results['total_power']*100:.1f}%)")
                print(f"  Air Resistance:       {results['air_resistance']} W ({results['air_resistance']/results['total_power']*100:.1f}%)")
                print(f"  Climbing:             {results['climbing_power']} W ({results['climbing_power']/results['total_power']*100:.1f}%)")
                print("="*60)
                
            except ValueError:
                print("Invalid input!")
        
        elif sub_choice == '2':
            try:
                ftp = float(input("\nFunctional Threshold Power (watts): "))
                weight = float(input("Rider weight (kg): "))
                
                results = analyzer.analyze_ftp(ftp, weight)
                
                print("\n" + "="*60)
                print("FTP ANALYSIS RESULTS")
                print("="*60)
                print(f"FTP:                    {results['ftp']} W")
                print(f"Power-to-Weight:        {results['w_per_kg']} W/kg")
                print(f"Classification:         {results['classification']}")
                print(f"\nTraining Zones:")
                for zone, (low, high) in results['zones'].items():
                    if high == float('inf'):
                        print(f"  {zone:20s} {low:.0f}+ W")
                    else:
                        print(f"  {zone:20s} {low:.0f}-{high:.0f} W")
                print("="*60)
                
                plot = input("\nPlot power zones? (y/n): ")
                if plot.lower() == 'y':
                    analyzer.plot_power_zones(results)
                
            except ValueError:
                print("Invalid input!")
    
    else:
        print("Invalid choice!")
    
    # Repeat option
    again = input("\nAnalyze another metric? (y/n): ")
    if again.lower() == 'y':
        main()


if __name__ == "__main__":
    main()
