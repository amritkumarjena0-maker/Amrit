import math
import matplotlib.pyplot as plt

class ProjectileMotion:
    def __init__(self, sport='basketball'):
        self.g = 9.81  # gravity
        self.rho = 1.225  # air density
        
        # Sport configurations
        self.sports = {
            'basketball': {
                'name': 'Basketball',
                'drag_coeff': 0.47,
                'mass': 0.624,
                'area': 0.0455,
                'target_height': 3.05,
                'target_distance': 6.75
            },
            'javelin': {
                'name': 'Javelin',
                'drag_coeff': 0.25,
                'mass': 0.8,
                'area': 0.0065,
                'target_height': 0,
                'target_distance': 70
            },
            'soccer': {
                'name': 'Soccer Ball',
                'drag_coeff': 0.25,
                'mass': 0.43,
                'area': 0.0388,
                'target_height': 2.44,
                'target_distance': 20
            }
        }
        
        self.set_sport(sport)
    
    def set_sport(self, sport):
        if sport in self.sports:
            self.config = self.sports[sport]
            self.sport_name = self.config['name']
        else:
            print(f"Unknown sport. Using basketball.")
            self.config = self.sports['basketball']
            self.sport_name = self.config['name']
    
    def calculate_trajectory(self, velocity, angle, height=2.0, wind_speed=0.0):
        """
        Calculate projectile trajectory with air resistance
        
        Parameters:
        - velocity: initial velocity (m/s)
        - angle: launch angle (degrees)
        - height: initial height (m)
        - wind_speed: wind speed (m/s, positive = tailwind)
        """
        dt = 0.01
        rad = math.radians(angle)
        
        # Initial velocities
        vx = velocity * math.cos(rad)
        vy = velocity * math.sin(rad)
        x = 0
        y = height
        
        # Data storage
        trajectory = {'x': [], 'y': []}
        max_height = height
        time_of_flight = 0
        
        # Simulation loop
        while y >= 0 and x < 200:
            trajectory['x'].append(x)
            trajectory['y'].append(y)
            
            # Calculate drag force
            v = math.sqrt(vx**2 + vy**2)
            if v > 0:
                drag_force = 0.5 * self.rho * self.config['area'] * self.config['drag_coeff'] * v**2
                
                # Acceleration from drag
                ax = -(drag_force / self.config['mass']) * (vx / v) - (wind_speed * 0.3 / self.config['mass'])
                ay = -self.g - (drag_force / self.config['mass']) * (vy / v)
            else:
                ax = 0
                ay = -self.g
            
            # Update velocities and positions
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt
            
            time_of_flight += dt
            if y > max_height:
                max_height = y
        
        # Check if target was hit
        target_x = self.config['target_distance']
        target_y = self.config['target_height']
        hit_target = False
        
        for i in range(len(trajectory['x'])):
            if abs(trajectory['x'][i] - target_x) < 0.5 and abs(trajectory['y'][i] - target_y) < 0.5:
                hit_target = True
                break
        
        results = {
            'trajectory': trajectory,
            'max_height': round(max_height, 2),
            'range': round(x, 2),
            'time_of_flight': round(time_of_flight, 2),
            'hit_target': hit_target,
            'target_x': target_x,
            'target_y': target_y
        }
        
        return results
    
    def plot_trajectory(self, results):
        """Plot the trajectory"""
        plt.figure(figsize=(12, 6))
        
        # Plot trajectory
        plt.plot(results['trajectory']['x'], results['trajectory']['y'], 
                'b-', linewidth=2, label='Projectile Path')
        
        # Plot target
        plt.axvline(x=results['target_x'], color='r', linestyle='--', 
                   alpha=0.5, label=f'Target X ({results["target_x"]}m)')
        plt.axhline(y=results['target_y'], color='r', linestyle='--', 
                   alpha=0.5, label=f'Target Y ({results["target_y"]}m)')
        
        # Mark target point
        plt.plot(results['target_x'], results['target_y'], 'r*', 
                markersize=20, label='Target')
        
        plt.xlabel('Distance (m)', fontsize=12)
        plt.ylabel('Height (m)', fontsize=12)
        plt.title(f'{self.sport_name} Projectile Motion', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def print_results(self, results):
        """Print results in a formatted way"""
        print(f"\n{'='*50}")
        print(f"{self.sport_name.upper()} PROJECTILE MOTION RESULTS")
        print(f"{'='*50}")
        print(f"Maximum Height:    {results['max_height']} m")
        print(f"Range:             {results['range']} m")
        print(f"Time of Flight:    {results['time_of_flight']} s")
        print(f"Target Hit:        {'YES ✓' if results['hit_target'] else 'NO ✗'}")
        print(f"Target Location:   ({results['target_x']}m, {results['target_y']}m)")
        print(f"{'='*50}\n")


def main():
    print("SPORTS PROJECTILE MOTION CALCULATOR")
    print("="*50)
    
    # Choose sport
    print("\nAvailable Sports:")
    print("1. Basketball")
    print("2. Javelin")
    print("3. Soccer")
    
    choice = input("\nSelect sport (1-3): ")
    sport_map = {'1': 'basketball', '2': 'javelin', '3': 'soccer'}
    sport = sport_map.get(choice, 'basketball')
    
    calc = ProjectileMotion(sport)
    
    # Get input parameters
    try:
        velocity = float(input(f"\nInitial velocity (m/s) [5-30]: "))
        angle = float(input("Launch angle (degrees) [10-80]: "))
        height = float(input("Release height (m) [0-3]: "))
        wind_speed = float(input("Wind speed (m/s) [-5 to 5, negative=headwind]: "))
    except ValueError:
        print("Invalid input! Using default values.")
        velocity = 10
        angle = 45
        height = 2
        wind_speed = 0
    
    # Calculate trajectory
    results = calc.calculate_trajectory(velocity, angle, height, wind_speed)
    
    # Display results
    calc.print_results(results)
    
    # Plot trajectory
    plot_choice = input("Plot trajectory? (y/n): ")
    if plot_choice.lower() == 'y':
        calc.plot_trajectory(results)
    
    # Option to try again
    again = input("\nCalculate another trajectory? (y/n): ")
    if again.lower() == 'y':
        main()


if __name__ == "__main__":
    main()
