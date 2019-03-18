import time


def one_moment(func):
	""" Waits one second before calling function"""
	def wrapper(*args, **kwargs):
		time.sleep(1)
		return func(*args, **kwargs)
	return wrapper


def slow_down(sec=1):
	""" Waits for a given number of seconds before calling function"""
	def one_moment(func):
		"" "Waits one second before calling function"""
		def wrapper(*args, **kwargs):
			time.sleep(1)
			return func(*args, **kwargs)
		return wrapper
	return one_moment

def timer(func):
	""" Print the runtime of the decorated function"""
	def wrapper(*args, **kwargs):
		start_time = time.perf_counter()
		result = func(*args, **kwargs)
		run_time = time.perf_counter() - start_time
		print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
		return result
	return wrapper

def print_args(func):
	""" Prints all the arguments received by the function
	    before it is executed
	"""
	def wrapper(*args, **kwargs):
		print('Function argumens: ')
		print(*args, **kwargs )
		return func(*args, **kwargs)
	return wrapper

def count_function(func):
	""" Counts how many times the function was called"""
	def wrapper(*args, **kwargs):
		wrapper.count += 1
		result = func(*args, **kwargs)
		print(f"Function {func.__name__!r} was called {wrapper.count} times")
		return result
	wrapper.count = 0
	return wrapper


def memoize(func):
	""" Save the resulf of the function in cache"""
	memo = {}
	def wrapper(*args):
		if args in memo:
			return memo[args]
		else:
			result = func(*args)
			memo[args] = result
			return result
	return wrapper

def singleton(cls):
	instances = {}
	def getinstance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return getinstance

