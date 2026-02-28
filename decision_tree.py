from collections import defaultdict
import itertools


class Node:
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child


class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms
	
			
def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records
		
		
class Diagnoser:
	def __init__(self, root: Node):
		self.root = root
		
	def diagnose(self, symptoms):
		current_node = self.root
		while current_node.positive_child is not None and current_node.negative_child is not None:
			if current_node.data in symptoms:
				current_node = current_node.positive_child
			else:
				current_node = current_node.negative_child
		return current_node.data


		
	def calculate_success_rate(self, records):
		if len(records) == 0:
			raise ValueError("Record list is empty")
		success_count = 0
		for record in records:
			if self.diagnose(record.symptoms) == record.illness:
				success_count += 1
		return success_count/len(records)


	def all_illnesses(self):
		illness_count = defaultdict(int)

		def traverse(node):
			if node is None:
				return
			if node.positive_child is None and node.negative_child is None:
				if node.data is not None:
					illness_count[node.data] += 1
			else:
				traverse(node.positive_child)
				traverse(node.negative_child)

		traverse(self.root)
		sorted_illnesses = sorted(illness_count.items(), key=lambda item: item[1], reverse=True)
		sorted_illnesses_list = []
		for illness, count in sorted_illnesses:
			sorted_illnesses_list.append(illness)
		return sorted_illnesses_list


	def paths_to_illness(self, illness):
		paths = []

		def traverse(node, path):
			if node is None:
				return
			if node.positive_child is None and node.negative_child is None:
				if node.data == illness:
					paths.append(path)
				return
			traverse(node.positive_child, path + [True])
			traverse(node.negative_child, path + [False])

		traverse(self.root, [])
		return paths

	def minimize(self, remove_empty=False):
		def is_redundant(node, remove_empty):
			if node is None:
				return False
			if node.positive_child is None and node.negative_child is None:
				return False
			if remove_empty:
				return (node.positive_child.data is None or node.negative_child.data is None)
			return node.positive_child.data == node.negative_child.data

		def minimize_node(node, remove_empty):
			if node is None:
				return None
			if node.positive_child is None and node.negative_child is None:
				return node
			node.positive_child = minimize_node(node.positive_child, remove_empty)
			node.negative_child = minimize_node(node.negative_child, remove_empty)
			if is_redundant(node, remove_empty):
				if remove_empty:
					return node.negative_child if node.positive_child.data is None else node.positive_child
				else:
					return node.positive_child

			return node

		self.root = minimize_node(self.root, remove_empty)

def build_tree(records, symptoms):
	if not all(isinstance(record, Record) for record in records):
		raise TypeError("Not all items in records are of the Record class.")
	if not all(isinstance(symptom, str) for symptom in symptoms):
		raise TypeError("Not all items in symptoms are strings.")

	def most_common_illness(records):
		illness_count = defaultdict(int)
		for record in records:
			illness_count[record.illness] += 1
		if not illness_count:
			return None
		return max(illness_count, key=illness_count.get)

	def build_subtree(records, symptoms):
		if not symptoms:
			return Node(most_common_illness(records))
		symptom = symptoms[0]
		positive_records = [record for record in records if symptom in record.symptoms]
		negative_records = [record for record in records if symptom not in record.symptoms]
		positive_child = build_subtree(positive_records, symptoms[1:])
		negative_child = build_subtree(negative_records, symptoms[1:])
		return Node(symptom, positive_child, negative_child)

	root = build_subtree(records, symptoms)
	return Diagnoser(root)


def optimal_tree(records, symptoms, depth):
	if not all(isinstance(record, Record) for record in records):
		raise TypeError("Not all items in records are of the Record class.")
	if not all(isinstance(symptom, str) for symptom in symptoms):
		raise TypeError("Not all items in symptoms are strings.")
	if not (0 <= depth <= len(symptoms)):
		raise ValueError("Depth is not between 0 and the number of symptoms.")
	if len(set(symptoms)) != len(symptoms):
		raise ValueError("Symptoms list contains duplications")
	best_tree = None
	best_success_rate = -1
	for subset in itertools.combinations(symptoms, depth):
		subset_list = list(subset)
		current_diagnoser = build_tree(records, subset_list)
		current_success_rate = current_diagnoser.calculate_success_rate(records)
		if current_success_rate > best_success_rate:
			best_success_rate = current_success_rate
			best_tree = current_diagnoser
	return best_tree





if __name__ == "__main__":
	
	# Manually build a simple tree.
	#                cough
	#          Yes /       \ No
	#        fever           healthy
	#   Yes /     \ No
	# covid-19   cold
	
	flu_leaf = Node("covid-19", None, None)
	cold_leaf = Node("cold", None, None)
	inner_vertex = Node("fever", flu_leaf, cold_leaf)
	healthy_leaf = Node("healthy", None, None)
	root = Node("cough", inner_vertex, healthy_leaf)
	
	diagnoser = Diagnoser(root)
	
	# Simple test
	diagnosis = diagnoser.diagnose(["cough"])
	if diagnosis == "cold":
		print("Test passed")
	else:
		print("Test failed. Should have printed cold, printed: ", diagnosis)
		
	# Add more tests for sections 2-7 here.

	def test_diagnose():
		flu_leaf = Node("covid-19", None, None)
		cold_leaf = Node("cold", None, None)
		inner_vertex = Node("fever", flu_leaf, cold_leaf)
		healthy_leaf = Node("healthy", None, None)
		root = Node("cough", inner_vertex, healthy_leaf)

		diagnoser = Diagnoser(root)

		# Test cases
		assert diagnoser.diagnose(
			["cough", "fever"]) == "covid-19", "Test failed: cough and fever should diagnose covid-19"
		assert diagnoser.diagnose(["cough"]) == "cold", "Test failed: cough without fever should diagnose cold"
		assert diagnoser.diagnose([]) == "healthy", "Test failed: no symptoms should diagnose healthy"

		print("Diagnose tests passed.")


	test_diagnose()


	def test_calculate_success_rate():
		records = [
			Record("covid-19", ["cough", "fever"]),
			Record("cold", ["cough"]),
			Record("healthy", [])
		]

		flu_leaf = Node("covid-19", None, None)
		cold_leaf = Node("cold", None, None)
		inner_vertex = Node("fever", flu_leaf, cold_leaf)
		healthy_leaf = Node("healthy", None, None)
		root = Node("cough", inner_vertex, healthy_leaf)

		diagnoser = Diagnoser(root)

		success_rate = diagnoser.calculate_success_rate(records)
		assert success_rate == 1.0, f"Test failed: success rate should be 1.0, got {success_rate}"

		print("Calculate success rate tests passed.")


	test_calculate_success_rate()


	def test_all_illnesses():
		flu_leaf = Node("covid-19", None, None)
		cold_leaf = Node("cold", None, None)
		inner_vertex = Node("fever", flu_leaf, cold_leaf)
		healthy_leaf = Node("healthy", None, None)
		root = Node("cough", inner_vertex, healthy_leaf)

		diagnoser = Diagnoser(root)

		illnesses = diagnoser.all_illnesses()
		expected_illnesses = ["covid-19", "cold", "healthy"]
		assert illnesses == expected_illnesses, f"Test failed: expected {expected_illnesses}, got {illnesses}"

		print("All illnesses tests passed.")


	test_all_illnesses()


	def test_paths_to_illness():
		flu_leaf = Node("covid-19", None, None)
		cold_leaf = Node("cold", None, None)
		inner_vertex = Node("fever", flu_leaf, cold_leaf)
		healthy_leaf = Node("healthy", None, None)
		root = Node("cough", inner_vertex, healthy_leaf)

		diagnoser = Diagnoser(root)

		paths_to_covid = diagnoser.paths_to_illness("covid-19")
		assert paths_to_covid == [[True, True]], f"Test failed: expected [[True, True]], got {paths_to_covid}"

		paths_to_cold = diagnoser.paths_to_illness("cold")
		assert paths_to_cold == [[True, False]], f"Test failed: expected [[True, False]], got {paths_to_cold}"

		paths_to_healthy = diagnoser.paths_to_illness("healthy")
		assert paths_to_healthy == [[False]], f"Test failed: expected [[False]], got {paths_to_healthy}"

		print("Paths to illness tests passed.")


	test_paths_to_illness()


	def test_minimize():
		flu_leaf = Node("covid-19", None, None)
		cold_leaf = Node("cold", None, None)
		inner_vertex = Node("fever", flu_leaf, cold_leaf)
		healthy_leaf = Node("healthy", None, None)
		root = Node("cough", inner_vertex, healthy_leaf)

		diagnoser = Diagnoser(root)
		diagnoser.minimize()

		# Manually check the minimized tree structure
		minimized_root = diagnoser.root
		assert minimized_root.positive_child.data == "fever", "Test failed: positive child of root should be 'fever'"
		assert minimized_root.negative_child.data == "healthy", "Test failed: negative child of root should be 'healthy'"
		assert minimized_root.positive_child.positive_child.data == "covid-19", "Test failed: positive child of 'fever' should be 'covid-19'"
		assert minimized_root.positive_child.negative_child.data == "cold", "Test failed: negative child of 'fever' should be 'cold'"

		print("Minimize tests passed.")


	test_minimize()





