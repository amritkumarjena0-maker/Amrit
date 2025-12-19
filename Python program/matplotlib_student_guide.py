import matplotlib.pyplot as plt
import numpy as np

# Example 1: Simple Line Plot
print("Example 1: Simple Line Plot")
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', color='blue', linewidth=2)
plt.title('Simple Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()

# Example 2: Bar Chart (Student Grades)
print("\nExample 2: Bar Chart - Student Grades")
subjects = ['Math', 'Science', 'English', 'History', 'Art']
marks = [85, 92, 78, 88, 95]

plt.figure(figsize=(8, 5))
plt.bar(subjects, marks, color='green', alpha=0.7)
plt.title("Mark's Grades by Subject")
plt.xlabel('Subjects')
plt.ylabel('Marks')
plt.ylim(0, 100)
plt.show()

# Example 3: Multiple Lines
print("\nExample 3: Multiple Lines Plot")
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y1, label='sin(x)', color='red')
plt.plot(x, y2, label='cos(x)', color='blue')
plt.title('Sine and Cosine Functions')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

# Example 4: Scatter Plot
print("\nExample 4: Scatter Plot")
x = np.random.rand(50) * 10
y = np.random.rand(50) * 10

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='purple', alpha=0.6, s=100)
plt.title('Scatter Plot Example')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.grid(True)
plt.show()

# Example 5: Pie Chart (Time Management)
print("\nExample 5: Pie Chart - Daily Activities")
activities = ['Study', 'Sleep', 'Sports', 'Entertainment', 'Other']
hours = [6, 8, 2, 4, 4]
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

plt.figure(figsize=(8, 8))
plt.pie(hours, labels=activities, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Daily Time Distribution')
plt.show()

# Example 6: Subplots (Multiple plots in one figure)
print("\nExample 6: Subplots")
x = np.linspace(0, 2*np.pi, 100)

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

axs[0, 0].plot(x, np.sin(x), 'r')
axs[0, 0].set_title('Sine Wave')

axs[0, 1].plot(x, np.cos(x), 'g')
axs[0, 1].set_title('Cosine Wave')

axs[1, 0].plot(x, np.tan(x), 'b')
axs[1, 0].set_title('Tangent Wave')
axs[1, 0].set_ylim(-5, 5)

axs[1, 1].plot(x, x**2, 'm')
axs[1, 1].set_title('Quadratic Function')

plt.tight_layout()
plt.show()

print("\nMatplotlib Tutorial Complete!")
print("Try modifying the values to create your own visualizations!")
