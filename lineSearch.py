import math
import numpy as np
import matplotlib.pyplot as plt


created_functions = []


def create_function(expression, variables):
	"""Create a callable from a mathematical expression.

	Args:
		expression: An expression such as ``"sin(x) + y**2"``.
		variables: Variable names in the order expected by the returned
			function, such as ``["x", "y"]``.

	Returns:
		A function that accepts one positional argument per variable.
	"""
	variables = tuple(variable.strip() for variable in variables)
	if not variables or any(not variable.isidentifier() for variable in variables):
		raise ValueError("variables must contain valid Python names")
	if len(set(variables)) != len(variables):
		raise ValueError("variables must be unique")

	allowed_names = {
		name: getattr(np, name)
		for name in dir(np)
		if not name.startswith("_")
	}
	allowed_names.update(
		{
			name: getattr(math, name)
			for name in dir(math)
			if not name.startswith("_") and name not in allowed_names
		}
	)
	allowed_names.update({"np": np, "math": math})

	try:
		compiled_expression = compile(expression, "<user_function>", "eval")
	except SyntaxError as error:
		raise ValueError(f"Invalid mathematical expression: {error.msg}") from error

	invalid_names = set(compiled_expression.co_names) - set(allowed_names) - set(variables)
	if invalid_names:
		names = ", ".join(sorted(invalid_names))
		raise ValueError(f"Unsupported name(s) in expression: {names}")

	def user_function(*values):
		if len(values) != len(variables):
			raise TypeError(
				f"Expected {len(variables)} value(s), got {len(values)}"
			)
		scope = dict(allowed_names)
		scope.update(zip(variables, values))
		return eval(compiled_expression, {"__builtins__": {}}, scope)

	return user_function


def input_function():
	"""Prompt for a function, store it, and return a NumPy-ready callable."""
	expression = input("Enter a function, for example sin(x) + y**2: ")
	variable_text = input("Enter variable names separated by commas: ")
	variables = variable_text.split(",")
	function = np.vectorize(create_function(expression, variables))
	function.variables = tuple(variable.strip() for variable in variables)
	created_functions.append(function)
	return function


def read_point(name, variable_count):
	"""Read a vector point containing one value for each variable."""
	point = np.fromstring(
		input(
			f"Enter the {name} point as {variable_count} comma-separated "
			"value(s): "
		),
		sep=",",
	)
	if point.size != variable_count:
		raise ValueError(
			f"The {name} point must contain {variable_count} value(s)."
		)
	return point


def run_interactive():
	"""Run direct function evaluation or uniform search interactively."""
	choice = input(
		"Choose an operation: \n1) evaluate function \n2) uniform search \n3) golden section search \n4) dichotomous search \n5) bisection search \n6) Armijo's Rule (approximate minimizer!) \nYour choice: "
	).strip()
	if choice == "2":
		uniform_search()
		return
	if choice == "3":
		golden_section_search()
		return
	if choice == "4":
		dichotomous_search()
		return
	if choice == "5":
		bisection_search()
		return
	if choice == "6":
		armijo_rule()
		return
	if choice != "1":
		raise ValueError("Please choose a valid option from 1 to 5.")

	expression = input("Enter your function (for example, sin(x) + y**2): ")
	variables = [
		variable.strip()
		for variable in input("Enter variables separated by commas: ").split(",")
	]
	function = create_function(expression, variables)
	values = [
		float(input(f"Enter a value for {variable}: "))
		for variable in variables
	]

	result = function(*values)
	print(f"Result: {result}")

def uniform_search():
	"""Perform a uniform search using vector lower and upper bounds."""
	function = input_function()
	variable_count = len(function.variables)

	lower_bound = read_point("lower bound", variable_count)
	upper_bound = read_point("upper bound", variable_count)
	if np.any(lower_bound >= upper_bound):
		raise ValueError("Each lower-bound value must be less than its upper bound.")

	num_points = int(input("Enter the number of points to evaluate (uniform bracketing): "))
	max_iter = int(input("Enter the maximum number of iterations: "))
	current_min = upper_bound
	for iteration in range(max_iter):
		points = np.linspace(lower_bound, current_min, num_points)
		y_values = function(*points.T)
		min_index = np.argmin(y_values)
		min_point = points[min_index]
		min_y = np.min(y_values)
		next_index = min_index + 1
		current_min = (
			points[next_index]
			if next_index < num_points
			else upper_bound
		)

	print(f"Minimum found at {min_point}, f(x) = {min_y}")

	if variable_count == 1:
		plt.plot(points[:, 0], y_values, label="Function")
		plt.scatter(min_point[0], min_y, color="red", label="Minimum")
		plt.xlabel(function.variables[0])
		plt.ylabel("f(x)")
		plt.legend()
		plt.grid()
		plt.show()
	else:
		print("Plot omitted for a function with multiple variables.")
  
def dichotomous_search():
	"""Minimize a function with bounded coordinate-wise dichotomous search."""
	function = input_function()
	variable_count = len(function.variables)

	lower_bound = read_point("lower bound", variable_count)
	upper_bound = read_point("upper bound", variable_count)
	if np.any(lower_bound >= upper_bound):
		raise ValueError("Each lower-bound value must be less than its upper bound.")
	num_iterations = int(input("Enter the number of iterations: "))
	tolerance = float(input("Enter the tolerance for convergence: "))
	if num_iterations <= 0:
		raise ValueError("The number of iterations must be positive.")
	if not np.isfinite(tolerance) or tolerance <= 0:
		raise ValueError("The tolerance must be a finite positive number.")

	delta = tolerance / 10
	min_point = (lower_bound + upper_bound) / 2
	for _ in range(num_iterations):
		previous_point = min_point.copy()
		for coordinate in range(variable_count):
			left_bound = lower_bound[coordinate]
			right_bound = upper_bound[coordinate]
			while right_bound - left_bound > tolerance:
				mid_point = (left_bound + right_bound) / 2
				m1 = mid_point - delta
				m2 = mid_point + delta
				point1 = min_point.copy()
				point2 = min_point.copy()
				point1[coordinate] = m1
				point2[coordinate] = m2
				f1 = function(*point1)
				f2 = function(*point2)

				if f1 <= f2:
					right_bound = m2
				else:
					left_bound = m1

			min_point[coordinate] = (left_bound + right_bound) / 2

		if np.linalg.norm(min_point - previous_point) <= tolerance:
			break

	print(f"Minimum found at {min_point}, f(x) = {function(*min_point)}")
 
	if variable_count == 1:
		search_pyplot(
			function, min_point, function(*min_point), lower_bound, upper_bound
		)
	else:
		print("Plot omitted for a function with multiple variables.")

 
        
def golden_section_search():
	"""Perform a golden section search using vector lower and upper bounds."""
	function = input_function()
	variable_count = len(function.variables)

	lower_bound = read_point("lower bound", variable_count)
	upper_bound = read_point("upper bound", variable_count)
	if np.any(lower_bound >= upper_bound):
		raise ValueError("Each lower-bound value must be less than its upper bound.")
	num_iterations = int(input("Enter the number of iterations: "))
	tolerance = float(input("Enter the tolerance for convergence: "))

	phi = (1 + np.sqrt(5)) / 2  # Golden ratio
	resphi = 2 - phi

	for iteration in range(num_iterations):
		point1 = lower_bound + resphi * (upper_bound - lower_bound)
		point2 = upper_bound - resphi * (upper_bound - lower_bound)

		f1 = function(*point1)
		f2 = function(*point2)

		if f1 < f2:
			upper_bound = point2
		else:
			lower_bound = point1

		if np.linalg.norm(upper_bound - lower_bound) < tolerance:
			break

	min_point = (lower_bound + upper_bound) / 2
	min_y = function(*min_point)

	print(f"Minimum found at {min_point}, f(x) = {min_y}")

	if variable_count == 1:
		search_pyplot(function, min_point, min_y, lower_bound, upper_bound)
	else:
		print("Plot omitted for a function with multiple variables.")
        
def bisection_search():
	"""Perform a bisection search using vector lower and upper bounds."""
	function = input_function()
	variable_count = len(function.variables)

	lower_bound = read_point("lower bound", variable_count)
	upper_bound = read_point("upper bound", variable_count)
	if np.any(lower_bound >= upper_bound):
		raise ValueError("Each lower-bound value must be less than its upper bound.")
	num_iterations = int(input("Enter the number of iterations: "))
	tolerance = float(input("Enter the tolerance for convergence: "))

	for iteration in range(num_iterations):
		mid_point = (lower_bound + upper_bound) / 2
		f_mid = function(*mid_point)
		slope = (function(*mid_point + 1e-5) - function(*mid_point - 1e-5)) / (2 * 1e-5)  # central difference approximation

		if abs(f_mid) < tolerance:
			break

		if slope > 0:
			upper_bound = mid_point
		else:
			lower_bound = mid_point

	min_point = (lower_bound + upper_bound) / 2
	min_y = function(*min_point)

	print(f"Minimum found at {min_point}, f(x) = {min_y}")

	if variable_count == 1:
		search_pyplot(function, min_point, min_y, lower_bound, upper_bound)
	else:
		print("Plot omitted for a function with multiple variables.")
  
def armijo_rule():
	"""Find a sufficient-decrease step along a supplied search direction."""
	function = input_function()
	variable_count = len(function.variables)

	initial_point = read_point("initial", variable_count)
	direction = read_point("search direction", variable_count)
	# alpha = float(input("Enter the initial step size (alpha): "))
	# epsilon = float(input("Enter the sufficient decrease parameter (epsilon, 0 < epsilon < 1): "))
	alpha = 2
	beta = alpha**-1
	epsilon = 0.4
	max_iterations = int(input("Enter the maximum number of backtracking steps: "))

	'''if not (0 < epsilon < 1):
		raise ValueError("Epsilon must be in the range (0, 1).") '''
	if max_iterations <= 0:
		raise ValueError("The maximum number of iterations must be positive.")

	current_value = float(function(*initial_point))
	gradient = np.empty(variable_count)
	for coordinate in range(variable_count):
		step = np.sqrt(np.finfo(float).eps) * max(1.0, abs(initial_point[coordinate]))
		point_plus = initial_point.copy()
		point_minus = initial_point.copy()
		point_plus[coordinate] += step
		point_minus[coordinate] -= step
		gradient[coordinate] = (
			float(function(*point_plus)) - float(function(*point_minus))
		) / (2 * step)

	directional_derivative = float(np.dot(gradient, direction))
	if not np.isfinite(directional_derivative) or directional_derivative >= 0:
		raise ValueError("The search direction must be a finite descent direction.")

	for _ in range(max_iterations):
		candidate_point = initial_point + alpha * direction
		candidate_value = float(function(*candidate_point))
		armijo_bound = current_value + epsilon * alpha * directional_derivative
		if candidate_value <= armijo_bound:
			print(f"Accepted step size: {alpha}")
			print(
				f"Next point: {candidate_point}, "
				f"f(x) = {candidate_value}"
			)
			return candidate_point
		alpha *= beta

	raise RuntimeError(
		f"Armijo condition was not met after {max_iterations} backtracking steps."
	)

def search_pyplot(function, min_point, min_y, lower_bound, upper_bound): #cleanup to reduce code repetition
    points = np.linspace(lower_bound, upper_bound, 100)
    y_values = function(*points.T)
    plt.plot(points[:, 0], y_values, label="Function")
    plt.scatter(min_point[0], min_y, color="red", label="Minimum")
    plt.xlabel(function.variables[0])
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid()
    plt.show()
 
if __name__ == "__main__":
	run_interactive()
